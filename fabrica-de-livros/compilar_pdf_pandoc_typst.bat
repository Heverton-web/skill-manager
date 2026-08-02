@echo off
chcp 65001 > nul
echo ========================================================
echo   COMPILACAO PANDOC + TYPST (PDF ABNT)
echo ========================================================
echo.

set OBRAPATH=output\livros\ai-driven-development-4-camadas-tela-harness-llm-tools

echo [1/2] Passo 1: Pandoc (Markdown -> Typst) ...
pandoc "%OBRAPATH%\livro_final.md" --template=templates\template.typ -o "%OBRAPATH%\livro_final.typ"

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao converter via Pandoc. Verifique se o Pandoc esta instalado e no PATH.
    pause
    exit /b %ERRORLEVEL%
)

echo [2/2] Passo 2: Typst CLI (Typst -> PDF) ...
typst compile --root . "%OBRAPATH%\livro_final.typ" "%OBRAPATH%\livro_final.pdf"

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Erro ao compilar via Typst. Verifique se o Typst esta instalado e no PATH.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ========================================================
echo   SUCESSO! PDF GERADO EM:
echo   %OBRAPATH%\livro_final.pdf
echo ========================================================
pause
