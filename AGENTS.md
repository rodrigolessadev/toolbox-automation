# Antigravity Rules — Toolbox Automation

Este arquivo orienta o assistente de IA na interpretação e execução das instruções de trabalho do ecossistema Toolbox.

---

## ⚡ Gatilhos Rápidos de Disparo de Issues

Sempre que o usuário enviar mensagens nos formatos simplificados abaixo, interprete-as imediatamente como uma instrução formal de implementação de issue:

### Padrões Reconhecidos:
1. **`toolbox #N`** ou **`toolbox #<numero>`**:
   - **Projeto**: `toolbox` (`C:\tools\toolbox-ecosystem\toolbox`, repositório `rodrigolessadev/toolbox`).
   - **Ação**: Buscar detalhes da issue `#N` via GitHub CLI (`gh issue view N -R rodrigolessadev/toolbox`), criar plano de implementação, aguardar aprovação e executar o ciclo de vida completo.

2. **`plugins #N`** ou **`toolbox-plugins #N`**:
   - **Projeto**: `toolbox-plugins` (`C:\tools\toolbox-ecosystem\toolbox-plugins`, repositório `rodrigolessadev/toolbox-plugins`).
   - **Ação**: Buscar detalhes da issue `#N` via GitHub CLI (`gh issue view N -R rodrigolessadev/toolbox-plugins`), criar plano de implementação, aguardar aprovação e executar o ciclo de vida completo.

3. **`release #N`** ou **`toolbox-release #N`**:
   - **Projeto**: `toolbox-release` (`C:\tools\toolbox-ecosystem\toolbox-release`, repositório `rodrigolessadev/toolbox-release`).
   - **Ação**: Buscar detalhes da issue `#N` via GitHub CLI (`gh issue view N -R rodrigolessadev/toolbox-release`), criar plano de implementação, aguardar aprovação e executar o ciclo de vida completo.

---

## 🔄 Fluxo Obrigatório de Execução

1. **Diagnóstico & Planejamento**:
   - Inspecionar a issue no GitHub no respectivo repositório.
   - Analisar o código relevante no repositório correspondente.
   - Gerar `implementation_plan.md` e aguardar aprovação do usuário.

2. **Branch & Implementação**:
   - Criar branch `feature/...` ou `fix/...` ou `refactor/...` ou `chore/...`.
   - Aplicar alterações respeitando os tokens de design do Toolbox, contraste visual rigoroso e contratos do projeto.

3. **Validação Automatizada**:
   - No `toolbox`: `cargo test` + `npm run build`.
   - No `toolbox-plugins`: `pytest` + validação de contratos/schemas.
   - No `toolbox-release`: `pytest`.

4. **Entrega & Pull Request**:
   - Commitar na branch de feature com referência `(Closes #N)`.
   - Fazer `git push` e abrir o Pull Request via `gh pr create`.

5. **Geração Obrigatória de Dados de Publicação (Release Notes & Nova Versão)**:
   - **SEMPRE** que finalizar a implementação e abrir a PR, gerar e apresentar obrigatoriamente:
     1. **Nova Versão SemVer** do componente (Toolbox ou Plugin), devidamente calculada (Major/Minor/Patch).
     2. **Notas da Versão (Release Notes)** completas em formato Markdown prontas para publicação (destacando novas funcionalidades, melhorias de UX, correções e estabilidade).
     3. **Link da Pull Request** aberta.
     4. **Próximos passos objetivos** para o usuário realizar o merge e acionar a publicação.

---

## 🏷️ Taxonomia Oficial de Issues

Ao criar ou categorizar issues nos repositórios do ecossistema, utilizar os 4 tipos oficiais:
- 🚀 **Feature** (`tipo: feature`): Novas funcionalidades, novos plugins ou novas ferramentas.
- 🐛 **Bug** (`tipo: bug`): Correções de erros, bugs ou comportamentos inesperados.
- ♻️ **Refactor** (`tipo: refactor`): Melhorias de código, reestruturações visuais ou migrações de arquitetura.
- ⚙️ **Infra** (`tipo: infra`): Workflows de CI/CD, automações de build/release, documentação interna.

---

## 🌐 Arquitetura Frontend dos Plugins: `pywebview`

Todos os plugins com interface gráfica adotam a arquitetura **`pywebview`** (HTML5/CSS3/JavaScript no frontend + Python 3 no backend).

### ⚠️ Regras Cruciais de Design & Autossuficiência (Anti-Regression):
1. **Autossuficiência Total de Assets Web (Regra de Ouro)**:
   - **NUNCA** referenciar arquivos CSS/JS com caminhos relativos externos como `../../shared/...` no HTML. Quando o plugin é instalado no `%LOCALAPPDATA%` do usuário ou distribuído em `.zip`, caminhos relativos fora da pasta do plugin falham silenciosamente (HTTP 404), quebrando todo o layout.
   - Toda pasta `ui/` do plugin deve conter seus próprios arquivos ou importar localmente:
     - `ui/toolbox-theme.css` (design tokens e reset do Toolbox)
     - `ui/style.css` (estilos dedicados do plugin)
     - `ui/icons.js` (ícones vetoriais SVG)
     - `ui/app.js` (lógica JS e bridge)
     - `ui/index.html` (estrutura semântica)

2. **Garantia Estrita de Contraste (Fim do Texto Escuro no Fundo Escuro)**:
   - Toda página DEVE aplicar explicitamente no `html, body` e nos elementos interativos:
     ```css
     html, body {
       background-color: #0e1014;
       color: #e8eaed;
       font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
     }
     input, select, textarea {
       background-color: #12151c !important;
       color: #e8eaed !important;
       border: 1px solid #262c36 !important;
     }
     input::placeholder, textarea::placeholder {
       color: #5a6270 !important;
     }
     ```
   - Nunca depender de herança do navegador para cores de `input`, `select` ou `button`.

3. **Redesenho de Alto Padrão (Não apenas trocar framework)**:
   - A migração deve trazer **evolução real de UX**: cards com hierarquia clara, cantos arredondados (`radius: 10px`), headers com badges de status, botões primários com destaque (`#6aa3ff`), botões secundários sutis (`#1f242d`), transições suaves e feedback visual rico.

### 📁 Estrutura Padrão de um Plugin `pywebview`:
```text
plugins/<plugin_id>/
  ├── plugin.json          (Manifesto com entry="main.py", icon, versão)
  ├── domain.py            (Regras de negócio puras e testáveis em Python)
  ├── main.py              (Inicializador pywebview + classe Api bridge)
  ├── ui/                  (Interface Web 100% Autossuficiente)
  │   ├── index.html       (HTML5 semântico com referências locais)
  │   ├── toolbox-theme.css(Design tokens e componentes do Toolbox)
  │   ├── style.css        (Estilos refinados específicos do plugin)
  │   ├── icons.js         (SVGs vetoriais estilo Lucide)
  │   └── app.js           (Lógica da UI e chamadas await window.pywebview.api.<metodo>())
  └── tests/
      ├── test_domain.py   (Testes unitários de regras de negócio)
      ├── test_manifest.py (Validação de manifesto e integridade)
      └── test_isolated_run.py (Validação de execução isolada com assets)
```

---

## 🎨 Design Tokens Oficiais do Toolbox

Os plugins devem usar rigorosamente os tokens oficiais extraídos de `src/styles/global.css`:

```css
:root {
  /* Superfícies Dark Mode */
  --bg:           #0e1014;   /* Fundo principal da janela */
  --bg-elev-1:    #161a21;   /* Cards e painéis principais */
  --bg-elev-2:    #1f242d;   /* Containers internos e headers */
  --bg-elev-3:    #262c36;   /* Efeito hover de cards e botões secundários */
  --bg-elev-4:    #2d3440;   /* Hover ativo */
  
  /* Inputs */
  --input-bg:     #12151c;   /* Fundo de campos de texto */
  --input-border: #262c36;   /* Borda de campos */
  --border:       #262c36;   /* Bordas de cards */
  --border-focus: #6aa3ff;   /* Foco em inputs */

  /* Tipografia */
  --fg:           #e8eaed;   /* Texto principal (alto contraste) */
  --fg-muted:     #8b94a3;   /* Texto secundário e labels */
  --fg-disabled:  #5a6270;   /* Placeholders e desabilitados */

  /* Destaques & Acentos */
  --accent:       #6aa3ff;   /* Botões primários e seleções */
  --accent-hover: #7bb3ff;   /* Hover primário */
  --accent-active:#5a93ef;   /* Clique primário */
  --accent-soft:  rgba(106, 163, 255, 0.16); /* Badges e fundos sutis */

  /* Status */
  --success:      #4cc38a;   /* Sucesso */
  --success-soft: rgba(76, 195, 138, 0.18);
  --warning:      #f5a524;   /* Alertas */
  --danger:       #ff6369;   /* Erros */
  --danger-soft:  rgba(255, 99, 105, 0.18);

  /* Geometria */
  --radius:       10px;
  --radius-sm:    6px;
  --radius-lg:    14px;
}
```
