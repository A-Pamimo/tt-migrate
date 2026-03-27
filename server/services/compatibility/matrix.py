"""Compatibility matrix loader and lookup."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


_MATRIX_PATH = Path(__file__).parent / "data" / "compatibility_matrix.json"

_matrix_data: Optional[Dict[str, Any]] = None
_op_index: Optional[Dict[str, Dict[str, Any]]] = None


def _load_matrix() -> None:
    """Load the compatibility matrix from disk and build the index."""
    global _matrix_data, _op_index
    with open(_MATRIX_PATH, "r") as f:
        _matrix_data = json.load(f)
    _op_index = {}
    for op in _matrix_data["operations"]:
        _op_index[op["torch_op"]] = op


def get_matrix() -> Dict[str, Any]:
    """Return the full compatibility matrix."""
    if _matrix_data is None:
        _load_matrix()
    assert _matrix_data is not None
    return _matrix_data


def get_all_operations() -> List[Dict[str, Any]]:
    """Return all operations from the matrix."""
    return get_matrix()["operations"]


def lookup_operation(torch_op: str) -> Optional[Dict[str, Any]]:
    """Look up a single torch operation in the compatibility matrix.

    Tries exact match first, then attempts normalized matching by
    expanding common aliases.
    """
    if _op_index is None:
        _load_matrix()
    assert _op_index is not None

    # Exact match
    if torch_op in _op_index:
        return _op_index[torch_op]

    # Try common normalizations
    # e.g., "F.relu" -> "torch.nn.functional.relu"
    # e.g., "nn.Conv2d" -> "torch.nn.Conv2d"
    normalizations = _build_normalizations(torch_op)
    for norm in normalizations:
        if norm in _op_index:
            return _op_index[norm]

    return None


def _build_normalizations(torch_op: str) -> List[str]:
    """Build possible fully-qualified names for an operation."""
    results: List[str] = []

    # If already starts with torch., no further normalization
    if torch_op.startswith("torch."):
        return results

    # nn.X -> torch.nn.X
    if torch_op.startswith("nn."):
        results.append(f"torch.{torch_op}")

    # F.X -> torch.nn.functional.X
    if torch_op.startswith("F."):
        func_name = torch_op[2:]
        results.append(f"torch.nn.functional.{func_name}")

    # Plain name: try torch.X, torch.nn.X, torch.nn.functional.X
    if "." not in torch_op:
        results.append(f"torch.{torch_op}")
        results.append(f"torch.nn.{torch_op}")
        results.append(f"torch.nn.functional.{torch_op}")

    return results


def lookup_by_category(category: str) -> List[Dict[str, Any]]:
    """Return all operations in a given category."""
    return [
        op for op in get_all_operations()
        if op["category"].lower() == category.lower()
    ]


def lookup_by_status(status: str) -> List[Dict[str, Any]]:
    """Return all operations with a given status."""
    return [
        op for op in get_all_operations()
        if op["status"].lower() == status.lower()
    ]
