# Registro de decisões

## Como utilizar este arquivo

Registre decisões que afetam a arquitetura, a segurança, os workflows ou a
organização da automação.

Cada decisão deve informar:

- contexto;
- decisão tomada;
- alternativas consideradas;
- impacto;
- data;
- responsável.

---

## DEC-001 — Separação da automação

- Data: 2026-08-13
- Status: aprovada
- Contexto: a automação atuará sobre o Toolbox e toolbox-plugins.
- Decisão: manter a plataforma de automação em um repositório separado.
- Motivo: evitar acoplamento entre a ferramenta de desenvolvimento e os produtos.
- Impacto: agentes, workflows, políticas e schemas serão mantidos em
  `toolbox-automation`.
- Responsável: Rodrigo

## DEC-002 — Diretórios locais autorizados

- Data: 2026-08-13
- Status: aprovada
- Contexto: a maior parte das ações será executada localmente.
- Decisão: autorizar inicialmente apenas:
  - `C:\tools\toolbox-automation`
  - `C:\tools\toolbox`
  - `C:\tools\toolbox-plugins`
- Motivo: limitar a superfície de acesso da automação.
- Impacto: outros diretórios exigirão aprovação explícita.
- Responsável: Rodrigo

## DEC-003 — Aprovação para ações externas

- Data: 2026-08-13
- Status: aprovada
- Contexto: push, pull request, merge, release e deploy podem afetar sistemas externos.
- Decisão: exigir aprovação humana explícita para essas ações.
- Motivo: segurança e controle operacional.
- Impacto: a automação poderá preparar essas ações, mas não executá-las
  automaticamente.
- Responsável: Rodrigo

## DEC-004 — Modelo de permissões em quatro níveis

- Data: 2026-08-13
- Status: aprovada
- Contexto: a automação precisará executar leituras, alterações locais,
  operações sensíveis e ações externas.
- Decisão: utilizar quatro níveis de permissão:
  1. leitura e análise;
  2. alteração reversível local;
  3. alteração sensível;
  4. ação externa ou destrutiva.
- Motivo: aplicar menor privilégio e tornar as aprovações explícitas.
- Impacto: cada agente e workflow deverá classificar as operações antes da
  execução.
- Responsável: Rodrigo

## DEC-005 — Workflows separados por tipo de tarefa

- Data: 2026-08-13
- Status: aprovada
- Contexto: diferentes tipos de tarefa possuem riscos, validações e agentes
  distintos.
- Decisão: utilizar workflows separados para retomada, novo recurso, plugins,
  correção de falhas e manutenção preventiva.
- Motivo: reduzir ambiguidade e permitir critérios específicos por tipo de
  operação.
- Impacto: cada workflow terá fases, bloqueios, validações e rollback próprios.
- Responsável: Rodrigo

## DEC-006 — Ferramentas separadas por responsabilidade

- Data: 2026-08-13
- Status: aprovada
- Contexto: agentes diferentes precisam de capacidades diferentes.
- Decisão: separar as integrações em arquivos e permissões específicas para
  arquivos, Graphify, GitHub, execução controlada, navegador e documentação.
- Motivo: aplicar menor privilégio e facilitar auditoria.
- Impacto: nenhum agente deverá receber acesso geral quando uma ferramenta
  específica for suficiente.
- Responsável: Rodrigo