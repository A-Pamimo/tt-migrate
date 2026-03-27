"""Request/response schemas for the /export endpoint."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class ExportFormat(str, Enum):
    PYTHON = "python"
    NOTEBOOK = "notebook"
    REPORT = "report"


class ExportRequest(BaseModel):
    """Request body for POST /api/v1/export."""

    original_code: str = Field(..., description="The original PyTorch code")
    refactored_code: str = Field(..., description="The refactored ttnn code")
    format: ExportFormat = Field(..., description="Export format: python, notebook, or report")
    filename: Optional[str] = Field(
        default=None, description="Desired output filename (auto-generated if omitted)"
    )


class ExportResponse(BaseModel):
    """Response body for POST /api/v1/export."""

    filename: str = Field(..., description="Generated filename")
    content: str = Field(..., description="File content (string for .py/.md, JSON string for .ipynb)")
    content_type: str = Field(..., description="MIME type of the content")
