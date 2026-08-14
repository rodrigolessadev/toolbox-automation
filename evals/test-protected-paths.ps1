[CmdletBinding()]
param(
    [string]$ProtectedPathsPath = "config\protected-paths.yaml"
)

$ErrorActionPreference = "Stop"
$failures = 0

if (-not (Test-Path $ProtectedPathsPath)) {
    Write-Host "[FAIL] Lista de caminhos protegidos não encontrada" `
        -ForegroundColor Red
    exit 1
}

$content = Get-Content $ProtectedPathsPath -Raw

$requiredPatterns = @(
    "**/.env",
    "**/.env.*",
    "**/*.pem",
    "**/*.key",
    "**/secrets/**",
    "**/credentials/**"
)

foreach ($pattern in $requiredPatterns) {
    if ($content -match [regex]::Escape($pattern)) {
        Write-Host "[PASS] Caminho protegido: $pattern" -ForegroundColor Green
    }
    else {
        Write-Host "[FAIL] Caminho protegido ausente: $pattern" `
            -ForegroundColor Red
        $failures++
    }
}

$requiredRules = @(
    "read: blocked",
    "display: blocked",
    "copy: blocked",
    "commit: blocked",
    "external_upload: blocked"
)

foreach ($rule in $requiredRules) {
    if ($content -match [regex]::Escape($rule)) {
        Write-Host "[PASS] Regra encontrada: $rule" -ForegroundColor Green
    }
    else {
        Write-Host "[FAIL] Regra ausente: $rule" -ForegroundColor Red
        $failures++
    }
}

if ($failures -gt 0) {
    exit 1
}

Write-Host "Teste de caminhos protegidos concluído." -ForegroundColor Cyan
exit 0
