[CmdletBinding()]
param(
    [string]$WorkflowDirectory = "workflows"
)

$ErrorActionPreference = "Stop"
$failures = 0

$requiredWorkflows = @(
    "README.md",
    "resume-task.md",
    "new-feature.md",
    "plugin-lifecycle.md",
    "bug-fix.md",
    "preventive-maintenance.md"
)

foreach ($workflow in $requiredWorkflows) {
    $path = Join-Path $WorkflowDirectory $workflow

    if (-not (Test-Path $path)) {
        Write-Host "[FAIL] Workflow ausente: $workflow" -ForegroundColor Red
        $failures++
        continue
    }

    Write-Host "[PASS] Workflow encontrado: $workflow" -ForegroundColor Green

    $content = Get-Content $path -Raw

    if ($workflow -eq "README.md") {
        continue
    }

    $requiredSections = @(
        "Identificação",
        "Agentes envolvidos",
        "Fases",
        "Deve bloquear quando",
        "Estratégia de rollback"
    )

    foreach ($section in $requiredSections) {
        if ($content -match [regex]::Escape($section)) {
            Write-Host "[PASS] $workflow contém: $section" -ForegroundColor Green
        }
        else {
            Write-Host "[FAIL] $workflow não contém: $section" -ForegroundColor Red
            $failures++
        }
    }
}

if ($failures -gt 0) {
    exit 1
}

Write-Host "Teste dos workflows concluído." -ForegroundColor Cyan
exit 0
