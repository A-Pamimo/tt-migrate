"""Main AST analyzer that uses the torch visitor and compatibility matrix."""

import ast
from typing import Optional

from server.services.compatibility.matrix import lookup_operation
from server.services.parser.diagnostic import (
    AnalysisResult,
    CompatibilityStatus,
    Diagnostic,
    Severity,
)
from server.services.parser.torch_visitor import TorchVisitor


def analyze_code(source_code: str, filename: str = "<input>") -> AnalysisResult:
    """Analyze Python source code for torch operations and their ttnn compatibility.

    Args:
        source_code: The Python source code to analyze.
        filename: Optional filename for error messages.

    Returns:
        An AnalysisResult with all diagnostics and summary statistics.

    Raises:
        SyntaxError: If the code cannot be parsed.
    """
    tree = ast.parse(source_code, filename=filename)
    visitor = TorchVisitor()
    visitor.visit(tree)

    result = AnalysisResult()

    for op in visitor.operations:
        compat = lookup_operation(op.operation)
        diagnostic = _build_diagnostic(op, compat)
        result.diagnostics.append(diagnostic)

    result.compute_stats()
    return result


def _build_diagnostic(
    op: "TorchVisitor.operations",
    compat: Optional[dict],
) -> Diagnostic:
    """Build a Diagnostic from a detected operation and its compatibility data."""
    from server.services.parser.torch_visitor import TorchOperation

    assert isinstance(op, TorchOperation)

    if compat is None:
        return Diagnostic(
            line=op.line,
            column=op.column,
            operation=op.operation,
            severity=Severity.WARNING,
            message=f"Operation '{op.operation}' not found in compatibility matrix",
            ttnn_equivalent=None,
            status=CompatibilityStatus.UNKNOWN,
            notes="This operation is not yet cataloged. Manual review recommended.",
            category="Unknown",
        )

    status_str = compat["status"]
    status = CompatibilityStatus(status_str)
    ttnn_eq = compat.get("ttnn_equivalent")
    notes = compat.get("notes", "")
    category = compat.get("category", "")

    if status == CompatibilityStatus.SUPPORTED:
        severity = Severity.INFO
        message = (
            f"'{op.operation}' is fully supported. "
            f"Use '{ttnn_eq}' in ttnn."
        )
    elif status == CompatibilityStatus.PARTIAL:
        severity = Severity.WARNING
        message = (
            f"'{op.operation}' has partial support in ttnn"
            f"{f' via {ttnn_eq}' if ttnn_eq else ''}. "
            f"{notes}"
        )
    elif status == CompatibilityStatus.UNSUPPORTED:
        severity = Severity.ERROR
        message = (
            f"'{op.operation}' is not supported in ttnn. "
            f"{notes}"
        )
    else:
        severity = Severity.WARNING
        message = f"'{op.operation}' compatibility is unknown."

    return Diagnostic(
        line=op.line,
        column=op.column,
        operation=op.operation,
        severity=severity,
        message=message,
        ttnn_equivalent=ttnn_eq,
        status=status,
        notes=notes,
        category=category,
    )
