from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

#  Copyright (c) 2019 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2023.
#
#  DataRobot, Inc. Confidential.
#  This is unpublished proprietary source code of DataRobot, Inc. and its affiliates.
#  The copyright notice above does not evidence any actual or intended publication of
#  such source code.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
import json
from builtins import str
from datetime import datetime

import datarobot.mlops.install_aliases  # noqa: F401
import pandas as pd
import six
from datarobot.mlops.channel.output_channel_queue import OutputChannelQueueAsync
from datarobot.mlops.channel.output_channel_queue import OutputChannelQueueSync
from datarobot.mlops.common import config
from datarobot.mlops.common.aggregation_util import build_aggregated_stats
from datarobot.mlops.common.aggregation_util import convert_dict_to_feature_types
from datarobot.mlops.common.aggregation_util import validate_feature_types
from datarobot.mlops.common.config import ConfigConstants
from datarobot.mlops.common.exception import DRApiException
from datarobot.mlops.common.exception import DRCommonException
from datarobot.mlops.common.exception import DRUnsupportedType
from datarobot.mlops.metric import AggregatedStatsContainer
from datarobot.mlops.metric import CustomMetric
from datarobot.mlops.metric import CustomMetricContainer
from datarobot.mlops.metric import DeploymentStats
from datarobot.mlops.metric import DeploymentStatsContainer
from datarobot.mlops.metric import EventContainer
from datarobot.mlops.metric import GeneralStats
from datarobot.mlops.metric import PredictionsData
from datarobot.mlops.metric import PredictionsDataContainer
from dateutil.tz import tzlocal
from six import string_types


class Model(object):
    DEFAULT_ASYNC_REPORTING = False
    MAX_TS_PREDICTIONS = 10000
    MAX_TS_FEATURE_ROWS = 10000

    REQUEST_PARAMETERS_MAPPING = {
        "forecast_point": "forecastPoint",
        "predictions_start_date": "predictionsStartDate",
        "predictions_end_date": "predictionsEndDate",
        "relax_kia_check": "relaxKnownInAdvanceFeaturesCheck",
        "relax_seen_cross_series_check": "relaxSeenCrossSeriesCheck",
        "relax_insufficient_history_check": "relaxInsufficientHistoryCheck",
    }

    DEFAULT_AGGREGATION_HISTOGRAM_BIN_COUNT = 10
    DEFAULT_AGGREGATION_DISTINCT_CATEGORY_COUNT = 10
    DEFAULT_SEGMENT_VALUE_ATTR_COUNT = 10000

    def __init__(self, feature_types=None):
        self._stats_counter = {}
        self._report_queue = None
        if config.get_config_default(ConfigConstants.ASYNC_REPORTING, self.DEFAULT_ASYNC_REPORTING):
            self._report_queue = OutputChannelQueueAsync()
        else:
            self._report_queue = OutputChannelQueueSync()

        # stats aggregation fields
        self._init_aggregation_params(feature_types)

    def _init_aggregation_params(self, feature_types):
        features_types_filename = config.get_config_default(
            ConfigConstants.FEATURE_TYPES_FILENAME, None
        )
        features_types_json = config.get_config_default(ConfigConstants.FEATURE_TYPES_JSON, None)
        if features_types_json or features_types_filename:
            self._feature_types = self._build_feature_types_from_vars(
                features_types_filename, features_types_json
            )
        else:
            self._feature_types = feature_types

        self._histogram_bin_count = config.get_config_default(
            ConfigConstants.STATS_AGGREGATION_HISTOGRAM_BIN_COUNT,
            self.DEFAULT_AGGREGATION_HISTOGRAM_BIN_COUNT,
        )
        self._distinct_category_count = config.get_config_default(
            ConfigConstants.STATS_AGGREGATION_DISTINCT_CATEGORY_COUNT,
            self.DEFAULT_AGGREGATION_DISTINCT_CATEGORY_COUNT,
        )
        self._segment_value_per_attribute_count = config.get_config_default(
            ConfigConstants.STATS_AGGREGATION_SEGMENT_VALUE_COUNT,
            self.DEFAULT_SEGMENT_VALUE_ATTR_COUNT,
        )
        segment_attributes_str = config.get_config_default(
            ConfigConstants.STATS_AGGREGATION_SEGMENT_ATTRIBUTES, None
        )
        if segment_attributes_str:
            self._segment_attributes = [attr.strip() for attr in segment_attributes_str.split(",")]
        else:
            self._segment_attributes = None
        self._prediction_timestamp_column_name = config.get_config_default(
            ConfigConstants.STATS_AGGREGATION_PREDICTION_TS_COLUMN_NAME, None
        )
        self._prediction_timestamp_column_format = config.get_config_default(
            ConfigConstants.STATS_AGGREGATION_PREDICTION_TS_COLUMN_FORMAT, None
        )

    def shutdown(self, timeout_sec=0):
        self._report_queue.shutdown(timeout_sec=timeout_sec, final_shutdown=False)
        self._report_queue = None

    def _validate_input_association_ids(self, predictions, association_ids):
        self._validate_parameter(predictions, association_ids, "association ids", string_types)
        if len(set(association_ids)) != len(association_ids):
            raise DRCommonException(
                "All association ids should be unique, "
                "association ids uniquely identify each individual prediction"
            )

    def _validate_input_features_and_predictions(self, feature_data_df, predictions):
        for feature_name, feature_values in feature_data_df.iteritems():
            if len(feature_values) != len(predictions):
                raise DRUnsupportedType(
                    """The number of feature values for feature '{}' ({}) does not match the number
                      of prediction values {}""".format(
                        feature_name, len(feature_values), len(predictions)
                    )
                )

    def _validate_predictions(self, predictions, class_names):
        if not isinstance(predictions, list):
            raise DRUnsupportedType("'predictions' should be a list of probabilities or numbers")

        likely_classification_predictions = False
        likely_regression_predictions = False
        class_names_present = False
        likely_num_classes = 0
        if class_names is not None:
            if not isinstance(class_names, list):
                raise DRUnsupportedType("'class_names' should be a list")
            if len(class_names) < 2:
                raise DRCommonException("'class_names' should contain at least 2 values")
            for class_name in class_names:
                if not isinstance(class_name, string_types):
                    raise DRUnsupportedType(
                        "Each class name is expected to be a string, but received {}".format(
                            type(class_name)
                        )
                    )
            class_names_present = True
            likely_num_classes = len(class_names)

        first_prediction = predictions[0]
        if isinstance(first_prediction, list):
            likely_classification_predictions = True
            likely_num_classes = len(first_prediction)
        elif isinstance(first_prediction, float) or isinstance(first_prediction, int):
            likely_regression_predictions = True
        else:
            raise DRUnsupportedType(
                "Predictions with type '{}' not supported".format(str(type(first_prediction)))
            )

        # Now verify that the remaining list of elements have the same instance / format
        for index, prediction in enumerate(predictions):
            if (
                likely_regression_predictions
                and not isinstance(prediction, float)
                and not isinstance(prediction, int)
            ):
                raise DRUnsupportedType(
                    """Invalid prediction '{}' at index '{}', expecting a prediction value of
                    type int or float""".format(
                        str(prediction), index
                    )
                )
            if likely_classification_predictions:
                if not isinstance(prediction, list):
                    raise DRUnsupportedType(
                        """Invalid prediction '{}' at index '{}', expecting list of prediction
                        probabilities""".format(
                            str(prediction), index
                        )
                    )
                if len(prediction) < 2:
                    raise DRCommonException(
                        """Invalid prediction '{}' at index '{}', expecting list of size at least 2
                        """.format(
                            str(prediction), index
                        )
                    )
                if len(prediction) != likely_num_classes:
                    raise DRCommonException(
                        """Invalid prediction '{}' at index '{}', length of class probabilities in
                        the prediction does not match, expected '{}', got '{}'""".format(
                            str(prediction), index, likely_num_classes, len(prediction)
                        )
                    )
                if class_names_present:
                    if len(prediction) != len(class_names):
                        raise DRUnsupportedType(
                            """Number of prediction probabilities '[{}]'({}) at index {} does not
                             match class_names length {}""".format(
                                str(prediction), len(prediction), index, len(class_names)
                            )
                        )
                for prob in prediction:
                    if not isinstance(prob, float):
                        raise DRCommonException(
                            """Probability value '{}' in prediction '{}' at index '{}' is not
                            a float value""".format(
                                prob, prediction, index
                            )
                        )
                    if prob > 1.0 or prob < 0.0:
                        raise DRCommonException(
                            """Probability value '{}' in prediction '{}' at index '{}' is not
                            between 0 and 1""".format(
                                prob, prediction, index
                            )
                        )

    def _report_stats(self, deployment_id, model_id, stats_serializer):
        """
        This function is used for reporting metrics and events.
        """
        data_type = stats_serializer.data_type()

        # Keep account of number of records submitted to channel
        self._report_queue.submit(stats_serializer, deployment_id)
        if data_type not in self._stats_counter:
            self._stats_counter[data_type] = 0
        self._stats_counter[data_type] += 1

    def get_stats_counters(self):
        return self._stats_counter

    @staticmethod
    def _get_general_stats(model_id, batch_name=None):
        return GeneralStats(model_id, batch_name=batch_name)

    def report_deployment_stats(
        self, deployment_id, model_id, num_predictions, execution_time_ms=None, batch_name=None
    ):
        """
        Report the number of predictions and execution time
        to DataRobot MLOps.

        :param deployment_id: the deployment for these metrics
        :type deployment_id: str
        :param model_id: the model for these metrics
        :type model_id: str
        :param num_predictions: number of predictions
        :type num_predictions: int
        :param execution_time_ms: time in milliseconds
        :type execution_time_ms: float
        """
        deployment_stats = DeploymentStats(num_predictions, execution_time_ms)
        deployment_stats_container = DeploymentStatsContainer(
            self._get_general_stats(model_id, batch_name), deployment_stats
        )

        self._report_stats(deployment_id, model_id, deployment_stats_container)

    def report_custom_metric(self, deployment_id, model_id, metric_id, value, timestamp=None):
        """
        Report an arbitrary metric to DataRobot MLOps. The metric_id is used to identify the metric.
        This method is used to report a metric which is tied to a deployment and not a model.

        :param deployment_id: Deployment id to report metric for
        :param model_id: Model id to report metric for. If None, metric is a deployment metric.
        :param metric_id: Metric id to use
        :param value: Numeric value to report
        :param timestamp: Timestamp to report for the metric
        """

        # If value is a single value pack it with timestamp into a list of items
        if not isinstance(metric_id, six.string_types):
            raise DRUnsupportedType(
                "Metric id must be of type str - got type ({}) {}".format(
                    type(metric_id), isinstance(metric_id, six.string_types)
                )
            )

        if not isinstance(value, (list, int, float)):
            raise DRUnsupportedType(
                "Value for custom metric must be either int or float (or list of int or float)"
            )

        if isinstance(value, list):
            if not all(isinstance(v, (int, float)) for v in value):
                raise DRUnsupportedType("Values for custom metrics should be all numeric")
            value_list = value[:]
            # We make sure timestamp is also a list
            if not isinstance(timestamp, list):
                raise DRUnsupportedType(
                    "When providing a list of values for custom metrics, "
                    + "timestamp must also be a list"
                )
            if len(timestamp) != len(value):
                raise DRCommonException(
                    "Length of timestamp list ({}) != Length of value list ({})".format(
                        len(timestamp), len(value)
                    )
                )
            timestamp_list = [GeneralStats.to_dr_timestamp(ts) for ts in timestamp]
        else:
            value_list = [value]
            # Allowing a None timestamp in the case where value is not a list.
            # The timestamp is generated using now()
            if timestamp is None:
                timestamp = GeneralStats.to_dr_timestamp(datetime.now(tzlocal()))
            elif isinstance(timestamp, (list, dict)):
                raise DRCommonException("Value is a scalar while timestamp is not")
            else:
                timestamp = GeneralStats.to_dr_timestamp(timestamp)
            timestamp_list = [timestamp]

        custom_metric = CustomMetric(metric_id, value_list, timestamp_list)
        metric_container = CustomMetricContainer(self._get_general_stats(model_id), custom_metric)
        self._report_stats(deployment_id, model_id, metric_container)

    def report_predictions_data(
        self,
        deployment_id,
        model_id,
        features_df=None,
        predictions=None,
        association_ids=None,
        class_names=None,
        skip_drift_tracking=False,
        skip_accuracy_tracking=False,
        batch_name=None,
    ):
        """
        Report features and predictions to DataRobot MLOps for tracking and monitoring.

        :param deployment_id: the deployment for these metrics
        :type deployment_id: str
        :param model_id: the model for these metrics
        :type model_id: str
        :param features_df: Dataframe containing features to track and monitor.  All the features
            in the dataframe are reported.  Omit the features from the dataframe that do not need
            reporting.
        :type features_df: pandas dataframe
        :param predictions: List of predictions.  For Regression deployments, this is 1D list
            containing prediction values.  For Classification deployments, this is a 2D list, in
            which the inner list is the list of probabilities for each class type
            Binary Classification: e.g. [[0.2, 0.8], [0.3, 0.7]].
            Regression Predictions: e.g. [1, 2, 4, 3, 2]
        :type predictions: list

        At least one of `features` or `predictions` must be specified.

        :param association_ids: an optional list of association IDs corresponding to each
            prediction used for accuracy calculations.  Association IDs have to be unique for each
            prediction reported.  Number of `predictions` should be equal to number of
            `association_ids` in the list
        :type association_ids: list
        :param class_names: names of predicted classes, e.g. ["class1", "class2", "class3"].  For
            classification deployments, class names must be in the same order as the prediction
            probabilities reported. If not specified, this prediction order defaults to the order
            of the class names on the deployment.
            This argument is ignored for Regression deployments.
        :type class_names: list
        :param skip_drift_tracking: Should the DataRobot App skip drift calculation for this raw
            data
        :type skip_drift_tracking: bool
        :param skip_accuracy_tracking: Should the DataRobot App skip accuracy calculation for
            these predictions
        :type skip_accuracy_tracking: bool
        :param batch_name: Name of the batch these statistics belong to
        :type batch_name: str
        """
        feature_data_df = self._validate_and_copy_feature_predictions(
            features_df, predictions, class_names, association_ids
        )
        self._report_metric(
            deployment_id,
            model_id,
            feature_data_df,
            predictions,
            association_ids,
            class_names,
            skip_drift_tracking=skip_drift_tracking,
            skip_accuracy_tracking=skip_accuracy_tracking,
            batch_name=batch_name,
        )

    def _validate_and_copy_feature_predictions(
        self,
        features_df=None,
        predictions=None,
        class_names=None,
        association_ids=None,
    ):
        if features_df is None and not predictions:
            raise DRCommonException("One of `features_df` or `predictions` argument is required")
        if predictions:
            self._validate_predictions(predictions, class_names)
        if features_df is not None and not isinstance(features_df, pd.DataFrame):
            raise DRUnsupportedType(
                "features_df argument has to be of type '{}'".format(pd.DataFrame)
            )
        if predictions and association_ids:
            self._validate_input_association_ids(predictions, association_ids)
        # If dataframe provided we do a deep copy, in case is modified before processing
        feature_data_df = None
        if features_df is not None:
            feature_data_df = features_df.copy(deep=True)
        if feature_data_df is not None and predictions:
            self._validate_input_features_and_predictions(feature_data_df, predictions)
        return feature_data_df

    def report_aggregated_predictions_data(
        self,
        deployment_id,
        model_id,
        features_df=None,
        predictions=None,
        class_names=None,
        batch_name=None,
    ):
        """
        Report features and predictions aggregated using mlops-stats-aggregator
         to DataRobot MLOps for tracking and monitoring.

        :param deployment_id: the deployment for these metrics
        :type deployment_id: str
        :param model_id: the model for these metrics
        :type model_id: str
        :param features_df: Dataframe containing features to track and monitor.  All the features
            in the dataframe are reported.  Omit the features from the dataframe that do not need
            reporting.
        :type features_df: pandas dataframe
        :param predictions: List of predictions.  For Regression deployments, this is 1D list
            containing prediction values.  For Classification deployments, this is a 2D list, in
            which the inner list is the list of probabilities for each class type
            Binary Classification: e.g. [[0.2, 0.8], [0.3, 0.7]].
            Regression Predictions: e.g. [1, 2, 4, 3, 2]
        :type predictions: list

        At least one of `features` or `predictions` must be specified.
        :param class_names: names of predicted classes, e.g. ["class1", "class2", "class3"].  For
            classification deployments, class names must be in the same order as the prediction
            probabilities reported. If not specified, this prediction order defaults to the order
            of the class names on the deployment.
            This argument is ignored for Regression deployments.
        :type class_names: list
        :param batch_name: Name of the batch these statistics belong to
        :type batch_name: str
        """
        if features_df is not None and self._feature_types is None:
            raise DRCommonException("Features type should be provided during MLOPS initialization")

        feature_data_df = self._validate_and_copy_feature_predictions(
            features_df, predictions, class_names
        )
        predictions_df = self._convert_predictions_to_df(predictions, class_names)

        # If the prediction timestamp column is not set or is not present in the feature list
        # follow the regular path
        if (
            self._prediction_timestamp_column_name
            and self._prediction_timestamp_column_format
            and self._prediction_timestamp_column_name in feature_data_df.columns
        ):
            # Split rows based on timestamps
            self._process_data_for_aggregation_with_prediction_timestamp(
                deployment_id, model_id, feature_data_df, predictions_df, class_names, batch_name
            )
        else:
            # Call method to report aggregated stats directly
            self._aggregate_stats(
                deployment_id,
                model_id,
                feature_data_df=features_df,
                predictions_df=predictions_df,
                class_names=class_names,
                batch_name=batch_name,
            )

    def _process_data_for_aggregation_with_prediction_timestamp(
        self,
        deployment_id,
        model_id,
        features_df=None,
        predictions_df=None,
        class_names=None,
        batch_name=None,
    ):
        from datarobot.mlops.stats_aggregator.type_conversion import convert_date_feature

        converted_timestamp = convert_date_feature(
            features_df[self._prediction_timestamp_column_name],
            self._prediction_timestamp_column_format,
        )
        # convert timestamp to near-est hour
        converted_timestamp = converted_timestamp.apply(lambda ts: ts - (ts % 3600))
        unique_timestamps = set(converted_timestamp)

        for timestamp in unique_timestamps:
            ts_filter = converted_timestamp == timestamp
            slice_feature_df = features_df[ts_filter] if features_df is not None else None
            slice_predictions_df = predictions_df[ts_filter] if predictions_df is not None else None

            self._aggregate_stats(
                deployment_id,
                model_id,
                feature_data_df=slice_feature_df,
                predictions_df=slice_predictions_df,
                class_names=class_names,
                timestamp=timestamp,
                batch_name=batch_name,
            )

    @staticmethod
    def _convert_predictions_to_df(predictions, class_names):
        if predictions is None:
            return None

        if class_names:
            return pd.DataFrame(predictions, columns=class_names)
        else:
            return pd.DataFrame(predictions)

    def _aggregate_stats(
        self,
        deployment_id,
        model_id,
        feature_data_df=None,
        predictions_df=None,
        class_names=None,
        timestamp=None,
        batch_name=None,
    ):
        from datarobot.mlops.stats_aggregator import aggregate_stats

        aggregated_out = aggregate_stats(
            features=feature_data_df,
            feature_types=self._feature_types,
            predictions=predictions_df,
            segment_attributes=self._segment_attributes,
            histogram_bin_count=self._histogram_bin_count,
            distinct_category_count=self._distinct_category_count,
            segment_value_per_attribute_count=self._segment_value_per_attribute_count,
        )

        self._report_aggregated_stats(
            deployment_id, model_id, aggregated_out, class_names, timestamp, batch_name
        )

    def _report_aggregated_stats(
        self, deployment_id, model_id, aggregated_out, class_names, timestamp, batch_name
    ):
        if timestamp is not None:
            timestamp = datetime.fromtimestamp(timestamp)

        aggregated_stats_container = AggregatedStatsContainer(
            general_stats=GeneralStats(
                model_id, GeneralStats.to_dr_timestamp(timestamp), batch_name=batch_name
            ),
            aggregated_stats=build_aggregated_stats(aggregated_out, class_names),
        )
        self._report_stats(deployment_id, model_id, aggregated_stats_container)

    @staticmethod
    def _get_num_rows(feature_data_df, predictions_df):
        if feature_data_df is not None:
            return len(feature_data_df)
        else:
            return len(predictions_df)

    def report_raw_time_series_predictions_data(
        self,
        deployment_id,
        model_id,
        features_df=None,
        predictions=None,
        association_ids=None,
        class_names=None,
        request_parameters=None,
        forecast_distance=None,
        row_index=None,
        partition=None,
        series_id=None,
        skip_drift_tracking=False,
        skip_accuracy_tracking=False,
    ):
        """
        Report features and predictions to DataRobot MLOps for tracking and monitoring
        of an external time series deployment

        :param series_id: List of series ids indicating the time series each prediction belongs to
        :type series_id: list[str]
        :param partition: List of forecast dates for which these time series predictions are made
        :type partition: list[datetime]
        :param row_index: Indexes of the rows in the input for which these predictions are made
        :type row_index: list[int]
        :param forecast_distance: list of forecast distance value used for each
            corresponding prediction
        :type forecast_distance: list[int]
        :param request_parameters: Request parameters used to make these predictions, either
            forecast point or bulk parameters
        :type request_parameters: dict[str, datetime]
        :param features_df: Dataframe containing features to track and monitor.  All the features
            in the dataframe are reported.  Omit the features from the dataframe that do not need
            reporting.
        :type features_df: pandas dataframe
        :param predictions: List of predictions.  For Regression deployments, this is a 1D list
            containing prediction values.  For Classification deployments, this is a 2D list, in
            which the inner list is the list of probabilities for each class type
            Regression Predictions: e.g. [1, 2, 4, 3, 2]
            Binary Classification: e.g. [[0.2, 0.8], [0.3, 0.7]].
        :type predictions: list

        At least one of `features` or `predictions` must be specified.

        :param association_ids: an optional list of association IDs corresponding to each
            prediction. Used for accuracy calculations.  Association IDs have to be unique for each
            prediction to report.  The number of `predictions` should be equal to number of
            `association_ids` in the list
        :type association_ids: list
        :param class_names: names of predicted classes, e.g. ["class1", "class2", "class3"].  For
            classification deployments, class names must be in the same order as the prediction
            probabilities reported. If not specified, this prediction order defaults to the order
            of the class names on the deployment.
            This argument is ignored for Regression deployments.
        :type class_names: list
        :param deployment_id: the deployment for these metrics
        :type deployment_id: str
        :param model_id: the model for these metrics
        :type model_id: str
        :param skip_drift_tracking: Should the DataRobot App skip drift calculation for this raw
            data
        :type skip_drift_tracking: bool
        :param skip_accuracy_tracking: Should the DataRobot App skip accuracy calculation for
            these predictions
        :type skip_accuracy_tracking: bool
        """
        if features_df is None and not predictions:
            raise DRCommonException("One of `features_df` or `predictions` argument is required")

        if predictions:
            self._validate_predictions(predictions, class_names)
            if len(predictions) > self.MAX_TS_PREDICTIONS:
                raise DRCommonException(
                    """MLOps library currently supports posting only {} predictions in
                     a single call""".format(
                        self.MAX_TS_PREDICTIONS
                    )
                )
            # Validate time series prediction report
            self._validate_time_series_prediction_report(
                predictions, forecast_distance, row_index, partition, series_id
            )
            series_id = self._validate_series_id(predictions, series_id)
            if association_ids:
                self._validate_input_association_ids(predictions, association_ids)

        if features_df is not None and not isinstance(features_df, pd.DataFrame):
            raise DRUnsupportedType("features_df argument has to be of type '{}'", pd.DataFrame)

        # If dataframe provided we do a deep copy, in case is modified before processing
        feature_data_df = None
        if features_df is not None:
            if features_df.shape[0] > self.MAX_TS_FEATURE_ROWS:
                raise DRCommonException(
                    """MLOps library currently supports posting only {} feature rows in
                     a single call""".format(
                        self.MAX_TS_FEATURE_ROWS
                    )
                )
            feature_data_df = features_df.copy(deep=True)

        # Validate and modify request parameters
        if request_parameters:
            request_parameters = self._update_request_parameters(request_parameters)

        self._report_metric(
            deployment_id,
            model_id,
            feature_data=feature_data_df,
            predictions=predictions,
            association_ids=association_ids,
            class_names=class_names,
            request_parameters=request_parameters,
            forecast_distance=forecast_distance,
            row_index=row_index,
            partition=partition,
            series_id=series_id,
            skip_drift_tracking=skip_drift_tracking,
            skip_accuracy_tracking=skip_accuracy_tracking,
        )

    def report_event(self, deployment_id, model_id, event):
        """
        Wrap event in a container and use report_stats() to place in queue.
        """
        # automatically set deployment ID so user's code doesn't need to
        if event.is_entity_a_deployment():
            event.set_entity_id(deployment_id)
        event_container = EventContainer(event)
        self._report_stats(deployment_id, model_id, event_container)

    def _report_metric(
        self,
        deployment_id,
        model_id,
        feature_data=None,
        predictions=None,
        association_ids=None,
        class_names=None,
        request_parameters=None,
        forecast_distance=None,
        row_index=None,
        partition=None,
        series_id=None,
        skip_drift_tracking=False,
        skip_accuracy_tracking=False,
        batch_name=None,
    ):
        predictions_data = PredictionsData(
            feature_data=feature_data,
            predictions=predictions,
            association_ids=association_ids,
            class_names=class_names,
            request_parameters=request_parameters,
            forecast_distance=forecast_distance,
            row_index=row_index,
            partition=partition,
            series_id=series_id,
            skip_drift_tracking=skip_drift_tracking,
            skip_accuracy_tracking=skip_accuracy_tracking,
        )
        predictions_data_container = PredictionsDataContainer(
            self._get_general_stats(model_id, batch_name=batch_name), predictions_data
        )
        self._report_stats(deployment_id, model_id, predictions_data_container)

    def _validate_time_series_prediction_report(
        self, predictions, forecast_distance, row_index, partition, series_id
    ):
        self._validate_parameter(predictions, forecast_distance, "forecast distance", int)
        self._validate_parameter(predictions, row_index, "row index", int)
        self._validate_parameter(predictions, partition, "partition", datetime)

    @staticmethod
    def _validate_parameter(predictions, parameter, param_name, expected_type):
        if not parameter:
            raise DRCommonException(
                "'{}' values are required to report time series predictions".format(parameter)
            )
        if not isinstance(parameter, list):
            raise DRUnsupportedType("{} argument has to be of type '{}'".format(param_name, list))
        if len(predictions) != len(parameter):
            raise DRCommonException(
                "Number of predictions and {} values should be the same".format(param_name)
            )
        for param in parameter:
            if not isinstance(param, expected_type):
                raise DRCommonException(
                    "Value {} is of type {}, expected of type {}".format(
                        param, type(param), expected_type
                    )
                )

    def _validate_series_id(self, predictions, series_id):
        if series_id is None:
            return None

        if not isinstance(series_id, list):
            raise DRUnsupportedType("'series_id' argument has to be of type 'list'")

        # If all values in the series are None, then simply convert series id to be None
        if all(_id is None for _id in series_id):
            return None

        self._validate_parameter(predictions, series_id, "series id", string_types)
        return series_id

    def _update_request_parameters(self, request_parameters):
        allowed_keys = self.REQUEST_PARAMETERS_MAPPING.keys()
        camel_case_values = self.REQUEST_PARAMETERS_MAPPING.values()
        updated_request_parameters = {}
        for key, value in request_parameters.items():
            if key in allowed_keys:
                new_key = self.REQUEST_PARAMETERS_MAPPING[key]
                if isinstance(value, datetime):
                    updated_request_parameters[new_key] = value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                else:
                    updated_request_parameters[self.REQUEST_PARAMETERS_MAPPING[key]] = value
            elif key in camel_case_values:
                # If the key is already a camel case, just copy it as it is
                if isinstance(value, datetime):
                    updated_request_parameters[key] = value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                else:
                    updated_request_parameters[key] = value
            # else:
            # Don't copy the keys which are not in requestParametersMapping or its values
        return updated_request_parameters

    def _build_feature_types_from_vars(self, features_types_filename, features_types_json):
        if features_types_filename and features_types_json:
            # if both vars are provided, raise error
            raise DRApiException(
                "Feature types are provided using file and json, only one is supported"
            )

        feature_types = None
        if features_types_filename:
            with open(features_types_filename, "rb") as f:
                feature_types = json.load(f)
        if features_types_json:
            feature_types = json.loads(features_types_json)

        validate_feature_types(feature_types)
        return convert_dict_to_feature_types(feature_types)
