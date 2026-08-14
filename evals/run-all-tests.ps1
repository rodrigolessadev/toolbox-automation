[CmdletBinding()]
param(
    [string]$ProjectRoot = (Get-Location).Path,
    [string]$ReportPath = "reports\platform-test-report.txt"
)

$ErrorActionPreference = "Stop"

$tests = @(
    "evals\test-config.ps1",
    "evals\test-schemas.ps1",
    "evals\test-policies.ps1",
    "evals\test-workflows.ps1",
    "evals\test-scripts.ps1",
    "evals\test-protected-paths.ps1"
)

$reportDirectory = Split-Path $ReportPath -Parent

if (-not [string]::IsNullOrWhiteSpace($reportDirectory)) {
    New-Item -ItemType Directory -Path $reportDirectory -Force | Out-Null
}

$lines = @()
$overallPassed = $true

$lines += "Relatório de validação da Toolbox Automation Platform"
$lines += "Data: $((Get-Date).ToUniversalTime().ToString('o'))"
$lines += ""

foreach ($test in $tests) {
    $testPath = Join-Path $ProjectRoot $test

    if (-not (Test-Path $testPath)) {
        $lines += "[FAIL] Teste ausente: $test"
        $overallPassed = $false
        continue
    }

    Write-Host ""
    Write-Host "Executando $test" -ForegroundColor Cyan

    & $testPath
    $exitCode = $LASTEXITCODE

    if ($exitCode -eq 0) {
        $lines += "[PASS] $test"
    }
    else {
        $lines += "[FAIL] $test - código $exitCode"
        $overallPassed = $false
    }
}

$lines | Set-Content -Encoding UTF8 $ReportPath

Write-Host ""
Write-Host "Relatório salvo em: $ReportPath" -ForegroundColor Cyan

if (-not $overallPassed) {
    Write-Host "A validação encontrou falhas." -ForegroundColor Red
    exit 1
}

Write-Host "Todos os testes obrigatórios passaram." -ForegroundColor Green
exit 0
