"""Tests for the AST parser and torch visitor."""

import sys
from pathlib import Path

import pytest

# Ensure the project root is on the path
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from server.services.parser.ast_analyzer import analyze_code
from server.services.parser.diagnostic import CompatibilityStatus, Severity
from server.services.parser.torch_visitor import TorchVisitor

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _read_fixture(name: str) -> str:
    return (FIXTURES_DIR / name).read_text()


# ── SimpleCNN tests ──


class TestSimpleCNN:
    """Tests for parsing the SimpleCNN fixture."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.code = _read_fixture("sample_cnn.py")
        self.result = analyze_code(self.code)

    def test_detects_operations(self):
        """Should detect multiple torch operations."""
        assert self.result.total_operations > 0

    def test_detects_conv2d(self):
        """Should detect nn.Conv2d calls."""
        ops = [d.operation for d in self.result.diagnostics]
        conv_ops = [o for o in ops if "Conv2d" in o]
        assert len(conv_ops) >= 2, f"Expected at least 2 Conv2d ops, found: {conv_ops}"

    def test_detects_batchnorm(self):
        """Should detect nn.BatchNorm2d calls."""
        ops = [d.operation for d in self.result.diagnostics]
        bn_ops = [o for o in ops if "BatchNorm2d" in o]
        assert len(bn_ops) >= 2, f"Expected at least 2 BatchNorm2d ops, found: {bn_ops}"

    def test_detects_linear(self):
        """Should detect nn.Linear calls."""
        ops = [d.operation for d in self.result.diagnostics]
        linear_ops = [o for o in ops if "Linear" in o]
        assert len(linear_ops) >= 2, f"Expected at least 2 Linear ops, found: {linear_ops}"

    def test_detects_maxpool(self):
        """Should detect nn.MaxPool2d calls."""
        ops = [d.operation for d in self.result.diagnostics]
        pool_ops = [o for o in ops if "MaxPool2d" in o]
        assert len(pool_ops) >= 1, f"Expected at least 1 MaxPool2d op, found: {pool_ops}"

    def test_detects_relu(self):
        """Should detect F.relu calls."""
        ops = [d.operation for d in self.result.diagnostics]
        relu_ops = [o for o in ops if "relu" in o.lower()]
        assert len(relu_ops) >= 1, f"Expected at least 1 relu op, found: {relu_ops}"

    def test_detects_dropout(self):
        """Should detect nn.Dropout calls."""
        ops = [d.operation for d in self.result.diagnostics]
        dropout_ops = [o for o in ops if "Dropout" in o]
        assert len(dropout_ops) >= 1, f"Expected at least 1 Dropout op, found: {dropout_ops}"

    def test_dropout_unsupported(self):
        """Dropout should be marked as unsupported."""
        dropout_diags = [
            d for d in self.result.diagnostics if "Dropout" in d.operation
        ]
        assert len(dropout_diags) > 0
        for d in dropout_diags:
            assert d.status == CompatibilityStatus.UNSUPPORTED

    def test_batchnorm_partial(self):
        """BatchNorm2d should be marked as partial."""
        bn_diags = [
            d for d in self.result.diagnostics if "BatchNorm2d" in d.operation
        ]
        assert len(bn_diags) > 0
        for d in bn_diags:
            assert d.status == CompatibilityStatus.PARTIAL

    def test_conv2d_supported(self):
        """Conv2d should be marked as supported."""
        conv_diags = [
            d for d in self.result.diagnostics if "Conv2d" in d.operation
        ]
        assert len(conv_diags) > 0
        for d in conv_diags:
            assert d.status == CompatibilityStatus.SUPPORTED

    def test_compatibility_score(self):
        """Compatibility score should be between 0 and 100."""
        assert 0.0 <= self.result.compatibility_score <= 100.0

    def test_score_not_perfect(self):
        """Score should not be 100 since there are unsupported ops."""
        assert self.result.compatibility_score < 100.0


# ── TransformerBlock tests ──


class TestTransformerBlock:
    """Tests for parsing the TransformerBlock fixture."""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.code = _read_fixture("sample_transformer.py")
        self.result = analyze_code(self.code)

    def test_detects_operations(self):
        """Should detect multiple torch operations."""
        assert self.result.total_operations > 0

    def test_detects_multihead_attention(self):
        """Should detect nn.MultiheadAttention."""
        ops = [d.operation for d in self.result.diagnostics]
        attn_ops = [o for o in ops if "MultiheadAttention" in o]
        assert len(attn_ops) >= 1, f"Expected MultiheadAttention, found: {ops}"

    def test_detects_layernorm(self):
        """Should detect nn.LayerNorm."""
        ops = [d.operation for d in self.result.diagnostics]
        ln_ops = [o for o in ops if "LayerNorm" in o]
        assert len(ln_ops) >= 2, f"Expected at least 2 LayerNorm, found: {ln_ops}"

    def test_detects_gelu(self):
        """Should detect nn.GELU."""
        ops = [d.operation for d in self.result.diagnostics]
        gelu_ops = [o for o in ops if "GELU" in o]
        assert len(gelu_ops) >= 1, f"Expected GELU, found: {ops}"

    def test_detects_linear(self):
        """Should detect nn.Linear."""
        ops = [d.operation for d in self.result.diagnostics]
        linear_ops = [o for o in ops if "Linear" in o]
        assert len(linear_ops) >= 2, f"Expected at least 2 Linear, found: {linear_ops}"

    def test_detects_dropout(self):
        """Should detect nn.Dropout."""
        ops = [d.operation for d in self.result.diagnostics]
        dropout_ops = [o for o in ops if "Dropout" in o]
        assert len(dropout_ops) >= 1

    def test_multihead_attention_partial(self):
        """MultiheadAttention should be marked as partial."""
        attn_diags = [
            d for d in self.result.diagnostics if "MultiheadAttention" in d.operation
        ]
        assert len(attn_diags) > 0
        for d in attn_diags:
            assert d.status == CompatibilityStatus.PARTIAL

    def test_layernorm_supported(self):
        """LayerNorm should be marked as supported."""
        ln_diags = [
            d for d in self.result.diagnostics if "LayerNorm" in d.operation
        ]
        assert len(ln_diags) > 0
        for d in ln_diags:
            assert d.status == CompatibilityStatus.SUPPORTED

    def test_gelu_supported(self):
        """GELU should be marked as supported."""
        gelu_diags = [
            d for d in self.result.diagnostics if "GELU" in d.operation
        ]
        assert len(gelu_diags) > 0
        for d in gelu_diags:
            assert d.status == CompatibilityStatus.SUPPORTED


# ── TorchVisitor unit tests ──


class TestTorchVisitor:
    """Direct tests for the TorchVisitor import resolution logic."""

    def test_resolves_import_alias(self):
        """Should resolve `import torch.nn.functional as F` -> F.relu -> torch.nn.functional.relu."""
        import ast

        code = "import torch.nn.functional as F\nF.relu(x)\n"
        tree = ast.parse(code)
        visitor = TorchVisitor()
        visitor.visit(tree)
        assert len(visitor.operations) == 1
        assert visitor.operations[0].operation == "torch.nn.functional.relu"

    def test_resolves_nn_alias(self):
        """Should resolve `import torch.nn as nn` -> nn.Conv2d -> torch.nn.Conv2d."""
        import ast

        code = "import torch.nn as nn\nnn.Conv2d(3, 16, 3)\n"
        tree = ast.parse(code)
        visitor = TorchVisitor()
        visitor.visit(tree)
        assert len(visitor.operations) == 1
        assert visitor.operations[0].operation == "torch.nn.Conv2d"

    def test_resolves_from_import(self):
        """Should resolve `from torch.nn import Linear` -> Linear(10, 5)."""
        import ast

        code = "from torch.nn import Linear\nLinear(10, 5)\n"
        tree = ast.parse(code)
        visitor = TorchVisitor()
        visitor.visit(tree)
        assert len(visitor.operations) == 1
        assert visitor.operations[0].operation == "torch.nn.Linear"

    def test_direct_torch_call(self):
        """Should detect `torch.matmul(a, b)`."""
        import ast

        code = "import torch\ntorch.matmul(a, b)\n"
        tree = ast.parse(code)
        visitor = TorchVisitor()
        visitor.visit(tree)
        assert len(visitor.operations) == 1
        assert visitor.operations[0].operation == "torch.matmul"

    def test_ignores_self_attributes(self):
        """Should not detect `self.conv1(x)` as a torch operation."""
        import ast

        code = "self.conv1(x)\n"
        tree = ast.parse(code)
        visitor = TorchVisitor()
        visitor.visit(tree)
        assert len(visitor.operations) == 0

    def test_classifies_instantiation(self):
        """Uppercase last part should be classified as instantiation."""
        import ast

        code = "import torch.nn as nn\nnn.Conv2d(3, 16, 3)\n"
        tree = ast.parse(code)
        visitor = TorchVisitor()
        visitor.visit(tree)
        assert visitor.operations[0].call_type == "instantiation"

    def test_classifies_function_call(self):
        """Lowercase last part should be classified as call."""
        import ast

        code = "import torch\ntorch.matmul(a, b)\n"
        tree = ast.parse(code)
        visitor = TorchVisitor()
        visitor.visit(tree)
        assert visitor.operations[0].call_type == "call"
