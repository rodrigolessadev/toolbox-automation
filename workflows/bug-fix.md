# Workflow: corrigir falha

## Identificação

- Nome: `bug-fix`
- Finalidade: reproduzir, investigar, corrigir e validar uma falha

## Quando utilizar

Utilizar quando houver:

- erro reportado;
- teste falhando;
- regressão;
- comportamento inesperado;
- falha de instalação;
- falha de execução;
- inconsistência no catálogo;
- problema de compatibilidade;
- falha visual;
- vulnerabilidade identificada.

## Agentes envolvidos

1. Orquestrador;
2. Analista;
3. Implementador;
4. Testador;
5. Revisor visual, se aplicável;
6. Revisor de segurança, se aplicável;
7. Gerente de release.

## Fases

### Fase 1 — Registrar a falha

Registrar:

- título;
- descrição;
- comportamento esperado;
- comportamento observado;
- passos para reproduzir;
- repositório;
- versão ou branch;
- ambiente;
- evidências;
- severidade;
- frequência;
- impacto.

### Fase 2 — Reproduzir

O analista ou testador deverá:

- confirmar os passos;
- verificar se a falha ainda ocorre;
- identificar condições necessárias;
- registrar resultado;
- evitar alterar arquivos durante a reprodução.

Se a falha não puder ser reproduzida, registrar como `A confirmar`.

### Fase 3 — Identificar a causa

Investigar:

- código relacionado;
- histórico Git;
- alterações recentes;
- dependências;
- contratos;
- fluxo de dados;
- logs não sensíveis;
- testes existentes;
- relações identificadas no Graphify.

Não corrigir apenas o sintoma sem compreender o impacto.

### Fase 4 — Criar teste de regressão

Sempre que possível, criar primeiro um teste que:

- reproduza a falha;
- falhe antes da correção;
- passe depois da correção;
- documente o comportamento esperado.

### Fase 5 — Criar o plano

O plano deverá conter:

- causa provável;
- arquivos afetados;
- correção proposta;
- teste de regressão;
- riscos;
- critérios de sucesso;
- rollback.

### Fase 6 — Aprovar

Solicitar aprovação quando a correção envolver:

- alteração sensível;
- mudança de contrato;
- alteração em mais de um projeto;
- risco alto ou crítico;
- migração;
- remoção de compatibilidade;
- alteração de segurança.

### Fase 7 — Criar Branch e Implementar

O implementador deverá:

- criar e alternar para a branch de correção (`git checkout -b fix/<slug>-<issue_number>`) antes de alterar qualquer código;
- nunca editar ou commitar diretamente na branch `main`;
- implementar a menor alteração capaz de corrigir a causa.

Evitar:

- refatorações não relacionadas;
- mudanças de estilo não necessárias;
- atualizações de dependência fora do plano;
- alteração de comportamento não documentada.

### Fase 8 — Validar

Executar:

- teste de regressão;
- testes relacionados;
- suíte completa, quando possível;
- lint;
- typecheck;
- build;
- testes de integração;
- compatibilidade;
- varredura de segredos.

### Fase 9 — Revisar

Acionar revisão de segurança para:

- falhas de autenticação;
- permissões;
- comandos;
- entrada de dados;
- execução de plugins;
- exposição de informações.

Acionar revisão visual para:

- falhas em componentes;
- telas;
- responsividade;
- acessibilidade.

## Deve bloquear quando

- a causa não puder ser determinada;
- a correção exigir alteração fora do escopo;
- a falha envolver dados sensíveis;
- o teste de regressão não puder ser criado;
- houver risco de mascarar outro problema;
- a solução quebrar compatibilidade;
- a severidade for crítica e exigir contenção imediata.

## Estratégia de rollback

Priorizar:

- reversão do commit local;
- restauração do comportamento anterior;
- preservação do teste de regressão;
- documentação do motivo da reversão.

Para falhas críticas, preparar também um plano de contenção separado.
