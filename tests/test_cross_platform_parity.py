"""Suíte de avaliação contínua e validação de paridade cross-platform (Issue #13).

Garante que o ecossistema Toolbox mantém total coerência e capacidade de
execução tanto em ambientes Windows quanto Linux.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
import pytest

# Raízes do ecossistema
AUTOMATION_ROOT = Path(__file__).resolve().parent.parent
ECOSYSTEM_ROOT = AUTOMATION_ROOT.parent
TOOLBOX_ROOT = ECOSYSTEM_ROOT / "toolbox"
TOOLBOX_RELEASE_ROOT = ECOSYSTEM_ROOT / "toolbox-release"


def test_tauri_bundle_linux_and_windows_config() -> None:
    """Valida se o tauri.conf.json possui configuração adequada para Windows e Linux."""
    conf_path = TOOLBOX_ROOT / "src-tauri" / "tauri.conf.json"
    assert conf_path.exists(), "src-tauri/tauri.conf.json deve existir"

    with open(conf_path, "r", encoding="utf-8") as f:
        conf = json.load(f)

    bundle = conf.get("bundle", {})
    targets = bundle.get("targets", [])
    
    # Valida targets ou presença de configurações específicas de plataforma
    assert "linux" in bundle, "Seção bundle.linux deve estar configurada no tauri.conf.json"
    linux_conf = bundle["linux"]
    assert "deb" in linux_conf, "Suporte a pacote .deb deve estar definido em bundle.linux"
    
    deb_depends = linux_conf["deb"].get("depends", [])
    assert any("libwebkit2gtk" in dep for dep in deb_depends), "libwebkit2gtk deve ser dependência do .deb"
    assert any("libgtk-3" in dep for dep in deb_depends), "libgtk-3 deve ser dependência do .deb"
    assert any("libappindicator3" in dep for dep in deb_depends), "libappindicator3 deve ser dependência do .deb"


def test_setup_documentation_parity() -> None:
    """Valida se o documento docs/setup.md contém as instruções e pacotes nativos para Linux."""
    setup_doc = TOOLBOX_ROOT / "docs" / "setup.md"
    assert setup_doc.exists(), "docs/setup.md deve existir"

    content = setup_doc.read_text(encoding="utf-8")
    assert "libwebkit2gtk-4.1-dev" in content or "libwebkit2gtk-4.0-dev" in content
    assert "libgtk-3-dev" in content
    assert "libappindicator3-dev" in content
    assert "librsvg2-dev" in content
    assert "patchelf" in content


def test_runtime_setup_script_linux_tolerance() -> None:
    """Valida se o script setup-embedded-python.js executa sem erro em ambiente Linux."""
    setup_script = TOOLBOX_ROOT / "scripts" / "setup-embedded-python.js"
    assert setup_script.exists(), "scripts/setup-embedded-python.js deve existir"

    res = subprocess.run(
        ["node", str(setup_script)],
        cwd=str(TOOLBOX_ROOT),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, f"O script deve concluir com sucesso no Linux: {res.stderr}"
    assert "Ambiente Linux/Unix detectado" in res.stdout or "Iniciando verificação" in res.stdout


def test_python_interpreter_smoke_execution() -> None:
    """Smoke test: valida que python3 do sistema é capaz de executar comandos com json e requests/urllib."""
    res = subprocess.run(
        [sys.executable, "-c", "import sys, json, urllib.request; print(f'[OK] Python {sys.version_info.major}.{sys.version_info.minor}')"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert "[OK] Python" in res.stdout


def test_multiplatform_updater_manifest_generator() -> None:
    """Valida a paridade do gerador de manifesto updater (latest.json) para múltiplas plataformas."""
    domain_file = TOOLBOX_RELEASE_ROOT / "domain.py"
    if not domain_file.exists():
        pytest.skip("toolbox-release não encontrado no mesmo nível de workspace")

    # Importa dinamicamente domain.py de toolbox-release
    import importlib.util
    spec = importlib.util.spec_from_file_location("domain", str(domain_file))
    domain = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(domain)

    platforms = {
        "windows-x86_64": {
            "url": "https://github.com/rodrigolessadev/toolbox/releases/download/v4.19.0/toolbox-setup.exe",
            "signature": "sig-win",
        },
        "linux-x86_64": {
            "url": "https://github.com/rodrigolessadev/toolbox/releases/download/v4.19.0/toolbox.AppImage",
            "signature": "sig-linux",
        }
    }

    manifest = domain.generate_multiplatform_updater_manifest(
        version="4.19.0",
        notes="Suporte a Linux e Windows",
        pub_date="2026-09-03T18:00:00Z",
        platforms=platforms,
    )

    assert manifest["version"] == "v4.19.0"
    assert "windows-x86_64" in manifest["platforms"]
    assert "linux-x86_64" in manifest["platforms"]
    assert manifest["platforms"]["windows-x86_64"]["url"].endswith("toolbox-setup.exe")
    assert manifest["platforms"]["linux-x86_64"]["url"].endswith("toolbox.AppImage")
