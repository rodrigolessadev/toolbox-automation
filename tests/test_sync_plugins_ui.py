"""Testes unitários para o script e comando de sincronização de UI compartilhada (sync-ui).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
import pytest

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import sync_plugins_ui


def setup_mock_plugins_env(root: Path) -> Tuple[Path, Path]:
    plugins_dir = root / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)

    # Master Shared UI
    shared_ui = plugins_dir / "shared" / "ui"
    shared_ui.mkdir(parents=True, exist_ok=True)
    (shared_ui / "toolbox-theme.css").write_text("/* MASTER THEME CSS */", encoding="utf-8")
    (shared_ui / "icons.js").write_text("const ICONS = { master: true };", encoding="utf-8")

    # Plugin A (sem pasta ui/)
    p_a = plugins_dir / "plugin-a"
    p_a.mkdir(parents=True, exist_ok=True)

    # Plugin B (com ui/ desatualizada)
    p_b = plugins_dir / "plugin-b"
    p_b_ui = p_b / "ui"
    p_b_ui.mkdir(parents=True, exist_ok=True)
    (p_b_ui / "toolbox-theme.css").write_text("/* OLD THEME */", encoding="utf-8")
    (p_b_ui / "icons.js").write_text("/* OLD ICONS */", encoding="utf-8")

    return plugins_dir, shared_ui


def test_sync_plugins_ui_full_propagation(tmp_path: Path) -> None:
    """Valida que todos os plugins recebem as cópias idênticas da fonte mestre."""
    plugins_dir, shared_ui = setup_mock_plugins_env(tmp_path)

    res = sync_plugins_ui.sync_plugins_ui(plugins_dir, shared_ui, check_mode=False)
    assert res["success"] is True
    assert res["total_plugins"] == 2
    assert res["plugins_divergent"] == 2

    # Verifica arquivos gerados
    p_a_ui = plugins_dir / "plugin-a" / "ui"
    p_b_ui = plugins_dir / "plugin-b" / "ui"

    assert (p_a_ui / "toolbox-theme.css").read_text(encoding="utf-8") == "/* MASTER THEME CSS */"
    assert (p_a_ui / "icons.js").read_text(encoding="utf-8") == "const ICONS = { master: true };"

    assert (p_b_ui / "toolbox-theme.css").read_text(encoding="utf-8") == "/* MASTER THEME CSS */"
    assert (p_b_ui / "icons.js").read_text(encoding="utf-8") == "const ICONS = { master: true };"

    # Segunda rodada: deve detectar que tudo já está em dia
    res_check = sync_plugins_ui.sync_plugins_ui(plugins_dir, shared_ui, check_mode=True)
    assert res_check["plugins_synced"] == 2
    assert res_check["plugins_divergent"] == 0


def test_sync_plugins_ui_check_mode_does_not_modify_disk(tmp_path: Path) -> None:
    """Valida que o modo --check apenas aponta divergências sem tocar no sistema de arquivos."""
    plugins_dir, shared_ui = setup_mock_plugins_env(tmp_path)

    p_b_theme = plugins_dir / "plugin-b" / "ui" / "toolbox-theme.css"
    assert p_b_theme.read_text(encoding="utf-8") == "/* OLD THEME */"

    res = sync_plugins_ui.sync_plugins_ui(plugins_dir, shared_ui, check_mode=True)
    assert res["success"] is True
    assert res["check_mode"] is True
    assert res["plugins_divergent"] == 2

    # O arquivo antigo deve permanecer intacto
    assert p_b_theme.read_text(encoding="utf-8") == "/* OLD THEME */"


def test_sync_plugins_ui_target_single_plugin(tmp_path: Path) -> None:
    """Valida a sincronização isolada passando target_plugin_id."""
    plugins_dir, shared_ui = setup_mock_plugins_env(tmp_path)

    res = sync_plugins_ui.sync_plugins_ui(
        plugins_dir,
        shared_ui,
        target_plugin_id="plugin-b",
        check_mode=False
    )
    assert res["total_plugins"] == 1
    assert res["plugins"][0]["id"] == "plugin-b"

    # Plugin B foi atualizado
    assert (plugins_dir / "plugin-b" / "ui" / "toolbox-theme.css").read_text(encoding="utf-8") == "/* MASTER THEME CSS */"
    # Plugin A não foi criado/tocado
    assert not (plugins_dir / "plugin-a" / "ui").exists()


def test_sync_plugins_ui_handles_missing_shared_source(tmp_path: Path) -> None:
    """Valida tratamento seguro quando o diretório mestre não existe."""
    plugins_dir = tmp_path / "plugins"
    plugins_dir.mkdir(parents=True, exist_ok=True)
    missing_shared = plugins_dir / "shared" / "ui"

    res = sync_plugins_ui.sync_plugins_ui(plugins_dir, missing_shared)
    assert res["success"] is False
    assert "não encontrado" in res["error"]


def test_sync_plugins_ui_cli_check_and_json(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Valida invocação CLI com --check, --json e código de saída de erro/sucesso."""
    plugins_dir, shared_ui = setup_mock_plugins_env(tmp_path)

    # 1. Modo Check retorna código 1 pois há divergências
    code_check = sync_plugins_ui.main(["--root", str(tmp_path), "--check", "--json"])
    assert code_check == 1
    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["check_mode"] is True
    assert data["plugins_divergent"] == 2

    # 2. Sincronização ativa retorna código 0
    code_sync = sync_plugins_ui.main(["--root", str(tmp_path)])
    assert code_sync == 0

    # 3. Novo check retorna código 0 pois agora está tudo sincronizado
    code_check_ok = sync_plugins_ui.main(["--root", str(tmp_path), "--check"])
    assert code_check_ok == 0
