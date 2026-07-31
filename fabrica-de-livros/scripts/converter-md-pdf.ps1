# Script de Conversao MD para PDF (Pandoc + Typst)
# Fabrica Agentica de Livros
# Uso: .\converter-md-pdf.ps1 [slug-do-livro]

param(
    [string]$Slug,
    [string]$OutputDir = "fabrica-de-livros\output",
    [string]$TemplatePath = "fabrica-de-livros\templates\template.typ"
)

# Auto-detectar executaveis
function Find-Executable {
    param([string]$Name)
    $inPath = Get-Command $Name -ErrorAction SilentlyContinue
    if ($inPath) { return $inPath.Source }
    $wingetBase = Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Packages"
    if (Test-Path $wingetBase) {
        $found = Get-ChildItem -Path $wingetBase -Recurse -Filter "$Name.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) { return $found.FullName }
    }
    return $null
}

$PandocPath = Find-Executable -Name "pandoc"
$TypstPath = Find-Executable -Name "typst"

if ($TypstPath) {
    $typstDir = Split-Path $TypstPath -Parent
    if ($env:PATH -notlike "*$typstDir*") { $env:PATH = "$typstDir;$env:PATH" }
}

function Test-Dependencies {
    if ((-not $PandocPath) -or (-not $TypstPath)) {
        Write-Host "Pandoc ou Typst nao encontrado" -ForegroundColor Red
        exit 1
    }
    Write-Host "OK Dependencias verificadas" -ForegroundColor Green
}

# Contar paginas do PDF (estimativa via regex)
function Get-PdfPageCount {
    param([string]$PdfPath)
    try {
        $bytes = [System.IO.File]::ReadAllBytes($PdfPath)
        $text = [System.Text.Encoding]::ASCII.GetString($bytes)
        $matches = [regex]::Matches($text, "/Type\s*/Page[^s]")
        return $matches.Count
    } catch {
        return 0
    }
}

function Convert-Livro {
    param([string]$LivroPath, [string]$SlugName)
    
    $mdFile = Join-Path $LivroPath "livro_final.md"
    $templateFile = Join-Path (Get-Location) $TemplatePath
    
    if (-not (Test-Path $mdFile)) {
        Write-Host "  SKIP $SlugName (sem livro_final.md)" -ForegroundColor Yellow
        return $false
    }
    
    # Ler conteudo e escapar dollar signs que nao sao math
    $content = Get-Content $mdFile -Raw -Encoding UTF8
    
    # Extrair titulo
    $titleMatch = [regex]::Match($content, '^#\s+(.+)$', 'Multiline')
    $title = if ($titleMatch.Success) { $titleMatch.Groups[1].Value } else { $SlugName }
    
    # Gerar nome do PDF a partir do titulo (sanitizado e truncado)
    $pdfName = $title -replace '[<>:"/\\|?*,]', '' -replace '\s+', '_' -replace ':', '_'
    if ($pdfName.Length -gt 60) { $pdfName = $pdfName.Substring(0, 60) }
    $pdfFile = Join-Path $LivroPath "$pdfName.pdf"
    
    # Escapar $ solitarios (nao-double) para evitar erros de TeX math
    $content = $content -replace '(?<!\\)\$(?!\$)', '\\$'
    
    # Salvar conteudo processado em arquivo temporario
    $tempMd = Join-Path $LivroPath "_temp_convert.md"
    [System.IO.File]::WriteAllText($tempMd, $content)
    
    Write-Host "  $SlugName..." -ForegroundColor Cyan -NoNewline
    
    # Rodar do diretorio do livro + resource-path
    Push-Location $LivroPath
    try {
        $pandocArgs = @(
            "_temp_convert.md",
            "-o", "$pdfName.pdf",
            "--pdf-engine=typst",
            "--toc", "--toc-depth=3",
            "--number-sections",
            "--template=$templateFile",
            "-V", "title=$title",
            "-V", "author=Heverton Eduardo Peres",
            "-V", "subtitle=",
            "--wrap=preserve",
            "--resource-path=$LivroPath",
            "--from=markdown-citations"
        )
        
        # Capturar stderr separado
        $stderr = & $PandocPath @pandocArgs 2>&1 | ForEach-Object { $_.ToString() }
        Pop-Location
        
        # Limpar arquivo temporario
        Remove-Item $tempMd -Force -ErrorAction SilentlyContinue
        
        if (Test-Path $pdfFile) {
            $size = [math]::Round((Get-Item $pdfFile).Length / 1KB, 1)
            $pageCount = Get-PdfPageCount -PdfPath $pdfFile
            $minPages = 70
            
            if ($pageCount -gt 0 -and $pageCount -lt $minPages) {
                Write-Host " OK ($size KB, ~$pageCount paginas estimadas) AVISO: abaixo de $minPages" -ForegroundColor Yellow
            } else {
                $pageInfo = if ($pageCount -gt 0) { ", ~$pageCount paginas estimadas" } else { "" }
                Write-Host " OK ($size KB$pageInfo)" -ForegroundColor Green
            }
            return $true
        } else {
            Write-Host " FALHA" -ForegroundColor Red
            if ($stderr) { 
                $errLines = $stderr | Select-Object -Last 3
                if ($errLines) { Write-Host "    $($errLines -join '; ')" -ForegroundColor DarkGray }
            }
            return $false
        }
    } catch {
        Pop-Location
        Remove-Item $tempMd -Force -ErrorAction SilentlyContinue
        Write-Host " ERRO: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Main
Write-Host ""
Write-Host "Conversor MD para PDF (Pandoc + Typst)" -ForegroundColor Magenta
Write-Host "========================================" -ForegroundColor DarkGray
Write-Host ""

Test-Dependencies

$livros = @()
if ($Slug) {
    $p = Join-Path $OutputDir $Slug
    if (Test-Path $p) { $livros += @{ Path = $p; Slug = $Slug } }
    else { Write-Host "Livro nao encontrado: $Slug" -ForegroundColor Red; exit 1 }
} else {
    Get-ChildItem -Path $OutputDir -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        if (Test-Path (Join-Path $_.FullName "livro_final.md")) {
            $livros += @{ Path = $_.FullName; Slug = $_.Name }
        }
    }
}

if ($livros.Count -eq 0) { Write-Host "Nenhum livro encontrado" -ForegroundColor Yellow; exit 0 }

Write-Host "$($livros.Count) livro(s) encontrado(s)" -ForegroundColor White
Write-Host ""

$s = 0; $f = 0
foreach ($l in $livros) {
    if (Convert-Livro -LivroPath $l.Path -SlugName $l.Slug) { $s++ } else { $f++ }
}

Write-Host ""
Write-Host "Resultado: $s OK, $f falha(s)" -ForegroundColor $(if ($f -eq 0) { "Green" } else { "Yellow" })
Write-Host "Meta: minimo 70 paginas por livro" -ForegroundColor DarkGray
Write-Host ""
