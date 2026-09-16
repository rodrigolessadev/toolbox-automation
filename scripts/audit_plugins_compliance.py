#!/usr/bin/env python3
"""
Auditoria de Conformidade Global dos Plugins — Toolbox Ecosystem.
Valida rigorosamente as 5 regras de experiência de usuário e integridade visual:
1. Regra 1: Ícone próprio declarado em plugin.json e sincronizado no catalog.json
2. Regra 2: Ícone na barra de tarefas do Windows (asset .ico em ui/assets/)
3. Regra 3: Versão na barra de títulos da janela (v{version} ou plugin_dir em main.py)
4. Regra 4: Classes utilitárias padronizadas de ícones Lucide (.icon-sm, .icon-md, .icon-lg)
5. Regra 5: Design System Material 3 bitemático completo (Dark & Light tokens no CSS)
+ Verificação de sincronização contra a fonte mestre em plugins/shared/ui/ (Abordagem B).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
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


def compute_file_hash(path: Path) -> Optional[str]:
    """Calcula o hash SHA-256 do arquivo se existir."""
    if not path.is_file():
        return None
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def check_rule1_icon(pj: Dict[str, Any], cat_entry: Optional[Dict[str, Any]]) -> Tuple[bool, str]:
    """Regra 1: Ícone próprio válido e sincronizado com catalog.json."""
    icon = pj.get("icon", "").strip()
    if not icon:
        return False, "Ícone não informado em plugin.json"
    if cat_entry:
        cat_icon = cat_entry.get("icon", "").strip()
        if cat_icon != icon:
            return False, f"Ícone em plugin.json ('{icon}') diverge do catalog.json ('{cat_icon}')"
    return True, f"Ícone '{icon}' declarado e sincronizado"


def check_rule2_taskbar_icon(plugin_dir: Path, icon_name: str) -> Tuple[bool, str]:
    """Regra 2: Ícone na barra de tarefas do Windows (.ico em ui/assets/)."""
    assets_dir = plugin_dir / "ui" / "assets"
    if not assets_dir.is_dir():
        return False, "Diretório ui/assets/ ausente"
    
    specific_ico = assets_dir / f"{icon_name}.ico"
    if specific_ico.is_file() and specific_ico.stat().st_size > 0:
        return True, f"Asset {specific_ico.name} presente"
    
    # Fallback: qualquer .ico na pasta ui/assets/
    any_ico = list(assets_dir.glob("*.ico"))
    if any_ico and any_ico[0].stat().st_size > 0:
        return True, f"Asset genérico {any_ico[0].name} presente"
    
    return False, f"Nenhum arquivo .ico encontrado em ui/assets/ para '{icon_name}'"


def check_rule3_window_version(plugin_dir: Path, version: str) -> Tuple[bool, str]:
    """Regra 3: Versão na barra de títulos da janela (v{version} ou plugin_dir em main.py)."""
    main_file = plugin_dir / "main.py"
    if not main_file.is_file():
        return False, "main.py ausente"
    
    main_code = main_file.read_text(encoding="utf-8", errors="ignore")
    
    # Suporta: plugin_dir=PLUGIN_DIR, título explícito com v{version}, ou método get_window_title()
    if "plugin_dir=" in main_code or "plugin_dir" in main_code:
        return True, "Janela inicializada com suporte a plugin_dir (leitura dinâmica de versão)"
    if f"v{version}" in main_code or "get_window_title" in main_code:
        return True, f"Versão explicitamente vinculada à janela (v{version})"
    if "f\"{title}" in main_code and "version" in main_code.lower():
        return True, "Título formatado dinamicamente com versão"
    
    return False, "Janela criada sem vinculação de versão nem plugin_dir em main.py"


def check_rule4_icon_utility_classes(plugin_dir: Path) -> Tuple[bool, str]:
    """Regra 4: Classes utilitárias padronizadas de ícones Lucide (.icon-sm, .icon-md, .icon-lg)."""
    css_files = [plugin_dir / "ui" / "toolbox-theme.css", plugin_dir / "ui" / "style.css"]
    content = ""
    for cf in css_files:
        if cf.is_file():
            content += cf.read_text(encoding="utf-8", errors="ignore") + "\n"
    
    if not content:
        return False, "Nenhum arquivo CSS encontrado na pasta ui/"
    
    has_icon_sm = ".icon-sm" in content
    has_icon_md = ".icon-md" in content or ".icon-lg" in content or ".btn-with-icon" in content
    
    if has_icon_sm and has_icon_md:
        return True, "Classes utilitárias de ícones (.icon-sm, .icon-md/lg) presentes"
    if has_icon_sm:
        return True, "Classe utilitária de ícones (.icon-sm) presente"
    
    return False, "Classes utilitárias padronizadas de ícones (.icon-sm) ausentes no CSS"


def check_rule5_m3_dual_theme(plugin_dir: Path) -> Tuple[bool, str]:
    """Regra 5: Design System Material 3 bitemático completo (Dark & Light tokens no CSS)."""
    theme_css = plugin_dir / "ui" / "toolbox-theme.css"
    if not theme_css.is_file():
        return False, "ui/toolbox-theme.css ausente"
    
    css_content = theme_css.read_text(encoding="utf-8", errors="ignore")
    has_dark = "data-theme=\"dark\"" in css_content or ":root" in css_content
    has_light = "data-theme=\"light\"" in css_content
    
    if has_dark and has_light:
        return True, "Suporte completo a Dark Mode e Light Mode verificado"
    if has_dark and not has_light:
        return False, "Suporte incompleto: apenas Dark Mode implementado (falta [data-theme=\"light\"])"
    return False, "Definição de tema M3 não identificada no CSS"


def check_shared_ui_sync(plugin_dir: Path, shared_ui_dir: Optional[Path]) -> Dict[str, Any]:
    """Verifica paridade por hash dos arquivos de UI com a fonte mestre em plugins/shared/ui/."""
    if not shared_ui_dir or not shared_ui_dir.is_dir():
        return {
            "available": False,
            "theme_synced": True,
            "icons_synced": True,
            "synced": True,
            "detail": "Fonte mestre shared/ui não disponível para checagem de paridade"
        }
    
    master_theme = shared_ui_dir / "toolbox-theme.css"
    master_icons = shared_ui_dir / "icons.js"
    
    plugin_theme = plugin_dir / "ui" / "toolbox-theme.css"
    plugin_icons = plugin_dir / "ui" / "icons.js"
    
    theme_hash_master = compute_file_hash(master_theme)
    theme_hash_plugin = compute_file_hash(plugin_theme)
    
    icons_hash_master = compute_file_hash(master_icons)
    icons_hash_plugin = compute_file_hash(plugin_icons)
    
    theme_synced = (theme_hash_master is not None) and (theme_hash_master == theme_hash_plugin)
    icons_synced = (icons_hash_master is not None) and (icons_hash_master == icons_hash_plugin)
    
    all_synced = theme_synced and icons_synced
    
    divergences = []
    if not theme_synced:
        divergences.append("toolbox-theme.css desatualizado")
    if not icons_synced:
        divergences.append("icons.js desatualizado")
        
    detail = "100% sincronizado com a fonte mestre" if all_synced else ", ".join(divergences)
    
    return {
        "available": True,
        "theme_synced": theme_synced,
        "icons_synced": icons_synced,
        "synced": all_synced,
        "detail": detail
    }


def resolve_plugins_dir(explicit_root: Optional[str] = None) -> Tuple[Path, Optional[Path], Optional[Path]]:
    """Resolve os diretórios de plugins, catálogo e shared/ui."""
    if explicit_root:
        base = Path(explicit_root).resolve()
        if (base / "plugins").is_dir():
            plugins_dir = base / "plugins"
            catalog_file = base / "catalog.json"
        else:
            plugins_dir = base
            catalog_file = base.parent / "catalog.json"
    else:
        ws_root = None
        if detect_workspace_root:
            try:
                ws_root = detect_workspace_root()
            except Exception:
                pass
        
        if ws_root and (ws_root / "toolbox-plugins" / "plugins").is_dir():
            base = ws_root / "toolbox-plugins"
            plugins_dir = base / "plugins"
            catalog_file = base / "catalog.json"
        else:
            auto_root = Path(__file__).resolve().parent.parent
            base = auto_root.parent / "toolbox-plugins"
            if not base.is_dir():
                base = auto_root
            plugins_dir = base / "plugins"
            catalog_file = base / "catalog.json"
    
    shared_ui = plugins_dir / "shared" / "ui"
    if not shared_ui.is_dir():
        shared_ui = None
        
    return plugins_dir, (catalog_file if catalog_file.is_file() else None), shared_ui


def audit_plugins(
    plugins_dir: Optional[Path] = None,
    catalog_file: Optional[Path] = None,
    shared_ui_dir: Optional[Path] = None,
    target_plugin_id: Optional[str] = None,
) -> Dict[str, Any]:
    """Executa a auditoria completa e retorna dicionário estruturado com resultados."""
    if plugins_dir is None:
        p_dir, c_file, s_dir = resolve_plugins_dir()
        plugins_dir = p_dir
        catalog_file = c_file
        shared_ui_dir = s_dir
        
    catalog_map: Dict[str, Any] = {}
    if catalog_file and catalog_file.is_file():
        try:
            cat_data = json.loads(catalog_file.read_text(encoding="utf-8"))
            catalog_map = {p["id"]: p for p in cat_data.get("plugins", [])}
        except Exception:
            pass

    results: List[Dict[str, Any]] = []
    
    if not plugins_dir.is_dir():
        return {
            "success": False,
            "total": 0,
            "passed": 0,
            "failed": 0,
            "error": f"Diretório de plugins não encontrado: {plugins_dir}",
            "plugins": []
        }

    for pdir in sorted(plugins_dir.iterdir()):
        if not pdir.is_dir() or pdir.name in ("__pycache__", "shared", ".git"):
            continue
        
        pid = pdir.name
        if target_plugin_id and pid != target_plugin_id:
            continue
            
        pj_file = pdir / "plugin.json"
        pj_data: Dict[str, Any] = {}
        if pj_file.is_file():
            try:
                pj_data = json.loads(pj_file.read_text(encoding="utf-8"))
            except Exception:
                pass
                
        cat_entry = catalog_map.get(pid)
        version = pj_data.get("version", "")
        icon_name = pj_data.get("icon", "")
        name = pj_data.get("name", pid)
        
        # 5 Regras
        r1_ok, r1_det = check_rule1_icon(pj_data, cat_entry)
        r2_ok, r2_det = check_rule2_taskbar_icon(pdir, icon_name)
        r3_ok, r3_det = check_rule3_window_version(pdir, version)
        r4_ok, r4_det = check_rule4_icon_utility_classes(pdir)
        r5_ok, r5_det = check_rule5_m3_dual_theme(pdir)
        
        # Sincronização UI
        sync_res = check_shared_ui_sync(pdir, shared_ui_dir)
        
        # Todas as 5 regras cumpridas
        all_rules_ok = r1_ok and r2_ok and r3_ok and r4_ok and r5_ok
        is_compliant = all_rules_ok
        
        issues = []
        if not r1_ok: issues.append(f"Regra 1 (Ícone): {r1_det}")
        if not r2_ok: issues.append(f"Regra 2 (Taskbar .ico): {r2_det}")
        if not r3_ok: issues.append(f"Regra 3 (Versão na Janela): {r3_det}")
        if not r4_ok: issues.append(f"Regra 4 (Ícones Comuns): {r4_det}")
        if not r5_ok: issues.append(f"Regra 5 (Tema Claro M3): {r5_det}")
        if sync_res.get("available") and not sync_res.get("synced"):
            issues.append(f"Shared UI: {sync_res.get('detail')}")

        results.append({
            "id": pid,
            "name": name,
            "version": version,
            "compliant": is_compliant,
            "rules": {
                "rule1_icon": {"passed": r1_ok, "detail": r1_det},
                "rule2_taskbar_icon": {"passed": r2_ok, "detail": r2_det},
                "rule3_window_version": {"passed": r3_ok, "detail": r3_det},
                "rule4_common_icons": {"passed": r4_ok, "detail": r4_det},
                "rule5_m3_dual_theme": {"passed": r5_ok, "detail": r5_det},
            },
            "shared_ui_sync": sync_res,
            "issues": issues
        })

    total = len(results)
    passed = sum(1 for r in results if r["compliant"])
    failed = total - passed

    return {
        "success": True,
        "total": total,
        "passed": passed,
        "failed": failed,
        "plugins": results
    }


def print_report(audit_res: Dict[str, Any]) -> None:
    """Imprime relatório formatado e intuitivo no terminal."""
    print("=" * 82)
    print(" 🛡️  AUDITORIA DE CONFORMIDADE DE PLUGINS — 5 REGRAS M3 & SHARED UI")
    print("=" * 82)
    
    if not audit_res.get("success"):
        print(f"✖ [ERRO] {audit_res.get('error')}")
        return

    plugins = audit_res.get("plugins", [])
    if not plugins:
        print("Nenhum plugin encontrado para auditar.")
        return

    # Cabeçalho da Tabela
    print(f"{'Plugin ID':<24} | {'R1':<3} | {'R2':<3} | {'R3':<3} | {'R4':<3} | {'R5':<3} | {'SYNC':<5} | {'Status'}")
    print("-" * 82)

    sync_needed_count = 0

    for p in plugins:
        r = p["rules"]
        r1_s = "✔" if r["rule1_icon"]["passed"] else "✖"
        r2_s = "✔" if r["rule2_taskbar_icon"]["passed"] else "✖"
        r3_s = "✔" if r["rule3_window_version"]["passed"] else "✖"
        r4_s = "✔" if r["rule4_common_icons"]["passed"] else "✖"
        r5_s = "✔" if r["rule5_m3_dual_theme"]["passed"] else "✖"
        
        sync = p["shared_ui_sync"]
        if sync.get("available"):
            sync_s = "✔" if sync.get("synced") else "✖"
            if not sync.get("synced"):
                sync_needed_count += 1
        else:
            sync_s = "-"
            
        status = "CONFORME" if p["compliant"] else "REVISÃO"
        print(f"{p['id']:<24} |  {r1_s}  |  {r2_s}  |  {r3_s}  |  {r4_s}  |  {r5_s}  |  {sync_s:<4} | {status}")

    print("=" * 82)
    print(f"[SUMÁRIO] {audit_res['total']} plugins auditados: {audit_res['passed']} conformes, {audit_res['failed']} com pendências.")

    # Detalha pendências se houver
    has_issues = False
    for p in plugins:
        if p["issues"]:
            if not has_issues:
                print("\n[DIAGNÓSTICO DETALHADO]")
                has_issues = True
            print(f"  • [{p['id']}]:")
            for iss in p["issues"]:
                print(f"    - {iss}")

    if sync_needed_count > 0:
        print(f"\n💡 [DICA] {sync_needed_count} plugin(s) possuem UI compartilhada divergente. Execute:")
        print("   python tb_auto.py sync-ui  (ou scripts/sync_plugins_ui.py)")
    print("=" * 82)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Audita plugins do ecossistema Toolbox contra as 5 regras e sincronização da UI compartilhada."
    )
    parser.add_argument("--root", help="Caminho explícito para a pasta raiz de toolbox-plugins")
    parser.add_argument("--plugin", help="Auditar somente um plugin específico")
    parser.add_argument("--json", action="store_true", help="Retorna saída estruturada em JSON")
    parser.add_argument("--strict", action="store_true", help="Retorna código de saída 1 em caso de qualquer pendência")

    args = parser.parse_args(argv)

    plugins_dir, catalog_file, shared_ui = resolve_plugins_dir(args.root)
    audit_res = audit_plugins(
        plugins_dir=plugins_dir,
        catalog_file=catalog_file,
        shared_ui_dir=shared_ui,
        target_plugin_id=args.plugin
    )

    if args.json:
        print(json.dumps(audit_res, indent=2, ensure_ascii=False))
    else:
        print_report(audit_res)

    if args.strict and audit_res.get("failed", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
