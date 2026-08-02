# Script PowerShell para gerar todos os PDFs e EPUBs
$ErrorActionPreference = "Stop"
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  GERANDO TODOS OS PDFS DA FABRICA AGENTICA DE LIVROS" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

$slug = "livros/ai-driven-development-4-camadas-tela-harness-llm-tools"

Write-Host "[1/4] Compilando PDF do Livro Principal..." -ForegroundColor Yellow
python compilar-para-pdf.py $slug

Write-Host "`n[2/4] Gerando Capas dos E-books e do Livro..." -ForegroundColor Yellow
python scripts/gerar-capa-ebooks.py $slug

Write-Host "`n[3/4] Gerando EPUBs dos E-books..." -ForegroundColor Yellow
python scripts/gerar-epub.py $slug

Write-Host "`n[4/4] Empacotando na pasta de Distribuição..." -ForegroundColor Yellow
python scripts/empacotar-distribuicao.py $slug

Write-Host "`n========================================================" -ForegroundColor Green
Write-Host "  TODOS OS PDFS E EPUBS GERADOS COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
