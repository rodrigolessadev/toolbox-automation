# Guia Oficial de Design Tokens e Anatomia UI (Material Design 3)

Este documento contém a especificação canônica de estilos, tokens CSS e convenções de interface para os plugins e ferramentas do **Toolbox Ecosystem**.

---

## 1. Regra de Ouro: Autossuficiência de Assets Web

Todos os plugins com interface gráfica adotam a arquitetura **`pywebview`** (HTML5/CSS3/JavaScript no frontend + Python 3 no backend).

> [!IMPORTANT]
> **Proibição de Caminhos Relativos Externos (`../../shared/...`):**
> Quando o plugin é instalado no `%LOCALAPPDATA%` do usuário ou distribuído em arquivo `.zip`, caminhos relativos para fora do diretório do plugin falham silenciosamente (HTTP 404), quebrando o layout.
> 
> Toda pasta `ui/` do plugin deve conter seus próprios arquivos autossuficientes:
> - `ui/toolbox-theme.css` (tokens de design e reset padrão)
> - `ui/style.css` (estilos dedicados da ferramenta)
> - `ui/icons.js` (biblioteca local de SVGs Lucide)
> - `ui/app.js` (gerenciamento de estado e chamadas `await window.pywebview.api.<metodo>()`)
> - `ui/index.html` (estrutura semântica)

---

## 2. Garantia Estrita de Contraste e Reset Base

Toda interface Web dos plugins DEVE aplicar explicitamente no reset:

```css
html, body {
  background-color: #0e1014;
  color: #e8eaed;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

input, select, textarea {
  background-color: #12151c !important;
  color: #e8eaed !important;
  border: 1px solid #262c36 !important;
  border-radius: 6px;
  padding: 8px 12px;
  font-size: 14px;
}

input:focus, select:focus, textarea:focus {
  border-color: #6aa3ff !important;
  outline: none;
  box-shadow: 0 0 0 2px rgba(106, 163, 255, 0.2);
}

input::placeholder, textarea::placeholder {
  color: #5a6270 !important;
}

button {
  font-family: inherit;
  cursor: pointer;
  border-radius: 6px;
  transition: background-color 0.2s ease, transform 0.1s ease;
}
```

---

## 3. Tokens CSS Oficiais do Toolbox (`toolbox-theme.css`)

Os plugins devem utilizar rigorosamente as variáveis CSS padronizadas:

```css
:root {
  /* Superfícies Dark Mode */
  --bg:           #0e1014;   /* Fundo principal da janela */
  --bg-elev-1:    #161a21;   /* Cards e painéis principais */
  --bg-elev-2:    #1f242d;   /* Containers internos e headers */
  --bg-elev-3:    #262c36;   /* Hover de cards e botões secundários */
  --bg-elev-4:    #2d3440;   /* Hover ativo e estados pressionados */
  
  /* Inputs e Campos */
  --input-bg:     #12151c;   /* Fundo de campos de texto */
  --input-border: #262c36;   /* Borda neutra de campos */
  --border:       #262c36;   /* Bordas de cards e divisores */
  --border-focus: #6aa3ff;   /* Destaque ao focar input */

  /* Tipografia & Hierarquia */
  --fg:           #e8eaed;   /* Texto principal (alto contraste) */
  --fg-muted:     #8b94a3;   /* Texto secundário e rótulos */
  --fg-disabled:  #5a6270;   /* Placeholders e elementos desabilitados */

  /* Destaques & Acentos (Brand Accent) */
  --accent:       #6aa3ff;   /* Botões primários e seleções ativas */
  --accent-hover: #7bb3ff;   /* Hover de botão primário */
  --accent-active:#5a93ef;   /* Clique/pressionamento primário */
  --accent-soft:  rgba(106, 163, 255, 0.16); /* Badges e seleções suaves */

  /* Cores de Status Semânticas */
  --success:      #4cc38a;   /* Sucesso e confirmações */
  --success-soft: rgba(76, 195, 138, 0.18);
  --warning:      #f5a524;   /* Alertas e atenção */
  --warning-soft: rgba(245, 165, 36, 0.18);
  --danger:       #ff6369;   /* Erros e ações destrutivas */
  --danger-soft:  rgba(255, 99, 105, 0.18);

  /* Geometria & Bordas */
  --radius:       10px;      /* Cards padrão */
  --radius-sm:    6px;       /* Botões, tags e inputs */
  --radius-lg:    14px;      /* Modais e containers flutuantes */
}
```

---

## 4. Estrutura Canônica de Pastas de Plugins

```text
plugins/<plugin_id>/
  ├── plugin.json          # Manifesto oficial (entry, id, version, icon)
  ├── package.json         # Dependências locais de UI (se houver)
  ├── domain.py            # Regras de negócio puras e testáveis em Python
  ├── main.py              # Inicializador pywebview + classe Api bridge
  ├── ui/                  # Interface Web 100% Autossuficiente
  │   ├── index.html       # HTML5 semântico com imports locais
  │   ├── toolbox-theme.css# Tokens de design e componentes compartilhados
  │   ├── style.css        # Estilos refinados específicos do plugin
  │   ├── icons.js         # Biblioteca local de SVGs Lucide
  │   └── app.js           # Lógica da interface e chamadas assíncronas à API
  └── tests/
      ├── test_domain.py   # Testes unitários de regras de negócio
      └── test_manifest.py # Validação de integridade do manifesto
```
