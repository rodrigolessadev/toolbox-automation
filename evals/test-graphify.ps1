[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Write-Host "Iniciando suite de testes: Governança e Isolamento do Graphify" -ForegroundColor Cyan

$passed = 0
$failed = 0

function Assert-Condition {
    param(
        [string]$TestName,
        [bool]$Condition,
        [string]$Details = ""
    )
    if ($Condition) {
        Write-Host "[PASS] $TestName" -ForegroundColor Green
        $script:passed++
    }
    else {
        Write-Host "[FAIL] $TestName - $Details" -ForegroundColor Red
        $script:failed++
    }
}

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

# 1. Configuração e arquivos base
Assert-Condition "Arquivo config/graphify.example.yaml existe" (Test-Path (Join-Path $repoRoot "config/graphify.example.yaml"))
Assert-Condition "Arquivo .graphifyignore existe" (Test-Path (Join-Path $repoRoot ".graphifyignore"))
Assert-Condition "Arquivo policies/graphify-policy.md existe" (Test-Path (Join-Path $repoRoot "policies/graphify-policy.md"))
Assert-Condition "Script scripts/update-graph.ps1 existe" (Test-Path (Join-Path $repoRoot "scripts/update-graph.ps1"))

# 2. Configuração desativada por padrão
$configContent = Get-Content (Join-Path $repoRoot "config/graphify.example.yaml") -Raw
Assert-Condition "Graphify desativado por padrão no example.yaml" ($configContent -match "enabled:\s*false")
Assert-Condition "Modo somente leitura ativado no example.yaml" ($configContent -match "read_only:\s*true")
Assert-Condition "Backend externo desativado no example.yaml" ($configContent -match "external_backend:\s*false")

# 3. Execução padrão sem -BuildGraph é somente leitura (exit code 0)
$outReadonly = & powershell -ExecutionPolicy Bypass -File (Join-Path $repoRoot "scripts/update-graph.ps1") 2>&1
Assert-Condition "Execução sem -BuildGraph é somente leitura" ($LASTEXITCODE -eq 0)

# 4. Rejeição de caminho protegido (.env / secrets)
$outProtected = & powershell -ExecutionPolicy Bypass -File (Join-Path $repoRoot "scripts/update-graph.ps1") -ImpactAnalysis -TargetFile ".env" 2>&1
Assert-Condition "Rejeição estrita de caminho protegido (.env)" ($LASTEXITCODE -eq 2 -or $outProtected -match "REJEIÇÃO")

# 5. Rejeição de caminho fora do repositório
$outExternal = & powershell -ExecutionPolicy Bypass -File (Join-Path $repoRoot "scripts/update-graph.ps1") -ImpactAnalysis -TargetFile "C:\Windows\System32\drivers\etc\hosts" 2>&1
Assert-Condition "Rejeição de caminho fora do repositório" ($LASTEXITCODE -eq 2 -or $outExternal -match "REJEIÇÃO")

# 6. Análise de impacto funciona em modo somente leitura
$outImpact = & powershell -ExecutionPolicy Bypass -File (Join-Path $repoRoot "scripts/update-graph.ps1") -ImpactAnalysis -TargetFile "scripts/load-context.ps1" 2>&1
Assert-Condition "Análise de impacto conclui com sucesso" ($LASTEXITCODE -eq 0)

# 7. load-context.ps1 com -WithGraph é tolerante e funciona normalmente
$outContext = & powershell -ExecutionPolicy Bypass -File (Join-Path $repoRoot "scripts/load-context.ps1") -WithGraph 2>&1
Assert-Condition "load-context com -WithGraph executa sem falhas" ($LASTEXITCODE -eq 0)

Write-Host "`nResultados dos Testes do Graphify: $passed PASS, $failed FAIL" -ForegroundColor Cyan

if ($failed -gt 0) {
    exit 1
}
exit 0
