# Checklist de revisão integrada

## Objetivo

Verificar a coerência entre os componentes da Toolbox Automation Platform
antes da primeira execução real.

## Estrutura

- [ ] README principal existe
- [ ] CHANGELOG existe
- [ ] Documento de escopo existe
- [ ] Diretório `.agent` existe
- [ ] Diretório `agents` existe
- [ ] Diretório `config` existe
- [ ] Diretório `docs` existe
- [ ] Diretório `evals` existe
- [ ] Diretório `mcp` existe
- [ ] Diretório `policies` existe
- [ ] Diretório `prompts` existe
- [ ] Diretório `schemas` existe
- [ ] Diretório `scripts` existe
- [ ] Diretório `workflows` existe

## Contexto persistente

- [ ] `project-context.md` existe
- [ ] `repository-inventory.md` existe
- [ ] `architecture-overview.md` existe
- [ ] `decisions.md` existe
- [ ] `handoff.md` existe
- [ ] `test-status.md` existe
- [ ] `work-log.md` existe

## Schemas

- [ ] Schema de solicitação existe
- [ ] Schema de análise existe
- [ ] Schema de plano existe
- [ ] Schema de implementação existe
- [ ] Schema de checkpoint existe
- [ ] Schema de validação existe
- [ ] Schema de revisão existe
- [ ] Schema de resultado do workflow existe
- [ ] Todos os schemas possuem JSON válido
- [ ] Todos os schemas possuem tipo principal definido

## Agentes

- [ ] Orquestrador documentado
- [ ] Analista documentado
- [ ] Implementador documentado
- [ ] Testador documentado
- [ ] Revisor visual documentado
- [ ] Revisor de segurança documentado
- [ ] Gerente de release documentado
- [ ] Nenhum agente possui publicação externa automática
- [ ] As responsabilidades não estão duplicadas de forma conflitante

## Políticas

- [ ] Níveis de permissão definidos
- [ ] Aprovações definidas
- [ ] Ações bloqueadas documentadas
- [ ] Acesso a arquivos documentado
- [ ] Ações externas documentadas
- [ ] Segredos protegidos
- [ ] Comandos destrutivos bloqueados
- [ ] Push, merge, release e deploy exigem aprovação

## Workflows

- [ ] Retomada documentada
- [ ] Novo recurso documentado
- [ ] Ciclo de vida de plugins documentado
- [ ] Correção de falhas documentada
- [ ] Manutenção preventiva documentada
- [ ] Todos possuem critérios de bloqueio
- [ ] Todos possuem validação
- [ ] Todos possuem checkpoint
- [ ] Todos possuem rollback
- [ ] Nenhum workflow pula diretamente para implementação

## MCPs e integrações

- [ ] Arquivos e código documentados
- [ ] Graphify documentado
- [ ] GitHub documentado
- [ ] Execução controlada documentada
- [ ] Navegador documentado
- [ ] Documentação técnica documentada
- [ ] Matriz de permissões existe
- [ ] Indisponibilidade de ferramentas possui tratamento
- [ ] Fallbacks não ampliam permissões

## Scripts

- [ ] Verificação dos projetos existe
- [ ] Carregamento do contexto existe
- [ ] Criação de tarefas existe
- [ ] Retomada de tarefas existe
- [ ] Os scripts preservam alterações locais
- [ ] Os scripts não fazem push
- [ ] Os scripts não executam comandos destrutivos
- [ ] O `task_id` é obrigatório para modificações
- [ ] Tarefas bloqueadas não são retomadas automaticamente

## Configuração

- [ ] Configuração de exemplo existe
- [ ] Configuração real existe localmente
- [ ] Configuração real está ignorada pelo Git
- [ ] Os três repositórios estão listados
- [ ] Os diretórios autorizados estão definidos
- [ ] Os caminhos protegidos estão definidos
- [ ] O checklist de inicialização existe

## Testes

- [ ] Teste da configuração existe
- [ ] Teste dos schemas existe
- [ ] Teste das políticas existe
- [ ] Teste dos workflows existe
- [ ] Teste dos scripts existe
- [ ] Teste dos caminhos protegidos existe
- [ ] Executor geral existe
- [ ] A suíte completa passou
- [ ] Relatórios temporários estão ignorados

## Resultado

A plataforma só poderá avançar para a próxima etapa quando:

- todos os itens obrigatórios estiverem concluídos;
- nenhuma inconsistência crítica permanecer;
- os testes obrigatórios passarem;
- os bloqueios estiverem registrados;
- o handoff estiver atualizado.
