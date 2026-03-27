"""Request/response schemas for the /analyze endpoint."""

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class SeverityEnum(str, Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class CompatibilityStatusEnum(str, Enum):
    SUPPORTED = "supported"
    PARTIAL = "partial"
    UNSUPPORTED = "unsupported"
    UNKNOWN = "unknown"


class AnalyzeRequest(BaseModel):
    """Request body for POST /api/v1/analyze."""

    code: str = Field(..., description="Python source code to analyze")
    filename: Optional[str] = Field(
        default="<input>", description="Optional filename for error messages"
    )


class DiagnosticItem(BaseModel):
    """A single diagnostic result."""

    line: int
    column: int
    operation: str
    severity: SeverityEnum
    message: str
    ttnn_equivalent: Optional[str] = None
    status: CompatibilityStatusEnum
    notes: Optional[str] = None
    category: str = ""


class AnalyzeResponse(BaseModel):
    """Response body for POST /api/v1/analyze."""

    diagnostics: List[DiagnosticItem]
    summary: "AnalysisSummary"


class AnalysisSummary(BaseModel):
    """Summary statistics for the analysis."""

    total_operations: int
    supported: int
    partial: int
    unsupported: int
    unknown: int
    compatibility_score: float = Field(
        ..., description="Compatibility score as a percentage (0-100)"
    )
