"""Offline SOS registry adapter scaffolding and strict CSV normalization."""

from .base import (
    BaseRegistryAdapter,
    BatchNormalizationResult,
    ComplianceFlag,
    NormalizedRecord,
    RecordValidationError,
    ValidationIssue,
)
from .csv_adapter import CSVRegistryAdapter

__all__ = [
    "BaseRegistryAdapter",
    "BatchNormalizationResult",
    "ComplianceFlag",
    "CSVRegistryAdapter",
    "NormalizedRecord",
    "RecordValidationError",
    "ValidationIssue",
]
