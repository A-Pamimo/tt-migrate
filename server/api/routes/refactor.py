"""POST /api/v1/refactor endpoint (+ SSE stream)."""

import json
import logging
from typing import AsyncIterator

from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse

from server.api.schemas.refactor import RefactorRequest, RefactorResponse
from server.services.llm.router import get_llm_router
from server.services.parser.ast_analyzer import analyze_code

logger = logging.getLogger(__name__)

router = APIRouter()


def _build_diagnostics_json(code: str) -> str:
    """Analyze code and return diagnostics as a JSON string."""
    try:
        result = analyze_code(code)
    except SyntaxError:
        return "[]"
    items = []
    for d in result.diagnostics:
        items.append(
            {
                "line": d.line,
                "operation": d.operation,
                "status": d.status.value,
                "ttnn_equivalent": d.ttnn_equivalent,
                "message": d.message,
            }
        )
    return json.dumps(items, indent=2)


@router.post("/refactor")
async def refactor(request: RefactorRequest):
    """Refactor PyTorch code to use ttnn.

    If `stream=true`, returns an SSE event stream.
    Otherwise, returns a JSON response with the refactored code.
    """
    llm_router = get_llm_router()
    diagnostics_json = _build_diagnostics_json(request.code)
    provider_name = request.provider.value if request.provider else None

    if request.stream:
        return EventSourceResponse(
            _stream_refactor(llm_router, request.code, diagnostics_json, provider_name)
        )

    try:
        refactored, used_provider = await llm_router.refactor(
            source_code=request.code,
            diagnostics=diagnostics_json,
            provider_name=provider_name,
        )
    except Exception as exc:
        logger.exception("Refactor failed")
        raise HTTPException(
            status_code=502,
            detail={"error": "LLM refactoring failed", "message": str(exc)},
        )

    return RefactorResponse(
        refactored_code=refactored,
        provider_used=used_provider,
        original_code=request.code,
        explanation=None,
    )


async def _stream_refactor(
    llm_router, code: str, diagnostics_json: str, provider_name: str | None
) -> AsyncIterator[dict]:
    """Yield SSE events for streaming refactoring."""
    try:
        async for chunk, used_provider in llm_router.refactor_stream(
            source_code=code,
            diagnostics=diagnostics_json,
            provider_name=provider_name,
        ):
            yield {
                "event": "chunk",
                "data": json.dumps({"content": chunk, "provider": used_provider}),
            }
        yield {"event": "done", "data": json.dumps({"status": "complete"})}
    except Exception as exc:
        logger.exception("Stream refactor failed")
        yield {
            "event": "error",
            "data": json.dumps({"error": str(exc)}),
        }
