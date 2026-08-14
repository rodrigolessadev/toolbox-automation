# Sugestões de Prompts para Disparo de Tarefas — Toolbox Automation

Este guia contém os formatos e modelos de prompts sugeridos para acionar o **Toolbox Automation** a partir de uma issue ou demanda de projeto.

---

## ⚡ 1. Formatos Rápidos (Recomendados)

Você não precisa digitar instruções longas. O assistente reconhece nativamente estes atalhos:

### Para o repositório `toolbox` (Aplicação Desktop):
```text
toolbox #10
```
ou
```text
Implementar issue #10 do toolbox
```

---

### Para o repositório `toolbox-plugins` (Marketplace e Plugins):
```text
plugins #4
```
ou
```text
toolbox-plugins #4
```
ou
```text
Implementar issue #4 de toolbox-plugins
```

---

## 🎯 2. Formatos com Contexto ou Restrições Adicionais

Quando você quiser direcionar o foco da implementação:

### Para o `toolbox`:
```text
toolbox #10: focar na camada de proteção do backend Rust e testes unitários.
```
```text
toolbox #1: aplicar tema Dark e High-Contrast de acordo com os tokens do design system.
```

### Para o `toolbox-plugins`:
```text
plugins #4: atualizar o plugin.json, testes de domínio puro e o catalog.json.
```
```text
plugins #2: criar novo plugin com suporte ao protocolo IPC v1.0.
```

---

## 🛠️ 3. Consultar Issues Abertas via Terminal

Você pode listar as issues abertas dos repositórios e obter os prompts gerados automaticamente executando:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/get-issues.ps1
```

O script listará as issues ativas no GitHub/Kanban e gerará os prompts prontos para copiar e colar na conversa.
