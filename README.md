# Toolbox Automation

Ferramentas, agentes, workflows, políticas e documentação para apoiar o desenvolvimento e a manutenção dos projetos:

- [Toolbox](https://github.com/rodrigolessadev/toolbox)
- [toolbox-plugins](https://github.com/rodrigolessadev/toolbox-plugins)

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

## Projetos locais

A configuração dos diretórios locais não é versionada. Crie o arquivo:


Use como referência:


## Diretórios

| Diretório | Finalidade |
|---|---|
| `agents` | Agentes especializados |
| `config` | Configurações da automação |
| `docs` | Documentação |
| `evals` | Avaliações dos agentes |
| `mcp` | Integrações e configurações de MCP |
| `policies` | Políticas de segurança e aprovação |
| `prompts` | Prompts persistentes |
| `schemas` | Contratos estruturados |
| `scripts` | Utilitários de suporte |
| `workflows` | Fluxos operacionais |

## Princípios

- preservar compatibilidade com plugins legados;
- trabalhar de forma incremental;
- consultar o Graphify antes de alterações relevantes;
- limitar alterações ao escopo aprovado;
- separar análise, implementação e revisão;
- proteger segredos e dados sensíveis;
- exigir aprovação para ações externas ou destrutivas;
- registrar checkpoints e pendências;
- manter o Toolbox e o toolbox-plugins consistentes.

## Estado atual

A primeira etapa definiu o escopo e os limites da automação. As próximas etapas irão configurar a documentação operacional, os agentes, os workflows e as validações.
