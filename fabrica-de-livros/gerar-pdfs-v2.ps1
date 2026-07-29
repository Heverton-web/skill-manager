# Script para Gerar PDFs de Todos os Livros - Versao Corrigida
$ErrorActionPreference = "Continue"

# Caminhos absolutos baseados no diretorio do script
$DirRaiz = Split-Path -Parent $MyInvocation.MyCommand.Path
$dirOutput = Join-Path $DirRaiz "output"
$dirCompiler = Join-Path $DirRaiz ".claude\mcp-servers\pdf-gen-server"

Write-Host "`n=== GERADOR DE PDFs - Fabrica Agentic ===`n"
Write-Host "Dir Raiz: $DirRaiz"
Write-Host "Dir Output: $dirOutput"
Write-Host "Dir Compiler: $dirCompiler`n"

# Verificar diretorios
if (-not (Test-Path $dirOutput)) {
    Write-Host "ERRO: Diretorio output nao encontrado!" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $dirCompiler)) {
    Write-Host "ERRO: Diretorio do compilador nao encontrado!" -ForegroundColor Red
    exit 1
}

# Listar livros
$livros = Get-ChildItem -Path $dirOutput -Directory | Where-Object { $_.Name -ne "output" }
Write-Host "Livros encontrados: $($livros.Count)`n"

$mdCount = 0
$pdfCount = 0
$erros = 0

foreach ($livro in $livros) {
    $slug = $livro.Name
    $caminhoMd = Join-Path $livro.FullName "livro_final.md"
    $caminhoPdf = Join-Path $livro.FullName "livro_final.pdf"
    
    Write-Host "--- $slug ---" -ForegroundColor Cyan
    
    # Verificar/compilar MD
    if (Test-Path $caminhoMd) {
        $tamanho = (Get-Item $caminhoMd).Length
        Write-Host "  MD: OK ($tamanho bytes)" -ForegroundColor Green
        $mdCount++
    } else {
        Write-Host "  MD: Compilando..." -ForegroundColor Yellow
        Push-Location $dirCompiler
        $output = & node compilar-livro.mjs $slug 2>&1
        Pop-Location
        
        if (Test-Path $caminhoMd) {
            Write-Host "  MD: Compilado com sucesso" -ForegroundColor Green
            $mdCount++
        } else {
            Write-Host "  MD: ERRO na compilacao" -ForegroundColor Red
            $erros++
            continue
        }
    }
    
    # Verificar PDF existente
    if (Test-Path $caminhoPdf) {
        $tamanhoPdf = (Get-Item $caminhoPdf).Length
        Write-Host "  PDF: JA EXISTE ($tamanhoPdf bytes)" -ForegroundColor Green
        $pdfCount++
        continue
    }
    
    # Gerar PDF
    Write-Host "  PDF: Gerando via CloudConvert..." -ForegroundColor Yellow
    Push-Location $dirCompiler
    $output = & node compilar-livro.mjs $slug 2>&1
    $outputStr = $output -join " "
    Pop-Location
    
    if ($outputStr -match "PDF gerado com sucesso") {
        Write-Host "  PDF: GERADO COM SUCESSO" -ForegroundColor Green
        $pdfCount++
    } elseif ($outputStr -match "402|run out of credits|out of conversion") {
        Write-Host "  PDF: SEM CREDITOS CLOUDCONVERT" -ForegroundColor Yellow
        $erros++
    } else {
        Write-Host "  PDF: ERRO" -ForegroundColor Red
        $erros++
    }
}

# Relatorio Final
Write-Host "`n" + ("=" * 60)
Write-Host "  RELATORIO FINAL"
Write-Host ("=" * 60)
Write-Host "  Total de livros: $($livros.Count)"
Write-Host "  MDs prontos: $mdCount" -ForegroundColor Green
Write-Host "  PDFs gerados: $pdfCount" -ForegroundColor Green
Write-Host "  Erros: $erros" -ForegroundColor $(if($erros -gt 0){"Yellow"}else{"Green"})

if ($outputStr -match "402|run out of credits|out of conversion") {
    Write-Host "`n  CREDITOS CLOUDCONVERT ESGOTADOS!" -ForegroundColor Yellow
    Write-Host "  Recarregue em: https://cloudconvert.com/pricing" -ForegroundColor Yellow
}

Write-Host "`n" + ("=" * 60) + "`n"
