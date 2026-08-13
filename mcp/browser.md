# MCP de navegador

## Identificação

- Nome conceitual: `browser`
- Categoria: validação visual e funcional
- Nível padrão: 1
- Acesso externo: não por padrão

## Objetivo

Permitir que os agentes validem interfaces, fluxos de navegação e estados
visuais localmente.

## Operações permitidas

- abrir a aplicação local;
- navegar por telas;
- preencher dados de teste não sensíveis;
- verificar estados de carregamento;
- verificar estados vazios;
- verificar mensagens de erro;
- verificar responsividade;
- capturar evidências visuais;
- verificar foco de teclado;
- verificar acessibilidade básica;
- comparar comportamento antes e depois.

## Dados proibidos

Não utilizar:

- contas reais;
- senhas reais;
- tokens;
- dados pessoais;
- dados de produção;
- cookies reais;
- informações financeiras;
- credenciais de serviços externos.

## Acesso externo

Navegação externa é bloqueada por padrão.

Caso seja necessária:

- informar o domínio;
- explicar a finalidade;
- registrar os dados que serão enviados;
- verificar se existem informações sensíveis;
- solicitar aprovação;
- limitar a navegação ao domínio aprovado.

## Agentes autorizados

| Agente | Uso |
|---|---:|
| Orquestrador | Não por padrão |
| Analista | Consulta limitada |
| Implementador | Verificação local quando prevista |
| Testador | Sim |
| Revisor visual | Sim |
| Revisor de segurança | Sim, quando necessário |
| Gerente de release | Não por padrão |

## Deve bloquear quando

- a aplicação não puder ser iniciada;
- houver necessidade de conta real;
- forem solicitados dados sensíveis;
- o domínio não estiver autorizado;
- a navegação provocar efeitos externos;
- a evidência visual for insuficiente.

## Evidências

Registrar:

- fluxo avaliado;
- ambiente;
- resolução ou viewport;
- estado observado;
- resultado;
- problemas encontrados;
- referência à captura, quando aplicável.

Não incluir dados sensíveis nas evidências.
