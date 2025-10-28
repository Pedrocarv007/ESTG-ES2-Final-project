# Script para gerenciar modos do StudyHub AI
param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("proxy", "direct")]
    [string]$Mode
)

Write-Host "StudyHub AI - Configurando modo: $Mode" -ForegroundColor Green

switch ($Mode) {
    "proxy" {
        Write-Host "Configurando para modo PROXY REVERSO..." -ForegroundColor Yellow
        Copy-Item ".env.proxy" ".env" -Force
        Write-Host "URLs serão acessíveis com prefixo /studyhubai" -ForegroundColor Cyan
        Write-Host "Exemplo: http://localhost/studyhubai/auth/login" -ForegroundColor Cyan
    }
    "direct" {
        Write-Host "Configurando para modo DIRETO..." -ForegroundColor Yellow
        Copy-Item ".env.direct" ".env" -Force
        Write-Host "URLs serão acessíveis diretamente" -ForegroundColor Cyan
        Write-Host "Exemplo: http://localhost:6002/auth/login" -ForegroundColor Cyan
    }
}

Write-Host "`nConfiguracao aplicada! Execute 'python run.py' para iniciar." -ForegroundColor Green