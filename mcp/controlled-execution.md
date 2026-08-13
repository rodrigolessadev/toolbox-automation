# MCP de execução controlada

## Identificação

- Nome conceitual: `controlled-execution`
- Categoria: comandos locais
- Nível padrão: 1 e 2
- Acesso externo: potencialmente sim

## Objetivo

Executar comandos locais necessários para análise, testes e validação, com
controle de diretório, finalidade e risco.

## Operações permitidas

Quando previstas no plano ou na validação:

- consultar versão de ferramentas;
- executar testes;
- executar lint;
- executar typecheck;
- executar build local;
- validar schemas;
- validar metadados;
- validar catálogo;
- executar verificações de segurança;
- consultar estado Git;
- gerar relatórios locais.

## Requisitos para cada comando

Antes da execução, registrar:

- comando;
- diretório;
- finalidade;
- risco;
- efeito esperado;
- se modifica arquivos;
- se acessa rede;
- se é reversível;
- resultado esperado.

## Comandos que exigem aprovação

- instalação de dependências;
- atualização de dependências;
- execução de scripts desconhecidos;
- comandos com acesso à rede;
- comandos que alterem configurações;
- geração de artefatos persistentes;
- comandos que modifiquem mais de um projeto;
- comandos de publicação;
- comandos destrutivos.

## Comandos bloqueados por padrão

- `git reset --hard`;
- `git clean -fd`;
- `git restore .`;
- `git checkout -- .`;
- `git push --force`;
- exclusão recursiva;
- formatação de unidades;
- remoção de branches compartilhadas;
- comandos equivalentes em outra ferramenta.

## Agentes autorizados

| Agente | Execução |
|---|---:|
| Orquestrador | Diagnóstico limitado |
| Analista | Comandos somente leitura |
| Implementador | Comandos previstos no plano |
| Testador | Comandos de validação |
| Revisor visual | Inicialização local quando autorizada |
| Revisor de segurança | Scanners não destrutivos |
| Gerente de release | Preparação, não publicação |

## Regras de segurança

- executar no diretório correto;
- não incluir segredos na saída;
- não executar comandos não compreendidos;
- preservar o código de retorno;
- registrar falhas;
- não repetir automaticamente comandos com efeitos externos;
- interromper se o comando alterar arquivos inesperadamente.

## Resultado

O resultado deverá distinguir:

- executado e aprovado;
- executado e falhou;
- bloqueado;
- não executado;
- executado com avisos.
