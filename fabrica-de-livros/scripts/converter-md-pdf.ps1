# Script de Conversao MD para PDF (Pandoc + Typst)
# Fabrica Agentica de Livros
# Uso: .\converter-md-pdf.ps1 [slug-do-livro]

param(
    [string]$Slug,
    [string]$OutputDir = "fabrica-de-livros\output",
    [string]$TemplatePath = "fabrica-de-livros\templates\template.typ",
    [switch]$SemDiagramas,   # pula a renderizacao dos blocos ```mermaid
    [switch]$SemCapa         # desativa capa/contracapa graficas
)

# Raiz do projeto (pasta acima de scripts\)
$ProjetoRaiz = Split-Path $PSScriptRoot -Parent

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

# Upgrade 2 - Renderiza blocos ```mermaid em PNG. Retorna o MD a usar.
function Invoke-Diagramas {
    param([string]$LivroPath, [string]$SlugName, [string]$MdFile)
    if ($SemDiagramas) { return $MdFile }
    $python = Find-Executable -Name "python"
    $renderizador = Join-Path $ProjetoRaiz "scripts\renderizar-diagramas.py"
    if ((-not $python) -or (-not (Test-Path $renderizador))) { return $MdFile }
    $conteudo = Get-Content $MdFile -Raw -Encoding UTF8
    if ($conteudo -notmatch '(?im)^\s*```\s*mermaid') { return $MdFile }

    $saida = Join-Path $LivroPath "_livro_render.md"
    & $python $renderizador $SlugName "--md" $MdFile "--saida" $saida | Out-Null
    if (Test-Path $saida) { return $saida }
    return $MdFile
}

# Upgrade 5 - Variaveis de capa grafica / ficha catalografica (CIP)
function Get-VariaveisVisuais {
    param([string]$SlugName)
    $extras = @()
    $python = Find-Executable -Name "python"
    $meta = Join-Path $ProjetoRaiz "scripts\metadados_livro.py"
    if ($python -and (Test-Path $meta)) {
        $linhas = & $python $meta $SlugName "--pandoc-args" 2>$null
        if ($LASTEXITCODE -eq 0 -and $linhas) {
            $extras += @($linhas | Where-Object { $_ -and $_.Trim() -ne "" })
        }
    }
    if ($SemCapa) { $extras += @("-V", "sem_capa_grafica=1") }
    return $extras
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

    # Absolutiza o caminho: dentro de Push-Location um caminho relativo deixaria de
    # resolver (Test-Path/Join-Path passariam a olhar para a pasta do livro).
    $LivroPath = (Resolve-Path $LivroPath).Path

    $mdFile = Join-Path $LivroPath "livro_final.md"
    $templateFile = Join-Path (Get-Location) $TemplatePath
    
    if (-not (Test-Path $mdFile)) {
        Write-Host "  SKIP $SlugName (sem livro_final.md)" -ForegroundColor Yellow
        return $false
    }
    
    # Renderizar diagramas Mermaid (Upgrade 2) e usar o MD resultante
    $mdUsado = Invoke-Diagramas -LivroPath $LivroPath -SlugName $SlugName -MdFile $mdFile

    # Ler conteudo e escapar dollar signs que nao sao math
    $content = Get-Content $mdUsado -Raw -Encoding UTF8

    # Extrair titulo: prioriza titulo_obra do sumario_macro.json (o primeiro "# " do
    # livro_final.md costuma ser "Prefacio", nao o titulo da obra)
    $title = $null
    $python = Find-Executable -Name "python"
    $meta = Join-Path $ProjetoRaiz "scripts\metadados_livro.py"
    if ($python -and (Test-Path $meta)) {
        $t = & $python $meta $SlugName "--titulo" 2>$null
        if ($LASTEXITCODE -eq 0 -and $t) { $title = ($t | Select-Object -First 1).Trim() }
    }
    if (-not $title) {
        $titleMatch = [regex]::Match($content, '^#\s+(.+)$', 'Multiline')
        $title = if ($titleMatch.Success) { $titleMatch.Groups[1].Value } else { $SlugName }
    }
    
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
    
    # Rodar do diretorio do livro + resource-path.
    # Pipeline: Pandoc -> .typ (preserva caminhos relativos das figuras) -> typst compile.
    # NAO usar --pdf-engine=typst: o Pandoc reescreve os caminhos das imagens em forma
    # absoluta e o Typst recusa ("path contains invalid component C:").
    Push-Location $LivroPath
    try {
        $pandocArgs = @(
            "_temp_convert.md",
            "-o", "_livro_compilado.typ",
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
        $pandocArgs += Get-VariaveisVisuais -SlugName $SlugName


        # Capturar stderr separado
        $stderr = & $PandocPath @pandocArgs 2>&1 | ForEach-Object { $_.ToString() }

        $typFile = Join-Path $LivroPath "_livro_compilado.typ"
        if (Test-Path $typFile) {
            $stderr += & $TypstPath compile --root $LivroPath "_livro_compilado.typ" "$pdfName.pdf" 2>&1 |
                ForEach-Object { $_.ToString() }
            Remove-Item $typFile -Force -ErrorAction SilentlyContinue
        } else {
            $stderr += "pandoc nao gerou _livro_compilado.typ"
        }
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
                $errLines = $stderr | Where-Object { $_ -and $_.Trim() -ne "" } | Select-Object -Last 8
                foreach ($l in $errLines) { Write-Host "    $l" -ForegroundColor DarkGray }
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
