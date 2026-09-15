[CmdletBinding()]
param(
    [string]$ConfigPath = ""
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "check_projects.py"

python $pythonScript
exit $LASTEXITCODE
