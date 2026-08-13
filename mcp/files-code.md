# MCP de arquivos e código

## Identificação

- Nome conceitual: `files-code`
- Categoria: arquivos, código e Git local
- Nível padrão: 1 e 2
- Acesso externo: não

## Objetivo

Permitir que os agentes leiam, pesquisem, comparem e, quando autorizado,
modifiquem arquivos dentro dos diretórios locais aprovados.

## Diretórios autorizados

- `C:\tools\toolbox-automation`
- `C:\tools\toolbox`
- `C:\tools\toolbox-plugins`

Nenhum outro diretório está autorizado por padrão.

## Operações de leitura permitidas

- listar diretórios;
- localizar arquivos;
- ler código;
- ler documentação;
- ler schemas;
- pesquisar referências;
- consultar histórico Git;
- consultar branches;
- consultar estado Git;
- analisar diffs;
- identificar arquivos não rastreados;
- identificar arquivos modificados;
- comparar versões locais.

## Operações de alteração permitidas

Somente quando previstas no plano aprovado:

- criar arquivos;
- editar arquivos;
- atualizar documentação;
- alterar testes;
- atualizar schemas;
- criar registros de checkpoint;
- criar branch local, quando previsto.

## Operações proibidas

- ler segredos;
- exibir tokens;
- acessar diretórios fora do escopo;
- descartar alterações locais;
- executar limpeza destrutiva;
- modificar arquivos não previstos;
- sobrescrever alterações de outra origem;
- apagar arquivos sem aprovação específica;
- fazer publicação externa.

## Arquivos protegidos

Não ler nem exibir:

- `.env`;
- `.env.*`;
- chaves;
- tokens;
- credenciais;
- certificados privados;
- arquivos de sessão;
- cookies;
- diretórios `secrets`;
- diretórios `credentials`.

## Agentes autorizados

| Agente | Leitura | Alteração |
|---|---:|---:|
| Orquestrador | Sim | Apenas registros da automação |
| Analista | Sim | Não |
| Implementador | Sim | Sim, conforme plano |
| Testador | Sim | Testes autorizados |
| Revisor visual | Sim | Não |
| Revisor de segurança | Sim | Não |
| Gerente de release | Sim | Commit local somente com aprovação |

## Registro obrigatório

Toda alteração deverá registrar:

- repositório;
- caminho relativo;
- tipo de alteração;
- motivo;
- agente responsável;
- tarefa;
- resultado;
- alterações inesperadas.

## Comportamento em caso de conflito

Se houver alteração local inesperada:

1. não sobrescrever;
2. não restaurar;
3. não fazer merge automático;
4. registrar o arquivo;
5. bloquear a fase;
6. solicitar orientação.
