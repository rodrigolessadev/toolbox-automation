[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TaskId,
    [string]$CheckpointsDir = ".agent\checkpoints"
)

$ErrorActionPreference = "Stop"

Write-Host "Verificando retomada da tarefa: $TaskId..." -ForegroundColor Cyan

$checkpointFile = Join-Path $CheckpointsDir "$TaskId.json"

if (-not (Test-Path $checkpointFile)) {
    Write-Host "[ERRO] Checkpoint da tarefa não encontrado: $checkpointFile" -ForegroundColor Red
    exit 1
}

$checkpointJson = Get-Content $checkpointFile -Raw | ConvertFrom-Json

Write-Host "Tarefa encontrada." -ForegroundColor Green
Write-Host "Status atual: $($checkpointJson.status)" -ForegroundColor Cyan
Write-Host "Fase atual: $($checkpointJson.current_phase)" -ForegroundColor Cyan

if ($checkpointJson.blocked -eq $true) {
    Write-Host "[AVISO] Esta tarefa possui bloqueios registrados. Requer análise prévia." -ForegroundColor Yellow
}

Write-Host "Tarefa $TaskId pronta para retomada segura." -ForegroundColor Green
exit 0
