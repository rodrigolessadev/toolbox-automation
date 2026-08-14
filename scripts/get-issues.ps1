[CmdletBinding()]
param(
    [ValidateSet("toolbox", "toolbox-plugins", "all")]
    [string]$Project = "all"
)

$ErrorActionPreference = "Continue"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "  Toolbox Automation - Consulta de Issues Abertas   " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

function Show-RepoIssues {
    param(
        [string]$RepoName,
        [string]$Prefix
    )

    Write-Host "`nBuscando issues abertas em rodrigolessadev/$RepoName..." -ForegroundColor Yellow
    
    $issuesJson = gh issue list -R "rodrigolessadev/$RepoName" --state open --json number,title,labels,updatedAt 2>$null
    
    if (-not $issuesJson -or $issuesJson -eq "[]") {
        Write-Host "Nenhuma issue aberta encontrada em $RepoName." -ForegroundColor Gray
        return
    }

    $issues = $issuesJson | ConvertFrom-Json
    
    foreach ($issue in $issues) {
        $labels = ($issue.labels | ForEach-Object { $_.name }) -join ", "
        Write-Host "[$($Prefix) #$($issue.number)] $($issue.title)" -ForegroundColor Green
        if ($labels) {
            Write-Host "    Labels: $labels" -ForegroundColor DarkGray
        }
        Write-Host "    Prompt rápido: " -NoNewline -ForegroundColor White
        Write-Host "$Prefix #$($issue.number)" -ForegroundColor Cyan
    }
}

if ($Project -eq "toolbox" -or $Project -eq "all") {
    Show-RepoIssues -RepoName "toolbox" -Prefix "toolbox"
}

if ($Project -eq "toolbox-plugins" -or $Project -eq "all") {
    Show-RepoIssues -RepoName "toolbox-plugins" -Prefix "plugins"
}

Write-Host "`nPara iniciar a automação, basta copiar e enviar o 'Prompt rápido' na conversa!" -ForegroundColor Magenta
