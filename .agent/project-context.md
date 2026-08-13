# Contexto dos projetos

## Objetivo

Este arquivo descreve o contexto operacional dos projetos utilizados pela
Toolbox Automation Platform.

A automação coordena análise, planejamento, implementação, testes, revisão e
manutenção dos projetos Toolbox e toolbox-plugins.

## Projetos autorizados

### toolbox-automation

- Caminho local: `C:\tools\toolbox-automation`
- Função: armazenar agentes, workflows, políticas, prompts, schemas e documentação da automação.
- Pode ser alterado pela automação: sim, dentro do escopo aprovado.

### toolbox

- Caminho local: `C:\tools\toolbox`
- Repositório remoto: https://github.com/rodrigolessadev/toolbox
- Função: aplicação principal do Toolbox.
- Pode ser alterado pela automação: sim, dentro do escopo aprovado.

### toolbox-plugins

- Caminho local: `C:\tools\toolbox-plugins`
- Repositório remoto: https://github.com/rodrigolessadev/toolbox-plugins
- Função: plugins, metadados, empacotamento e catálogo.
- Pode ser alterado pela automação: sim, dentro do escopo aprovado.

## Regras operacionais

- Nenhuma alteração deve ser feita sem identificar o projeto afetado.
- Nenhum arquivo fora do escopo aprovado pode ser modificado.
- Alterações nos dois projetos principais devem possuir checkpoints independentes.
- A automação deve preservar compatibilidade com plugins existentes.
- Ações externas ou destrutivas exigem aprovação humana.
- Arquivos contendo segredos não devem ser lidos, exibidos ou versionados.
- Quando houver dúvida, a automação deve parar e solicitar orientação.

## Estado deste documento

- Status: inicial
- Última revisão: 2026-08-13
- Próxima revisão: após o inventário técnico dos três projetos
