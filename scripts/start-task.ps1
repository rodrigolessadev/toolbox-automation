[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$TaskId = "TASK-$((Get-Date).ToString('yyyyMMdd-HHmmss'))",
    [Parameter(Mandatory = $false)]
    [string]$Description = "Nova tarefa de automação",
    [string]$CheckpointsDir = ".agent\checkpoints"
)

$ErrorActionPreference = "Stop"

Write-Host "Inicializando tarefa: $TaskId..." -ForegroundColor Cyan

if (-not (Test-Path $CheckpointsDir)) {
    New-Item -ItemType Directory -Path $CheckpointsDir -Force | Out-Null
}

$checkpointFile = Join-Path $CheckpointsDir "$TaskId.json"

$initialCheckpoint = @{
    task_id = $TaskId
    description = $Description
    status = "in_progress"
    created_at = (Get-Date).ToUniversalTime().ToString("o")
    current_phase = "analysis"
    blocked = $false
}

$initialCheckpoint | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $checkpointFile

Write-Host "Checkpoint inicial criado em: $checkpointFile" -ForegroundColor Green
Write-Host "Tarefa $TaskId iniciada com sucesso." -ForegroundColor Green
exit 0
