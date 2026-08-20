# Material Design 3 (M3) — Diretrizes de Design & Guia de Migração

Este documento define os padrões oficiais do **Design System (Material Design 3 - M3)** para o **Toolbox Ecosystem** e **Toolbox Automation Platform**.

---

## 1. Visão Geral e Princípios

O ecossistema adota a especificação do **Material Design 3** para assegurar:
- **Hierarquia Visual Clara:** Uso de superfícies tonais em substituição a sombras pesadas ou bordas artificiais.
- **Acessibilidade Universal:** Conformidade estrita com o padrão **WCAG AA** (contraste mínimo de $4.5:1$ para textos e $3.0:1$ para elementos gráficos).
- **Consistência Cross-Platform:** Experiência visual uniforme em aplicações desktop Tauri, web apps React/Vite, páginas de documentação e Data Apps em Streamlit.
- **Zero Cores Hardcoded:** Proibição do uso direto de valores `#HEX`, `rgb()` ou `hsl()`, exigindo variáveis semânticas.

---

## 2. Tabela Mestre de Color Roles

### A. Cores Primárias e Acentos

| Token M3 | Finalidade | Tema Escuro (Padrão) | Tema Claro |
| :--- | :--- | :--- | :--- |
| `--md-sys-color-primary` | Cor principal de destaque e botões de ação | `#a8c7fa` | `#0b57d0` |
| `--md-sys-color-on-primary` | Texto/ícones sobre a cor primária | `#062e6f` | `#ffffff` |
| `--md-sys-color-primary-container` | Superfícies tonais de destaque ativo | `#0842a0` | `#d3e3fd` |
| `--md-sys-color-on-primary-container` | Texto sobre o container primário | `#d3e3fd` | `#041e49` |
| `--md-sys-color-secondary` | Ações secundárias e complementares | `#7cacf8` | `#005db4` |
| `--md-sys-color-secondary-container` | Botões tonais e chips secundários | `#004494` | `#d6e3ff` |
| `--md-sys-color-tertiary` | Acentos de apoio e informações | `#6dd5ed` | `#00687a` |

### B. Superfícies Tonais e Elevação

| Token M3 | Uso Recomendado | Dark Mode | Light Mode |
| :--- | :--- | :--- | :--- |
| `--md-sys-color-surface-container-lowest` | Fundo principal da aplicação (Background) | `#0c0e13` | `#ffffff` |
| `--md-sys-color-surface-container-low` | Barra de título, cabeçalhos e sidebars | `#191c20` | `#f3f3fa` |
| `--md-sys-color-surface-container` | Cards de conteúdo, painéis e seções | `#1d2024` | `#ededf4` |
| `--md-sys-color-surface-container-high` | Dropdowns, menus flutuantes e inputs inativos | `#282a2f` | `#e7e7ee` |
| `--md-sys-color-surface-container-highest`| Modais, diálogos e caixas de alerta | `#33353a` | `#e1e2e8` |
| `--md-sys-color-surface-dim` | Superfície atenuada | `#111318` | `#dad9e0` |
| `--md-sys-color-surface-bright` | Superfície iluminada | `#37393e` | `#f9f9ff` |

### C. Contornos e Feedback

| Token M3 | Uso | Dark Mode | Light Mode |
| :--- | :--- | :--- | :--- |
| `--md-sys-color-outline` | Bordas com alto contraste | `#8e9099` | `#74777f` |
| `--md-sys-color-outline-variant` | Divisores, contornos sutis de cards e inputs | `#44474f` | `#c4c6d0` |
| `--md-sys-color-error` | Estados de erro, exclusão e falhas | `#f2b8b5` | `#b3261e` |
| `--md-sys-color-success` | Sucesso, conclusão e status verde | `#6dd58c` | `#146c2e` |
| `--md-sys-color-warning` | Avisos, pendências e alertas amarelos | `#fdd663` | `#7c5800` |

---

## 3. Escala de Formas (Shape Scale)

| Token | Valor | Componentes Recomendados |
| :--- | :--- | :--- |
| `--md-sys-shape-corner-none` | `0px` | Divisores, réguas |
| `--md-sys-shape-corner-xs` | `4px` | Badges pequenos, tooltips, tags de código |
| `--md-sys-shape-corner-sm` | `8px` | Inputs de formulário, selects, textareas |
| `--md-sys-shape-corner-md` | `12px` | Cards, painéis, blocos de código |
| `--md-sys-shape-corner-lg` | `16px` | Modais, caixas de diálogo |
| `--md-sys-shape-corner-xl` | `28px` | Banners flutuantes, gavetas laterais (Drawers) |
| `--md-sys-shape-corner-full` | `9999px` | Botões (*Filled*, *Tonal*), Abas *Pills*, Avatares |

---

## 4. Matriz de Casos de Uso de Superfícies

```
+-------------------------------------------------------------------+
|  Titlebar / Header  (--md-sys-color-surface-container-low)        |
+-------------------+-----------------------------------------------+
|                   |  App Background (--surface-container-lowest)  |
|  Sidebar / Nav    |                                               |
|  (--surface-      |   +---------------------------------------+   |
|   container-low)  |   |  Content Card (--surface-container)   |   |
|                   |   |                                       |   |
|  - Tab (Active):  |   |  [ Input ] (--surface-container-low)  |   |
|    primary-       |   |                                       |   |
|    container      |   |  ( Button Primary ) ( Button Tonal )  |   |
|                   |   +---------------------------------------+   |
|                   |                                               |
|                   |   +---------------------------------------+   |
|                   |   |  Modal (--surface-container-highest)  |   |
|                   |   +---------------------------------------+   |
+-------------------+-----------------------------------------------+
|  Status Bar (--md-sys-color-surface-container-low)                |
+-------------------------------------------------------------------+
```

---

## 5. Guia Passo a Passo de Migração de Componentes Legados

Ao refatorar telas e plugins antigos:

1. **Substituir Cores Literais por Variáveis M3:**
   - De: `background: #1e1e1e;` ➔ Para: `background: var(--md-sys-color-surface-container);`
   - De: `color: #ffffff;` ➔ Para: `color: var(--md-sys-color-on-surface);`
   - De: `border: 1px solid #333;` ➔ Para: `border: 1px solid var(--md-sys-color-outline-variant);`
2. **Atualizar Botões:**
   - Aplicar `border-radius: var(--md-sys-shape-corner-full);` para botões principais.
   - Usar `var(--md-sys-color-primary)` no fundo e `var(--md-sys-color-on-primary)` no texto.
3. **Validar com o Linter de UI:**
   ```powershell
   python scripts/lint_ui_tokens.py --dir <caminho-do-projeto>
   ```

---

## 6. Criação de Novos Projetos & Scaffolding

Para criar um novo projeto já configurado com M3:

```powershell
# Web React + Vite
python scripts/scaffold_project.py --type react-m3 --name meu-novo-plugin --output ../toolbox-plugins

# Data App Streamlit
python scripts/scaffold_project.py --type streamlit-m3 --name meu-data-app --output ../
```

---

## 7. Quality Gates e Automações

- **Stylelint:** Utilize `linters/stylelint.config.js` para impedir regressão de `#HEX`.
- **ESLint:** Utilize `linters/eslint.config.js` para impedir cores hardcoded em JSX/TSX.
- **Tokens Sync:** Execute `python scripts/sync_tokens.py` para atualizar os tokens em sincronia com o repositório principal `toolbox`.
