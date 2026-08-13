# Guia de permissões e aprovações

## Objetivo

Este documento resume como os agentes devem aplicar as políticas de
permissão, aprovação e bloqueio.

## Regra geral

A automação deve executar a menor ação necessária para concluir a tarefa.

Se uma operação puder ser realizada somente por leitura, não deve modificar
arquivos.

Se uma operação puder ser realizada localmente, não deve ser publicada
automaticamente.

Se uma operação for reversível, não deve ser substituída por uma operação
destrutiva.

## Matriz de decisão

| Operação | Nível | Aprovação |
|---|---:|---:|
| Ler documentação | 1 | Não |
| Consultar Git | 1 | Não |
| Consultar Graphify | 1 | Não |
| Criar relatório local | 2 | Conforme o plano |
| Alterar teste previsto | 2 | Plano aprovado |
| Alterar código de produto | 2 | Plano aprovado |
| Adicionar dependência | 3 | Sim |
| Alterar autenticação | 3 | Sim |
| Alterar permissões | 3 | Sim |
| Alterar executor de plugins | 3 | Sim |
| Remover arquivo | 3 ou 4 | Sim |
| Criar commit | 2 ou 3 | Conforme o plano |
| Fazer push | 4 | Sempre |
| Criar pull request | 4 | Sempre |
| Fazer merge | 4 | Sempre |
| Fazer deploy | 4 | Sempre |

## Fluxo de decisão

Antes de executar uma operação, o agente deverá perguntar:

1. O projeto está autorizado?
2. O arquivo está dentro do escopo?
3. A operação está prevista no plano?
4. A operação é reversível?
5. Existe risco de segurança?
6. Existe impacto externo?
7. A aprovação necessária foi registrada?
8. O estado Git está conforme o esperado?
9. Há alterações locais de outra origem?
10. O resultado poderá ser validado?

Se qualquer resposta relevante for negativa ou desconhecida, o agente deverá
bloquear ou solicitar esclarecimento.

## Regra de parada

O agente deve parar quando encontrar:

- escopo ambíguo;
- repositório incerto;
- arquivo protegido;
- alteração local inesperada;
- risco alto ou crítico;
- ação externa sem aprovação;
- tentativa de operação destrutiva;
- falha de validação;
- saída incompatível com o schema.

## Registro

Toda decisão relevante deverá ser registrada em um destes locais:

- checkpoint da tarefa;
- `.agent/handoff.md`;
- `.agent/decisions.md`;
- `.agent/work-log.md`;
- resultado estruturado do workflow.

Não registrar segredos ou dados sensíveis.
