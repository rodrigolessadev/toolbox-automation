[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("toolbox", "toolbox-plugins", "toolbox-automation", "toolbox-release")]
    [string]$Repo,

    [Parameter(Mandatory = $true)]
    [int]$IssueNumber
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "init_task.py"

python $pythonScript --repo $Repo --issue $IssueNumber
exit $LASTEXITCODE
