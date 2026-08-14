# Procedimento de interrupção segura

## Quando interromper

Interromper imediatamente quando ocorrer:

- alteração fora do escopo;
- arquivo inesperado;
- acesso a arquivo protegido;
- comando não previsto;
- tentativa de ação externa;
- falha de segurança;
- conflito Git;
- mudança inesperada no branch;
- teste obrigatório falhando;
- perda de contexto;
- necessidade de aprovação adicional.

## Procedimento

1. parar a fase atual;
2. não executar comandos de limpeza;
3. não restaurar arquivos automaticamente;
4. registrar o último estado conhecido;
5. consultar o estado Git;
6. listar arquivos modificados;
7. registrar o motivo da interrupção;
8. atualizar o checkpoint;
9. classificar a tarefa como `blocked`;
10. informar a decisão necessária;
11. aguardar orientação humana.

## Informações obrigatórias

Registrar:

- task_id;
- fase;
- agente responsável;
- repositório;
- branch;
- commit atual;
- arquivos alterados;
- comando ou evento causador;
- risco;
- ação já executada;
- ação proibida de continuar;
- próxima decisão necessária.

## Retomada

A tarefa só poderá ser retomada após:

- análise do bloqueio;
- confirmação do estado Git;
- revisão do escopo;
- renovação da aprovação, quando aplicável;
- atualização do plano;
- atualização do checkpoint.
