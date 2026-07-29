# Script para Gerar PDFs de Todos os Livros
$ErrorActionPreference = "Continue"
$dirOutput = Join-Path $PSScriptRoot "output"
$dirCompiler = ".\.claude\mcp-servers\pdf-gen-server"

Write-Host "`n=== GERADOR DE PDFs - Fabrica Agentic ===`n"

# Listar livros
$livros = Get-ChildItem -Path $dirOutput -Directory | Where-Object { $_.Name -ne "output" }
Write-Host "Livros encontrados: $($livros.Count)`n"

$mdCount = 0
$pdfCount = 0
$creditosEsgotados = 0

foreach ($livro in $livros) {
    $slug = $livro.Name
    $caminhoMd = Join-Path $livro.FullName "livro_final.md"
    $caminhoPdf = Join-Path $livro.FullName "livro_final.pdf"
    
    Write-Host "--- $slug ---"
    
    # Verificar/compilar MD
    if (Test-Path $caminhoMd) {
        Write-Host "  MD: OK"
        $mdCount++
    } else {
        Write-Host "  MD: Compilando..."
        Push-Location $dirCompiler
        node compilar-livro.mjs $slug 2>&1 | Out-Null
        Pop-Location
        if (Test-Path $caminhoMd) {
            Write-Host "  MD: Compilado"
            $mdCount++
        } else {
            Write-Host "  MD: ERRO"
            continue
        }
    }
    
    # Verificar PDF existente
    if (Test-Path $caminhoPdf) {
        Write-Host "  PDF: JA EXISTE"
        $pdfCount++
        continue
    }
    
    # Gerar PDF
    Write-Host "  PDF: Gerando..."
    Push-Location $dirCompiler
    $output = node compilar-livro.mjs $slug 2>&1
    $outputStr = $output -join " "
    Pop-Location
    
    if ($outputStr -match "PDF gerado com sucesso") {
        Write-Host "  PDF: OK"
        $pdfCount++
    } elseif ($outputStr -match "402|run out of credits") {
        Write-Host "  PDF: SEM CREDITOS"
        $creditosEsgotados++
    } else {
        Write-Host "  PDF: ERRO"
    }
}

Write-Host "`n=== RESUMO ==="
Write-Host "MDs prontos: $mdCount / $($livros.Count)"
Write-Host "PDFs gerados: $pdfCount / $($livros.Count)"

if ($creditosEsgotados -gt 0) {
    Write-Host "`nCREDITOS CLOUDCONVERT ESGOTADOS para $creditosEsgotados livro(s)"
    Write-Host "Recarregue em: https://cloudconvert.com/pricing"
}
