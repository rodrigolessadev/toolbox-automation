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

$projects = @(
    @{ Name = "toolbox-automation"; Path = "C:\tools\toolbox-automation"; Required = $true },
    @{ Name = "toolbox"; Path = "C:\tools\toolbox"; Required = $true },
    @{ Name = "toolbox-plugins"; Path = "C:\tools\toolbox-plugins"; Required = $true },
    @{ Name = "release-plugin (privado)"; Path = "C:\tools\toolbox-plugins\plugins\release"; Required = $false }
)

$hasErrors = $false

foreach ($proj in $projects) {
    Write-Host "Verificando projeto: $($proj.Name)..." -NoNewline
    if (-not (Test-Path $proj.Path)) {
        if ($proj.Required) {
            Write-Host " [FALHA] Diretório não existe: $($proj.Path)" -ForegroundColor Red
            $hasErrors = $true
        }
        else {
            Write-Host " [OPCIONAL - AUSENTE]" -ForegroundColor Yellow
        }
        continue
    }

    $gitDir = Join-Path $proj.Path ".git"
    if (-not (Test-Path $gitDir)) {
        if ($proj.Required) {
            Write-Host " [FALHA] Não é um repositório Git válido: $($proj.Path)" -ForegroundColor Red
            $hasErrors = $true
        }
        else {
            Write-Host " [OPCIONAL - SEM GIT]" -ForegroundColor Yellow
        }
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
