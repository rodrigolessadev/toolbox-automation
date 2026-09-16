# MCPs e integrações da Toolbox Automation Platform

## Objetivo

Este diretório documenta as ferramentas e integrações que poderão ser usadas
pelos agentes da automação.

A documentação define:

- finalidade;
- agentes autorizados;
- operações permitidas;
- operações bloqueadas;
- nível de permissão;
- necessidade de aprovação;
- dados que não podem ser enviados;
- comportamento esperado em caso de falha.

## MCPs documentados

| Arquivo | Integração |
|---|---|
| `files-code.md` | Arquivos e código |
| `graphify.md` | Graphify |
| `github.md` | GitHub |
| `controlled-execution.md` | Execução controlada |
| `browser.md` | Navegador |
| `documentation.md` | Documentação técnica |
| `permissions-matrix.md` | Matriz de permissões |

## ⚙️ Configuração Executável Pronta

Para ativar o **GitHub MCP Server oficial** no Antigravity, Claude Desktop ou Cursor:
1. Copie o arquivo de exemplo:
   ```bash
   cp config/mcp_config.example.json config/mcp_config.json
   ```
2. Defina sua variável `GITHUB_PERSONAL_ACCESS_TOKEN` com escopos de leitura de repositórios, issues, pull requests e projects.
3. No Antigravity ou cliente MCP compatível, adicione o arquivo aos servidores ativos para habilitar tool calls diretas de GitHub.

Consulte os detalhes em [`github.md`](github.md).

## Princípios

- menor privilégio;
- acesso somente dentro do escopo;
- separação entre leitura e alteração;
- aprovação para ações externas;
- proteção de segredos;
- registro de operações relevantes;
- parada segura diante de falhas;
- nenhum fallback que amplie permissões.

## Regra de precedência

As políticas em `policies/` têm precedência sobre esta documentação.

Quando uma ferramenta permitir uma operação, mas a política da automação
proibir essa operação, a política mais restritiva deverá ser aplicada.

## Regra de indisponibilidade

Se um MCP necessário estiver indisponível:

1. registrar a indisponibilidade;
2. informar o impacto;
3. verificar se existe alternativa segura;
4. não substituir automaticamente por uma ferramenta de maior privilégio;
5. bloquear a tarefa se a ferramenta for obrigatória.
