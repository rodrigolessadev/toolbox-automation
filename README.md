# Toolbox Automation

Ferramentas, agentes, workflows, políticas e documentação para apoiar o desenvolvimento e a manutenção dos projetos:

- [Toolbox](https://github.com/rodrigolessadev/toolbox)
- [toolbox-plugins](https://github.com/rodrigolessadev/toolbox-plugins)

Consulte o [**Tutorial de Uso Passo a Passo**](docs/tutorial-uso.md) para começar a utilizar a plataforma.

## Objetivo

Este repositório contém a camada de automação usada pelo Antigravity para:

- analisar os projetos;
- planejar alterações;
- implementar mudanças aprovadas;
- executar testes;
- revisar código;
- revisar interfaces;
- verificar segurança;
- manter documentação e catálogos;
- registrar checkpoints;
- retomar tarefas interrompidas.

## Projetos locais e Configurações

As configurações locais não são versionadas. Use os arquivos de exemplo para configurar seu ambiente:

- `config/local-projects.yaml` (referência: `config/local-projects.example.yaml`)
- `config/graphify.yaml` (referência: `config/graphify.example.yaml` — integração opcional, desativada por padrão)

## Diretórios

| Diretório | Finalidade |
|---|---|
| `.agent` | Memória persistente, inventário e checkpoints |
| `agents` | Agentes especializados |
| `config` | Configurações da automação |
| `docs` | Documentação operacional |
| `evals` | Avaliações e testes de validação dos agentes |
| `mcp` | Integrações e configurações de MCP |
| `policies` | Políticas de segurança, governança e aprovação |
| `prompts` | Prompts operacionais |
| `schemas` | Contratos estruturados JSON Schema |
| `scripts` | Utilitários de suporte e automação |
| `workflows` | Fluxos operacionais padronizados |

## Princípios

- preservar compatibilidade com plugins legados;
- trabalhar de forma incremental;
- consultar o Graphify de forma segura e somente leitura antes de alterações relevantes;
- limitar alterações ao escopo aprovado;
- separar análise, implementação e revisão;
- proteger segredos e dados sensíveis;
- exigir aprovação para ações externas ou destrutivas;
- registrar checkpoints e pendências;
- manter o Toolbox e o toolbox-plugins consistentes.

## Integração com Graphify (Opcional)

A integração com o Graphify é **somente leitura por padrão** e estritamente opcional.
- **Análise de Impacto**: `powershell -ExecutionPolicy Bypass -File scripts/update-graph.ps1 -ImpactAnalysis -TargetFile <caminho>`
- **Geração Explícita de Grafo**: `powershell -ExecutionPolicy Bypass -File scripts/update-graph.ps1 -BuildGraph`
- **Governança**: consulte [`policies/graphify-policy.md`](policies/graphify-policy.md).
