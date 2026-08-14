# Guia de configuração local

## Objetivo

Este documento explica como configurar a automação para trabalhar com os
três repositórios autorizados.

## Repositórios esperados

- `toolbox-automation`
- `toolbox`
- `toolbox-plugins`

## Configuração local

A configuração real deve estar em:


Esse arquivo contém caminhos específicos da máquina e não deve ser versionado.

A configuração de exemplo está em:


## Inicialização

Executar, nesta ordem:


A inicialização deve ser interrompida quando:

- um repositório não existir;
- um diretório não for um repositório Git;
- o contexto persistente estiver incompleto;
- a configuração local estiver ausente.

## Criar uma tarefa

Exemplo:

A criação da tarefa apenas gera os registros iniciais. Ela não modifica os
projetos de produto.

## Retomar uma tarefa

A retomada deve sempre ser seguida de:

1. verificação do estado Git;
2. confirmação do escopo;
3. revisão dos arquivos modificados;
4. verificação dos bloqueios;
5. confirmação da validade das aprovações.

## Regras de segurança

- não adicionar credenciais à configuração;
- não descartar alterações locais;
- não executar comandos destrutivos;
- não fazer push automaticamente;
- não iniciar implementação sem plano aprovado;
- não ignorar arquivos protegidos;
- não utilizar caminhos fora dos diretórios autorizados.
