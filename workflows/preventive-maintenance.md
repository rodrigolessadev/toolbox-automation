# Workflow: manutenção preventiva

## Identificação

- Nome: `preventive-maintenance`
- Finalidade: identificar e corrigir riscos técnicos antes de falhas
- Frequência: definida posteriormente pelo usuário

## Quando utilizar

Utilizar para revisar periodicamente:

- dependências;
- testes;
- documentação;
- compatibilidade;
- catálogo;
- plugins;
- configurações;
- segurança;
- desempenho;
- acessibilidade;
- arquivos temporários;
- inconsistências entre repositórios.

## Regra importante

A manutenção preventiva não deve gerar alterações em massa sem análise,
priorização e aprovação.

## Agentes envolvidos

1. Orquestrador;
2. Analista;
3. Testador;
4. Revisor de segurança;
5. Revisor visual, quando aplicável;
6. Implementador, após aprovação;
7. Gerente de release.

## Fases

### Fase 1 — Definir o escopo da inspeção

Determinar:

- repositório;
- área;
- tipo de manutenção;
- janela de análise;
- arquivos permitidos;
- critérios de risco;
- comandos seguros autorizados.

### Fase 2 — Fazer o diagnóstico

Verificar:

- dependências desatualizadas;
- testes ausentes;
- testes instáveis;
- documentação desatualizada;
- arquivos sem uso;
- configurações inconsistentes;
- divergências entre Toolbox e plugins;
- vulnerabilidades conhecidas;
- permissões excessivas;
- inconsistências no catálogo;
- componentes visuais fora do padrão;
- problemas de acessibilidade;
- build e lint;
- cobertura, quando disponível.

### Fase 3 — Classificar os achados

Classificar cada achado como:

- informativo;
- baixo;
- médio;
- alto;
- crítico.

Registrar:

- descrição;
- evidência;
- arquivo;
- causa provável;
- impacto;
- recomendação;
- urgência;
- esforço estimado.

### Fase 4 — Priorizar

Priorizar nesta ordem:

1. riscos críticos;
2. exposição de segredos;
3. vulnerabilidades altas;
4. falhas de compatibilidade;
5. falhas de build ou testes;
6. inconsistências do catálogo;
7. problemas de acessibilidade;
8. documentação;
9. melhorias de manutenção;
10. otimizações não urgentes.

### Fase 5 — Criar tarefas independentes

Cada correção relevante deverá receber:

- `task_id` próprio;
- escopo próprio;
- arquivos próprios;
- critérios de sucesso;
- risco;
- estratégia de rollback;
- checkpoint independente.

Não agrupar alterações sem relação apenas para reduzir o número de tarefas.

### Fase 6 — Solicitar aprovação

Solicitar aprovação para:

- atualizações de dependências;
- alterações sensíveis;
- refatorações amplas;
- remoção de arquivos;
- mudanças de contrato;
- mudanças em CI;
- alterações nos dois repositórios;
- correções de segurança;
- qualquer ação externa.

### Fase 7 — Implementar uma correção por vez

Evitar alterações grandes e simultâneas.

Após cada correção:

- revisar o diff;
- executar testes;
- atualizar o checkpoint;
- registrar o resultado;
- verificar se o achado foi realmente resolvido.

### Fase 8 — Validar

Executar, conforme aplicável:

- testes;
- lint;
- typecheck;
- build;
- validação de plugins;
- validação do catálogo;
- testes de compatibilidade;
- varredura de segredos;
- revisão de segurança;
- revisão visual;
- análise de regressão.

### Fase 9 — Produzir relatório

O resultado deverá informar:

- áreas analisadas;
- achados;
- itens corrigidos;
- itens pendentes;
- riscos remanescentes;
- aprovações necessárias;
- próxima revisão recomendada.

## Deve bloquear quando

- a inspeção exigir acesso fora do escopo;
- houver segredo exposto;
- houver vulnerabilidade crítica;
- a correção exigir ação externa;
- o estado dos repositórios não puder ser determinado;
- a manutenção envolver alterações destrutivas;
- os resultados não puderem ser reproduzidos.

## Estratégia de rollback

Cada correção deverá possuir rollback independente.

Não realizar uma reversão global sem identificar:

- quais tarefas foram executadas;
- quais commits foram criados;
- quais arquivos foram alterados;
- quais dependências foram atualizadas;
- quais efeitos externos ocorreram.
