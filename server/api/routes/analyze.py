"""POST /api/v1/analyze endpoint."""

from fastapi import APIRouter, HTTPException

from server.api.schemas.analyze import (
    AnalysisSummary,
    AnalyzeRequest,
    AnalyzeResponse,
    CompatibilityStatusEnum,
    DiagnosticItem,
    SeverityEnum,
)
from server.services.parser.ast_analyzer import analyze_code

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Analyze Python source code for torch operations and ttnn compatibility."""
    try:
        result = analyze_code(request.code, filename=request.filename or "<input>")
    except SyntaxError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Failed to parse Python code",
                "message": str(exc),
                "line": getattr(exc, "lineno", None),
            },
        )

    diagnostics = [
        DiagnosticItem(
            line=d.line,
            column=d.column,
            operation=d.operation,
            severity=SeverityEnum(d.severity.value),
            message=d.message,
            ttnn_equivalent=d.ttnn_equivalent,
            status=CompatibilityStatusEnum(d.status.value),
            notes=d.notes,
            category=d.category,
        )
        for d in result.diagnostics
    ]

    summary = AnalysisSummary(
        total_operations=result.total_operations,
        supported=result.supported_count,
        partial=result.partial_count,
        unsupported=result.unsupported_count,
        unknown=result.unknown_count,
        compatibility_score=result.compatibility_score,
    )

    return AnalyzeResponse(diagnostics=diagnostics, summary=summary)
