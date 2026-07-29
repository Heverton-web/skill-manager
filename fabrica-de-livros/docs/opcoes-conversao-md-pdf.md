# Plano de Conversão: Markdown → PDF (Gratuito)

## Visão Geral

Este documento apresenta as opções gratuitas para conversão de arquivos `.md` em `.pdf` com qualidade profissional, ordenadas da **mais eficiente** para a **menos eficiente**.

---

## 🏆 Ranking de Opções

### 1. 🥇 Pandoc + Typst (RECOMENDADO)

**Eficiência: ⭐⭐⭐⭐⭐**

| Aspecto | Detalhe |
|---------|---------|
| **Custo** | Gratuito (open source) |
| **Qualidade** | Excelente (moderna/limpa) |
| **Velocidade** | Extremamente rápida (< 1s) |
| **Instalação** | Leve (~50MB) |
| **Curva de aprendizado** | Baixa/Média |

**Por que é a melhor opção:**
- Compilação em frações de segundo (10-50x mais rápido que LaTeX)
- Binário único e leve (sem gigabytes de distribuição TeX)
- Suporte nativo a fontes do sistema
- Sumário dinâmico automático
- Numeração de páginas automática
- Integração direta com Pandoc

**Como usar:**
```bash
# Instalar Typst
winget install Typst.Typst

# Converter MD para PDF
pandoc arquivo.md -o arquivo.pdf --pdf-engine=typst --toc --number-sections
```

**Template personalizado:**
```bash
# Com template customizado
pandoc arquivo.md -o arquivo.pdf \
  --pdf-engine=typst \
  --template=template.typ \
  --toc \
  --number-sections \
  -V mainfont="Times New Roman" \
  -V geometry:margin=3cm
```

---

### 2. 🥈 md-to-pdf (NPM)

**Eficiência: ⭐⭐⭐⭐**

| Aspecto | Detalhe |
|---------|---------|
| **Custo** | Gratuito (open source) |
| **Qualidade** | Alta (baseada em CSS/Chrome) |
| **Velocidade** | Rápida (~2-5s) |
| **Instalação** | NPM (~100MB com Chromium) |
| **Curva de aprendizado** | Baixa |

**Vantagens:**
- Totalmente estilizável com CSS moderno
- Suporte a fontes web (Google Fonts)
- Modo watch para desenvolvimento
- Headers/footers dinâmicos com paginação
- Fidelidade visual perfeita (motor do Chrome)

**Limitações:**
- Não possui paginação editorial avançada
- Requer Chromium instalado

**Como usar:**
```bash
# Instalar
npm install -g md-to-pdf

# Converter
md-to-pdf arquivo.md

# Com opções
md-to-pdf arquivo.md --stylesheet=custom.css --pdf-options='{"format":"A4","margin":{"top":"20mm"}}'
```

**CSS para headers/footers:**
```css
@page {
  @top-center { content: "Título do Livro"; }
  @bottom-center { content: "Página " counter(page) " de " counter(pages); }
}
```

---

### 3. 🥉 Pandoc + XeLaTeX

**Eficiência: ⭐⭐⭐**

| Aspecto | Detalhe |
|---------|---------|
| **Custo** | Gratuito (open source) |
| **Qualidade** | Excelente (acadêmica/editorial) |
| **Velocidade** | Lenta (~10-30s) |
| **Instalação** | Pesada (~3-5GB com TeX Live) |
| **Curva de aprendizado** | Média/Alta |

**Vantagens:**
- Padrão ouro para documentos acadêmicos
- Suporte completo a bibliografias (BibTeX/CSL)
- Fórmulas matemáticas avançadas
- Controle preciso de tipografia

**Limitações:**
- Instalação pesada (TeX Live)
- Compilação lenta
- Erros difíceis de depurar

**Como usar:**
```bash
# Instalar Pandoc + MiKTeX ou TeX Live
winget install JohnMacFarlane.Pandoc

# Converter
pandoc arquivo.md -o arquivo.pdf --pdf-engine=xelatex --toc --number-sections
```

---

### 4. WeasyPrint (Python)

**Eficiência: ⭐⭐⭐**

| Aspecto | Detalhe |
|---------|---------|
| **Custo** | Gratuito (open source) |
| **Qualidade** | Alta (focada em Paged Media) |
| **Velocidade** | Média (~5-15s) |
| **Instalação** | Média (~200MB) |
| **Curva de aprendizado** | Média |

**Vantagens:**
- Suporte completo a CSS Paged Media
- Margens espelhadas para livros (`@page :left/:right`)
- Controle preciso de quebras de página
- Não requer navegador

**Limitações:**
- Não renderiza JavaScript
- Suporte limitado a CSS moderno

**Como usar:**
```bash
# Instalar
pip install weasyprint

# Converter (via HTML intermediário)
pandoc arquivo.md -o arquivo.html
weasyprint arquivo.html arquivo.pdf
```

---

### 5. Puppeteer/Playwright (HTML → PDF)

**Eficiência: ⭐⭐**

| Aspecto | Detalhe |
|---------|---------|
| **Custo** | Gratuito (open source) |
| **Qualidade** | Alta (motor do Chrome) |
| **Velocidade** | Rápida (~2-5s) |
| **Instalação** | Média (~300MB com Chromium) |
| **Curva de aprendizado** | Média |

**Vantagens:**
- Fidelidade visual perfeita
- Suporte a CSS moderno
- Headers/footers dinâmicos

**Limitações:**
- Requer Chromium
- Não possui paginação editorial avançada

**Como usar:**
```javascript
const puppeteer = require('puppeteer');
const marked = require('marked');

async function convertMdToPdf(mdFile, pdfFile) {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  const html = marked.parse(fs.readFileSync(mdFile, 'utf8'));
  await page.setContent(html);
  
  await page.pdf({
    path: pdfFile,
    format: 'A4',
    margin: { top: '20mm', bottom: '20mm', left: '25mm', right: '25mm' },
    printBackground: true,
    headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:10px;text-align:center;width:100%">Página <span class="pageNumber"></span> de <span class="totalPages"></span></div>'
  });
  
  await browser.close();
}
```

---

### 6. Quarto

**Eficiência: ⭐⭐**

| Aspecto | Detalhe |
|---------|---------|
| **Custo** | Gratuito (open source) |
| **Qualidade** | Excelente (científica) |
| **Velocidade** | Média |
| **Instalação** | Média (~500MB) |
| **Curva de aprendizado** | Média |

**Vantagens:**
- Framework completo de publicação
- Suporte a múltiplos formatos (PDF, HTML, EPUB)
- Código executável embutido
- Gestão automática de dependências

**Limitações:**
- Mais complexo que necessário para apenas MD→PDF
- Focado em documentos científicos

---

### 7. wkhtmltopdf

**Eficiência: ⭐**

| Aspecto | Detalhe |
|---------|---------|
| **Custo** | Gratuito (open source) |
| **Qualidade** | Média |
| **Velocidade** | Rápida |
| **Instalação** | Leve |
| **Curva de aprendizado** | Baixa |

**Limitações:**
- Tecnologia desatualizada (WebKit antigo)
- Qualidade inferior às opções modernas
- Não suporta CSS moderno

---

## 📊 Tabela Comparativa Final

| Ferramenta | Qualidade | Velocidade | Instalação | Recomendação |
|------------|-----------|------------|------------|--------------|
| **Pandoc + Typst** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 🏆 **MELHOR ESCOLHA** |
| **md-to-pdf** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 🥈 Boa alternativa |
| **Pandoc + XeLaTeX** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | 🥉 Para acadêmicos |
| **WeasyPrint** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Para Python |
| **Puppeteer** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | Para web devs |
| **Quarto** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Para científicos |
| **wkhtmltopdf** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ❌ Não recomendado |

---

## 🎯 Recomendação Final

### Para este projeto (Fábrica Agêntica de Livros):

**Use Pandoc + Typst** porque:
1. **Velocidade**: Compila 238 capítulos em segundos
2. **Qualidade**: Tipografia profissional moderna
3. **Leveza**: Instalação mínima (~50MB)
4. **Integração**: Compatível com o compilador existente
5. **Gratuito**: 100% open source

### Script de Conversão

```bash
#!/bin/bash
# converter-todos-livros.sh

OUTPUT_DIR="fabrica-de-livros/output"

for livro in $OUTPUT_DIR/*/; do
  slug=$(basename "$livro")
  
  if [ -f "$livro/livro_final.md" ]; then
    echo "Convertendo: $slug"
    
    pandoc "$livro/livro_final.md" \
      -o "$livro/livro_final.pdf" \
      --pdf-engine=typst \
      --toc \
      --number-sections \
      -V mainfont="Times New Roman" \
      -V geometry:margin=3cm \
      -V fontsize=12pt \
      -V documentclass=book
    
    echo "  ✅ $slug convertido"
  fi
done

echo "Conversão concluída!"
```

---

## 📋 Próximos Passos

1. **Instalar Typst**: `winget install Typst.Typst`
2. **Instalar Pandoc**: `winget install JohnMacFarlane.Pandoc`
3. **Testar conversão**: `pandoc teste.md -o teste.pdf --pdf-engine=typst`
4. **Adaptar template**: Criar `template.typ` personalizado
5. **Executar conversão em massa**: Rodar script de conversão
