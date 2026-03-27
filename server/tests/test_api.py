"""Tests for API endpoints using FastAPI TestClient."""

import json
import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from server.main import app

SAMPLE_CNN_CODE = '''
import torch
import torch.nn as nn
import torch.nn.functional as F

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.fc1 = nn.Linear(16, 10)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.dropout(x)
        x = self.fc1(x)
        return x
'''

INVALID_CODE = "def foo(:\n    pass"


@pytest.fixture
def transport():
    return ASGITransport(app=app)


@pytest.fixture
async def client(transport):
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# ── Health endpoint ──


class TestHealthEndpoint:
    @pytest.mark.anyio
    async def test_health(self, client):
        resp = await client.get("/api/v1/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "healthy"
        assert "version" in data


# ── Analyze endpoint ──


class TestAnalyzeEndpoint:
    @pytest.mark.anyio
    async def test_analyze_valid_code(self, client):
        resp = await client.post(
            "/api/v1/analyze",
            json={"code": SAMPLE_CNN_CODE},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "diagnostics" in data
        assert "summary" in data
        assert data["summary"]["total_operations"] > 0
        assert 0 <= data["summary"]["compatibility_score"] <= 100

    @pytest.mark.anyio
    async def test_analyze_returns_diagnostics(self, client):
        resp = await client.post(
            "/api/v1/analyze",
            json={"code": SAMPLE_CNN_CODE},
        )
        data = resp.json()
        diagnostics = data["diagnostics"]
        assert len(diagnostics) > 0
        # Each diagnostic should have required fields
        for d in diagnostics:
            assert "line" in d
            assert "column" in d
            assert "operation" in d
            assert "severity" in d
            assert "status" in d

    @pytest.mark.anyio
    async def test_analyze_detects_dropout(self, client):
        resp = await client.post(
            "/api/v1/analyze",
            json={"code": SAMPLE_CNN_CODE},
        )
        data = resp.json()
        dropout_diags = [
            d for d in data["diagnostics"] if "Dropout" in d["operation"]
        ]
        assert len(dropout_diags) > 0
        assert dropout_diags[0]["status"] == "unsupported"

    @pytest.mark.anyio
    async def test_analyze_invalid_code(self, client):
        resp = await client.post(
            "/api/v1/analyze",
            json={"code": INVALID_CODE},
        )
        assert resp.status_code == 422

    @pytest.mark.anyio
    async def test_analyze_empty_code(self, client):
        resp = await client.post(
            "/api/v1/analyze",
            json={"code": ""},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["summary"]["total_operations"] == 0
        assert data["summary"]["compatibility_score"] == 100.0


# ── Compatibility endpoint ──


class TestCompatibilityEndpoint:
    @pytest.mark.anyio
    async def test_get_all(self, client):
        resp = await client.get("/api/v1/compatibility")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 24
        assert len(data["operations"]) == 24

    @pytest.mark.anyio
    async def test_lookup_specific_op(self, client):
        resp = await client.get(
            "/api/v1/compatibility", params={"operation": "torch.matmul"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["found"] is True
        assert data["operation"]["torch_op"] == "torch.matmul"

    @pytest.mark.anyio
    async def test_lookup_unknown_op(self, client):
        resp = await client.get(
            "/api/v1/compatibility", params={"operation": "torch.fake_op"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["found"] is False

    @pytest.mark.anyio
    async def test_filter_by_category(self, client):
        resp = await client.get(
            "/api/v1/compatibility", params={"category": "Activations"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] > 0
        assert all(
            op["category"] == "Activations" for op in data["operations"]
        )

    @pytest.mark.anyio
    async def test_filter_by_status(self, client):
        resp = await client.get(
            "/api/v1/compatibility", params={"status": "unsupported"}
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] > 0
        assert all(op["status"] == "unsupported" for op in data["operations"])


# ── Export endpoint ──


class TestExportEndpoint:
    @pytest.mark.anyio
    async def test_export_python(self, client):
        resp = await client.post(
            "/api/v1/export",
            json={
                "original_code": SAMPLE_CNN_CODE,
                "refactored_code": "import ttnn\n# refactored code here\n",
                "format": "python",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["filename"] == "migrated_model.py"
        assert data["content_type"] == "text/x-python"
        assert "ttnn" in data["content"]

    @pytest.mark.anyio
    async def test_export_notebook(self, client):
        resp = await client.post(
            "/api/v1/export",
            json={
                "original_code": SAMPLE_CNN_CODE,
                "refactored_code": "import ttnn\n# refactored\n",
                "format": "notebook",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["filename"] == "migrated_model.ipynb"
        assert data["content_type"] == "application/x-ipynb+json"
        # Verify it's valid JSON (notebook format)
        nb = json.loads(data["content"])
        assert "cells" in nb
        assert len(nb["cells"]) > 0

    @pytest.mark.anyio
    async def test_export_report(self, client):
        resp = await client.post(
            "/api/v1/export",
            json={
                "original_code": SAMPLE_CNN_CODE,
                "refactored_code": "import ttnn\n# refactored\n",
                "format": "report",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["filename"] == "migration_report.md"
        assert data["content_type"] == "text/markdown"
        assert "Migration Report" in data["content"]

    @pytest.mark.anyio
    async def test_export_custom_filename(self, client):
        resp = await client.post(
            "/api/v1/export",
            json={
                "original_code": "x = 1",
                "refactored_code": "import ttnn\nx = 1\n",
                "format": "python",
                "filename": "my_model.py",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["filename"] == "my_model.py"
