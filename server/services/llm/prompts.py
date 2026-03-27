"""System and refactoring prompt templates for LLM-based code migration."""

SYSTEM_PROMPT = """You are an expert in migrating PyTorch models to Tenstorrent's ttnn library.
Your task is to refactor PyTorch code to use ttnn operations where compatible.

Key rules:
1. Replace torch operations with their ttnn equivalents where supported.
2. For partially supported operations, add comments noting limitations.
3. For unsupported operations (like Dropout), remove or comment them out with an explanation.
4. Preserve the original model's logic and structure.
5. Add necessary ttnn imports at the top.
6. Include comments explaining each significant change.
7. Maintain proper Python formatting and readability.
8. Do NOT wrap the code in markdown code blocks - return raw Python code only.
"""

REFACTOR_PROMPT_TEMPLATE = """Refactor the following PyTorch code to use Tenstorrent's ttnn library.

## Original Code
```python
{source_code}
```

## Compatibility Analysis
The following diagnostics were identified:
{diagnostics}

## Instructions
- Replace all supported torch operations with their ttnn equivalents.
- For partially supported operations, use the ttnn equivalent but add a comment noting any limitations.
- For unsupported operations (e.g., Dropout), comment them out or remove them with an explanatory comment.
- Add `import ttnn` at the top of the file.
- Keep the overall model structure intact.
- Return ONLY the refactored Python code, no markdown formatting or explanations outside of code comments.
"""


def build_refactor_prompt(source_code: str, diagnostics: str) -> str:
    """Build the full refactoring prompt from source code and diagnostics."""
    return REFACTOR_PROMPT_TEMPLATE.format(
        source_code=source_code,
        diagnostics=diagnostics,
    )
