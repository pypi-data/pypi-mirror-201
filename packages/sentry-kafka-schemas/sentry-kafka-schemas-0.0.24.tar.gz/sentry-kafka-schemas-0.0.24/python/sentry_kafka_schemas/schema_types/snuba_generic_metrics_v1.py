from typing import Dict, Literal, Union, Any, List, TypedDict
from typing_extensions import Required


class GenericMetric(TypedDict, total=False):
    """generic_metric."""

    version: Literal[2]
    use_case_id: Required[str]
    """Required property"""

    org_id: Required[int]
    """Required property"""

    project_id: Required[int]
    """Required property"""

    metric_id: Required[int]
    """Required property"""

    type: Required[str]
    """Required property"""

    timestamp: Required[int]
    """Required property"""

    tags: Required[Dict[str, str]]
    """Required property"""

    value: Required[Union[Union[int, float], List[Union[int, float]]]]
    """Required property"""

    retention_days: Required[int]
    """Required property"""

    mapping_meta: Required["_GenericMetricMappingMeta"]
    """Required property"""



_GenericMetricMappingMeta = Dict[str, Any]
"""
patternProperties:
  ^[chdfr]$:
    $ref: '#/definitions/IntToString'
"""

