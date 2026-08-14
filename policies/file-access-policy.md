# Política de acesso a arquivos

## Diretórios autorizados

A automação poderá atuar somente nos diretórios:

- `C:\tools\toolbox-automation`
- `C:\tools\toolbox`
- `C:\tools\toolbox-plugins`

O agente deverá identificar o projeto antes de ler ou modificar arquivos. Contém proteção estrita a segredos e credenciais.

## Plugins Privados e Exclusões de Publicação

- O plugin **`plugins/release/`** (`C:\tools\toolbox-plugins\plugins\release`) é classificado como **plugin privado e de uso estritamente local/operacional**.
- **Regra de Bloqueio**: O plugin `release` **NUNCA** deve ser publicado no catálogo público (`catalog.json`), empacotado para o Marketplace ou enviado como release pública de plugin.

## Arquivos permitidos para leitura

Podem ser lidos, dentro do escopo:

- código-fonte;
- testes;
- documentação;
- schemas;
- configurações públicas;
- arquivos de build;
- manifests;
- metadados;
- histórico Git;
- diffs;
- arquivos de configuração de ferramentas.

## Arquivos protegidos

A automação não deverá ler, exibir, copiar ou versionar:

- `.env`;
- `.env.*`;
- arquivos de credenciais;
- tokens;
- senhas;
- chaves privadas;
- certificados privados;
- arquivos `.pem`;
- arquivos `.key`;
- arquivos `.p12`;
- arquivos `.pfx`;
- diretórios `secrets`;
- diretórios `credentials`;
- arquivos de sessão;
- cookies;
- dumps com dados pessoais;
- arquivos pessoais não relacionados ao projeto.

## Exceções

Um arquivo protegido só poderá ser tratado mediante:

- finalidade claramente documentada;
- escopo específico;
- aprovação explícita;
- proteção para evitar exposição do conteúdo;
- registro da operação sem incluir o segredo.

Mesmo com aprovação, o agente deverá evitar exibir o conteúdo completo.

## Arquivos protegidos dentro dos projetos

O fato de um arquivo estar dentro de um diretório autorizado não remove sua
proteção.

## Verificação antes da alteração

Antes de modificar um arquivo, o agente deverá confirmar:

1. o projeto correto;
2. o caminho relativo;
3. a existência do arquivo;
4. que o arquivo está no plano;
5. que não é protegido;
6. que não possui alterações locais inesperadas;
7. que a alteração é compatível com o escopo.

## Arquivos fora do escopo

Arquivos fora do escopo da tarefa não devem ser modificados, mesmo quando
estiverem em um diretório autorizado.

## Arquivos gerados

Artefatos temporários devem ser armazenados somente em locais definidos para
esse fim e não devem ser confundidos com alterações de produto.

Ao final da tarefa, os artefatos devem ser:

- removidos, quando temporários;
- preservados, quando necessários para evidência;
- registrados no resultado;
- excluídos do commit, quando não fizerem parte do produto.
