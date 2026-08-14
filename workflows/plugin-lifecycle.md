# Workflow: ciclo de vida de plugins

## Identificação

- Nome: `plugin-lifecycle`
- Finalidade: criar, alterar, validar ou preparar plugins
- Repositório principal: `toolbox-plugins`
- Repositório relacionado: `toolbox`

## Regra para Plugins Privados (ex: `plugins/release`)

- Plugins classificados como **privados/operacionais** (como `C:\tools\toolbox-plugins\plugins\release`) **NÃO** devem ser incluídos no `catalog.json` público nem empacotados para distribuição no Marketplace remoto.
- Eles operam exclusivamente no ambiente local da máquina do desenvolvedor.

## Quando utilizar

Utilizar quando a tarefa envolver:

- criação de plugin;
- alteração de plugin;
- metadados;
- catálogo;
- empacotamento;
- instalação;
- compatibilidade;
- documentação de plugin;
- validação de versões;
- remoção ou descontinuação de plugin.

## Agentes envolvidos

1. Orquestrador;
2. Analista;
3. Implementador;
4. Testador;
5. Revisor de segurança;
6. Revisor de compatibilidade;
7. Gerente de release.

## Fases

### Fase 1 - Identificar o plugin

Registrar:

- nome;
- identificador;
- versão atual;
- versão desejada;
- localização;
- status no catálogo;
- dependências;
- compatibilidade mínima;
- arquivos relacionados.

### Fase 2 - Analisar o contrato

Verificar:

- formato dos metadados;
- estrutura do pacote;
- ponto de entrada;
- parâmetros;
- saída esperada;
- permissões;
- comunicação com o Toolbox;
- compatibilidade com plugins existentes;
- tratamento de erros.

### Fase 3 - Analisar o catálogo

Confirmar:

- se o plugin já existe;
- se a versão está consistente;
- se os metadados estão completos;
- se o catálogo aponta para o pacote correto;
- se a alteração afeta versões anteriores;
- se o Toolbox consegue interpretar a mudança.

### Fase 4 - Criar o plano

O plano deverá separar, quando necessário:

- alteração do plugin;
- alteração dos metadados;
- alteração do catálogo;
- alteração do Toolbox;
- testes;
- empacotamento;
- documentação.

Cada projeto deverá possuir checkpoint independente.

### Fase 5 - Aprovação

Solicitar aprovação quando houver:

- alteração do contrato do plugin;
- alteração do formato do catálogo;
- remoção de compatibilidade;
- mudança de permissões;
- execução de comandos;
- alteração em mais de um repositório;
- publicação de pacote.

### Fase 6 - Implementação

O implementador deverá:

- alterar somente arquivos aprovados;
- manter a estrutura do pacote;
- atualizar metadados;
- atualizar testes;
- atualizar documentação;
- não publicar o pacote;
- registrar todas as mudanças.

### Fase 7 - Validação

Executar, quando disponíveis:

- validação do schema;
- validação dos metadados;
- testes do plugin;
- testes de integração;
- validação do catálogo;
- teste de instalação local;
- teste de empacotamento;
- teste de compatibilidade;
- varredura de segredos.

### Fase 8 - Revisão de segurança

Verificar:

- permissões solicitadas;
- comandos executados;
- acesso a arquivos;
- chamadas externas;
- exposição de dados;
- traversal de diretórios;
- instalação de dependências;
- execução arbitrária.

### Fase 9 - Preparar a entrega

Preparar:

- pacote local;
- resumo do plugin;
- versão;
- alterações de metadados;
- alterações no catálogo;
- testes;
- riscos;
- instruções de publicação;
- rollback.

## Deve bloquear quando

- o identificador do plugin estiver duplicado;
- os metadados forem inconsistentes;
- o pacote não puder ser validado;
- a compatibilidade for desconhecida;
- houver permissão excessiva;
- o plugin executar comandos não documentados;
- o catálogo ficar inconsistente;
- o Toolbox não conseguir consumir a nova versão.

## Estratégia de rollback

Manter:

- versão anterior do plugin;
- catálogo anterior;
- metadados anteriores;
- pacote local anterior;
- registro de compatibilidade.

Não remover a versão anterior automaticamente.
