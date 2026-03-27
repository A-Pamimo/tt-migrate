"""Tests for the compatibility matrix loader and lookup."""

import sys
from pathlib import Path

import pytest

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from server.services.compatibility.matrix import (
    get_all_operations,
    get_matrix,
    lookup_by_category,
    lookup_by_status,
    lookup_operation,
)


class TestMatrixLoader:
    """Tests for loading and querying the compatibility matrix."""

    def test_matrix_loads(self):
        """Matrix should load without error."""
        matrix = get_matrix()
        assert "operations" in matrix
        assert "version" in matrix

    def test_has_24_operations(self):
        """Matrix should contain exactly 24 operations."""
        ops = get_all_operations()
        assert len(ops) == 24

    def test_all_operations_have_required_fields(self):
        """Every operation should have torch_op, category, status, notes."""
        for op in get_all_operations():
            assert "torch_op" in op
            assert "category" in op
            assert "status" in op
            assert "notes" in op

    def test_valid_statuses(self):
        """All statuses should be one of: supported, partial, unsupported."""
        valid = {"supported", "partial", "unsupported"}
        for op in get_all_operations():
            assert op["status"] in valid, f"Invalid status for {op['torch_op']}: {op['status']}"


class TestLookup:
    """Tests for operation lookup."""

    def test_exact_match(self):
        """Should find torch.matmul by exact name."""
        result = lookup_operation("torch.matmul")
        assert result is not None
        assert result["torch_op"] == "torch.matmul"
        assert result["status"] == "supported"

    def test_conv2d_lookup(self):
        """Should find torch.nn.Conv2d."""
        result = lookup_operation("torch.nn.Conv2d")
        assert result is not None
        assert result["ttnn_equivalent"] == "ttnn.conv2d"

    def test_functional_relu_lookup(self):
        """Should find torch.nn.functional.relu."""
        result = lookup_operation("torch.nn.functional.relu")
        assert result is not None
        assert result["ttnn_equivalent"] == "ttnn.relu"

    def test_dropout_unsupported(self):
        """Dropout should be unsupported."""
        result = lookup_operation("torch.nn.Dropout")
        assert result is not None
        assert result["status"] == "unsupported"
        assert result["ttnn_equivalent"] is None

    def test_batchnorm_partial(self):
        """BatchNorm2d should be partial."""
        result = lookup_operation("torch.nn.BatchNorm2d")
        assert result is not None
        assert result["status"] == "partial"

    def test_multihead_attention_partial(self):
        """MultiheadAttention should be partial."""
        result = lookup_operation("torch.nn.MultiheadAttention")
        assert result is not None
        assert result["status"] == "partial"

    def test_unknown_op_returns_none(self):
        """Unknown operations should return None."""
        result = lookup_operation("torch.nn.FakeOp")
        assert result is None

    def test_normalization_nn_prefix(self):
        """Should find nn.Conv2d via normalization to torch.nn.Conv2d."""
        result = lookup_operation("nn.Conv2d")
        assert result is not None
        assert result["torch_op"] == "torch.nn.Conv2d"

    def test_normalization_f_prefix(self):
        """Should find F.relu via normalization to torch.nn.functional.relu."""
        result = lookup_operation("F.relu")
        assert result is not None
        assert result["torch_op"] == "torch.nn.functional.relu"


class TestFilterQueries:
    """Tests for category and status filtering."""

    def test_filter_by_category(self):
        """Should return all activations."""
        ops = lookup_by_category("Activations")
        assert len(ops) > 0
        assert all(op["category"] == "Activations" for op in ops)

    def test_filter_by_status_supported(self):
        """Should return supported operations."""
        ops = lookup_by_status("supported")
        assert len(ops) > 0
        assert all(op["status"] == "supported" for op in ops)

    def test_filter_by_status_unsupported(self):
        """Should return unsupported operations."""
        ops = lookup_by_status("unsupported")
        assert len(ops) > 0
        assert all(op["status"] == "unsupported" for op in ops)

    def test_filter_by_status_partial(self):
        """Should return partially supported operations."""
        ops = lookup_by_status("partial")
        assert len(ops) > 0
        assert all(op["status"] == "partial" for op in ops)
