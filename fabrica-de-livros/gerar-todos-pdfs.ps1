# Script para Compilar e Gerar PDFs de Todos os Livros
# Execute: powershell -ExecutionPolicy Bypass -File .\gerar-todos-pdfs.ps1

$ErrorActionPreference = "Continue"
$dirOutput = ".\output"
$dirCompiler = ".\.claude\mcp-servers\pdf-gen-server"

Write-Host "`n" -NoNewline
Write-Host "=" * 70
Write-Host "  GERADOR DE PDFs - Fábrica Agêntica de Livros"
Write-Host "=" * 70

# Listar todos os diretórios de livros
$livros = Get-ChildItem -Path $dirOutput -Directory | Where-Object { $_.Name -ne "output" }

Write-Host "`n📚 Livros encontrados: $($livros.Count)`n"

$resultados = @()

foreach ($livro in $livros) {
    $slug = $livro.Name
    $caminhoMd = Join-Path $livro.FullName "livro_final.md"
    $caminhoPdf = Join-Path $livro.FullName "livro_final.pdf"
    
    Write-Host "─" * 50
    Write-Host "📖 Processando: $slug" -ForegroundColor Cyan
    
    # Verificar se já tem livro_final.md
    if (Test-Path $caminhoMd) {
        $tamanhoMd = (Get-Item $caminhoMd).Length
        Write-Host "  ✅ livro_final.md existe ($tamanhoMd bytes)" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  livro_final.md não encontrado - compilando..." -ForegroundColor Yellow
        
        # Compilar o livro
        Push-Location $dirCompiler
        try {
            $output = node compilar-livro.mjs $slug 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "  ✅ Compilado com sucesso" -ForegroundColor Green
            } else {
                Write-Host "  ❌ Erro na compilação" -ForegroundColor Red
                $resultados += [PSCustomObject]@{Livro=$slug; Status="ERRO_COMPILACAO"; MD="❌"; PDF="❌"}
                continue
            }
        } catch {
            Write-Host "  ❌ Exceção: $_" -ForegroundColor Red
            $resultados += [PSCustomObject]@{Livro=$slug; Status="EXCECAO"; MD="❌"; PDF="❌"}
            continue
        } finally {
            Pop-Location
        }
    }
    
    # Verificar se já tem PDF
    if (Test-Path $caminhoPdf) {
        $tamanhoPdf = (Get-Item $caminhoPdf).Length
        Write-Host "  ✅ livro_final.pdf já existe ($tamanhoPdf bytes)" -ForegroundColor Green
        $resultados += [PSCustomObject]@{Livro=$slug; Status="PRONTO"; MD="✅"; PDF="✅"}
        continue
    }
    
    # Tentar gerar PDF
    Write-Host "  🔄 Gerando PDF via CloudConvert..." -ForegroundColor Yellow
    
    Push-Location $dirCompiler
    try {
        $output = node compilar-livro.mjs $slug 2>&1
        $outputStr = $output -join "`n"
        
        if ($outputStr -match "PDF gerado com sucesso") {
            Write-Host "  ✅ PDF gerado com sucesso" -ForegroundColor Green
            $resultados += [PSCustomObject]@{Livro=$slug; Status="PDF_GERADO"; MD="✅"; PDF="✅"}
        } elseif ($outputStr -match "402|run out of credits") {
            Write-Host "  ⚠️  Créditos CloudConvert esgotados" -ForegroundColor Yellow
            $resultados += [PSCustomObject]@{Livro=$slug; Status="SEM_CREDITOS"; MD="✅"; PDF="⏳"}
        } else {
            Write-Host "  ❌ Erro na geração do PDF" -ForegroundColor Red
            $resultados += [PSCustomObject]@{Livro=$slug; Status="ERRO_PDF"; MD="✅"; PDF="❌"}
        }
    } catch {
        Write-Host "  ❌ Exceção: $_" -ForegroundColor Red
        $resultados += [PSCustomObject]@{Livro=$slug; Status="EXCECAO"; MD="✅"; PDF="❌"}
    } finally {
        Pop-Location
    }
}

# Relatório Final
Write-Host "`n`n" -NoNewline
Write-Host "=" * 70
Write-Host "  RELATÓRIO FINAL"
Write-Host "=" * 70

$resultados | Format-Table -AutoSize

$mdProntos = ($resultados | Where-Object { $_.MD -eq "✅" }).Count
$pdfGerados = ($resultados | Where-Object { $_.PDF -eq "✅" }).Count
$semCreditos = ($resultados | Where-Object { $_.Status -eq "SEM_CREDITOS" }).Count

Write-Host "`n📊 Resumo:"
Write-Host "  📄 Markdowns prontos: $mdProntos / $($resultados.Count)" -ForegroundColor Cyan
Write-Host "  📑 PDFs gerados: $pdfGerados / $($resultados.Count)" -ForegroundColor Green

if ($semCreditos -gt 0) {
    Write-Host "`n⚠️  ATENÇÃO: $semCreditos livro(s) não puderam gerar PDF por falta de créditos CloudConvert" -ForegroundColor Yellow
    Write-Host "  Para gerar os PDFs, recarregue os créditos em: https://cloudconvert.com/pricing" -ForegroundColor Yellow
}

Write-Host "`n" + "=" * 70 + "`n"
