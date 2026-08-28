# Política de Persistência e Banco de Dados SQLite Central (Abordagem B)

Esta política estabelece os padrões e requisitos arquiteturais obrigatórios para qualquer funcionalidade de persistência estruturada ou relacional no **Toolbox Ecosystem** (core desktop e plugins).

---

## 🏛️ 1. Princípio Fundamental: Banco SQLite Único e Centralizado

Conforme definido e consolidado nas issues **Toolbox #96 e #97** (Abordagem B):
- **O ecossistema adota um único arquivo SQLite central para toda a persistência da aplicação e de seus plugins.**
- **É estritamente proibido** criar arquivos de banco de dados isolados (`.db`, `.sqlite`, `.sqlite3`) nos diretórios dos plugins ou em pastas paralelas divergentes.

---

## 📍 2. Caminhos Canônicos Oficiais

A localização padrão e mandatória do arquivo `toolbox.db` é:

| Plataforma | Caminho Oficial |
| :--- | :--- |
| **Windows** | `%APPDATA%\com.toolbox.desktop\toolbox.db` |
| **Linux (padrão XDG)** | `~/.local/share/com.toolbox.desktop/toolbox.db` *(ou `~/.toolbox/toolbox.db`)* |
| **macOS** | `~/Library/Application Support/com.toolbox.desktop/toolbox.db` *(ou `~/.toolbox/toolbox.db`)* |

---

## 🔌 3. Regras para Desenvolvimento de Plugins

### 3.1. Uso Obrigatório do Utilitário Centralizado
Todo plugin desenvolvido em Python que necessite de acesso ao SQLite DEVE utilizar o utilitário compartilhado:
```python
from shared.db_utils import get_central_db_path

db_path = get_central_db_path()
```

### 3.2. Namespacing de Tabelas
Para evitar conflitos com tabelas do core do Toolbox (`commands`, `history`, `settings`, `system_commands_cache`) ou de outros plugins:
- Todas as tabelas criadas por um plugin DEVEM utilizar como prefixo o identificador do plugin.
- **Formato:** `<plugin_id>_<nome_tabela>` (ou convenção de escopo como `safe_entries`, `safe_metadata`).

### 3.3. DDL e Migrações Defensivas
- Todo script DDL de criação de tabelas deve utilizar `CREATE TABLE IF NOT EXISTS`.
- Chaves estrangeiras e relacionamentos devem ativar explicitamente `PRAGMA foreign_keys = ON;`.
- Operações de escrita devem utilizar transações atômicas e timeouts seguros (ex.: `timeout=10.0` no SQLite) para suportar concorrência leve entre processos.

---

## 🧪 4. Regras para Testes Automatizados (Isolamento)

1. **Nunca gravar no banco real durante testes:** Todo teste unitário ou de integração de banco de dados (`pytest`) DEVE utilizar diretórios temporários (`tmp_path` / `TemporaryDirectory`).
2. **Auto-migração defensiva:** Ao inicializar a camada de banco de dados de um plugin, se existirem bases legadas em versões anteriores ou em pastas divergentes, o plugin deve migrar transacionalmente os dados para o `toolbox.db` canônico e renomear o arquivo antigo para `.migrated.bak`.
