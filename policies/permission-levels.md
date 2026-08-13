# Níveis de permissão

## Objetivo

Definir quais operações podem ser executadas automaticamente e quais exigem
aprovação humana.

## Nível 1 — Leitura e análise

### Permitido

- listar diretórios autorizados;
- ler arquivos não sensíveis;
- consultar documentação;
- consultar histórico Git;
- consultar branch atual;
- consultar estado Git;
- analisar diffs;
- pesquisar referências;
- consultar o Graphify;
- identificar testes;
- identificar comandos de validação;
- produzir relatórios;
- atualizar registros de contexto da automação, quando previsto.

### Condições

- a operação deve estar dentro dos diretórios autorizados;
- arquivos sensíveis não devem ser lidos;
- nenhuma alteração deve ser realizada nos projetos de produto;
- alterações locais existentes não podem ser descartadas.

### Aprovação

Não é necessária, desde que a leitura esteja dentro do escopo autorizado.

---

## Nível 2 — Alteração reversível local

### Permitido mediante plano

- criar arquivo previsto no plano;
- editar arquivo previsto no plano;
- alterar testes;
- atualizar documentação;
- atualizar schemas;
- criar branch local;
- executar formatadores autorizados;
- executar testes;
- gerar relatórios locais;
- atualizar checkpoints;
- atualizar registros da automação.

### Condições

- deve existir um plano de implementação;
- os arquivos devem estar listados no plano;
- o repositório deve estar identificado;
- o diff deve permanecer dentro do escopo;
- a alteração deve ser reversível;
- não pode envolver segredos;
- não pode alterar configurações externas;
- não pode publicar dados.

### Aprovação

Pode ser executado sem nova aprovação quando estiver coberto por um plano
aprovado e não envolver alteração sensível.

---

## Nível 3 — Alteração sensível

### Exemplos

- alterar autenticação;
- alterar autorização;
- alterar permissões;
- alterar o executor de plugins;
- alterar o instalador;
- alterar comandos shell;
- alterar workflows de CI;
- adicionar dependência;
- alterar contratos entre repositórios;
- alterar o formato do catálogo;
- alterar o processo de empacotamento;
- alterar arquivos de configuração críticos;
- remover compatibilidade legada;
- modificar mecanismos de isolamento;
- alterar políticas de segurança.

### Condições

- análise técnica obrigatória;
- plano detalhado obrigatório;
- revisão de segurança obrigatória;
- testes específicos obrigatórios;
- registro da decisão;
- aprovação humana antes da implementação.

### Aprovação

Sempre necessária.

---

## Nível 4 — Ação externa ou destrutiva

### Exemplos

- `git push`;
- criação de pull request;
- merge;
- publicação de release;
- criação de tag;
- deploy;
- publicação de pacote;
- alteração de issues;
- envio de mensagens;
- remoção definitiva de arquivos;
- reset ou descarte de alterações;
- limpeza de branches;
- alteração de dados externos;
- instalação de dependências com efeitos não controlados.

### Condições

- confirmação explícita do usuário;
- descrição da ação;
- lista de alvos;
- resumo dos riscos;
- confirmação do estado final dos testes;
- confirmação de que não há segredos;
- confirmação do conteúdo que será enviado ou removido.

### Aprovação

Sempre necessária e não pode ser inferida de aprovações anteriores.

---

## Regra de escalonamento

Quando uma operação combinar mais de um nível, aplicar o nível mais alto.

Exemplo:

- editar um arquivo local: Nível 2;
- editar um arquivo local que controla permissões: Nível 3;
- editar e publicar esse arquivo: Nível 4.
