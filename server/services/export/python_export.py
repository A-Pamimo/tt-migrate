"""Generate clean .py files with ttnn imports."""


def generate_python(refactored_code: str) -> str:
    """Generate a clean Python file from refactored code.

    Ensures the output has proper ttnn imports and a module docstring.

    Args:
        refactored_code: The ttnn-refactored Python code.

    Returns:
        A complete Python file as a string.
    """
    lines = refactored_code.strip().splitlines()

    # Check if ttnn import already present
    has_ttnn_import = any(
        line.strip().startswith("import ttnn") or "from ttnn" in line
        for line in lines
    )

    output_lines: list[str] = []

    # Add module docstring if not present
    if not (lines and lines[0].strip().startswith('"""')):
        output_lines.append('"""Model migrated to Tenstorrent ttnn by TT-Migrate."""')
        output_lines.append("")

    # Insert ttnn import if missing
    if not has_ttnn_import:
        # Find the right place to insert (after existing imports)
        import_end = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("import ") or stripped.startswith("from "):
                import_end = i + 1
            elif stripped and not stripped.startswith("#") and import_end > 0:
                break

        if import_end == 0:
            # No imports found, put at the top
            output_lines.append("import ttnn")
            output_lines.append("")
            output_lines.extend(lines)
        else:
            output_lines.extend(lines[:import_end])
            output_lines.append("import ttnn")
            output_lines.append("")
            output_lines.extend(lines[import_end:])
    else:
        output_lines.extend(lines)

    # Ensure trailing newline
    result = "\n".join(output_lines)
    if not result.endswith("\n"):
        result += "\n"
    return result
