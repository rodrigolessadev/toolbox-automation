"""
test_automation_scripts.py - Testes automatizados para os scripts operacionais multiplataforma.
Garante a integridade de caminhos dinâmicos, checkpoints e comandos CLI no Linux e Windows.
"""

import json
import os
import sys
from pathlib import Path

import pytest

# Adiciona o diretório scripts ao path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from common_utils import (
    Colors,
    detect_workspace_root,
    get_project_path,
)
import check_projects
import load_context
import resume_task
import start_task
import update_graph


def test_detect_workspace_root():
    """Valida se a detecção dinâmica de workspace encontra a raiz do monorepo."""
    root = detect_workspace_root()
    assert root.exists()
    assert (root / "toolbox-automation").is_dir()


def test_get_project_path():
    """Valida se a resolução de caminho absoluto dos projetos funciona."""
    auto_path = get_project_path("toolbox-automation")
    assert auto_path.is_dir()
    assert (auto_path / "scripts").is_dir()


def test_check_projects_mock(tmp_path):
    """Testa a lógica de verificação de projetos com mock em diretório temporário."""
    # Cria estrutura simulada
    auto_dir = tmp_path / "toolbox-automation"
    auto_dir.mkdir()
    (auto_dir / ".git").mkdir()

    toolbox_dir = tmp_path / "toolbox"
    toolbox_dir.mkdir()
    (toolbox_dir / ".git").mkdir()

    plugins_dir = tmp_path / "toolbox-plugins"
    plugins_dir.mkdir()
    (plugins_dir / ".git").mkdir()

    report = check_projects.check_projects(tmp_path)
    assert report["success"] is True
    assert len(report["projects"]) == 4

    # Remove um obrigatório
    (plugins_dir / ".git").rmdir()
    report_fail = check_projects.check_projects(tmp_path)
    assert report_fail["success"] is False


def test_start_and_resume_task(tmp_path):
    """Testa o ciclo de vida de criação e retomada de checkpoint de tarefa."""
    checkpoints_dir = tmp_path / "checkpoints"
    task_id = "TASK-TEST-001"
    desc = "Implementação de teste unitário"

    # Criação
    cp_path = start_task.create_task_checkpoint(
        task_id=task_id,
        description=desc,
        checkpoints_dir=checkpoints_dir,
        metadata={"branch": "feat/test", "custom_key": "val123"},
    )
    assert cp_path.is_file()

    # Leitura
    data = resume_task.read_task_checkpoint(task_id, checkpoints_dir)
    assert data["task_id"] == task_id
    assert data["description"] == desc
    assert data["status"] == "in_progress"
    assert data["custom_key"] == "val123"
    assert data["blocked"] is False


def test_load_context(tmp_path):
    """Testa a validação de arquivos de contexto persistente."""
    agent_dir = tmp_path / ".agent"
    agent_dir.mkdir()

    # Cenário com arquivos ausentes
    res_missing = load_context.validate_context(agent_dir)
    assert res_missing["success"] is False
    assert res_missing["missing_count"] == len(load_context.REQUIRED_CONTEXT_FILES)

    # Cria todos os arquivos mandatórios
    for fname in load_context.REQUIRED_CONTEXT_FILES:
        (agent_dir / fname).write_text(f"# {fname}", encoding="utf-8")

    res_ok = load_context.validate_context(agent_dir)
    assert res_ok["success"] is True
    assert res_ok["missing_count"] == 0


def test_update_graph_security():
    """Valida as regras de segurança e proteção de caminhos do Graphify."""
    assert update_graph.is_protected_path(".env") is True
    assert update_graph.is_protected_path("config/secrets/api.key") is True
    assert update_graph.is_protected_path("certs/client.pem") is True
    assert update_graph.is_protected_path("scripts/common_utils.py") is False


def test_update_graph_within_repo(tmp_path):
    """Valida se caminhos fora do repositório são corretamente detectados e rejeitados."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    inside_file = repo_root / "src" / "index.js"
    inside_file.parent.mkdir()
    inside_file.touch()

    outside_file = tmp_path / "outside.txt"
    outside_file.touch()

    assert update_graph.is_within_repo(inside_file, repo_root) is True
    assert update_graph.is_within_repo(outside_file, repo_root) is False
