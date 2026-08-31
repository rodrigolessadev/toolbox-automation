"""Testes unitários e de integração para o orquestrador de Batch Release (Issue #11).
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
import pytest

# Garante path para importação de scripts/
AUTOMATION_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AUTOMATION_ROOT / "scripts"))

import orchestrate_batch_release as obr


def test_extract_issues_from_commits():
    """Valida a extração de números de issues a partir de commits."""
    commits = [
        {"issues": [10, 20]},
        {"issues": [20, 30]},
        {"issues": []},
    ]
    extracted = obr.extract_issues_from_commits(commits, extra_issues=[40, 10])
    assert extracted == [10, 20, 30, 40]


def test_determine_bump_type():
    """Valida o cálculo do tipo de bump SemVer com base na lista de commits."""
    # Breaking change
    assert obr.determine_bump_type([{"type": "fix"}, {"type": "breaking"}]) == "major"
    assert obr.determine_bump_type([{"type": "feat", "is_breaking": True}]) == "major"

    # Feat
    assert obr.determine_bump_type([{"type": "fix"}, {"type": "feat"}]) == "minor"

    # Only fixes / chores
    assert obr.determine_bump_type([{"type": "fix"}, {"type": "chore"}]) == "patch"

    # Empty
    assert obr.determine_bump_type([]) == "patch"


def test_format_issue_release_comment():
    """Valida a formatação padronizada do comentário de release."""
    comment = obr.format_issue_release_comment("1.18.0", "rodrigolessadev/toolbox")
    assert "v1.18.0" in comment
    assert "rodrigolessadev/toolbox" in comment
    assert "publicada oficialmente" in comment


def test_notify_and_close_issue_dry_run():
    """Valida a simulação de notificação e fechamento em modo dry-run."""
    res = obr.notify_and_close_issue(
        repo_full_name="rodrigolessadev/toolbox",
        issue_number=105,
        version="1.18.0",
        close_issue=True,
        add_label="status: released",
        dry_run=True
    )
    assert res["success"] is True
    assert res["dry_run"] is True
    assert len(res["actions"]) == 3
    assert any("Comentário na issue #105" in a for a in res["actions"])
    assert any("Fechar issue #105" in a for a in res["actions"])
    assert any("Adicionar label 'status: released'" in a for a in res["actions"])


def test_orchestrate_batch_release_with_mock_repo(tmp_path: Path, monkeypatch):
    """Cria repositório git temporário e executa orquestração completa em modo dry-run."""
    repo_dir = tmp_path / "mock_toolbox"
    repo_dir.mkdir()

    def run_git(args):
        subprocess.run(["git"] + args, cwd=str(repo_dir), check=True, capture_output=True, text=True)

    run_git(["init"])
    run_git(["config", "user.name", "Test Bot"])
    run_git(["config", "user.email", "bot@toolbox.local"])

    # Base commit e tag inicial
    (repo_dir / "README.md").write_text("Toolbox", encoding="utf-8")
    run_git(["add", "."])
    run_git(["commit", "-m", "chore: initial commit"])
    run_git(["tag", "-a", "v1.0.0", "-m", "Release v1.0.0"])

    # Commit 1 com issue
    (repo_dir / "feature.txt").write_text("Feature 1", encoding="utf-8")
    run_git(["add", "."])
    run_git(["commit", "-m", "feat: nova funcionalidade de busca (Closes #88)"])

    # Commit 2 com issue
    (repo_dir / "fix.txt").write_text("Fix 1", encoding="utf-8")
    run_git(["add", "."])
    run_git(["commit", "-m", "fix: corrigir overflow no layout (#92)"])

    # Monkeypatch do ECOSYSTEM_REPOS para apontar para o repo temporário
    mock_ecosystem = {
        "mock_toolbox": {
            "full_name": "rodrigolessadev/mock_toolbox",
            "path": repo_dir
        }
    }
    monkeypatch.setattr(obr, "ECOSYSTEM_REPOS", mock_ecosystem)

    result = obr.orchestrate_batch_release(
        repo_name="mock_toolbox",
        version="1.1.0",
        from_ref="v1.0.0",
        to_ref="HEAD",
        explicit_issues=[99],
        notify=True,
        close_issues=True,
        dry_run=True
    )

    assert result["success"] is True
    assert result["total_commits"] == 2
    assert result["suggested_bump"] == "minor"
    assert 88 in result["issues_processed"]
    assert 92 in result["issues_processed"]
    assert 99 in result["issues_processed"]
    assert len(result["notifications"]) == 3
