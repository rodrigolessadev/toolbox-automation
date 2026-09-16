#!/usr/bin/env python3
"""
Sincronização de UI Compartilhada — Toolbox Ecosystem.
Propaga as folhas de estilo M3 (toolbox-theme.css) e o catálogo de ícones (icons.js)
da fonte mestre centralizada em plugins/shared/ui/ para os plugins do catálogo.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from common_utils import detect_workspace_root
except ImportError:
    try:
        from scripts.common_utils import detect_workspace_root
    except ImportError:
        detect_workspace_root = None

SHARED_UI_FILES = ("toolbox-theme.css", "icons.js")


def compute_file_hash(path: Path) -> Optional[str]:
    """Calcula o hash SHA-256 do arquivo se existir."""
    if not path.is_file():
        return None
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def resolve_sync_paths(explicit_root: Optional[str] = None) -> Tuple[Optional[Path], Optional[Path]]:
    """Localiza o diretório de plugins e o diretório mestre shared/ui."""
    if explicit_root:
        base = Path(explicit_root).resolve()
        if (base / "plugins").is_dir():
            plugins_dir = base / "plugins"
        else:
            plugins_dir = base
    else:
        ws_root = None
        if detect_workspace_root:
            try:
                ws_root = detect_workspace_root()
            except Exception:
                pass

        if ws_root and (ws_root / "toolbox-plugins" / "plugins").is_dir():
            plugins_dir = ws_root / "toolbox-plugins" / "plugins"
        else:
            auto_root = Path(__file__).resolve().parent.parent
            candidate = auto_root.parent / "toolbox-plugins" / "plugins"
            if candidate.is_dir():
                plugins_dir = candidate
            else:
                plugins_dir = auto_root / "plugins"

    shared_ui_dir = plugins_dir / "shared" / "ui"
    return plugins_dir if plugins_dir.is_dir() else None, shared_ui_dir if shared_ui_dir.is_dir() else None


def sync_plugins_ui(
    plugins_dir: Path,
    shared_ui_dir: Path,
    target_plugin_id: Optional[str] = None,
    check_mode: bool = False,
    verbose: bool = False,
) -> Dict[str, Any]:
    """Executa a sincronização ou verificação da UI compartilhada."""
    start_time = time.perf_counter()

    if not shared_ui_dir.is_dir():
        return {
            "success": False,
            "error": f"Diretório mestre shared/ui não encontrado: {shared_ui_dir}",
            "check_mode": check_mode,
            "total_plugins": 0,
            "plugins_synced": 0,
            "plugins_divergent": 0,
            "divergences": [],
            "plugins": []
        }

    master_hashes: Dict[str, Optional[str]] = {
        fname: compute_file_hash(shared_ui_dir / fname) for fname in SHARED_UI_FILES
    }

    results: List[Dict[str, Any]] = []
    total_divergences = 0

    for pdir in sorted(plugins_dir.iterdir()):
        if not pdir.is_dir() or pdir.name in ("__pycache__", "shared", ".git"):
            continue

        plugin_id = pdir.name
        if target_plugin_id and plugin_id != target_plugin_id:
            continue

        ui_dir = pdir / "ui"
        file_status: Dict[str, Any] = {}
        plugin_has_divergence = False

        for fname in SHARED_UI_FILES:
            master_hash = master_hashes.get(fname)
            dest_file = ui_dir / fname
            dest_hash = compute_file_hash(dest_file)

            is_synced = (master_hash is not None) and (master_hash == dest_hash)

            if not is_synced:
                plugin_has_divergence = True
                total_divergences += 1

                if not check_mode:
                    ui_dir.mkdir(parents=True, exist_ok=True)
                    src_file = shared_ui_dir / fname
                    if src_file.is_file():
                        shutil.copy2(src_file, dest_file)
                        action = "updated"
                    else:
                        action = "missing_source"
                else:
                    action = "divergent"
            else:
                action = "in_sync"

            file_status[fname] = {
                "synced": is_synced,
                "action": action,
                "master_hash": master_hash[:8] if master_hash else None,
                "dest_hash": dest_hash[:8] if dest_hash else None,
            }

        results.append({
            "id": plugin_id,
            "synced": not plugin_has_divergence,
            "files": file_status
        })

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    total_plugins = len(results)
    in_sync_count = sum(1 for r in results if r["synced"])
    divergent_count = total_plugins - in_sync_count

    return {
        "success": True,
        "check_mode": check_mode,
        "elapsed_ms": round(elapsed_ms, 2),
        "total_plugins": total_plugins,
        "plugins_synced": in_sync_count,
        "plugins_divergent": divergent_count,
        "plugins": results
    }


def print_report(res: Dict[str, Any], verbose: bool = False) -> None:
    """Imprime relatório intuitivo no terminal."""
    mode_str = "[VERIFICAÇÃO / DRY-RUN]" if res.get("check_mode") else "[SINCRONIZAÇÃO ATIVA]"
    print("=" * 80)
    print(f" 🔄 SINCRONIZAÇÃO DE UI COMPARTILHADA (SHARED/UI) — {mode_str}")
    print("=" * 80)

    if not res.get("success"):
        print(f"✖ [ERRO] {res.get('error')}")
        print("=" * 80)
        return

    plugins = res.get("plugins", [])
    if not plugins:
        print("Nenhum plugin encontrado para processar.")
        print("=" * 80)
        return

    check_mode = res.get("check_mode", False)

    for p in plugins:
        pid = p["id"]
        files = p["files"]

        if check_mode:
            if p["synced"]:
                if verbose:
                    print(f"  ✔ [EM DIA] {pid:<24} | toolbox-theme.css e icons.js sincronizados")
            else:
                divergent_files = [f for f, st in files.items() if not st["synced"]]
                print(f"  ✖ [DIVERGENTE] {pid:<20} | Arquivos desatualizados: {', '.join(divergent_files)}")
        else:
            updated_files = [f for f, st in files.items() if st["action"] == "updated"]
            if updated_files:
                print(f"  ✔ [SINCRONIZADO] {pid:<18} | Atualizado(s): {', '.join(updated_files)}")
            elif verbose:
                print(f"  ℹ [INALTERADO]   {pid:<18} | Já se encontrava idêntico à fonte mestre")

    print("-" * 80)
    if check_mode:
        if res["plugins_divergent"] == 0:
            print(f"✔ [SUCESSO] Todos os {res['total_plugins']} plugins estão 100% sincronizados com shared/ui.")
        else:
            print(f"✖ [AVISO] {res['plugins_divergent']} de {res['total_plugins']} plugins possuem arquivos desatualizados.")
            print("  Execute 'python tb_auto.py sync-ui' para aplicar as atualizações.")
    else:
        print(f"✔ [CONCLUÍDO] {res['total_plugins']} plugins processados ({res['plugins_divergent']} atualizados) em {res.get('elapsed_ms')}ms.")
    print("=" * 80)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Sincroniza folhas de estilo e ícones da fonte mestre (shared/ui/) para os plugins."
    )
    parser.add_argument("--root", help="Caminho explícito para a pasta raiz de toolbox-plugins")
    parser.add_argument("--plugin", help="Sincroniza apenas um plugin específico")
    parser.add_argument("--check", "--dry-run", action="store_true", help="Apenas verifica se há arquivos divergentes sem alterá-los")
    parser.add_argument("--verbose", action="store_true", help="Exibe detalhes de todos os arquivos processados")
    parser.add_argument("--json", action="store_true", help="Retorna resultado em formato JSON")

    args = parser.parse_args(argv)

    plugins_dir, shared_ui_dir = resolve_sync_paths(args.root)

    if not plugins_dir or not shared_ui_dir:
        err_msg = "Não foi possível localizar o repositório de plugins ou a pasta plugins/shared/ui/."
        if args.json:
            print(json.dumps({"success": False, "error": err_msg}, indent=2))
        else:
            print(f"✖ [ERRO] {err_msg}", file=sys.stderr)
        return 1

    res = sync_plugins_ui(
        plugins_dir=plugins_dir,
        shared_ui_dir=shared_ui_dir,
        target_plugin_id=args.plugin,
        check_mode=args.check,
        verbose=args.verbose,
    )

    if args.json:
        print(json.dumps(res, indent=2, ensure_ascii=False))
    else:
        print_report(res, verbose=args.verbose)

    if args.check and res.get("plugins_divergent", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
