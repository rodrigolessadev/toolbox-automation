[CmdletBinding()]
param(
    [ValidateSet("toolbox", "toolbox-plugins", "toolbox-automation", "toolbox-release", "all")]
    [string]$Project = "all"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "get_issues.py"

python $pythonScript --project $Project
exit $LASTEXITCODE
