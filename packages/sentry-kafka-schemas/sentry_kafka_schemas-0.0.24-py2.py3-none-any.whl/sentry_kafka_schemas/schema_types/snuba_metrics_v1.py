from typing import Union, List, Dict, TypedDict, Literal, Any
from typing_extensions import Required


class Metric(TypedDict, total=False):
    """metric."""

    version: Literal[1]
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

    tags: Required["_MetricTags"]
    """Required property"""

    value: Required[Union[Union[int, float], List[Union[int, float]]]]
    """Required property"""

    retention_days: Required[int]
    """Required property"""

    mapping_meta: Required["_MetricMappingMeta"]
    """Required property"""



_MetricMappingMeta = Dict[str, Any]
"""
patternProperties:
  ^[chdfr]$:
    $ref: '#/definitions/IntToString'
"""



_MetricTags = Dict[str, Any]
"""
patternProperties:
  ^[0-9]$:
    type: integer
"""

