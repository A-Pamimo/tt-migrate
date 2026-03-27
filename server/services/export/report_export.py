"""Generate Markdown migration reports."""

from server.services.parser.ast_analyzer import analyze_code
from server.services.parser.diagnostic import CompatibilityStatus


def generate_report(original_code: str, refactored_code: str) -> str:
    """Generate a Markdown migration report.

    Includes:
    - Summary statistics
    - Compatibility score
    - Change log for each detected operation
    - The refactored code

    Args:
        original_code: The original PyTorch source code.
        refactored_code: The refactored ttnn code.

    Returns:
        The report as a Markdown string.
    """
    try:
        result = analyze_code(original_code)
    except SyntaxError:
        result = None

    lines: list[str] = []
    lines.append("# TT-Migrate: Migration Report")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    if result:
        lines.append(f"- **Total operations detected:** {result.total_operations}")
        lines.append(f"- **Supported:** {result.supported_count}")
        lines.append(f"- **Partially supported:** {result.partial_count}")
        lines.append(f"- **Unsupported:** {result.unsupported_count}")
        lines.append(f"- **Unknown:** {result.unknown_count}")
        lines.append(f"- **Compatibility score:** {result.compatibility_score}%")
    else:
        lines.append("*Could not analyze original code.*")
    lines.append("")

    # Change log
    lines.append("## Change Log")
    lines.append("")
    if result and result.diagnostics:
        lines.append("| Line | Operation | Status | ttnn Equivalent | Notes |")
        lines.append("|------|-----------|--------|-----------------|-------|")
        for d in result.diagnostics:
            ttnn_eq = d.ttnn_equivalent or "N/A"
            notes = d.notes or ""
            status_icon = _status_icon(d.status)
            lines.append(
                f"| {d.line} | `{d.operation}` | {status_icon} {d.status.value} "
                f"| `{ttnn_eq}` | {notes} |"
            )
    else:
        lines.append("*No operations detected.*")
    lines.append("")

    # Refactored code
    lines.append("## Refactored Code")
    lines.append("")
    lines.append("```python")
    lines.append(refactored_code.strip())
    lines.append("```")
    lines.append("")

    return "\n".join(lines)


def _status_icon(status: CompatibilityStatus) -> str:
    """Return a text indicator for a compatibility status."""
    mapping = {
        CompatibilityStatus.SUPPORTED: "[OK]",
        CompatibilityStatus.PARTIAL: "[PARTIAL]",
        CompatibilityStatus.UNSUPPORTED: "[UNSUPPORTED]",
        CompatibilityStatus.UNKNOWN: "[?]",
    }
    return mapping.get(status, "")
