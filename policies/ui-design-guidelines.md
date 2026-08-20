# Diretrizes de UI, Contraste e Acessibilidade (Material Design 3)

Esta política estabelece os requisitos mandatórios para desenvolvimento visual e interfaces no **Toolbox Ecosystem**.

---

## 1. Regras Mandatórias

1. **Uso Obrigatório de Tokens Semânticos:**
   - É terminantemente proibido utilizar valores de cor literais `#HEX`, `rgb()` ou `hsl()` diretamente em folhas de estilo ou componentes.
   - Todo componente deve consumir tokens `var(--md-sys-color-*)` ou utilitários Tailwind definidos no preset oficial.
2. **Contraste WCAG AA:**
   - Textos sobre qualquer fundo devem ter contraste mínimo de **4.5:1** (WCAG AA).
   - Componentes visuais e contornos de campos devem ter contraste mínimo de **3.0:1**.
   - As combinações oficiais `on-*` (ex: `on-primary`, `on-surface`) são matematicamente calibradas para atender a esses limites.
3. **Suporte Obrigatório a Dark & Light Theme:**
   - Nenhuma tela ou plugin pode assumir que o tema é exclusivamente escuro ou claro.
   - Cores e superfícies devem responder dinamicamente ao atributo `[data-theme="dark"]` ou `[data-theme="light"]`.
4. **Fontes e Assets Offline:**
   - É proibido referenciar fontes remotas (ex: chamadas diretas a `fonts.googleapis.com` em tempo de execução). Todas as fontes devem ser carregadas via fontes do sistema (`sans-serif`, `Segoe UI`, `Roboto`, `Inter`) ou empacotadas localmente.

---

## 2. Verificação Pré-Commit e Pré-Release

Todos os projetos do ecossistema são inspecionados automaticamente pelo Quality Gate:
- `scripts/lint_ui_tokens.py`
- `linters/stylelint.config.js`
- `linters/eslint.config.js`
