[CmdletBinding()]
param(
    [string]$SchemaDirectory = "schemas"
)

$ErrorActionPreference = "Stop"
$failures = 0

$requiredSchemas = @(
    "task-request.schema.json",
    "analysis-result.schema.json",
    "implementation-plan.schema.json",
    "implementation-result.schema.json",
    "validation-result.schema.json",
    "review-result.schema.json",
    "checkpoint.schema.json",
    "workflow-result.schema.json"
)

foreach ($schema in $requiredSchemas) {
    $path = Join-Path $SchemaDirectory $schema

    if (-not (Test-Path $path)) {
        Write-Host "[FAIL] Schema ausente: $schema" -ForegroundColor Red
        $failures++
        continue
    }

    try {
        $content = Get-Content $path -Raw
        $json = $content | ConvertFrom-Json

        if ($null -eq $json.'$schema') {
            Write-Host "[FAIL] $schema não possui campo `$schema" -ForegroundColor Red
            $failures++
            continue
        }

        if ($json.type -ne "object") {
            Write-Host "[FAIL] $schema não define type object" -ForegroundColor Red
            $failures++
            continue
        }

        Write-Host "[PASS] Schema válido: $schema" -ForegroundColor Green
    }
    catch {
        Write-Host "[FAIL] JSON inválido: $schema" -ForegroundColor Red
        Write-Host $_.Exception.Message
        $failures++
    }
}

if ($failures -gt 0) {
    exit 1
}

Write-Host "Teste dos schemas concluído." -ForegroundColor Cyan
exit 0
