# Política de aprovação

## Objetivo

Definir quando a automação deve solicitar aprovação humana antes de continuar.

## Aprovação obrigatória antes da implementação

A automação deverá solicitar aprovação quando a tarefa:

- alterar mais de um repositório;
- modificar um contrato compartilhado;
- adicionar dependência;
- modificar autenticação;
- modificar autorização;
- modificar permissões;
- modificar o executor de plugins;
- modificar o instalador;
- alterar comandos shell;
- alterar workflows de CI;
- alterar o sistema de empacotamento;
- remover compatibilidade legada;
- remover arquivos;
- alterar arquivos protegidos;
- acessar diretórios fora do escopo;
- exigir migração de dados;
- envolver risco alto ou crítico;
- tiver impacto arquitetural relevante;
- não possuir critérios de sucesso claros.

## Aprovação obrigatória antes de ações externas

Solicitar aprovação separada para:

- `git push`;
- criação de pull request;
- merge;
- release;
- deploy;
- publicação de pacote;
- criação de tag;
- alteração de issue;
- envio de mensagens;
- qualquer operação em serviço externo.

Uma aprovação para implementação local não autoriza nenhuma dessas operações.

## Conteúdo mínimo da solicitação de aprovação

Toda solicitação deverá informar:


## Exemplo de solicitação


## Respostas válidas

A automação deverá interpretar apenas respostas explícitas como aprovação:

- `aprovo`;
- `aprovado`;
- `autorizo`;
- `pode executar`;
- `pode publicar`;
- `pode fazer push`.

Respostas ambíguas não devem ser interpretadas como aprovação:

- `ok`;
- `parece bom`;
- `continue`;
- `pode ser`;
- `faça o necessário`.

Quando a ação for externa ou destrutiva, exigir uma confirmação específica
para aquela ação.

## Expiração da aprovação

A aprovação deverá ser considerada inválida quando:

- o escopo mudar;
- novos arquivos forem incluídos;
- o risco aumentar;
- o repositório mudar;
- o diff mudar substancialmente;
- surgirem bloqueios de segurança;
- a tarefa for retomada após alteração externa;
- a aprovação estiver relacionada a outra tarefa.

## Registro da aprovação

A aprovação deverá ser registrada no checkpoint ou no log da tarefa, contendo:

- data;
- responsável;
- tarefa;
- ação aprovada;
- escopo aprovado;
- observações;
- limitações.

Nunca registrar tokens, senhas ou credenciais.
