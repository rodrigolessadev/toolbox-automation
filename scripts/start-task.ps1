[CmdletBinding()]
param(
    [string]$TaskId = "",
    [string]$Description = "Nova tarefa de automação",
    [string]$CheckpointsDir = ".agent/checkpoints"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "start_task.py"

$pyArgs = @($pythonScript, "--description", $Description, "--dir", $CheckpointsDir)
if ($TaskId) {
    $pyArgs += @("--task-id", $TaskId)
}

python @pyArgs
exit $LASTEXITCODE
