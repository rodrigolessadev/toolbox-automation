# Guia dos MCPs e integrações

## Objetivo

Este guia explica como os agentes devem selecionar e utilizar ferramentas
durante os workflows da automação.

## Regra geral

Antes de utilizar uma ferramenta, o agente deverá confirmar:

1. qual é a finalidade da operação;
2. qual MCP é adequado;
3. qual é o repositório afetado;
4. qual é o nível de permissão;
5. se a operação está prevista no plano;
6. se há necessidade de aprovação;
7. se existem dados sensíveis;
8. como o resultado será validado;
9. como a operação será registrada.

## Seleção por finalidade

| Necessidade | MCP |
|---|---|
| Ler código | `files-code` |
| Pesquisar referências | `files-code` |
| Consultar dependências | `graphify` |
| Consultar commits remotos | `github` |
| Executar testes | `controlled-execution` |
| Validar interface | `browser` |
| Consultar documentação | `documentation` |
| Preparar PR ou release | `github` + `controlled-execution` |

## Regra contra substituição insegura

Se o MCP correto estiver indisponível, não utilizar automaticamente outro MCP
com permissões superiores.

Exemplo:

- se o Graphify estiver indisponível, não afirmar que uma simples pesquisa de
  texto substituiu a análise estrutural;
- se o navegador estiver indisponível, não afirmar que a revisão visual foi
  concluída com base apenas na leitura do código;
- se a execução controlada estiver indisponível, não afirmar que os testes
  passaram.

## Registro mínimo

Para cada operação relevante, registrar:

- tarefa;
- agente;
- MCP;
- finalidade;
- alvo;
- resultado;
- falha ou bloqueio;
- próxima ação.

## Tratamento de falhas

Em caso de falha:

1. preservar os arquivos;
2. preservar o estado Git;
3. registrar o erro sem segredos;
4. não repetir automaticamente operações externas;
5. avaliar se existe alternativa segura;
6. bloquear se a ferramenta for obrigatória.

## Proteção de dados

Nunca enviar a ferramentas externas:

- segredos;
- tokens;
- chaves privadas;
- credenciais;
- dados pessoais;
- conteúdo proprietário não necessário;
- arquivos completos quando apenas um trecho não sensível for suficiente.

## Ações externas

As ações abaixo sempre exigem aprovação separada:

- push;
- pull request;
- merge;
- release;
- deploy;
- publicação de pacote;
- alteração de issue;
- alteração de configuração remota.

## Critério de conclusão

O uso dos MCPs só será considerado adequado quando:

- a ferramenta utilizada for compatível com a finalidade;
- o nível de acesso tiver sido respeitado;
- o resultado estiver registrado;
- falhas e limitações estiverem explícitas;
- nenhum segredo tiver sido exposto;
- as aprovações necessárias estiverem registradas.
