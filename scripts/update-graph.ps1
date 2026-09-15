[CmdletBinding()]
param(
    [switch]$BuildGraph,
    [switch]$ImpactAnalysis,
    [string]$TargetFile
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "update_graph.py"

$pyArgs = @($pythonScript)
if ($BuildGraph) {
    $pyArgs += "--build-graph"
}
if ($ImpactAnalysis) {
    $pyArgs += "--impact-analysis"
}
if ($TargetFile) {
    $pyArgs += @("--target-file", $TargetFile)
}

python @pyArgs
exit $LASTEXITCODE
