# Visão geral da arquitetura

## Status

Este documento ainda está em elaboração.

## toolbox

### Responsabilidade

Aplicação principal responsável pela interface, execução, instalação e
gerenciamento dos plugins.

### Componentes principais

- Interface:
- Camada de aplicação:
- Camada de domínio:
- Executor de plugins:
- Instalador:
- Gerenciador de catálogo:
- Persistência:
- Configuração:
- Testes:

### Fluxo principal

1. Usuário inicia o Toolbox.
2. A aplicação carrega sua configuração.
3. O catálogo de plugins é consultado.
4. O usuário seleciona uma ação ou plugin.
5. O Toolbox valida e executa o plugin.
6. O resultado é apresentado ao usuário.

> Confirmar este fluxo durante o inventário técnico.

## toolbox-plugins

### Responsabilidade

Armazenar os plugins, metadados, pacotes, documentação e catálogo relacionados
ao ecossistema do Toolbox.

### Componentes principais

- Plugins:
- Metadados:
- Catálogo:
- Scripts de validação:
- Empacotamento:
- Documentação:
- Testes:

### Fluxo de publicação

1. Plugin é criado ou alterado.
2. Metadados são validados.
3. O pacote é gerado.
4. O catálogo é atualizado.
5. O Toolbox consome o plugin.

> Confirmar este fluxo durante o inventário técnico.

## Pontos de integração

- Contrato entre Toolbox e plugins:
- Versão mínima suportada:
- Formato do pacote:
- Formato do catálogo:
- Protocolo de execução:
- Tratamento de erros:
- Compatibilidade legada:

## Riscos arquiteturais conhecidos

- A confirmar após a análise dos arquivos.
