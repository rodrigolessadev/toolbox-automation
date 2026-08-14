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
   - Aplicar alterações respeitando os tokens de design do Toolbox e contratos do projeto.

3. **Validação Automatizada**:
   - No `toolbox`: `cargo test` + `npm run build`.
   - No `toolbox-plugins`: `pytest` + validação de contratos/schemas.

4. **Entrega & Pull Request**:
   - Commitar com referência `(Closes #N)`.
   - Fazer `git push` e abrir o Pull Request via `gh pr create`.

5. **Retorno Estruturado para o Plugin Release**:
   - Entregar sempre: Nova versão (SemVer), mensagem de commit, bloco de notas do release e link do PR.
