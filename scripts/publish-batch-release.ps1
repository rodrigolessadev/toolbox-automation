[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("toolbox", "toolbox-plugins", "toolbox-release", "toolbox-automation")]
    [string]$Repo,

    [Parameter(Mandatory = $true)]
    [string]$Version,

    [string]$FromRef = "",
    [string]$ToRef = "HEAD",
    [string]$Issues = "",
    [string]$Label = "status: released",
    [switch]$NoNotify,
    [switch]$NoClose,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonScript = Join-Path $scriptDir "orchestrate_batch_release.py"

if (-not (Test-Path $pythonScript)) {
    Write-Host "[ERRO] Script orquestrador não encontrado em $pythonScript" -ForegroundColor Red
    exit 1
}

$pyArgs = @(
    $pythonScript,
    "--repo", $Repo,
    "--version", $Version,
    "--to-ref", $ToRef
)

if (-not [string]::IsNullOrWhiteSpace($FromRef)) {
    $pyArgs += @("--from-ref", $FromRef)
}

if (-not [string]::IsNullOrWhiteSpace($Issues)) {
    $pyArgs += @("--issues", $Issues)
}

if (-not [string]::IsNullOrWhiteSpace($Label)) {
    $pyArgs += @("--label", $Label)
}

if ($NoNotify) {
    $pyArgs += "--no-notify"
}

if ($NoClose) {
    $pyArgs += "--no-close"
}

if ($DryRun) {
    $pyArgs += "--dry-run"
}

Write-Host "Iniciando orquestração de batch release para o repositório $Repo (v$Version)..." -ForegroundColor Cyan
if ($DryRun) {
    Write-Host "Modo [DRY-RUN] ativado: nenhuma alteração será persistida no GitHub." -ForegroundColor Yellow
}

python @pyArgs
