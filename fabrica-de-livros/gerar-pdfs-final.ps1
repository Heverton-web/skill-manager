# Script Final para Gerar PDFs de Todos os Livros
# Uso: powershell -ExecutionPolicy Bypass -File gerar-pdfs-final.ps1

$ErrorActionPreference = "Continue"

# Determinar diretorio raiz do projeto (fabrica-de-livros)
$DirScript = Split-Path -Parent $MyInvocation.MyCommand.Path
$DirRaiz = if ($DirScript) { $DirScript } else { Get-Location }
$dirOutput = Join-Path $DirRaiz "output"
$dirCompiler = Join-Path $DirRaiz ".claude\mcp-servers\pdf-gen-server"

Write-Host "`n=== GERADOR DE PDFs - Fabrica Agentic ===" -ForegroundColor Cyan
Write-Host "Diretorio: $DirRaiz`n"

# Validar diretorios
if (-not (Test-Path $dirOutput)) {
    Write-Host "ERRO: Diretorio output nao encontrado em $dirOutput" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $dirCompiler)) {
    Write-Host "ERRO: Compilador nao encontrado em $dirCompiler" -ForegroundColor Red
    exit 1
}

# Listar livros e verificar status
$livros = Get-ChildItem -Path $dirOutput -Directory | Where-Object { $_.Name -ne "output" }
Write-Host "Livros encontrados: $($livros.Count)`n" -ForegroundColor White

# Verificar quais precisam de compilacao
$precisamCompilar = @()
$jaCompilados = @()

foreach ($livro in $livros) {
    $caminhoMd = Join-Path $livro.FullName "livro_final.md"
    if (Test-Path $caminhoMd) {
        $jaCompilados += $livro.Name
    } else {
        $precisamCompilar += $livro.Name
    }
}

Write-Host "Status inicial:" -ForegroundColor Yellow
Write-Host "  Ja compilados: $($jaCompilados.Count)" -ForegroundColor Green
Write-Host "  Precisam compilar: $($precisamCompilar.Count)`n" -ForegroundColor $(if($precisamCompilar.Count -gt 0){"Yellow"}else{"Green"})

# Compilar livros que faltam
if ($precisamCompilar.Count -gt 0) {
    Write-Host "=== Compilando livros pendentes ===" -ForegroundColor Cyan
    Push-Location $dirCompiler
    
    foreach ($slug in $precisamCompilar) {
        Write-Host "  Compilando $slug..." -ForegroundColor Yellow -NoNewline
        $output = & node compilar-livro.mjs $slug 2>&1
        $caminhoMd = Join-Path (Join-Path $dirOutput $slug) "livro_final.md"
        
        if (Test-Path $caminhoMd) {
            Write-Host " OK" -ForegroundColor Green
        } else {
            Write-Host " ERRO" -ForegroundColor Red
        }
    }
    
    Pop-Location
}

# Verificar status apos compilacao
$livrosComMd = @()
$livrosSemMd = @()

foreach ($livro in $livros) {
    $caminhoMd = Join-Path $livro.FullName "livro_final.md"
    if (Test-Path $caminhoMd) {
        $livrosComMd += $livro
    } else {
        $livrosSemMd += $livro.Name
    }
}

Write-Host "`n=== Status apos compilacao ===" -ForegroundColor Cyan
Write-Host "  Com MD: $($livrosComMd.Count)" -ForegroundColor Green
Write-Host "  Sem MD: $($livrosSemMd.Count)" -ForegroundColor $(if($livrosSemMd.Count -gt 0){"Red"}else{"Green"})

if ($livrosSemMd.Count -gt 0) {
    Write-Host "  Livros sem MD: $($livrosSemMd -join ', ')" -ForegroundColor Red
}

# Verificar PDFs existentes
$jaTemPdf = @()
$precisaPdf = @()

foreach ($livro in $livrosComMd) {
    $caminhoPdf = Join-Path $livro.FullName "livro_final.pdf"
    if (Test-Path $caminhoPdf) {
        $jaTemPdf += $livro.Name
    } else {
        $precisaPdf += $livro
    }
}

Write-Host "`n=== Status de PDFs ===" -ForegroundColor Cyan
Write-Host "  Ja existem: $($jaTemPdf.Count)" -ForegroundColor Green
Write-Host "  Precisam gerar: $($precisaPdf.Count)" -ForegroundColor $(if($precisaPdf.Count -gt 0){"Yellow"}else{"Green"})

# Gerar PDFs
if ($precisaPdf.Count -gt 0) {
    Write-Host "`n=== Gerando PDFs ===" -ForegroundColor Cyan
    $creditosEsgotados = $false
    $pdfsGerados = 0
    $erros = 0
    
    Push-Location $dirCompiler
    
    foreach ($livro in $precisaPdf) {
        $slug = $livro.Name
        
        if ($creditosEsgotados) {
            Write-Host "  $slug - Pulando (creditos esgotados)" -ForegroundColor Gray
            continue
        }
        
        Write-Host "  $slug - Gerando..." -ForegroundColor Yellow -NoNewline
        $output = & node compilar-livro.mjs $slug 2>&1
        $outputStr = $output -join " "
        
        $caminhoPdf = Join-Path $livro.FullName "livro_final.pdf"
        
        if (Test-Path $caminhoPdf) {
            $tamanho = (Get-Item $caminhoPdf).Length
            Write-Host " OK ($([math]::Round($tamanho/1KB)) KB)" -ForegroundColor Green
            $pdfsGerados++
        } elseif ($outputStr -match "402|run out of credits|out of conversion") {
            Write-Host " SEM CREDITOS" -ForegroundColor Red
            $creditosEsgotados = $true
            $erros++
        } else {
            Write-Host " ERRO" -ForegroundColor Red
            $erros++
        }
    }
    
    Pop-Location
    
    # Relatorio
    Write-Host "`n=== RELATORIO FINAL ===" -ForegroundColor Cyan
    Write-Host "  Total de livros: $($livros.Count)"
    Write-Host "  MDs prontos: $($livrosComMd.Count)" -ForegroundColor Green
    Write-Host "  PDFs totais: $($jaTemPdf.Count + $pdfsGerados)" -ForegroundColor Green
    Write-Host "  PDFs novos: $pdfsGerados" -ForegroundColor Green
    
    if ($creditosEsgotados) {
        Write-Host "`n  CREDITOS CLOUDCONVERT ESGOTADOS!" -ForegroundColor Yellow
        Write-Host "  Para gerar os PDFs restantes, recarregue em:" -ForegroundColor Yellow
        Write-Host "  https://cloudconvert.com/pricing" -ForegroundColor Cyan
    }
}

Write-Host "`n=== Concluido ===" -ForegroundColor Cyan
