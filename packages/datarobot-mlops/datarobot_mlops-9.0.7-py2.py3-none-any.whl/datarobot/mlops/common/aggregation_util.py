from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict

import numpy as np
import six
from datarobot.mlops.common.exception import DRApiException
from datarobot.mlops.common.stringutil import camelize
from datarobot.mlops.metric import AggregatedStats
from datarobot.mlops.metric import SerializationConstants

#  Copyright (c) 2021 DataRobot, Inc. and its affiliates. All rights reserved.
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


agg_stats_data_keys = SerializationConstants.AggregatedStatsConstants


def build_aggregated_stats(aggregated_output, class_names):
    numeric_stats = aggregated_output.get("numeric_stats")
    categorical_stats = aggregated_output.get("categorical_stats")
    prediction_stats = aggregated_output.get("prediction_stats")
    segment_attributes_stats = aggregated_output.get("segment_stats")

    return AggregatedStats(
        numeric_aggregate_map=_convert_stats_to_dict(numeric_stats),
        categorical_aggregate_map=_convert_stats_to_dict(categorical_stats),
        prediction_aggregate_map=_convert_predictions_stats_to_dict(prediction_stats, class_names),
        segment_attributes_aggregated_stats=_convert_segments_attributes_stats_to_dict(
            segment_attributes_stats, class_names
        ),
        class_names=class_names,
    )


def _aggregated_stat_to_dict(aggregated_stat):
    from datarobot.mlops.stats_aggregator.histogram import CentroidHistogram

    return_dict = dict()
    for k1, v1 in six.iteritems(aggregated_stat._asdict()):
        if isinstance(v1, np.int64):
            return_dict[camelize(k1)] = int(v1)
        elif isinstance(v1, np.floating):
            return_dict[camelize(k1)] = float(v1)
        elif isinstance(v1, CentroidHistogram):
            # convert histogram to spooler format
            return_dict[camelize(k1)] = {
                "maxLength": v1.max_length,
                "bucketList": [
                    {"centroid": float(b.centroid), "count": int(b.count)} for b in v1.buckets
                ],
            }
        else:
            return_dict[camelize(k1)] = v1

    return return_dict


def _convert_stats_to_dict(aggregated_stats):
    return {k: _aggregated_stat_to_dict(v) for k, v in six.iteritems(aggregated_stats)}


def _convert_predictions_stats_to_dict(prediction_stats, class_names):
    return_dict = {}
    if class_names is None:
        class_names = ["0"]  # Regression

    for class_name, prediction_stat in zip(class_names, prediction_stats):
        return_dict[class_name] = _aggregated_stat_to_dict(prediction_stat)
    return return_dict


def _convert_segments_attributes_stats_to_dict(segment_attributes_stats, class_names):
    return_dict = defaultdict(dict)
    for attribute_name, values in six.iteritems(segment_attributes_stats):
        for value_name, agg_stats in six.iteritems(values):
            return_dict[attribute_name][value_name] = {
                agg_stats_data_keys.NUMERIC_AGGREGATE_MAP: _convert_stats_to_dict(
                    agg_stats.get("numeric_stats")
                ),
                agg_stats_data_keys.CATEGORICAL_AGGREGATE_MAP: _convert_stats_to_dict(
                    agg_stats.get("categorical_stats")
                ),
                agg_stats_data_keys.PREDICTION_AGGREGATE_MAP: _convert_predictions_stats_to_dict(
                    agg_stats.get("prediction_stats"), class_names
                ),
            }
    return {"segmentStatsMap": dict(return_dict)}


# methods to convert dict to DR controller format


def _dict_to_histogram(histogram):
    if not histogram or "bucketList" not in histogram:
        return None

    centroids, counts = list(), list()
    for bucket in histogram["bucketList"]:
        centroids.append(bucket["centroid"])
        counts.append(bucket["count"])

    return {"centroids": centroids, "counts": counts}


def _convert_stat_format(stat):
    stat.pop("missingCount")
    stat["histogram"] = _dict_to_histogram(stat["histogram"])
    return stat


def _convert_to_numeric_stat(feature_name, stat):
    missing_count = stat.pop("missingCount", 0)
    stat["histogram"] = _dict_to_histogram(stat["histogram"])
    return {
        "name": feature_name,
        "stats": {
            "numericStats": stat,
            "missingCount": missing_count,
        },
    }


def _convert_to_category_stat(feature_name, stat):
    categories, counts = list(), list()
    for category, count in six.iteritems(stat["categoryCounts"]):
        categories.append(category)
        counts.append(count)

    return {
        "name": feature_name,
        "stats": {
            "count": stat["count"],
            "missingCount": stat["missingCount"],
            "categories": {
                "values": categories,
                "counts": counts,
            },
        },
    }


def convert_aggregated_stats_features_to_dr_format(numeric_stat=None, category_stat=None):
    feature_list = list()
    if numeric_stat:
        for feature_name, stat in six.iteritems(numeric_stat):
            feature_list.append(_convert_to_numeric_stat(feature_name, stat))

    if category_stat:
        for feature_name, stat in six.iteritems(category_stat):
            feature_list.append(_convert_to_category_stat(feature_name, stat))

    return feature_list


def convert_aggregated_stats_predictions_to_dr_format(prediction_stats=None):
    prediction_list = list()
    if prediction_stats:
        for _, stat in six.iteritems(prediction_stats):
            prediction_list.append(_convert_stat_format(stat))
    return prediction_list


def convert_aggregated_stats_segment_attr_to_dr_format(segment_attributes_stats=None):
    if (not segment_attributes_stats) or ("segmentStatsMap" not in segment_attributes_stats):
        return None

    segment_attributes_stats_map = segment_attributes_stats["segmentStatsMap"]
    segment_list = list()
    for attribute_name, values in six.iteritems(segment_attributes_stats_map):
        segment_attr = list()
        for value_name, stats in six.iteritems(values):
            segment_attr.append(
                {
                    "value": value_name,
                    "features": convert_aggregated_stats_features_to_dr_format(
                        stats.get(agg_stats_data_keys.NUMERIC_AGGREGATE_MAP),
                        stats.get(agg_stats_data_keys.CATEGORICAL_AGGREGATE_MAP),
                    ),
                    "predictions": convert_aggregated_stats_predictions_to_dr_format(
                        stats.get(agg_stats_data_keys.PREDICTION_AGGREGATE_MAP)
                    ),
                }
            )
        segment_list.append({"name": attribute_name, "data": segment_attr})
    return segment_list


def validate_feature_types(feature_types):
    if not isinstance(feature_types, list):
        raise DRApiException("feature_types needs to be a list.")

    if len(feature_types) == 0:
        raise DRApiException("feature_types is empty.")

    from datarobot.mlops.stats_aggregator.types import FeatureDescriptor

    for feature_desc in feature_types:
        if isinstance(feature_desc, FeatureDescriptor):
            continue
        elif isinstance(feature_desc, dict):
            if "name" not in feature_desc:
                raise DRApiException("feature_types does not contains field[name].")

            if "feature_type" not in feature_desc:
                raise DRApiException("feature_types does not contains field[feature_type].")
        else:
            raise DRApiException("feature_types items should be a FeatureDescriptor or dict.")


def convert_dict_to_feature_types(feature_types):
    if feature_types is None:
        return None

    from datarobot.mlops.stats_aggregator.types import FeatureDescriptor

    return [FeatureDescriptor(**f) if isinstance(f, dict) else f for f in feature_types]
