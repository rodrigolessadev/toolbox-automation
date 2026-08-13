# MCP Graphify

## Identificação

- Nome conceitual: `graphify`
- Categoria: análise estrutural e relações
- Nível padrão: 1
- Acesso externo: depende da configuração utilizada

## Objetivo

Consultar relações entre arquivos, módulos, componentes, plugins, contratos e
dependências antes de alterações relevantes.

## Operações permitidas

- consultar dependências;
- localizar referências;
- identificar consumidores de uma função;
- identificar dependências de um módulo;
- consultar relações entre projetos;
- localizar pontos de entrada;
- analisar possíveis impactos;
- identificar ciclos;
- consultar vínculos entre Toolbox e plugins;
- produzir evidências para o planejamento.

## Operações de alteração

Não permitidas por padrão.

Caso o Graphify possua operação de atualização ou indexação, ela deverá ser
tratada separadamente e dependerá de aprovação quando:

- modificar arquivos;
- gerar artefatos dentro de um projeto;
- enviar dados para serviço externo;
- incluir arquivos protegidos;
- processar conteúdo fora do escopo.

## Agentes autorizados

| Agente | Pode consultar |
|---|---:|
| Orquestrador | Sim |
| Analista | Sim, obrigatoriamente quando aplicável |
| Implementador | Somente para confirmação |
| Testador | Quando necessário para compatibilidade |
| Revisor visual | Não por padrão |
| Revisor de segurança | Sim |
| Gerente de release | Somente para verificar impacto |

## Quando a consulta é obrigatória

Consultar o Graphify antes de:

- alterar contratos;
- modificar APIs internas;
- alterar o executor de plugins;
- alterar o instalador;
- modificar componentes compartilhados;
- atualizar metadados consumidos por outro projeto;
- remover arquivos;
- alterar dependências;
- fazer refatorações amplas;
- modificar fluxos que envolvam múltiplos projetos.

## Limitações

O Graphify não substitui:

- leitura do código;
- execução de testes;
- revisão de segurança;
- validação de compatibilidade;
- análise do estado Git.

## Falha ou indisponibilidade

Se a tarefa depender de relações que não possam ser obtidas sem o Graphify:

- registrar `performed: false`;
- explicar a limitação;
- não afirmar que o impacto foi analisado;
- solicitar aprovação para continuar sem a consulta;
- bloquear quando o risco for alto.
