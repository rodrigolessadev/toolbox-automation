# Guia dos workflows da automação

## Objetivo

Os workflows organizam o trabalho dos agentes em fases previsíveis,
rastreáveis e retomáveis.

## Seleção do workflow

| Situação | Workflow |
|---|---|
| Tarefa interrompida | `resume-task` |
| Nova funcionalidade | `new-feature` |
| Criação ou alteração de plugin | `plugin-lifecycle` |
| Falha ou regressão | `bug-fix` |
| Revisão preventiva | `preventive-maintenance` |

## Fluxo padrão


## Checkpoints obrigatórios

Atualizar o checkpoint:

- após a análise;
- após o plano;
- após a aprovação;
- após a implementação;
- após os testes;
- após as revisões;
- antes do encerramento;
- quando ocorrer bloqueio;
- quando a tarefa for interrompida.

## Regra para múltiplos repositórios

Quando uma tarefa envolver mais de um repositório:

- identificar cada projeto separadamente;
- listar os arquivos de cada projeto;
- criar checkpoints independentes;
- validar cada projeto individualmente;
- registrar a relação entre os resultados;
- não considerar o workflow concluído se um projeto estiver bloqueado.

## Regra para aprovação

As aprovações abaixo são independentes:

- aprovação do plano;
- aprovação da implementação;
- aprovação de dependência;
- aprovação de commit;
- aprovação de push;
- aprovação de pull request;
- aprovação de merge;
- aprovação de release;
- aprovação de deploy.

## Regra de bloqueio

Ao encontrar um bloqueio:

1. interromper a fase atual;
2. preservar o estado local;
3. registrar o problema;
4. atualizar o checkpoint;
5. identificar a decisão necessária;
6. informar a próxima ação possível;
7. aguardar orientação.

## Resultado final

O resultado deve utilizar `workflow-result.schema.json` e informar:

- status;
- resumo;
- repositórios;
- arquivos alterados;
- validação;
- revisões;
- aprovações pendentes;
- riscos remanescentes;
- próxima ação.
