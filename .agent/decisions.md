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
