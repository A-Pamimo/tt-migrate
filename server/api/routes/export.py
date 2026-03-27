"""POST /api/v1/export endpoint."""

from fastapi import APIRouter, HTTPException

from server.api.schemas.export import ExportFormat, ExportRequest, ExportResponse
from server.services.export.notebook_export import generate_notebook
from server.services.export.python_export import generate_python
from server.services.export.report_export import generate_report

router = APIRouter()


@router.post("/export", response_model=ExportResponse)
async def export_code(request: ExportRequest) -> ExportResponse:
    """Export refactored code in the requested format."""
    try:
        if request.format == ExportFormat.PYTHON:
            filename = request.filename or "migrated_model.py"
            content = generate_python(request.refactored_code)
            content_type = "text/x-python"

        elif request.format == ExportFormat.NOTEBOOK:
            filename = request.filename or "migrated_model.ipynb"
            content = generate_notebook(
                original_code=request.original_code,
                refactored_code=request.refactored_code,
            )
            content_type = "application/x-ipynb+json"

        elif request.format == ExportFormat.REPORT:
            filename = request.filename or "migration_report.md"
            content = generate_report(
                original_code=request.original_code,
                refactored_code=request.refactored_code,
            )
            content_type = "text/markdown"

        else:
            raise HTTPException(
                status_code=400,
                detail={"error": f"Unsupported export format: {request.format}"},
            )
    except Exception as exc:
        if isinstance(exc, HTTPException):
            raise
        raise HTTPException(
            status_code=500,
            detail={"error": "Export generation failed", "message": str(exc)},
        )

    return ExportResponse(
        filename=filename,
        content=content,
        content_type=content_type,
    )
