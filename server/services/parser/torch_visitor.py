"""Custom AST visitor for torch.* calls."""

import ast
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class TorchOperation:
    """A detected torch operation in the source code."""

    line: int
    column: int
    operation: str  # Fully qualified name, e.g. "torch.nn.Conv2d"
    call_type: str  # "call", "instantiation", "method_call", "attribute"
    raw_name: str  # The name as it appeared in source code


# Prefixes we consider torch-related
_TORCH_PREFIXES = {"torch", "torchvision"}


class TorchVisitor(ast.NodeVisitor):
    """AST visitor that identifies all torch.* related calls.

    Resolves import aliases so that e.g. `F.relu(x)` is reported as
    `torch.nn.functional.relu`.
    """

    def __init__(self) -> None:
        self.operations: List[TorchOperation] = []
        # Maps alias -> fully qualified module name
        # e.g., {"F": "torch.nn.functional", "nn": "torch.nn"}
        self.import_aliases: Dict[str, str] = {}
        # Track "from X import Y" individual names
        # e.g., {"Conv2d": "torch.nn.Conv2d"}
        self.from_imports: Dict[str, str] = {}
        # Track which names are torch-related modules imported directly
        self._torch_modules: Set[str] = set()

    def visit_Import(self, node: ast.Import) -> None:
        """Handle `import torch`, `import torch.nn as nn`, etc."""
        for alias in node.names:
            module = alias.name
            local_name = alias.asname if alias.asname else alias.name
            if self._is_torch_related(module):
                self.import_aliases[local_name] = module
                self._torch_modules.add(local_name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Handle `from torch.nn import Conv2d`, `from torch import nn`, etc."""
        module = node.module or ""
        if not self._is_torch_related(module):
            self.generic_visit(node)
            return

        for alias in node.names:
            name = alias.name
            local_name = alias.asname if alias.asname else name
            full_name = f"{module}.{name}" if module else name

            # If we're importing a submodule (e.g., `from torch import nn`)
            # treat it as an alias
            if self._looks_like_module(name):
                self.import_aliases[local_name] = full_name
                self._torch_modules.add(local_name)
            else:
                # Importing a specific class/function
                self.from_imports[local_name] = full_name
                self.import_aliases[local_name] = full_name

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """Handle all function/constructor calls."""
        resolved = self._resolve_call(node.func)
        if resolved is not None:
            fq_name, raw_name = resolved
            call_type = self._classify_call(fq_name)
            self.operations.append(
                TorchOperation(
                    line=node.lineno,
                    column=node.col_offset,
                    operation=fq_name,
                    call_type=call_type,
                    raw_name=raw_name,
                )
            )
        self.generic_visit(node)

    def _resolve_call(self, node: ast.expr) -> Optional[tuple]:
        """Resolve a call node to (fully_qualified_name, raw_name) or None."""
        if isinstance(node, ast.Attribute):
            # e.g., F.relu, torch.matmul, self.conv1 (skip self.*)
            chain = self._get_attribute_chain(node)
            if chain is None:
                return None
            raw_name = ".".join(chain)
            fq_name = self._resolve_chain(chain)
            if fq_name and self._is_torch_related(fq_name):
                return fq_name, raw_name
        elif isinstance(node, ast.Name):
            # e.g., bare name like `relu` if imported via `from torch.nn.functional import relu`
            name = node.id
            if name in self.from_imports:
                return self.from_imports[name], name
        return None

    def _get_attribute_chain(self, node: ast.expr) -> Optional[List[str]]:
        """Convert an attribute access chain to a list of names.

        E.g., `a.b.c` -> ["a", "b", "c"].
        Returns None if the chain contains non-Name/Attribute nodes.
        """
        parts: List[str] = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.append(current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            # Skip self.* chains
            if current.id == "self":
                return None
            parts.append(current.id)
            parts.reverse()
            return parts
        return None

    def _resolve_chain(self, chain: List[str]) -> Optional[str]:
        """Resolve an attribute chain using import aliases.

        E.g., ["F", "relu"] with alias F -> torch.nn.functional
        becomes "torch.nn.functional.relu".
        """
        if not chain:
            return None

        head = chain[0]

        # Check if head is a known alias
        if head in self.import_aliases:
            resolved_head = self.import_aliases[head]
            if len(chain) == 1:
                return resolved_head
            return resolved_head + "." + ".".join(chain[1:])

        # Check multi-part prefixes: e.g., chain = ["torch", "nn", "Conv2d"]
        # Build up checking each prefix
        for i in range(len(chain), 0, -1):
            prefix = ".".join(chain[:i])
            if self._is_torch_related(prefix):
                return ".".join(chain)

        return None

    def _classify_call(self, fq_name: str) -> str:
        """Classify a call as instantiation, method call, etc."""
        parts = fq_name.split(".")
        if not parts:
            return "call"
        last = parts[-1]
        # If the last part starts with uppercase, it's likely a class instantiation
        if last and last[0].isupper():
            return "instantiation"
        return "call"

    @staticmethod
    def _is_torch_related(name: str) -> bool:
        """Check if a name belongs to torch or torchvision."""
        for prefix in _TORCH_PREFIXES:
            if name == prefix or name.startswith(prefix + "."):
                return True
        return False

    @staticmethod
    def _looks_like_module(name: str) -> bool:
        """Heuristic: module names are lowercase."""
        return name and name[0].islower()
