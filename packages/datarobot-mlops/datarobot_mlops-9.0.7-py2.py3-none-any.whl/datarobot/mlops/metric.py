from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import abc
import json

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
from builtins import dict
from builtins import object
from builtins import range
from datetime import datetime
from decimal import Decimal
from math import isnan

import datarobot.mlops.install_aliases  # noqa: F401
import pandas as pd
from datarobot.mlops.common.enums import DataFormat
from datarobot.mlops.common.enums import DataType
from datarobot.mlops.common.exception import DRUnsupportedType
from datarobot.mlops.event import Event
from dateutil.tz import sys
from dateutil.tz import tzlocal
from future.utils import with_metaclass
from six import string_types

"""
Currently there are the following independent types of information:

GeneralStats: model ID, timestamp
DeploymentStats: number of predictions, execution time
PredictionsStats: predictions, class names

These parameters may be combined and reported in different ways and structures:

Reporting deployment stats includes: model ID, timestamp, num predictions, execution time.
Reporting predictions includes: timestamp, predictions and class names.

DeploymentStatsContainer and PredictionStatsContainer are responsible
for implementing to_iterable() method for data structuring.
"""


def estimate_metric_size(metric):
    """
    Estimate the memory usage of object metric
    :param metric:
    :return: size of metric in bytes
    """
    estimate_size = sys.getsizeof(metric)

    if hasattr(metric, "__dict__"):
        estimate_size += sum([sys.getsizeof(x) for x in metric.__dict__.values() if x is not None])
    return estimate_size


class SerializationConstants(object):
    class GeneralConstants(object):
        MODEL_ID_FIELD_NAME = "modelId"
        TIMESTAMP_FIELD_NAME = "timestamp"
        BATCH_NAME_FIELD_NAME = "batchName"

    class DeploymentStatsConstants(object):
        NUM_PREDICTIONS_FIELD_NAME = "numPredictions"
        EXECUTION_TIME_FIELD_NAME = "executionTime"

    class CustomMetricStatsConstants(object):
        BUCKETS_FIELD_NAME = "buckets"
        METRIC_ID_FIELD_NAME = "customMetricId"
        MODEL_PACKAGE_ID_FIELD_NAME = "modelPackageId"
        METRIC_VALUE_FIELD_NAME = "value"

    class PredictionsStatsConstants(object):
        PREDICTIONS_FIELD_NAME = "predictions"
        ASSOCIATION_IDS_FIELD_NAME = "associationIds"
        RESULTS_FIELD_NAME = "results"
        CLASS_NAMES_FIELD_NAME = "classNames"

    class PredictionsDataConstants(object):
        PREDICTIONS_FIELD_NAME = "predictions"
        ASSOCIATION_IDS_FIELD_NAME = "associationIds"
        FEATURES_FIELD_NAME = "features"
        CLASS_NAMES_FIELD_NAME = "classNames"
        REQUEST_PARAMETERS_FIELD_NAME = "requestParameters"
        FORECAST_DISTANCE_FIELD_NAME = "forecastDistance"
        ROW_INDEX_FIELD_NAME = "rowIndex"
        PARTITION_FIELD_NAME = "partition"
        SERIES_ID_FIELD_NAME = "seriesId"
        SKIP_DRIFT_TRACKING_FIELD_NAME = "skipDriftTracking"
        SKIP_ACCURACY_TRACKING_FIELD_NAME = "skipAccuracyTracking"

    class AggregatedStatsConstants(object):
        NUMERIC_AGGREGATE_MAP = "numericAggregateMap"
        CATEGORICAL_AGGREGATE_MAP = "categoricalAggregateMap"
        PREDICTION_AGGREGATE_MAP = "predictionAggregateMap"
        SEGMENT_ATTRIBUTES_AGGREGATE_STATS = "segmentAttributesAggregatedStats"
        SEGMENT_ATTRIBUTES_FIELD_NAME = "segments"

    class EventConstants(object):
        EVENT_TYPE_FIELD_NAME = "eventType"
        ORG_ID_FIELD_NAME = "orgId"
        ENTITY_ID_FIELD_NAME = "deploymentId"  # todo this is changing
        MESSAGE_FIELD_NAME = "message"
        PREDICTION_REQUEST_DATA_FIELD_NAME = "predictionRequestData"


class GeneralStats(object):
    """
    General statistics.
    """

    def __init__(self, model_id, timestamp=None, batch_name=None):
        self._model_id = model_id
        self._batch_name = batch_name
        if timestamp is None:
            self._timestamp = self.to_dr_timestamp(datetime.now(tzlocal()))
        else:
            self._timestamp = timestamp

    @staticmethod
    def to_dr_timestamp(ts):
        if ts is None:
            return None

        micro_timestamp = ts.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        return micro_timestamp[0:23] + micro_timestamp[26:]

    def get_model_id(self):
        return self._model_id

    def get_timestamp(self):
        return self._timestamp

    def get_batch_name(self):
        return self._batch_name


class DeploymentStats(object):
    """
    Class to keep data about deployment statistics.
    """

    def __init__(self, num_predictions, execution_time):
        self._num_predictions = num_predictions
        self._execution_time = execution_time

    def get_num_predictions(self):
        return self._num_predictions

    def get_execution_time(self):
        return self._execution_time


class CustomMetric(object):
    """
    Class to keep data about a custom metric.
    """

    def __init__(self, metric_id, values, timestamps):
        self._metric_id = metric_id
        self._values = values
        self._timestamps = timestamps

    def get_nr_rows(self):
        return len(self._values)

    def get_metric_id(self):
        return self._metric_id

    def get_values(self):
        return self._values

    def get_timestamps(self):
        return self._timestamps


class PredictionsStats(object):
    """
    Class to keep data about predictions statistics.
    """

    def __init__(self, predictions, class_names, association_ids=None):
        self._predictions = predictions
        self._class_names = class_names
        self._association_ids = association_ids

    def get_predictions(self):
        return self._predictions

    def get_class_names(self):
        return self._class_names

    def get_association_ids(self):
        return self._association_ids


class FeatureDataStats(object):
    """
    Class to keep feature data.
    """

    def __init__(self, feature_data):
        self._feature_data = feature_data

    def get_feature_data(self):
        return self._feature_data


class PredictionsData(object):
    """
    Class to keep features and predictions data together
    """

    def __init__(
        self,
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
    ):
        self._feature_data = feature_data
        self._has_feature_data = False if feature_data is None else True
        self._predictions = predictions
        self._association_ids = association_ids
        self._class_names = class_names
        self._request_parameters = request_parameters
        self._forecast_distance = forecast_distance
        self._row_index = row_index
        self._partition = partition
        self._series_id = series_id
        self._skip_drift_tracking = skip_drift_tracking
        self._skip_accuracy_tracking = skip_accuracy_tracking

    def get_num_rows(self):
        if self.has_feature_data():
            return len(self._feature_data)
        else:
            return len(self._predictions)

    def get_predictions(self):
        return self._predictions

    def get_class_names(self):
        return self._class_names

    def get_association_ids(self):
        return self._association_ids

    def has_feature_data(self):
        return self._has_feature_data

    def get_feature_data_df(self):
        return self._feature_data

    def get_request_parameters(self):
        return self._request_parameters

    def get_forecast_distance(self):
        return self._forecast_distance

    def get_row_index(self):
        return self._row_index

    def get_partition(self):
        return self._partition

    def get_series_id(self):
        return self._series_id

    def skip_drift_tracking(self):
        return self._skip_drift_tracking

    def skip_accuracy_tracking(self):
        return self._skip_accuracy_tracking


class AggregatedStats(object):
    def __init__(
        self,
        numeric_aggregate_map=None,
        categorical_aggregate_map=None,
        prediction_aggregate_map=None,
        segment_attributes_aggregated_stats=None,
        class_names=None,
    ):
        self.numeric_aggregate_map = numeric_aggregate_map
        self.categorical_aggregate_map = categorical_aggregate_map
        self.prediction_aggregate_map = prediction_aggregate_map
        self.segment_attributes_aggregated_stats = segment_attributes_aggregated_stats
        self._class_names = class_names

    def get_numeric_aggregate_map(self):
        return self.numeric_aggregate_map

    def get_categorical_aggregate_maps(self):
        return self.categorical_aggregate_map

    def get_prediction_aggregate_map(self):
        return self.prediction_aggregate_map

    def get_segment_attributes_aggregated_stats(self):
        return self.segment_attributes_aggregated_stats

    def get_class_names(self):
        return self._class_names


class StatsContainer(with_metaclass(abc.ABCMeta)):
    def __init(self):
        pass

    @abc.abstractmethod
    def to_iterable(self):
        """ """

    @abc.abstractmethod
    def get_estimate_size(self):
        """
        Return current stats estimated size in memory
        :return: estimated size of object in bytes
        """

    @abc.abstractmethod
    def data_type(self):
        """
        Get type of the data current metric represents.
        Check @DataType.

        :return: type of the data for current metric.
        :rtype: DataType
        """

    def serialize(self, data_format):
        if data_format == DataFormat.JSON:
            return self.to_iterable()
        elif data_format == DataFormat.BYTE_ARRAY:
            json_str = json.dumps(self.to_iterable())
            return bytearray(json_str, encoding="utf8")
        else:
            raise NotImplementedError(
                "Metric serialization does not support data format {}".format(data_format)
            )

    def serialize_iterable(self, data_format, stat_iterable):
        if data_format == DataFormat.JSON:
            return stat_iterable
        elif data_format == DataFormat.BYTE_ARRAY:
            json_str = json.dumps(stat_iterable)
            return bytearray(json_str, encoding="utf8")
        else:
            raise NotImplementedError(
                "Metric serialization does not support data format {}".format(data_format)
            )


class DeploymentStatsContainer(StatsContainer):
    """
    Deployment stats data formatter.
    """

    def __init__(self, general_stats, deployment_stats):
        if not isinstance(general_stats, GeneralStats):
            raise DRUnsupportedType(
                "Wrong value type for general_stats. Expected: {}, provided: {}".format(
                    GeneralStats, type(general_stats)
                )
            )
        if not isinstance(deployment_stats, DeploymentStats):
            raise DRUnsupportedType(
                "Wrong value type for deployment_stats. Expected: {}, provided: {}".format(
                    DeploymentStats, type(deployment_stats)
                )
            )

        self._general_stats = general_stats
        self._deployment_stats = deployment_stats
        self._estimate_size = None

    def get_estimate_size(self):
        if self._estimate_size is None:
            self._estimate_size = estimate_metric_size(self._general_stats) + estimate_metric_size(
                self._deployment_stats
            )
        return self._estimate_size

    def data_type(self):
        return DataType.DEPLOYMENT_STATS

    def to_iterable(self):
        ret = dict()
        ret[
            SerializationConstants.GeneralConstants.TIMESTAMP_FIELD_NAME
        ] = self._general_stats.get_timestamp()
        ret[
            SerializationConstants.GeneralConstants.MODEL_ID_FIELD_NAME
        ] = self._general_stats.get_model_id()
        if self._general_stats.get_batch_name():
            ret[
                SerializationConstants.GeneralConstants.BATCH_NAME_FIELD_NAME
            ] = self._general_stats.get_batch_name()
        ret[
            SerializationConstants.DeploymentStatsConstants.NUM_PREDICTIONS_FIELD_NAME
        ] = self._deployment_stats.get_num_predictions()
        ret[
            SerializationConstants.DeploymentStatsConstants.EXECUTION_TIME_FIELD_NAME
        ] = self._deployment_stats.get_execution_time()
        return ret


class CustomMetricContainer(StatsContainer):
    """
    Custom Metric data formatter.
    """

    MODEL_PACKAGE_ID_FIELD_NAME = (
        SerializationConstants.CustomMetricStatsConstants.MODEL_PACKAGE_ID_FIELD_NAME
    )
    METRIC_ID_FIELD_NAME = SerializationConstants.CustomMetricStatsConstants.METRIC_ID_FIELD_NAME
    METRIC_VALUE_FIELD_NAME = (
        SerializationConstants.CustomMetricStatsConstants.METRIC_VALUE_FIELD_NAME
    )
    TIMESTAMP_FIELD_NAME = SerializationConstants.GeneralConstants.TIMESTAMP_FIELD_NAME
    BUCKETS_FIELD_NAME = SerializationConstants.CustomMetricStatsConstants.BUCKETS_FIELD_NAME

    def __init__(self, general_stats, custom_metric):
        if not isinstance(general_stats, GeneralStats):
            raise DRUnsupportedType(
                "Wrong value type for general_stats. Expected: {}, provided: {}".format(
                    GeneralStats, type(general_stats)
                )
            )
        if not isinstance(custom_metric, CustomMetric):
            raise DRUnsupportedType(
                "Wrong value type for custom_metric. Expected: {}, provided: {}".format(
                    CustomMetric, type(custom_metric)
                )
            )

        self._general_stats = general_stats
        self._custom_metric = custom_metric
        self._estimate_size = None

    def get_estimate_size(self):
        if self._estimate_size is None:
            self._estimate_size = estimate_metric_size(self._general_stats) + estimate_metric_size(
                self._custom_metric
            )
        return self._estimate_size

    def data_type(self):
        return DataType.CUSTOM_METRIC

    def get_num_rows(self):
        return self._custom_metric.get_nr_rows()

    def to_iterable(self):
        """
        This is how the payload looks like.
        Note: the metricId is part of the payload we send over the queue but is not part of the
              payload when sending to the Agent. This is since the agent is getting the metric ID
              as part of the request structure.

        payload = {
            "modelPackageId": "634d4cac98e7e9d429a81e85",
            "metricId": "xxxxxxxx" # this is only in the agent payloads
            "buckets": [
                {"timestamp": "2016-12-13T11:12:13.141516Z", "value": 10.0},
                {"timestamp": "2016-12-13T11:12:14.565122Z", "value": 20.0},
            ],
        }
        """
        ret = dict()
        ret[self.MODEL_PACKAGE_ID_FIELD_NAME] = self._general_stats.get_model_id()
        ret[self.METRIC_ID_FIELD_NAME] = self._custom_metric.get_metric_id()

        buckets = []
        for value, timestamp in zip(
            self._custom_metric.get_values(), self._custom_metric.get_timestamps()
        ):
            buckets.append(
                {self.TIMESTAMP_FIELD_NAME: timestamp, self.METRIC_VALUE_FIELD_NAME: value}
            )
        ret[self.BUCKETS_FIELD_NAME] = buckets
        return ret


class PredictionsStatsContainer(StatsContainer):
    """
    Predictions stats data formatter.
    """

    def __init__(self, general_stats, predictions_stats):
        if not isinstance(general_stats, GeneralStats):
            raise DRUnsupportedType(
                "Wrong value type for general_stats. Expected: {}, provided: {}".format(
                    GeneralStats, type(general_stats)
                )
            )
        if not isinstance(predictions_stats, PredictionsStats):
            raise DRUnsupportedType(
                "Wrong value type for predictions_stats. Expected: {}, provided: {}".format(
                    PredictionsStats, type(predictions_stats)
                )
            )

        self._general_stats = general_stats
        self._predictions_stats = predictions_stats

    def data_type(self):
        return DataType.TARGET_DRIFT

    def to_iterable(self):
        results_array = []
        results_object = dict()
        results_object[
            SerializationConstants.GeneralConstants.TIMESTAMP_FIELD_NAME
        ] = self._general_stats.get_timestamp()
        results_object[
            SerializationConstants.PredictionsStatsConstants.PREDICTIONS_FIELD_NAME
        ] = self._predictions_stats.get_predictions()

        # If association_ids are specified, then include them
        if self._predictions_stats.get_association_ids():
            results_object[
                SerializationConstants.PredictionsStatsConstants.ASSOCIATION_IDS_FIELD_NAME
            ] = self._predictions_stats.get_association_ids()

        results_object[
            SerializationConstants.GeneralConstants.MODEL_ID_FIELD_NAME
        ] = self._general_stats.get_model_id()
        results_array.append(results_object)

        ret = dict()
        ret[SerializationConstants.PredictionsStatsConstants.RESULTS_FIELD_NAME] = results_array
        if self._predictions_stats.get_class_names() is not None:
            ret[
                SerializationConstants.PredictionsStatsConstants.CLASS_NAMES_FIELD_NAME
            ] = self._predictions_stats.get_class_names()
        return ret


class FeatureDataStatsContainer(StatsContainer):
    """
    Feature data formatter.
    """

    def __init__(self, feature_data_stats):
        if not isinstance(feature_data_stats, FeatureDataStats):
            raise DRUnsupportedType(
                "Wrong value type for feature_data_stats. Expected: {}, provided: {}".format(
                    FeatureDataStats, type(feature_data_stats)
                )
            )

        self._feature_data_stats = feature_data_stats

    def data_type(self):
        return DataType.FEATURE_DATA

    def to_iterable(self):
        return self._feature_data_stats.get_feature_data()


class PredictionsDataContainer(StatsContainer):
    """
    Features and Predictions data formatter.
    """

    def __init__(self, general_stats, predictions_data):
        if not isinstance(general_stats, GeneralStats):
            raise DRUnsupportedType(
                "Wrong value type for general_stats. Expected: {}, provided: {}".format(
                    GeneralStats, type(general_stats)
                )
            )
        if not isinstance(predictions_data, PredictionsData):
            raise DRUnsupportedType(
                "Wrong value type for predictions data. Expected: {}, provided: {}".format(
                    PredictionsData, type(predictions_data)
                )
            )

        self._general_stats = general_stats
        self._predictions_data = predictions_data
        self._num_rows = predictions_data.get_num_rows()
        self._estimate_size = None

    def get_estimate_size(self):
        # This is a CPU expensive operation so delay doing it until asked.
        if self._estimate_size is None:
            self._estimate_size = (
                estimate_metric_size(self._num_rows)
                + estimate_metric_size(self._general_stats)
                + estimate_metric_size(self._predictions_data)
            )
        return self._estimate_size

    def get_num_rows(self):
        return self._num_rows

    def data_type(self):
        return DataType.PREDICTIONS_DATA

    def to_iterable(self):
        predictions_data_object = dict()
        predictions_data_object[
            SerializationConstants.GeneralConstants.TIMESTAMP_FIELD_NAME
        ] = self._general_stats.get_timestamp()
        if self._general_stats.get_model_id():
            predictions_data_object[
                SerializationConstants.GeneralConstants.MODEL_ID_FIELD_NAME
            ] = self._general_stats.get_model_id()
        if self._general_stats.get_batch_name():
            predictions_data_object[
                SerializationConstants.GeneralConstants.BATCH_NAME_FIELD_NAME
            ] = self._general_stats.get_batch_name()

        # If features are specified, include them
        if self._predictions_data.has_feature_data():
            feature_data = self._feature_dataframe_to_feature_dict(
                self._predictions_data.get_feature_data_df()
            )
            predictions_data_object[
                SerializationConstants.PredictionsDataConstants.FEATURES_FIELD_NAME
            ] = feature_data

        # If predictions are specified, include them
        if self._predictions_data.get_predictions():
            predictions_data_object[
                SerializationConstants.PredictionsDataConstants.PREDICTIONS_FIELD_NAME
            ] = self._predictions_data.get_predictions()

        # If association_ids are specified, then include them
        if self._predictions_data.get_association_ids():
            predictions_data_object[
                SerializationConstants.PredictionsStatsConstants.ASSOCIATION_IDS_FIELD_NAME
            ] = self._predictions_data.get_association_ids()

        if self._predictions_data.get_class_names():
            predictions_data_object[
                SerializationConstants.PredictionsDataConstants.CLASS_NAMES_FIELD_NAME
            ] = self._predictions_data.get_class_names()

        if self._predictions_data.get_request_parameters():
            predictions_data_object[
                SerializationConstants.PredictionsDataConstants.REQUEST_PARAMETERS_FIELD_NAME
            ] = self._predictions_data.get_request_parameters()

        if self._predictions_data.get_forecast_distance():
            predictions_data_object[
                SerializationConstants.PredictionsDataConstants.FORECAST_DISTANCE_FIELD_NAME
            ] = self._predictions_data.get_forecast_distance()

        if self._predictions_data.get_row_index():
            predictions_data_object[
                SerializationConstants.PredictionsDataConstants.ROW_INDEX_FIELD_NAME
            ] = self._predictions_data.get_row_index()

        if self._predictions_data.get_partition():
            predictions_data_object[
                SerializationConstants.PredictionsDataConstants.PARTITION_FIELD_NAME
            ] = [
                ts.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                for ts in self._predictions_data.get_partition()
            ]

        if self._predictions_data.get_series_id():
            predictions_data_object[
                SerializationConstants.PredictionsDataConstants.SERIES_ID_FIELD_NAME
            ] = self._predictions_data.get_series_id()

        # Default value for skip aggregation is False, include them in payload only if they are True
        if self._predictions_data.skip_drift_tracking():
            predictions_data_object[
                SerializationConstants.PredictionsDataConstants.SKIP_DRIFT_TRACKING_FIELD_NAME
            ] = self._predictions_data.skip_drift_tracking()

        if self._predictions_data.skip_accuracy_tracking():
            predictions_data_object[
                SerializationConstants.PredictionsDataConstants.SKIP_ACCURACY_TRACKING_FIELD_NAME
            ] = self._predictions_data.skip_accuracy_tracking()
        return predictions_data_object

    def _feature_dataframe_to_feature_dict(self, feature_dataframe):
        if not isinstance(feature_dataframe, pd.DataFrame):
            raise DRUnsupportedType("feature_data argument has to be of type '{}'", pd.DataFrame)

        # Building feature data structure from dataframe
        feature_data = {}

        headers = list(feature_dataframe.columns)
        try:
            values = feature_dataframe.to_numpy()
        except AttributeError:
            # pandas before 0.24 doesn't have .to_numpy()
            values = feature_dataframe.values

        # TODO: Walking through a whole pandas dataframe is not efficient. Orjson supports ndarray
        # natively.

        # save columns of values into a dictionary:
        # {"feature1": [0.1, 0.2, 0.7], "feature2": ["aa", "bb", "cc"]}.
        for i in range(0, len(headers)):
            vals = values[:, i].tolist()
            supported_type = False
            missing_values = 0
            for j in range(0, len(vals)):
                val = vals[j]
                if val is None:
                    # missing features reported from the Java SDK are NoneType
                    missing_values += 1
                    continue
                if isinstance(val, float):
                    # Missing values of any column type are encoded as float nan in the pandas df.
                    # We need to read another column to determine the type of the column.
                    if isnan(val):
                        missing_values += 1
                        continue
                    supported_type = True
                    break
                if isinstance(val, int):
                    supported_type = True
                    break
                if isinstance(val, string_types):
                    supported_type = True
                    break
                if isinstance(val, Decimal):
                    # Decimal type cannot be json serialized; convert column to float.
                    # TODO: another approach is to convert with a `default` serializer with the
                    # call to `dumps`
                    for k in range(j, len(vals)):
                        vals[k] = float(vals[k])
                    supported_type = True
                    break
                else:
                    # TODO: once we have a logging mechanism, this should be logged and col skipped
                    raise DRUnsupportedType(
                        "feature_data field type is not supported '{}'".format(type(vals[j]))
                    )

            # If all values are NaN, then also include the feature
            if missing_values == len(vals):
                supported_type = True

            if supported_type:
                feature_data[headers[i]] = vals

        return feature_data


class AggregatedStatsContainer(StatsContainer):
    """
    Aggregated Stats formatter.
    """

    def __init__(self, general_stats, aggregated_stats):
        if not isinstance(general_stats, GeneralStats):
            raise DRUnsupportedType(
                "Wrong value type for general_stats. Expected: {}, provided: {}".format(
                    GeneralStats, type(general_stats)
                )
            )
        if not isinstance(aggregated_stats, AggregatedStats):
            raise DRUnsupportedType(
                "Wrong value type for predictions data. Expected: {}, provided: {}".format(
                    PredictionsData, type(aggregated_stats)
                )
            )
        self._general_stats = general_stats
        self._aggregated_stats = aggregated_stats
        self._estimate_size = None

    def get_estimate_size(self):
        # This is a CPU expensive operation so delay doing it until asked.
        if self._estimate_size is None:
            self._estimate_size = estimate_metric_size(self._general_stats) + estimate_metric_size(
                self._aggregated_stats
            )
        return self._estimate_size

    def to_iterable(self):
        aggregated_stat_object = dict()
        aggregated_stat_object[
            SerializationConstants.GeneralConstants.TIMESTAMP_FIELD_NAME
        ] = self._general_stats.get_timestamp()

        if self._general_stats.get_model_id():
            aggregated_stat_object[
                SerializationConstants.GeneralConstants.MODEL_ID_FIELD_NAME
            ] = self._general_stats.get_model_id()

        if self._general_stats.get_batch_name():
            aggregated_stat_object[
                SerializationConstants.GeneralConstants.BATCH_NAME_FIELD_NAME
            ] = self._general_stats.get_batch_name()

        aggregated_stat_object[
            SerializationConstants.AggregatedStatsConstants.NUMERIC_AGGREGATE_MAP
        ] = self._aggregated_stats.get_numeric_aggregate_map()
        aggregated_stat_object[
            SerializationConstants.AggregatedStatsConstants.CATEGORICAL_AGGREGATE_MAP
        ] = self._aggregated_stats.get_categorical_aggregate_maps()
        aggregated_stat_object[
            SerializationConstants.AggregatedStatsConstants.PREDICTION_AGGREGATE_MAP
        ] = self._aggregated_stats.get_prediction_aggregate_map()
        aggregated_stat_object[
            SerializationConstants.AggregatedStatsConstants.SEGMENT_ATTRIBUTES_AGGREGATE_STATS
        ] = self._aggregated_stats.get_segment_attributes_aggregated_stats()

        if self._aggregated_stats.get_class_names():
            aggregated_stat_object[
                SerializationConstants.PredictionsDataConstants.CLASS_NAMES_FIELD_NAME
            ] = self._aggregated_stats.get_class_names()

        return aggregated_stat_object

    def data_type(self):
        return DataType.PREDICTION_STATS


class EventContainer(StatsContainer):
    """
    External event data formatter.
    """

    def __init__(self, event):
        if not isinstance(event, Event):
            raise DRUnsupportedType(
                "Wrong value type for event. Expected: {}, provided: {}".format(Event, type(event))
            )
        self._event = event
        self._estimate_size = None

    def get_estimate_size(self):
        if self._estimate_size is None:
            self._estimate_size = estimate_metric_size(self._event)
        return self._estimate_size

    def data_type(self):
        return DataType.EXTERNAL_EVENT

    def to_iterable(self):
        ret = dict()
        ret[
            SerializationConstants.GeneralConstants.TIMESTAMP_FIELD_NAME
        ] = self._event.get_timestamp()
        ret[
            SerializationConstants.EventConstants.EVENT_TYPE_FIELD_NAME
        ] = self._event.get_event_type()
        ret[SerializationConstants.EventConstants.MESSAGE_FIELD_NAME] = self._event.get_message()
        ret[SerializationConstants.EventConstants.ORG_ID_FIELD_NAME] = self._event.get_org_id()
        ret[
            SerializationConstants.EventConstants.ENTITY_ID_FIELD_NAME
        ] = self._event.get_entity_id()
        ret[
            SerializationConstants.EventConstants.PREDICTION_REQUEST_DATA_FIELD_NAME
        ] = self._event.get_prediction_request_data()
        return ret
