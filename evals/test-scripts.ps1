[CmdletBinding()]
param(
    [string]$ScriptsDirectory = "scripts"
)

$ErrorActionPreference = "Stop"
$failures = 0

$requiredScripts = @(
    "check-projects.ps1",
    "load-context.ps1",
    "start-task.ps1",
    "resume-task.ps1"
)

foreach ($scriptName in $requiredScripts) {
    $path = Join-Path $ScriptsDirectory $scriptName

    if (-not (Test-Path $path)) {
        Write-Host "[FAIL] Procedimento ausente: $scriptName" -ForegroundColor Red
        $failures++
        continue
    }

    $content = Get-Content $path -Raw

    if ($content -match "\$ErrorActionPreference") {
        Write-Host "[PASS] $scriptName define tratamento de erros" `
            -ForegroundColor Green
    }
    else {
        Write-Host "[WARN] $scriptName não define tratamento explícito de erros" `
            -ForegroundColor Yellow
    }

    if ($content -match "(?i)reset --hard|clean -fd|push --force|Remove-Item -Recurse") {
        Write-Host "[FAIL] $scriptName contém comando potencialmente destrutivo" `
            -ForegroundColor Red
        $failures++
    }
    else {
        Write-Host "[PASS] $scriptName não contém comando destrutivo conhecido" `
            -ForegroundColor Green
    }
}

if ($failures -gt 0) {
    exit 1
}

Write-Host "Teste dos procedimentos concluído." -ForegroundColor Cyan
exit 0
