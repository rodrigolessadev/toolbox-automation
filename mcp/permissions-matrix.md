# Matriz de permissões dos MCPs

## Legenda

- `L`: leitura permitida;
- `A`: alteração local permitida conforme plano;
- `R`: revisão ou validação;
- `P`: preparação de ação;
- `B`: bloqueado por padrão;
- `AP`: exige aprovação específica.

## Matriz

| Agente | Arquivos | Graphify | GitHub leitura | GitHub escrita | Execução | Navegador | Documentação |
|---|---|---|---|---|---|---|---|
| Orquestrador | L, A* | L | L | B | L | B | L |
| Analista | L | L | L | B | L | B | L |
| Implementador | L, A | L | B | B | A | R | L |
| Testador | L | L | R | B | R | R | L |
| Revisor visual | L | B | B | B | R | R | L |
| Revisor de segurança | L | L | L | B | R | R | L |
| Gerente de release | L | L | L | P, AP | L | B | L |

\* O orquestrador pode alterar somente registros da automação, como
checkpoints e handoffs, quando isso estiver previsto no fluxo.

## Regras

1. Nenhum agente possui escrita externa automática.
2. GitHub escrito é sempre `AP`.
3. Acesso a arquivos protegidos é sempre bloqueado.
4. Execução depende do comando, do diretório e do risco.
5. Navegador externo é bloqueado por padrão.
6. O gerente de release prepara, mas não publica.
7. Uma ferramenta autorizada não amplia o escopo da tarefa.
8. A política mais restritiva sempre prevalece.

## Casos especiais

### Alteração em dois repositórios

Exige:

- análise de impacto;
- plano por repositório;
- checkpoint por repositório;
- validação independente;
- aprovação quando houver contrato compartilhado.

### Ação externa

Exige:

- resumo da ação;
- destino;
- conteúdo;
- testes;
- riscos;
- aprovação específica.

### Arquivo sensível

A operação deve ser bloqueada, mesmo que o agente possua permissão de leitura
no diretório pai.
