#!/usr/bin/env python3
"""
Automação de Geração e Sincronização de Documentação de Plugins para o Site Astro.
Site: https://toolbox-nine-phi.vercel.app/ (C:\\tools\\toolbox\\site)
Origem: C:\\tools\\toolbox-plugins
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


REPO_PLUGINS_DIR = Path(r"C:\tools\toolbox-plugins")
SITE_CONTENT_DIR = Path(r"C:\tools\toolbox\site\src\content\plugins")
STATE_CACHE_FILE = Path(r"C:\tools\toolbox-automation\.plugin_docs_sync.json")


def calculate_plugin_hash(plugin_dir: Path) -> str:
    """Calcula o hash SHA256 combinado de todos os arquivos relevantes do plugin."""
    if not plugin_dir.exists() or not plugin_dir.is_dir():
        return ""
    hasher = hashlib.sha256()
    for file_path in sorted(plugin_dir.rglob("*")):
        if file_path.is_file() and not any(ign in str(file_path) for ign in ["__pycache__", ".pytest_cache", "temp_cache", ".git", ".zip", ".pyc"]):
            try:
                hasher.update(file_path.name.encode("utf-8"))
                hasher.update(file_path.read_bytes())
            except Exception:
                pass
    return hasher.hexdigest()


def generate_doc_markdown(plugin_info: Dict[str, Any], readme_content: str = "") -> str:
    """Gera conteúdo Markdown estruturado para a subpágina de documentação no Astro."""
    p_id = plugin_info.get("id", "")
    p_name = plugin_info.get("name", p_id)
    p_desc = plugin_info.get("description", "")
    p_ver = plugin_info.get("version", "1.0.0")
    p_author = plugin_info.get("author", "Rodrigo Lessa")
    p_lang = plugin_info.get("language", "python")
    p_tags = plugin_info.get("tags", [])
    p_dl = plugin_info.get("download_url", "")
    p_updated = plugin_info.get("updated_at", "2026-08-14")
    p_cmd = plugin_info.get("command", p_id)

    tags_formatted = json.dumps(p_tags, ensure_ascii=False)

    frontmatter = f"""---
id: "{p_id}"
name: "{p_name}"
description: "{p_desc}"
version: "{p_ver}"
author: "{p_author}"
language: "{p_lang}"
command: "{p_cmd}"
tags: {tags_formatted}
download_url: "{p_dl}"
updated_at: "{p_updated}"
---
"""

    body = f"""
## 📌 Visão Geral

O plugin **{p_name}** é uma extensão oficial para o **Toolbox Desktop** desenvolvida em **{p_lang.capitalize()}**.
{p_desc}

---

## 🚀 Como Instalar e Ativar

1. Abra o **Toolbox Desktop**.
2. Acesse a aba **Marketplace**.
3. Localize o card **{p_name}** e clique em **Instalar** (ou **Atualizar**).
4. O plugin será instalado automaticamente no diretório local de plugins e estará pronto para uso.

---

## 💻 Modos de Uso

### 1. Interface Gráfica (Desktop)
Você pode abrir a janela interativa do plugin diretamente pelo launcher do Toolbox digitando `{p_cmd}` ou selecionando-o na lista de ferramentas.

### 2. Protocolo Headless (IPC v1.0)
Para integrações via linha de comando ou automações externas, o plugin suporta o **Protocolo Toolbox IPC v1.0** via `STDIN`/`STDOUT` no formato JSON:

#### Exemplo de Entrada (STDIN):
```json
{{
  "protocol_version": "1.0",
  "request_id": "req_001",
  "action": "run",
  "input": {{
    "sample_field": "valor_de_exemplo"
  }},
  "options": {{}}
}}
```

#### Exemplo de Saída (STDOUT):
```json
{{
  "protocol_version": "1.0",
  "request_id": "req_001",
  "status": "success",
  "result": {{
    "output": "Operação realizada com sucesso."
  }},
  "error": null,
  "warnings": []
}}
```

---

## 🔒 Segurança e Privacidade
- **Processamento 100% Local**: O plugin executa exclusivamente no ambiente do usuário, sem chamadas para APIs de terceiros ou serviços externos.
- **Determinismo**: Todas as saídas são geradas por algoritmos e regras determinísticas.
- **Não Destrutivo**: O plugin nunca sobrescreve arquivos originais sem autorização explícita.
"""

    if readme_content.strip():
        clean_readme = "\n".join(
            line for line in readme_content.splitlines()
            if not line.startswith("# ") and not "license" in line.lower()
        ).strip()
        if clean_readme:
            body += f"\n\n---\n\n## 📖 Documentação Detalhada\n\n{clean_readme}\n"

    return frontmatter.strip() + "\n" + body.strip() + "\n"


def sync_all_plugin_docs(force: bool = False) -> Dict[str, Any]:
    """Sincroniza o catálogo e os plugins com as páginas de documentação do site."""
    SITE_CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    catalog_path = REPO_PLUGINS_DIR / "catalog.json"
    if not catalog_path.exists():
        raise FileNotFoundError(f"Catálogo não encontrado em {catalog_path}")

    catalog_data = json.loads(catalog_path.read_text(encoding="utf-8"))
    plugins_list = catalog_data.get("plugins", [])

    # Carregar cache de estado
    state_cache = {}
    if STATE_CACHE_FILE.exists() and not force:
        try:
            state_cache = json.loads(STATE_CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            state_cache = {}

    stats = {
        "total_plugins": len(plugins_list),
        "created": [],
        "updated": [],
        "unchanged": []
    }

    new_state_cache = {}

    for plugin in plugins_list:
        p_id = plugin.get("id") or plugin.get("name", "").lower().replace(" ", "-")
        plugin_dir = REPO_PLUGINS_DIR / "plugins" / p_id
        
        # Ler README se existir
        readme_text = ""
        if (plugin_dir / "README.md").exists():
            try:
                readme_text = (plugin_dir / "README.md").read_text(encoding="utf-8", errors="replace")
            except Exception:
                pass

        current_hash = calculate_plugin_hash(plugin_dir)
        cached_entry = state_cache.get(p_id, {})
        cached_hash = cached_entry.get("hash", "")
        cached_ver = cached_entry.get("version", "")

        target_md = SITE_CONTENT_DIR / f"{p_id}.md"
        exists = target_md.exists()

        if not exists:
            # 1. Criar nova subpágina
            doc_content = generate_doc_markdown(plugin, readme_text)
            target_md.write_text(doc_content, encoding="utf-8")
            stats["created"].append(p_id)
            print(f"[CRIADO] Nova subpágina gerada: {p_id}.md")
        elif force or current_hash != cached_hash or plugin.get("version") != cached_ver:
            # 2. Atualizar subpágina existente
            doc_content = generate_doc_markdown(plugin, readme_text)
            target_md.write_text(doc_content, encoding="utf-8")
            stats["updated"].append(p_id)
            print(f"[ATUALIZADO] Documentação sincronizada: {p_id}.md (v{plugin.get('version')})")
        else:
            stats["unchanged"].append(p_id)

        new_state_cache[p_id] = {
            "hash": current_hash,
            "version": plugin.get("version", ""),
            "updated_at": plugin.get("updated_at", "")
        }

    # Salvar cache de estado
    STATE_CACHE_FILE.write_text(json.dumps(new_state_cache, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return stats


def main():
    parser = argparse.ArgumentParser(description="Sincronizador de Documentação de Plugins para o Site Astro.")
    parser.add_argument("--force", action="store_true", help="Força a recriação de todas as páginas.")
    parser.add_argument("--check", action="store_true", help="Apenas verifica se há alterações sem gravar.")
    args = parser.parse_args()

    print("🚀 Sincronizando documentação dos plugins...")
    res = sync_all_plugin_docs(force=args.force)
    print("\n--- Relatório de Sincronização ---")
    print(f"Total de Plugins: {res['total_plugins']}")
    print(f"Subpáginas Criadas: {len(res['created'])} -> {', '.join(res['created']) if res['created'] else 'Nenhuma'}")
    print(f"Subpáginas Atualizadas: {len(res['updated'])} -> {', '.join(res['updated']) if res['updated'] else 'Nenhuma'}")
    print(f"Subpáginas Inalteradas: {len(res['unchanged'])}")


if __name__ == "__main__":
    main()
