# Antigravity Rules — Toolbox Automation

Este arquivo orienta o assistente de IA na interpretação e execução das instruções de trabalho do ecossistema Toolbox.

---

## ⚡ Gatilhos Rápidos de Disparo de Issues

Sempre que o usuário enviar mensagens nos formatos simplificados abaixo, interprete-as imediatamente como uma instrução formal de implementação de issue:

### Padrões Reconhecidos:
1. **`toolbox #N`** ou **`toolbox #<numero>`**:
   - **Projeto**: `toolbox` (`C:\tools\toolbox`, repositório `rodrigolessadev/toolbox`).
   - **Ação**: Buscar detalhes da issue `#N` via GitHub CLI (`gh issue view N -R rodrigolessadev/toolbox`), criar plano de implementação, aguardar aprovação e executar o ciclo de vida completo.

2. **`plugins #N`** ou **`toolbox-plugins #N`**:
   - **Projeto**: `toolbox-plugins` (`C:\tools\toolbox-plugins`, repositório `rodrigolessadev/toolbox-plugins`).
   - **Ação**: Buscar detalhes da issue `#N` via GitHub CLI (`gh issue view N -R rodrigolessadev/toolbox-plugins`), criar plano de implementação, aguardar aprovação e executar o ciclo de vida completo.

---

## 🔄 Fluxo Obrigatório de Execução

1. **Diagnóstico & Planejamento**:
   - Inspecionar a issue no GitHub.
   - Analisar o código relevante no repositório correspondente.
   - Gerar `implementation_plan.md` e aguardar aprovação do usuário.

2. **Branch & Implementação**:
   - Criar branch `feature/...` ou `fix/...`.
   - Aplicar alterações respeitando os tokens de design do Toolbox, contraste visual e contratos do projeto.

3. **Validação Automatizada**:
   - No `toolbox`: `cargo test` + `npm run build`.
   - No `toolbox-plugins`: `pytest` + validação de contratos/schemas.

4. **Entrega & Pull Request**:
   - Commitar com referência `(Closes #N)`.
   - Fazer `git push` e abrir o Pull Request via `gh pr create`.

5. **Retorno Estruturado & Próximos Passos Obrigatórios**:
   - Entregar sempre: Nova versão (SemVer), mensagem de commit, bloco de notas do release, link do PR e **Lista Detalhada dos Próximos Passos a Serem Realizados**.

---

## 🎨 Diretrizes de Design & Contraste Visual (UI)

Ao criar ou modificar interfaces gráficas (Tkinter, Web, etc.):
1. **Contraste Obrigatório**: É estritamente proibido criar campos de entrada (`Entry`, `Text`, `Combobox`, `Inputs`), áreas de texto ou botões com cores de fundo e cores de texto idênticas ou muito parecidas.
2. **Padrão Dark Theme do Toolbox**:
   - **Fundo da janela principal (`bg`)**: `#0e1014`
   - **Fundo de cards e containers (`bg2` / `bg_card`)**: `#161a21` ou `#12151c`
   - **Fundo de campos de entrada (`input_bg`)**: `#161a21` ou `#0e1014`
   - **Texto principal (`fg`)**: `#e8eaed` (alto contraste nítido sobre fundos escuros)
   - **Texto atenuado (`muted`)**: `#8b94a3` (apenas para labels auxiliares, nunca para texto digitado pelo usuário)
   - **Cursor de inserção (`insertbackground` / `insertcolor`)**: `#e8eaed`
   - **Bordas de campos (`border`)**: `#2b3240` (com foco em `#6aa3ff`)
3. **Compatibilidade Tkinter no Windows**:
   - Nunca confiar apenas em herança de temas (`clam`, `default`) para campos de texto.
   - Sempre definir explicitamente `bg`, `fg`, `insertbackground` e bordas nos componentes de entrada (`tk.Entry`, `ScrolledText`) ou configurar `TEntry` e `TCombobox` com `fieldbackground`, `foreground` e `insertcolor` explícitos.

