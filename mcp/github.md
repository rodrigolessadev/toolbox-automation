# MCP GitHub

## Identificação

- Nome conceitual: `github`
- Categoria: repositórios e colaboração externa
- Nível padrão: 1 para leitura
- Nível de escrita: 4
- Acesso externo: sim

## Repositórios autorizados

- `https://github.com/rodrigolessadev/toolbox`
- `https://github.com/rodrigolessadev/toolbox-plugins`
- o repositório remoto de `toolbox-automation`, quando definido.

## Operações de leitura permitidas

Mediante escopo:

- consultar repositórios;
- consultar branches;
- consultar commits;
- consultar tags;
- consultar issues;
- consultar pull requests;
- consultar comentários;
- consultar workflows;
- consultar status de verificações;
- consultar releases;
- consultar documentação pública;
- comparar referências remotas.

## Operações de escrita

Sempre exigem aprovação específica:

- criar issue;
- alterar issue;
- criar branch remoto;
- abrir pull request;
- comentar em pull request;
- solicitar revisão;
- criar tag;
- publicar release;
- alterar configurações;
- fazer merge;
- fazer push;
- excluir branch;
- publicar pacote.

## Agentes autorizados

| Agente | Leitura | Escrita |
|---|---:|---:|
| Orquestrador | Sim | Não |
| Analista | Sim | Não |
| Implementador | Não por padrão | Não |
| Testador | Consultar status | Não |
| Revisor visual | Não por padrão | Não |
| Revisor de segurança | Sim | Não |
| Gerente de release | Sim | Somente após aprovação |

## Proteção de credenciais

Nunca:

- ler ou exibir tokens;
- copiar credenciais;
- incluir tokens em relatórios;
- registrar cabeçalhos de autenticação;
- enviar segredos para outro serviço;
- armazenar credenciais nos arquivos do projeto.

## Requisitos antes de uma ação externa

Antes de solicitar aprovação, apresentar:

- repositório;
- branch;
- remoto;
- ação;
- arquivos ou commits;
- resumo;
- testes;
- revisões;
- riscos;
- rollback;
- destino da publicação.

## Falhas

Se uma operação externa falhar:

1. preservar o estado local;
2. registrar a operação tentada;
3. não repetir automaticamente;
4. verificar se a operação pode ter sido parcialmente concluída;
5. solicitar orientação.
