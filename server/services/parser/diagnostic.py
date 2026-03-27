"""Diagnostic result dataclasses for AST analysis."""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class Severity(str, Enum):
    """Severity level for a diagnostic."""

    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class CompatibilityStatus(str, Enum):
    """Compatibility status for a torch operation."""

    SUPPORTED = "supported"
    PARTIAL = "partial"
    UNSUPPORTED = "unsupported"
    UNKNOWN = "unknown"


@dataclass
class Diagnostic:
    """A single diagnostic result from AST analysis."""

    line: int
    column: int
    operation: str
    severity: Severity
    message: str
    ttnn_equivalent: Optional[str] = None
    status: CompatibilityStatus = CompatibilityStatus.UNKNOWN
    notes: Optional[str] = None
    category: str = ""


@dataclass
class AnalysisResult:
    """Complete analysis result for a piece of code."""

    diagnostics: List[Diagnostic] = field(default_factory=list)
    total_operations: int = 0
    supported_count: int = 0
    partial_count: int = 0
    unsupported_count: int = 0
    unknown_count: int = 0
    compatibility_score: float = 0.0

    def compute_stats(self) -> None:
        """Compute summary statistics from diagnostics."""
        self.total_operations = len(self.diagnostics)
        self.supported_count = sum(
            1 for d in self.diagnostics if d.status == CompatibilityStatus.SUPPORTED
        )
        self.partial_count = sum(
            1 for d in self.diagnostics if d.status == CompatibilityStatus.PARTIAL
        )
        self.unsupported_count = sum(
            1 for d in self.diagnostics if d.status == CompatibilityStatus.UNSUPPORTED
        )
        self.unknown_count = sum(
            1 for d in self.diagnostics if d.status == CompatibilityStatus.UNKNOWN
        )
        if self.total_operations > 0:
            # Supported = 1.0, Partial = 0.5, Unsupported/Unknown = 0.0
            score = (
                self.supported_count * 1.0 + self.partial_count * 0.5
            ) / self.total_operations
            self.compatibility_score = round(score * 100, 1)
        else:
            self.compatibility_score = 100.0
