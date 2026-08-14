# Avaliações da Toolbox Automation Platform

## Objetivo

Este diretório contém verificações automatizadas e sem efeitos destrutivos para
validar a configuração, os schemas, as políticas, os workflows e os
procedimentos da plataforma.

## Testes disponíveis

| Arquivo | Finalidade |
|---|---|
| `test-config.ps1` | Validar configuração local |
| `test-schemas.ps1` | Validar sintaxe dos schemas |
| `test-policies.ps1` | Validar políticas obrigatórias |
| `test-workflows.ps1` | Validar workflows obrigatórios |
| `test-scripts.ps1` | Validar scripts de inicialização |
| `test-protected-paths.ps1` | Validar proteção de caminhos |
| `run-all-tests.ps1` | Executar toda a suíte |

## Princípios

- os testes não devem modificar os repositórios de produto;
- os testes não devem fazer acesso externo;
- os testes não devem ler o conteúdo de segredos;
- os testes devem preservar alterações locais;
- falhas devem possuir mensagens claras;
- o código de retorno deve indicar o resultado real.

## Classificação

- `PASS`: verificação aprovada;
- `FAIL`: verificação reprovada;
- `WARN`: aviso não bloqueador;
- `SKIP`: verificação não executada por condição conhecida.

## Regra de conclusão

A plataforma não deve ser considerada validada quando um teste obrigatório
falhar.
