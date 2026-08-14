[CmdletBinding()]
param(
    [string]$PolicyDirectory = "policies"
)

$ErrorActionPreference = "Stop"
$failures = 0

$requiredPolicies = @(
    "README.md",
    "permission-levels.md",
    "approval-policy.md",
    "blocked-actions.md",
    "file-access-policy.md",
    "external-actions-policy.md"
)

foreach ($policy in $requiredPolicies) {
    $path = Join-Path $PolicyDirectory $policy

    if (-not (Test-Path $path)) {
        Write-Host "[FAIL] Política ausente: $policy" -ForegroundColor Red
        $failures++
    }
    else {
        Write-Host "[PASS] Política encontrada: $policy" -ForegroundColor Green
    }
}

$requiredTerms = @{
    "permission-levels.md" = @("Nível 1", "Nível 2", "Nível 3", "Nível 4")
    "approval-policy.md" = @("git push", "pull request", "aprovação")
    "blocked-actions.md" = @("git reset --hard", "git clean -fd")
    "file-access-policy.md" = @(".env", "segredos", "credenciais")
    "external-actions-policy.md" = @("deploy", "release", "rollback")
}

foreach ($file in $requiredTerms.Keys) {
    $path = Join-Path $PolicyDirectory $file

    if (-not (Test-Path $path)) {
        continue
    }

    $content = Get-Content $path -Raw

    foreach ($term in $requiredTerms[$file]) {
        if ($content -match [regex]::Escape($term)) {
            Write-Host "[PASS] $file contém: $term" -ForegroundColor Green
        }
        else {
            Write-Host "[FAIL] $file não contém: $term" -ForegroundColor Red
            $failures++
        }
    }
}

if ($failures -gt 0) {
    exit 1
}

Write-Host "Teste das políticas concluído." -ForegroundColor Cyan
exit 0
