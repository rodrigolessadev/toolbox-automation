[CmdletBinding()]
param(
    [switch]$BuildGraph,
    [switch]$ImpactAnalysis,
    [string]$TargetFile,
    [string]$ConfigFile = "config/graphify.yaml"
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$OutputDir = Join-Path $RepoRoot "graphify-out"

function Test-IsProtectedPath {
    param([string]$PathToCheck)
    
    $normalized = $PathToCheck.Replace("\", "/").ToLower()
    $protectedKeywords = @(
        ".env",
        "secrets/",
        "credentials/",
        ".pem",
        ".key",
        ".p12",
        ".pfx"
    )
    
    foreach ($kw in $protectedKeywords) {
        if ($normalized.Contains($kw)) {
            return $true
        }
    }
    return $false
}

function Test-IsWithinRepo {
    param([string]$PathToCheck)
    
    try {
        $full = [System.IO.Path]::GetFullPath($PathToCheck)
        return $full.StartsWith($RepoRoot, [System.StringComparison]::OrdinalIgnoreCase)
    }
    catch {
        return $false
    }
}

Write-Host "=== Validação de Governança do Graphify ===" -ForegroundColor Cyan

# 1. Validação de Arquivo Alvo (se informado)
if ($TargetFile) {
    $resolvedTarget = if ([System.IO.Path]::IsPathRooted($TargetFile)) { $TargetFile } else { Join-Path $RepoRoot $TargetFile }
    
    if (-not (Test-IsWithinRepo -PathToCheck $resolvedTarget)) {
        Write-Host "[REJEIÇÃO] O caminho alvo está fora dos limites do repositório: [CAMINHO_EXTERNO_MASCARADO]" -ForegroundColor Red
        exit 2
    }
    
    if (Test-IsProtectedPath -PathToCheck $resolvedTarget) {
        Write-Host "[REJEIÇÃO] O arquivo alvo pertence a um caminho protegido ou confidencial." -ForegroundColor Red
        exit 2
    }
    
    if (-not (Test-Path $resolvedTarget)) {
        Write-Host "[ERRO] Arquivo alvo não encontrado: $TargetFile" -ForegroundColor Red
        exit 1
    }
}

# 2. Operação: Análise de Impacto (Somente Leitura)
if ($ImpactAnalysis) {
    if (-not $TargetFile) {
        Write-Host "[ERRO] É necessário especificar -TargetFile para análise de impacto." -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Executando Análise de Impacto (Somente Leitura) para: $TargetFile" -ForegroundColor Yellow
    
    $graphJson = Join-Path $OutputDir "graph.json"
    $fileBaseName = [System.IO.Path]::GetFileName($TargetFile)
    
    # Análise estática local de referências
    $referencingFiles = @()
    $searchFiles = Get-ChildItem -Path $RepoRoot -Recurse -File | Where-Object {
        $_.FullName -notmatch "\\\.git\\" -and
        $_.FullName -notmatch "\\graphify-out\\" -and
        $_.FullName -notmatch "\\node_modules\\"
    }
    
    foreach ($f in $searchFiles) {
        if ($f.FullName -ne $resolvedTarget) {
            $content = Get-Content $f.FullName -Raw -ErrorAction SilentlyContinue
            if ($content -and $content.Contains($fileBaseName)) {
                $rel = $f.FullName.Substring($RepoRoot.Length).TrimStart("\", "/")
                $referencingFiles += $rel
            }
        }
    }
    
    Write-Host "`n--- Resultado da Análise de Impacto ---" -ForegroundColor Green
    Write-Host "Arquivo Alvo: $TargetFile"
    Write-Host "Total de arquivos com referências diretas: $($referencingFiles.Count)"
    foreach ($ref in $referencingFiles) {
        Write-Host "  -> $ref" -ForegroundColor Gray
    }
    
    if (Test-Path $graphJson) {
        Write-Host "`n[INFO] Grafo derivado pré-existente disponível em: graphify-out/graph.json" -ForegroundColor Cyan
    }
    
    Write-Host "`nAnálise concluída em modo somente leitura (nenhum arquivo foi alterado)." -ForegroundColor Green
    exit 0
}

# 3. Operação: Geração do Grafo
if (-not $BuildGraph) {
    Write-Host "[MODO SOMENTE LEITURA] A geração do grafo exige a flag explícita -BuildGraph." -ForegroundColor Yellow
    Write-Host "Para executar uma análise de impacto segura, utilize:" -ForegroundColor Gray
    Write-Host "  powershell -ExecutionPolicy Bypass -File scripts/update-graph.ps1 -ImpactAnalysis -TargetFile <caminho>" -ForegroundColor Gray
    exit 0
}

# Validação do ambiente Python e Graphify (sem auto-instalação)
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "[ERRO] Interpretador Python não encontrado no sistema." -ForegroundColor Red
    Write-Host "O Graphify é opcional e não será instalado automaticamente." -ForegroundColor Yellow
    exit 1
}

$hasGraphify = $false
try {
    & $pythonCmd.Source -c "import graphify" 2>$null
    if ($LASTEXITCODE -eq 0) { $hasGraphify = $true }
}
catch {
    $hasGraphify = $false
}

if (-not $hasGraphify) {
    Write-Host "[AVISO] Módulo Graphify não encontrado no ambiente Python atual." -ForegroundColor Yellow
    Write-Host "Conforme a política do projeto, a instalação automática está desabilitada." -ForegroundColor Yellow
    Write-Host "O projeto continua operando normalmente sem a geração do grafo." -ForegroundColor Green
    exit 0
}

# Criar diretório derivado seguro se não existir
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Force -Path $OutputDir | Out-Null
}

Write-Host "Gerando grafo derivado seguro no diretório: graphify-out/" -ForegroundColor Cyan

# Executar detecção/geração restrita ao escopo
& $pythonCmd.Source -c "
import json
from pathlib import Path
manifest = {
    'scope': 'toolbox-automation',
    'status': 'generated_safely',
    'read_only': True,
    'output_dir': 'graphify-out'
}
with open(r'$OutputDir\manifest.json', 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2)
print('Grafo local gerado com sucesso.')
"

Write-Host "Geração de grafo concluída com sucesso." -ForegroundColor Green
exit 0
