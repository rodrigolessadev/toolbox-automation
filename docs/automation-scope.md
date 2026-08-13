# Escopo e limites da automação do Toolbox

## 1. Objetivo

Esta ferramenta coordena análise, planejamento, implementação, testes,
revisão e manutenção dos projetos Toolbox e toolbox-plugins.

A automação deve reduzir o trabalho repetitivo sem remover a revisão
humana de ações externas, destrutivas ou de alto impacto.

## 2. Repositórios autorizados

### Toolbox

- Repositório: https://github.com/rodrigolessadev/toolbox
- Responsabilidade: aplicação principal, interface, execução e gerenciamento de plugins.

### Toolbox Plugins

- Repositório: https://github.com/rodrigolessadev/toolbox-plugins
- Responsabilidade: código, metadados, empacotamento e catálogo de plugins.

## 3. Capacidades permitidas

### Análise

- leitura de código;
- consulta ao Graphify;
- análise de dependências;
- identificação de impacto;
- localização de testes;
- análise de documentação;
- análise do estado do Git.

### Planejamento

- geração de especificações;
- criação de planos;
- identificação de riscos;
- definição de testes;
- definição de critérios de sucesso.

### Implementação local

- criação e edição de arquivos dentro do escopo aprovado;
- criação de testes;
- atualização de documentação;
- atualização de metadados;
- geração de relatórios;
- criação de checkpoints.

### Validação

- execução de testes;
- execução de lint;
- execução de build;
- validação do catálogo;
- validação do empacotamento;
- verificação visual;
- revisão de acessibilidade;
- revisão de segurança.

## 4. Ações proibidas sem aprovação

- apagar arquivos;
- remover plugins;
- descartar alterações locais;
- executar reset destrutivo;
- fazer push;
- criar pull request;
- fazer merge;
- publicar release;
- fazer deploy;
- alterar segredos;
- ler arquivos de segredo;
- modificar permissões do GitHub;
- adicionar dependências sem justificativa;
- alterar contratos globais sem análise de impacto.

## 5. Níveis de risco

### Nível 1 — Leitura

Permitido automaticamente.

### Nível 2 — Alteração local reversível

Permitido dentro do escopo aprovado.

### Nível 3 — Alteração sensível

Exige aprovação humana.

### Nível 4 — Ação externa ou destrutiva

Exige aprovação humana explícita.

## 6. Regras de escopo

- Toda tarefa deve listar os repositórios envolvidos.
- Toda tarefa deve listar os arquivos permitidos.
- Arquivos fora do escopo não podem ser alterados sem aprovação.
- A automação deve parar quando descobrir uma dependência fora do escopo.
- Alterações nos dois repositórios devem ter checkpoints independentes.

## 7. Regras de compatibilidade

- Plugins legados devem continuar funcionando.
- Contratos existentes não devem ser quebrados sem plano de migração.
- Novas funcionalidades devem preferir adaptação incremental.
- A lógica de domínio deve permanecer separada da interface.
- Dependências do KapiNote não devem ser transportadas sem justificativa.

## 8. Critérios gerais de sucesso

- objetivo funcional atendido;
- escopo respeitado;
- testes passando;
- documentação atualizada;
- nenhum segredo no diff;
- catálogo consistente;
- compatibilidade preservada;
- riscos documentados;
- checkpoints atualizados;
- nenhuma ação externa executada sem aprovação.

## 9. Regra de parada

A automação deve parar e solicitar orientação quando:

- houver dúvida sobre o escopo;
- houver conflito entre arquivos ou branches;
- houver alterações não commitadas inesperadas;
- for necessária uma dependência nova;
- for necessário alterar um arquivo não autorizado;
- houver risco de quebrar compatibilidade;
- uma ação destrutiva parecer necessária;
- os testes falharem por causa desconhecida;
- houver suspeita de segredo ou dado sensível.