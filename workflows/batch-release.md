# Workflow: Publicação em Lote (Batch Release) e Notificação de Issues

## Identificação

- Nome: `batch-release`
- Finalidade: orquestrar o ciclo de entrega de múltiplos desenvolvimentos acumulados, gerar changelog unificado, calcular SemVer cumulativo e realizar o fechamento e notificação em massa das issues participantes.
- Repositórios aplicáveis: `toolbox`, `toolbox-plugins`, `toolbox-release`, `toolbox-automation`

---

## Quando Utilizar

Utilizar este workflow quando:
- Múltiplas branches de features e correções foram mescladas em uma branch de release ou na `main`;
- Uma sprint ou ciclo de entrega acumulou várias issues resolvidas que devem ser disponibilizadas em uma versão única;
- Houver necessidade de rastreabilidade formal notificando os autores e issues participantes com a tag de versão oficial.

---

## Agentes Envolvidos

1. **Orquestrador**: Coordena a inspeção de commits e validação de requisitos;
2. **Testador / Quality Gate**: Executa as suítes de testes automatizados e linters;
3. **Gerente de Release**: Prepara as notas consolidadas e dispara a publicação;
4. **Notificador**: Adiciona comentários de rastreabilidade e atualiza status no GitHub.

---

## Fases do Fluxo

### Fase 1 — Análise do Intervalo Git e Extração de Issues
1. Identificar a tag base anterior (`get_latest_tag` ou flag `--from-ref`);
2. Inspecionar o histórico até `HEAD` (`git log <last_tag>..HEAD`);
3. Mapear todas as issues mencionadas nos commits (`#123`, `Closes #123`);
4. Identificar autores e contribuidores únicos do pacote.

### Fase 2 — Cálculo Semântico de Versão (SemVer)
1. Avaliar impacto cumulativo:
   - Se houver `BREAKING CHANGE:` ou `!:` $\rightarrow$ **MAJOR**;
   - Se houver `feat:` $\rightarrow$ **MINOR**;
   - Se houver apenas `fix:` e tarefas internas $\rightarrow$ **PATCH**.

### Fase 3 — Validação Pré-Release (Quality Gate)
1. Executar a suíte de testes (`pytest`);
2. Verificar linter e integridade de documentação;
3. Assegurar que nenhuma alteração pendente (dirty workspace) esteja corrompida.

### Fase 4 — Publicação e Notificação em Massa
1. Gerar o changelog consolidado estruturado por categorias;
2. Comitar e publicar a release no GitHub (via `toolbox-release`);
3. Para cada issue mapeada:
   - Adicionar comentário padronizado: `🚀 Esta alteração foi incluída e publicada oficialmente na versão **vX.Y.Z** do repositório <repo>.`
   - Adicionar label `status: released`;
   - Fechar a issue com motivo `completed`.

---

## Comandos de Execução

```powershell
# Simulação prévia (Dry-Run)
.\scripts\publish-batch-release.ps1 -Repo "toolbox" -Version "1.18.0" -DryRun

# Execução oficial
.\scripts\publish-batch-release.ps1 -Repo "toolbox" -Version "1.18.0"
```
