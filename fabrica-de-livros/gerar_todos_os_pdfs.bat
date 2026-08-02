@echo off
chcp 65001 > nul
echo ========================================================
echo   GERANDO TODOS OS PDFS DA FABRICA AGENTICA DE LIVROS
echo ========================================================
echo.

set SLUG=livros/ai-driven-development-4-camadas-tela-harness-llm-tools

echo [1/4] Compilando PDF do Livro Principal...
python compilar-para-pdf.py %SLUG%

echo.
echo [2/4] Gerando Capas dos E-books e do Livro...
python scripts/gerar-capa-ebooks.py %SLUG%

echo.
echo [3/4] Gerando EPUBs dos E-books...
python scripts/gerar-epub.py %SLUG%

echo.
echo [4/4] Empacotando tudo na pasta de Distribuicao...
python scripts/empacotar-distribuicao.py %SLUG%

echo.
echo ========================================================
echo   PROCESSO CONCLUIDO COM SUCESSO!
echo ========================================================
pause
