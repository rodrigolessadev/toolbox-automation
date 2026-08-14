[CmdletBinding()]
param(
    [string]$ConfigPath = "config\local-projects.yaml"
)

$ErrorActionPreference = "Stop"

Write-Host "Iniciando verificação dos projetos locais..." -ForegroundColor Cyan

if (-not (Test-Path $ConfigPath)) {
    Write-Host "[ERRO] Arquivo de configuração não encontrado: $ConfigPath" -ForegroundColor Red
    exit 1
}

$configContent = Get-Content $ConfigPath -Raw

$projects = @(
    @{ Name = "toolbox-automation"; Path = "C:\tools\toolbox-automation" },
    @{ Name = "toolbox"; Path = "C:\tools\toolbox" },
    @{ Name = "toolbox-plugins"; Path = "C:\tools\toolbox-plugins" }
)

$hasErrors = $false

foreach ($proj in $projects) {
    Write-Host "Verificando projeto: $($proj.Name)..." -NoNewline
    if (-not (Test-Path $proj.Path)) {
        Write-Host " [FALHA] Diretório não existe: $($proj.Path)" -ForegroundColor Red
        $hasErrors = $true
        continue
    }

    $gitDir = Join-Path $proj.Path ".git"
    if (-not (Test-Path $gitDir)) {
        Write-Host " [FALHA] Não é um repositório Git válido: $($proj.Path)" -ForegroundColor Red
        $hasErrors = $true
        continue
    }

    Write-Host " [OK]" -ForegroundColor Green
}

if ($hasErrors) {
    Write-Host "A verificação dos projetos encontrou pendências." -ForegroundColor Red
    exit 1
}

Write-Host "Todos os projetos autorizados foram verificados com sucesso." -ForegroundColor Green
exit 0
