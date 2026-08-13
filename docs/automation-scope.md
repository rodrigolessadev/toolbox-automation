## 3. Diretórios locais autorizados

A automação atuará localmente nos seguintes diretórios:

### Repositório da automação

- Caminho local: `C:\tools\toolbox-automation`
- Repositório remoto: não definido ou definido posteriormente
- Função: prompts, agentes, workflows, políticas, schemas e documentação da automação.

### Toolbox

- Caminho local: `C:\tools\toolbox`
- Repositório remoto: https://github.com/rodrigolessadev/toolbox
- Função: aplicação principal, interface, execução, instalação e gerenciamento de plugins.

### Toolbox Plugins

- Caminho local: `C:\tools\toolbox-plugins`
- Repositório remoto: https://github.com/rodrigolessadev/toolbox-plugins
- Função: código, metadados, empacotamento e catálogo dos plugins.

## 4. Regras para os diretórios locais

- A automação só poderá modificar arquivos dentro dos diretórios locais autorizados.
- A automação não poderá acessar ou alterar outros diretórios sem aprovação explícita.
- O diretório `C:\tools\toolbox-automation` contém as regras da automação e deve ser tratado como repositório de controle.
- O diretório `C:\tools\toolbox` contém o código do aplicativo principal.
- O diretório `C:\tools\toolbox-plugins` contém os plugins e seus metadados.
- A automação deverá identificar previamente qual diretório será afetado por cada tarefa.
- Uma tarefa não deverá modificar os três diretórios automaticamente.
- Alterações que envolvam mais de um repositório deverão possuir plano e checkpoints independentes.
- Arquivos fora do escopo autorizado não poderão ser criados, editados, removidos ou executados.

## 5. Mapeamento entre repositórios e diretórios locais

| Projeto | Caminho local | Repositório remoto | Pode ser alterado |
|---|---|---|---|
| Automação | `C:\tools\toolbox-automation` | Repositório da automação | Sim, dentro do escopo |
| Toolbox | `C:\tools\toolbox` | `https://github.com/rodrigolessadev/toolbox` | Sim, dentro do escopo |
| Toolbox Plugins | `C:\tools\toolbox-plugins` | `https://github.com/rodrigolessadev/toolbox-plugins` | Sim, dentro do escopo |

## 6. Arquivos protegidos

Mesmo dentro dos diretórios autorizados, a automação não poderá ler, exibir,
alterar ou versionar automaticamente:

- `.env`;
- `.env.*`;
- arquivos de credenciais;
- chaves privadas;
- tokens;
- certificados;
- arquivos de configuração com segredos;
- diretórios temporários;
- caches;
- artefatos de build;
- arquivos pessoais não relacionados ao projeto.

Quando houver suspeita de que um arquivo contém informação sensível, a automação
deverá interromper a operação e solicitar orientação.

## 7. Seleção do diretório de trabalho

Antes de executar qualquer alteração, a automação deverá:

1. classificar o tipo da tarefa;
2. identificar o projeto afetado;
3. consultar o estado Git do projeto;
4. verificar se existem alterações locais;
5. listar os arquivos que pretende modificar;
6. confirmar que os arquivos estão dentro do escopo;
7. interromper a execução caso o projeto afetado não possa ser determinado.

Exemplos:

- alterações na interface principal: `C:\tools\toolbox`;
- alterações em plugins e catálogo: `C:\tools\toolbox-plugins`;
- alterações nos agentes e workflows: `C:\tools\toolbox-automation`;
- alterações no contrato compartilhado: analisar os três projetos, com checkpoints independentes.