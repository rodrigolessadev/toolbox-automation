# Política de Integração com o Graphify

## 1. Finalidade

O Graphify é utilizado no projeto `toolbox-automation` estritamente como uma camada opcional, passiva e somente leitura para análise estrutural de dependências, mapeamento de impacto pré-tarefa e auditoria de relacionamentos entre módulos, políticas, scripts e documentações.

---

## 2. Princípios Obrigatórios de Governança

1. **Desativado por Padrão**: Nenhuma rotina padrão depende da execução ou presença do Graphify para funcionar normalmente.
2. **Operação Somente Leitura**: As consultas ao grafo são informativas e não têm permissão de alterar arquivos nem instruir comandos executáveis sem supervisão humana.
3. **Proibição de Instalação Automática**: O projeto não instalará ou atualizará pacotes Python (`pip`, `uv`, `graphifyy`) automaticamente em tempo de execução.
4. **Proibição de Hooks e Configurações Globais**: Nenhuma modificação automática em `.git/hooks`, configurações de IDE ou prompts de agentes é permitida.
5. **Geração Explícita (`-BuildGraph`)**: A geração ou regeneração de artefatos de grafo em `graphify-out/` exige o parâmetro explícito `-BuildGraph`.
6. **Isolamento de Dados Sensíveis**: É estritamente vedada a indexação de `.env`, credenciais, certificados, chaves criptográficas (`*.pem`, `*.key`) ou caminhos fora do repositório.
7. **Proibição de Serviços Externos**: Todos os dados processados permanecem estritamente no ambiente local. Nenhum grafo ou trecho de código pode ser enviado para APIs externas.

---

## 3. Tratamento de Falhas e Resiliência

Se o executável do Graphify não estiver presente, ou se a análise falhar:
- A operação falhará de forma limpa, emitindo mensagens de diagnóstico compreensíveis.
- O fluxo principal de tarefas (`start-task.ps1`, `resume-task.ps1`, `init-task-from-issue.ps1`) continuará operando normalmente.
- O grafo nunca será tratado como fonte única de verdade arquitetural.

---

## 4. Auditoria e Rastreabilidade

Sempre que um grafo for gerado, o manifesto gerado deve registrar:
- Commit Git analisado.
- Escopo dos diretórios incluídos.
- Padrões excluídos.
- Data e hora UTC da geração.
- Modo de execução (somente leitura / local).
