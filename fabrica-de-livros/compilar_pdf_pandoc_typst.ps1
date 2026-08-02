# Script PowerShell para compilar via Pandoc + Typst no Windows
$ErrorActionPreference = "Stop"

$obraPath = "output/livros/ai-driven-development-4-camadas-tela-harness-llm-tools"

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  COMPILAÇÃO PANDOC + TYPST (PDF ABNT)" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/2] Passo 1: Pandoc (Markdown -> Typst)..." -ForegroundColor Yellow
pandoc "$obraPath/livro_final.md" --template=templates/template.typ -o "$obraPath/livro_final.typ"

Write-Host "[2/2] Passo 2: Typst CLI (Typst -> PDF)..." -ForegroundColor Yellow
typst compile --root . "$obraPath/livro_final.typ" "$obraPath/livro_final.pdf"

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host "  SUCESSO! PDF GERADO EM:" -ForegroundColor Green
Write-Host "  $obraPath/livro_final.pdf" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
