[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("toolbox", "toolbox-plugins", "toolbox-automation")]
    [string]$Repo,

    [Parameter(Mandatory = $true)]
    [int]$IssueNumber,

    [string]$Owner = "rodrigolessadev",
    [string]$StateFile = "C:\tools\toolbox\.release_plugin_state\state.json"
)

$ErrorActionPreference = "Stop"

Write-Host "Buscando informações da issue #$IssueNumber no repositório $Owner/$Repo..." -ForegroundColor Cyan

$ghOutput = gh issue view $IssueNumber --repo "$Owner/$Repo" --json number,title,body,labels 2>$null

if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($ghOutput)) {
    Write-Host "[ERRO] Não foi possível consultar a issue #$IssueNumber via GitHub CLI." -ForegroundColor Red
    exit 1
}

$issueData = $ghOutput | ConvertFrom-Json

$title = $issueData.title
$body = $issueData.body
$labels = $issueData.labels | ForEach-Object { $_.name }

Write-Host "Issue encontrada: #$IssueNumber - $title" -ForegroundColor Green

# Classificar tipo de tarefa
$taskType = "feature"
$workflow = "new-feature"

if ($labels -contains "tipo: bug" -or $title -match "(?i)\bbug\b|\bfix\b|correção|erro") {
    $taskType = "bug_fix"
    $workflow = "bug-fix"
}
elseif ($Repo -eq "toolbox-plugins") {
    $taskType = "plugin"
    $workflow = "plugin-lifecycle"
}

$taskId = "TASK-$Repo-$IssueNumber"

# 1. Gerar Task Request estruturado
$requestsDir = ".agent\requests"
if (-not (Test-Path $requestsDir)) {
    New-Item -ItemType Directory -Path $requestsDir -Force | Out-Null
}

$taskRequest = @{
    task_id = $taskId
    issue_number = $IssueNumber
    repository = $Repo
    title = $title
    description = $body
    task_type = $taskType
    workflow = $workflow
    labels = $labels
    created_at = (Get-Date).ToUniversalTime().ToString("o")
}

$requestFile = Join-Path $requestsDir "$taskId.json"
$taskRequest | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 $requestFile
Write-Host "Requisição estruturada salva em: $requestFile" -ForegroundColor Green

# 2. Iniciar checkpoint
& "$PSScriptRoot\start-task.ps1" -TaskId $taskId -Description "Issue #$($IssueNumber) - $title"

# 3. Criar/identificar branch padronizada no repositório de destino
$slug = ($title.ToLower() -replace '[^a-z0-9]+', '-').Trim('-')
if ($slug.Length -gt 40) { $slug = $slug.Substring(0, 40).TrimEnd('-') }
$branchPrefix = if ($taskType -eq "bug_fix") { "fix" } else { "feature" }
$branchName = "$branchPrefix/$slug"

$targetRepoPath = "C:\tools\$Repo"
if (Test-Path $targetRepoPath) {
    Write-Host "Configurando branch $branchName em $targetRepoPath..." -ForegroundColor Cyan
    $prevEA = $ErrorActionPreference
    $ErrorActionPreference = "SilentlyContinue"
    & git.exe -C $targetRepoPath checkout -B $branchName *>$null
    $ErrorActionPreference = $prevEA
}

# 4. Atualizar estado local do Kanban (se existir)
if (Test-Path $StateFile) {
    try {
        $stateJson = Get-Content $StateFile -Raw | ConvertFrom-Json
        $issueKey = "$Repo#$IssueNumber"

        $issueEntry = [PSCustomObject]@{
            repo = $Repo
            issue_number = $IssueNumber
            branch = $branchName
            last_status = "🚀 Em andamento"
            updated_at = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss")
        }

        $stateJson.issues | Add-Member -NotePropertyName $issueKey -NotePropertyValue $issueEntry -Force

        $stateJson | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 $StateFile
        Write-Host "Kanban local atualizado: $issueKey -> 🚀 Em andamento" -ForegroundColor Green
    }
    catch {
        Write-Host "[AVISO] Não foi possível atualizar o estado do Kanban local: $_" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Tarefa $taskId inicializada com sucesso!" -ForegroundColor Cyan
Write-Host "Repositório: $Repo"
Write-Host "Workflow sugerido: $workflow"
Write-Host "Branch ativa: $branchName"
Write-Host "Pronto para análise e planejamento." -ForegroundColor Green
exit 0
