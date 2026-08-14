# Ações bloqueadas

## Objetivo

Listar ações que a automação não pode executar automaticamente.

## Ações sempre bloqueadas sem aprovação explícita

- `git push`;
- criação de pull request;
- merge;
- deploy;
- publicação de release;
- publicação de pacote;
- criação de tag remota;
- alteração de issues;
- envio de mensagens externas;
- exclusão de repositório;
- exclusão de branch compartilhada;
- reset destrutivo;
- descarte de alterações locais;
- limpeza de arquivos não versionados;
- alteração de configurações fora do escopo;
- execução em diretório não autorizado;
- leitura de segredos;
- exibição de tokens;
- cópia de credenciais;
- envio de dados sensíveis a serviços externos.

## Ações proibidas mesmo com aprovação comum

As seguintes ações exigem uma decisão específica e não devem ser tratadas como
aprovação genérica:

- remover dados de produção;
- modificar credenciais;
- alterar chaves privadas;
- remover controles de segurança;
- desativar scanners;
- desativar validações obrigatórias;
- ignorar vulnerabilidade crítica;
- publicar segredo;
- sobrescrever alterações locais de outra pessoa;
- reescrever histórico compartilhado;
- remover uma proteção de branch.

## Comandos de alto risco

Os agentes deverão interromper e solicitar aprovação específica antes de
executar comandos equivalentes a:

- `git reset --hard`
- `git clean -fd`
- `git push --force`
- `Remove-Item -Recurse`

A lista é indicativa. Comandos com efeito semelhante também devem ser tratados
como destrutivos.

## Regra de dúvida

Se o agente não conseguir determinar se uma operação é destrutiva, deverá
tratá-la como destrutiva e bloquear a execução.

## Tratamento de alterações locais

Alterações locais existentes devem ser:

1. preservadas;
2. registradas;
3. excluídas do escopo da tarefa, salvo aprovação;
4. nunca sobrescritas automaticamente.
