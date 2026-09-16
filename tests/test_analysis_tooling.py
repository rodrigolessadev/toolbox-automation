"""
test_analysis_tooling.py - Testes automatizados para ferramentas de análise e configuração MCP.
Valida o template do GitHub MCP Server, a busca estrutural com AST e o empacotamento cirúrgico de contexto.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import code_search
import pack_context


def test_mcp_config_example_validity():
    """Valida se o arquivo config/mcp_config.example.json possui sintaxe e schema JSON válidos."""
    cfg_file = ROOT_DIR / "config" / "mcp_config.example.json"
    assert cfg_file.exists(), "config/mcp_config.example.json deve existir"

    data = json.loads(cfg_file.read_text(encoding="utf-8"))
    assert "mcpServers" in data
    assert "github" in data["mcpServers"]

    gh_server = data["mcpServers"]["github"]
    assert gh_server["command"] == "npx"
    assert any("@modelcontextprotocol/server-github" in arg for arg in gh_server["args"])
    assert "GITHUB_PERSONAL_ACCESS_TOKEN" in gh_server.get("env", {})
    assert len(gh_server.get("authorized_repositories", [])) >= 3


def test_code_search_finds_classes_and_functions():
    """Valida se a busca estrutural por AST localiza classes e funções sem regex."""
    common_utils_file = SCRIPTS_DIR / "common_utils.py"
    assert common_utils_file.exists()

    # Busca por classe Colors
    matches_class = code_search.search_python_ast(common_utils_file, "Colors", sym_type="class")
    assert len(matches_class) >= 1
    assert matches_class[0]["name"] == "Colors"
    assert matches_class[0]["kind"] == "class"

    # Busca por função detect_workspace_root
    matches_func = code_search.search_python_ast(common_utils_file, "detect_workspace_root", sym_type="func")
    assert len(matches_func) >= 1
    assert matches_func[0]["name"] == "detect_workspace_root"
    assert matches_func[0]["kind"] == "function"


def test_code_search_search_symbols(tmp_path):
    """Valida busca estrutural em árvore de diretórios simulada."""
    py_file = tmp_path / "sample_plugin.py"
    py_file.write_text(
        "class SamplePluginApi:\n"
        "    def execute_task(self, param1):\n"
        "        return True\n",
        encoding="utf-8",
    )

    results = code_search.search_symbols(tmp_path, "SamplePluginApi", sym_type="class")
    assert len(results) == 1
    assert results[0]["name"] == "SamplePluginApi"

    func_results = code_search.search_symbols(tmp_path, "execute_task", sym_type="func")
    assert len(func_results) == 1
    assert func_results[0]["name"] == "execute_task"


def test_estimate_tokens():
    """Valida a precisão da estimativa heurística de tokens."""
    assert pack_context.estimate_tokens("1234") == 1
    assert pack_context.estimate_tokens("12345678") == 2
    assert pack_context.estimate_tokens("") == 1


def test_pack_context_directory(tmp_path):
    """Valida o empacotamento cirúrgico de um diretório com árvore e métricas."""
    # Cria estrutura de arquivos mock
    (tmp_path / "plugin.json").write_text('{"name": "test"}', encoding="utf-8")
    (tmp_path / "main.py").write_text('print("hello")', encoding="utf-8")
    (tmp_path / "README.md").write_text("# Doc", encoding="utf-8")

    # Arquivos e pastas que DEVEM ser ignorados
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_text("dummy", encoding="utf-8")

    pycache_dir = tmp_path / "__pycache__"
    pycache_dir.mkdir()
    (pycache_dir / "sample.pyc").write_text("bytecode", encoding="utf-8")

    bin_file = tmp_path / "archive.zip"
    bin_file.write_bytes(b"PK000")

    markdown_pack, meta = pack_context.pack_directory(tmp_path)

    # Asserções de conteúdo
    assert "Context Pack:" in markdown_pack
    assert "File: `plugin.json`" in markdown_pack
    assert "File: `main.py`" in markdown_pack
    assert "File: `README.md`" in markdown_pack
    assert "archive.zip" not in markdown_pack
    assert "__pycache__" not in markdown_pack

    # Asserções de metadados
    assert meta["total_files"] == 3
    assert meta["estimated_tokens"] > 0
    assert meta["total_bytes"] > 0
