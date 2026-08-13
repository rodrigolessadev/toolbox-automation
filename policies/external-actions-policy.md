# Política de ações externas

## Objetivo

Controlar qualquer operação que altere o GitHub, serviços externos, pacotes,
ambientes de execução ou sistemas fora dos diretórios locais autorizados.

## Ações que podem ser preparadas

A automação pode preparar:

- mensagem de commit;
- descrição de pull request;
- notas de release;
- checklist de publicação;
- lista de arquivos;
- resumo de testes;
- lista de riscos;
- comando sugerido;
- plano de rollback.

Preparar uma ação não significa executá-la.

## Ações que exigem aprovação específica

- `git push`;
- abertura de pull request;
- merge;
- criação de tag;
- release;
- deploy;
- publicação de pacote;
- alteração de issue;
- alteração de configuração remota;
- solicitação de revisão;
- envio de notificações;
- execução em serviço externo.

## Informações antes da aprovação

Antes de solicitar autorização, apresentar:

- tarefa;
- repositório;
- branch;
- remoto ou serviço de destino;
- arquivos incluídos;
- resumo das alterações;
- resultado dos testes;
- resultado das revisões;
- riscos;
- ação exata que será executada;
- possibilidade de rollback;
- conteúdo que será publicado.

## Regra de separação

As aprovações abaixo são independentes:

- aprovação da implementação;
- aprovação do commit;
- aprovação do push;
- aprovação do pull request;
- aprovação do merge;
- aprovação do release;
- aprovação do deploy.

A aprovação de uma etapa não autoriza as demais.

## Regra para publicação

A automação não deverá publicar quando:

- houver segredo no diff;
- houver arquivo fora do escopo;
- houver teste obrigatório pendente;
- houver vulnerabilidade alta ou crítica;
- houver revisão de segurança pendente;
- houver alterações locais inesperadas;
- o usuário não tiver autorizado explicitamente;
- o branch ou remoto não estiver claro.

## Regra para falhas

Se uma ação externa falhar:

1. preservar o estado local;
2. registrar o erro;
3. não repetir automaticamente ações potencialmente duplicadas;
4. informar ao usuário;
5. solicitar orientação antes de tentar novamente.

## Regra para comandos sugeridos

Comandos apresentados ao usuário devem indicar:

- o objetivo;
- o diretório de execução;
- o efeito esperado;
- o risco;
- se são reversíveis;
- se exigem aprovação.
