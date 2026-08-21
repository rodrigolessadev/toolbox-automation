# Workflow: implementar novo recurso

## Identificação

- Nome: `new-feature`
- Finalidade: implementar uma nova funcionalidade
- Schema inicial: `task-request.schema.json`
- Schema final: `workflow-result.schema.json`

## Quando utilizar

Utilizar quando o usuário solicitar:

- uma nova funcionalidade;
- uma nova tela;
- um novo fluxo;
- uma nova integração;
- uma nova capacidade do Toolbox;
- uma nova capacidade da automação;
- uma expansão do sistema de plugins.

## Entradas

- descrição do recurso;
- objetivo esperado;
- critérios de aceitação;
- repositório provável;
- restrições conhecidas;
- prioridade, quando informada.

Se os critérios de aceitação forem insuficientes, o workflow deverá solicitar esclarecimento antes da implementação.

## Agentes envolvidos

1. Orquestrador;
2. Analista;
3. Implementador;
4. Testador;
5. Revisor visual, se houver interface;
6. Revisor de segurança, se houver risco;
7. Gerente de release.

## Fases

### Fase 1 — Formalizar a solicitação

Criar uma solicitação com:

- `task_id`;
- título;
- descrição;
- repositórios envolvidos;
- nível de risco;
- arquivos permitidos;
- arquivos proibidos;
- critérios de sucesso;
- status inicial.

### Fase 2 — Analisar a arquitetura

O analista deverá:

- localizar componentes relacionados;
- identificar pontos de extensão;
- consultar o Graphify;
- verificar contratos existentes;
- verificar compatibilidade legada;
- localizar testes;
- identificar dependências;
- informar arquivos que deverão ser alterados.

### Fase 3 — Criar o plano

O plano deverá conter:

- objetivo;
- etapas ordenadas;
- arquivos a criar ou modificar;
- testes;
- revisões necessárias;
- pontos de aprovação;
- critérios de sucesso;
- estratégia de rollback.

### Fase 4 — Solicitar aprovação

Solicitar aprovação antes da implementação quando houver:

- alteração em mais de um projeto;
- alteração de contrato;
- dependência nova;
- alteração sensível;
- risco alto ou crítico;
- mudança de comportamento incompatível;
- alteração destrutiva.

### Fase 5 — Implementar

O implementador deverá:

- confirmar o estado Git;
- ler os arquivos previstos;
- executar somente as etapas aprovadas;
- registrar arquivos modificados;
- registrar comandos executados;
- atualizar o checkpoint.

### Fase 6 — Testar

O testador deverá executar:

- testes unitários;
- testes de integração;
- lint;
- typecheck;
- build, se aplicável;
- testes de compatibilidade;
- validação de catálogo ou plugins, quando aplicável;
- varredura de segredos;
- verificação do escopo.

### Fase 7 — Revisar

Acionar:

- revisor visual para alterações de interface;
- revisor de segurança para executor, instalador, permissões, dependências ou comandos;
- revisão de compatibilidade para contratos entre projetos;
- revisão de documentação quando o recurso alterar comportamento público.

### Fase 8 — Preparar a entrega e dados de publicação

O gerente de release deverá preparar e apresentar obrigatoriamente:

- resumo da alteração e arquivos modificados;
- testes executados;
- mensagem de commit e link da Pull Request criada;
- **Nova versão SemVer** calculada do componente (Toolbox ou Plugin);
- **Notas de Release (Release Notes)** completas em Markdown para publicação imediata.

## Deve bloquear quando

- o comportamento esperado não estiver claro;
- o recurso exigir alteração fora do escopo;
- houver dependência não aprovada;
- a compatibilidade não puder ser preservada;
- os testes obrigatórios não puderem ser executados;
- houver falha de segurança;
- houver arquivo inesperado.

## Estratégia de rollback

Priorizar:

- reversão por commit local;
- restauração manual de arquivos específicos;
- preservação de migrações;
- remoção somente com aprovação;
- registro do estado anterior.

Não utilizar comandos destrutivos automaticamente.
