[CmdletBinding()]
param(
    [string]$ConfigPath = "config\local-projects.example.yaml"
)

$ErrorActionPreference = "Stop"
$script:Failures = 0
$script:Warnings = 0

function Write-Pass {
    param([string]$Message)
    Write-Host "[PASS] $Message" -ForegroundColor Green
}

function Write-Fail {
    param([string]$Message)
    Write-Host "[FAIL] $Message" -ForegroundColor Red
    $script:Failures++
}

function Write-Warn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
    $script:Warnings++
}

if (-not (Test-Path $ConfigPath)) {
    Write-Fail "Configuração de exemplo não encontrada: $ConfigPath"
    exit 1
}

$configText = Get-Content $ConfigPath -Raw

$requiredProjects = @(
    "toolbox-automation",
    "toolbox",
    "toolbox-plugins"
)

foreach ($project in $requiredProjects) {
    if ($configText -match [regex]::Escape($project)) {
        Write-Pass "Projeto configurado: $project"
    }
    else {
        Write-Fail "Projeto ausente na configuração: $project"
    }
}

$requiredPatterns = @(
    "authorized_roots",
    "protected_patterns",
    "local_only",
    "validation"
)

foreach ($pattern in $requiredPatterns) {
    if ($configText -match [regex]::Escape($pattern)) {
        Write-Pass "Seção encontrada: $pattern"
    }
    else {
        Write-Fail "Seção ausente: $pattern"
    }
}

if ($configText -match "(?i)(password|token|secret|private_key)\s*:") {
    Write-Fail "Possível credencial encontrada na configuração"
}
else {
    Write-Pass "Nenhuma credencial evidente encontrada"
}

if ($script:Failures -gt 0) {
    exit 1
}

Write-Host "Teste da configuração concluído." -ForegroundColor Cyan
exit 0
