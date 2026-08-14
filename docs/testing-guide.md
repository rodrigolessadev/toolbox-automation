# Guia de testes da plataforma

## Objetivo

Validar se a Toolbox Automation Platform possui estrutura, políticas,
workflows e procedimentos coerentes antes de receber agentes reais.

## Teste individual

Executar um teste específico:

## Suíte completa

Executar:


O resultado esperado é:

## Categorias avaliadas

### Configuração

Verifica se os três projetos e as seções obrigatórias estão definidos.

### Schemas

Verifica existência e sintaxe JSON dos contratos estruturados.

### Políticas

Verifica níveis de permissão, aprovação, bloqueios, proteção de arquivos e
ações externas.

### Workflows

Verifica se os workflows possuem identificação, agentes, fases, bloqueios e
rollback.

### Scripts

Verifica existência dos procedimentos e ausência de comandos destrutivos
conhecidos.

### Caminhos protegidos

Verifica se segredos, credenciais e arquivos sensíveis estão bloqueados.

## Interpretação

- uma falha obrigatória bloqueia a validação;
- um aviso deve ser registrado;
- um teste não executado deve ser tratado como pendência;
- não declarar a plataforma validada quando houver teste obrigatório pendente.

## Auditoria manual

Além dos testes automatizados, revisar:

- conteúdo das políticas;
- coerência entre schemas e workflows;
- permissões dos agentes;
- caminhos locais;
- estado Git;
- arquivos ignorados;
- presença de dados sensíveis;
- decisões registradas;
- handoff atualizado.

## Limitações

Esses testes verificam estrutura e regras básicas. Eles não substituem:

- revisão de segurança independente;
- testes de integração;
- execução real de workflows;
- validação dos MCPs;
- validação de agentes no ambiente final;
- testes de compatibilidade dos projetos de produto.
