[CmdletBinding()]
param(
    [string]$AgentDir = ".agent",
    [switch]$WithGraph
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "load_context.py"

$pyArgs = @($pythonScript, "--dir", $AgentDir)
if ($WithGraph) {
    $pyArgs += "--with-graph"
}

python @pyArgs
exit $LASTEXITCODE
