[CmdletBinding()]
param(
    [string]$AgentDir = ".agent",
    [switch]$WithGraph
)

$ErrorActionPreference = "Stop"

Write-Host "Carregando contexto persistente da automação..." -ForegroundColor Cyan

if (-not (Test-Path $AgentDir)) {
    Write-Host "[ERRO] Diretório de contexto $AgentDir não encontrado." -ForegroundColor Red
    exit 1
}

$requiredContextFiles = @(
    "project-context.md",
    "architecture-overview.md",
    "decisions.md",
    "handoff.md",
    "work-log.md"
)

$missingFiles = 0

foreach ($file in $requiredContextFiles) {
    $filePath = Join-Path $AgentDir $file
    if (-not (Test-Path $filePath)) {
        Write-Host "[FALHA] Arquivo de contexto ausente: $file" -ForegroundColor Red
        $missingFiles++
    }
    else {
        Write-Host "[OK] Contexto carregado: $file" -ForegroundColor Green
    }
}

if ($missingFiles -gt 0) {
    Write-Host "Contexto persistente incompleto." -ForegroundColor Red
    exit 1
}

# Integração opcional com Graphify (somente leitura e não bloqueante)
if ($WithGraph) {
    $graphPath = "graphify-out/graph.json"
    if (Test-Path $graphPath) {
        Write-Host "[GRAPHIFY] Grafo estrutural detectado e carregado em modo somente leitura." -ForegroundColor Cyan
    }
    else {
        Write-Host "[GRAPHIFY] Grafo derivado não encontrado (operação continua normalmente)." -ForegroundColor Yellow
    }
}

Write-Host "Contexto carregado com sucesso." -ForegroundColor Green
exit 0
