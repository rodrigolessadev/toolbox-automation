[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TaskId,
    [string]$CheckpointsDir = ".agent/checkpoints"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "resume_task.py"

python $pythonScript $TaskId --dir $CheckpointsDir
exit $LASTEXITCODE
