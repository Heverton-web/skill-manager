#!/usr/bin/env python3
"""
Dados das 5 Séries de Livros de Perfumaria (P1-P5)
Cada série tem 10 livros, cada livro tem 4 Partes e 16 Capítulos (EITA-V2).
Usado por gerar-livros-perfumaria.py e compilar-para-pdf.py
"""

SERIES_PERFUMARIA = {
    "P1": {"nome": "Fundamentos da Perfumaria e Concentrações", "prefixo": "P1"},
    "P2": {"nome": "O Universo da Perfumaria Árabe e Oriental", "prefixo": "P2"},
    "P3": {"nome": "Sazonalidade, Clima e Ocasiões", "prefixo": "P3"},
    "P4": {"nome": "Aplicação, Conservação e Cuidados", "prefixo": "P4"},
    "P5": {"nome": "Comportamento, Psicologia dos Aromas e Estilo", "prefixo": "P5"},
}

# Títulos das Partes por série (4 partes × 4 capítulos = 16 capítulos)
SERIES_PARTES = {
    "P1": ["Fundamentos da Perfumaria", "Concentrações e Técnicas", "Aplicação e Escolha Consciente", "Aprofundamento e Tendências"],
    "P2": ["Raízes da Perfumaria Árabe", "Ingredientes e Notas Orientais", "Rituais e Experiência Sensorial", "Cultura, Mercado e Futuro"],
    "P3": ["Estações e Climas", "Ocasiões e Ambientes", "Assinatura e Estilo Pessoal", "Planejamento e Adaptação"],
    "P4": ["Fundamentos da Aplicação", "Técnicas de Performance", "Conservação e Cuidados", "Erros, Mitos e Soluções"],
    "P5": ["Psicologia e Comportamento", "Memória, Emoção e Identidade", "Estilo e Consumo Consciente", "Mercado, Ética e Futuro"],
}

# slug -> (nome, titulo_obra, subtitulo, introducao, conclusao, capitulo1_explica)
LIVROS_PERFUMARIA = {
    # ═══════════════ SÉRIE P1 — FUNDAMENTOS DA PERFUMARIA E CONCENTRAÇÕES ═══════════════
    "P1-01-guia-definitivo-das-concentracoes": (
        "O Guia Definitivo das Concentrações",
        "O Guia Definitivo das Concentrações: Entenda a diferença real entre Eau de Cologne, EDT, EDP, Extratos e Óleos",
        "Entenda a diferença real entre Eau de Cologne, EDT, EDP, Extratos e Óleos",
        "Eau de Cologne, EDT, EDP, Extrait, óleos concentrados — rótulos que confundem até apreciadores experientes. Este livro desmonta, um a um, os níveis de concentração da perfumaria e mostra o que realmente muda entre eles: intensidade, projeção, fixação e preço.",
        "A concentração é o primeiro filtro de escolha de um perfume, mas não é o único. Saber o que cada rótulo significa — e o que ele não garante — transforma a compra em decisão consciente e permite montar um guarda-roupa olfativo equilibrado.",
        "Concentração é a proporção de essência perfumada diluída em álcool e água. Eau de Cologne usa entre 2% e 5% de essência; Eau de Toilette, entre 5% e 15%; Eau de Parfum, entre 15% e 20%; Extrait (ou Parfum), acima de 20%, chegando a 40% em criações artesanais [1]. Os óleos concentrados e attars, por sua vez, são essências quase puras, usadas sem álcool e aplicadas em pequenas gotas [2].\n\n**Por que importa?** A concentração influencia a projeção (quanto o perfume irradia), a fixação (quanto dura na pele) e o custo final. Mas concentração alta não significa automaticamente perfume melhor: a qualidade das matérias-primas e o equilíbrio da fórmula contam tanto quanto a dosagem.\n\n**O que muda na prática:** Perfumes mais concentrados exigem menos borrifadas, funcionam melhor em climas frios e costumam evoluir de forma mais lenta e rica na pele. Já as concentrações leves são ideais para calor intenso, uso diário e ambientes fechados [3]."
    ),
    "P1-02-o-mito-da-fixacao": (
        "O Mito da Fixação",
        "O Mito da Fixação: Por que a fixação de um perfume varia de pele para pele e como a química corporal influencia",
        "Por que a fixação de um perfume varia de pele para pele e como a química corporal influencia",
        "O mesmo perfume dura oito horas na sua pele e apenas duas na do seu amigo. A fixação não depende só da fragrância: a química corporal, o pH, a temperatura e até a alimentação interferem. Este livro explica, com base científica, por que isso acontece e como você pode prever — e melhorar — a duração dos seus perfumes.",
        "A fixação é um diálogo entre a fragrância e a sua pele, não uma característica absoluta do frasco. Entender os fatores que regem essa interação permite escolher melhor, aplicar melhor e abandonar de vez o mito de que existe um único padrão de duração.",
        "A fixação é o tempo durante o qual uma fragrância permanece perceptível após a aplicação. Ela depende de três grupos de fatores: as moléculas do perfume (tamanho, volatilidade e persistência), a pele de quem usa (pH, oleosidade, temperatura e hidratação) e o ambiente (umidade e temperatura externas) [1].\n\n**Por que importa?** Peles mais oleosas retêm moléculas apolares por mais tempo; peles secas evaporam rapidamente as notas de saída. O pH da pele altera a percepção dos acordes: variações de 4,5 a 6,5 modificam a intensidade percebida de notas cítricas e almiscaradas [2].\n\n**O que muda na prática:** Em vez de trocar de perfume quando a duração decepciona, ajuste a camada: hidrate a pele, aplique em pontos de pulso quentes e evite esfregar os pulsos, pois a fricção quebra as moléculas mais frágeis [3]."
    ),
    "P1-03-oleos-concentrados-e-attars": (
        "O Que São Óleos Concentrados e Attars?",
        "O Que São Óleos Concentrados e Attars?: A tradição milenar da perfumaria oriental sem álcool",
        "A tradição milenar da perfumaria oriental sem álcool",
        "Antes do álcool dominar a perfumaria, o Oriente já produzia fragrâncias com óleos puros. Os attars — essências destiladas de flores, madeiras e especiarias — representam uma tradição de séculos que sobrevive até hoje. Este livro mergulha nesse universo e ensina a usar óleos concentrados com técnica.",
        "Os óleos concentrados e attars não são uma alternativa inferior aos perfumes alcoólicos: são uma escola perfumística completa, com estética, ritmo e protocolos próprios. Dominá-los amplia o repertório de quem deseja explorar a perfumaria em sua forma mais pura.",
        "Attar (ou ittar) é uma fragrância tradicional sem álcool, obtida por destilação de matérias-primas naturais em óleo de sândalo ou em base gordurosa, prática que remonta à Índia e ao Oriente Médio há mais de mil anos [1]. Por não conter álcool, o attar fixa-se de forma diferente: evapora mais lentamente e adere à pele por contato direto com os óleos naturais [2].\n\n**Por que importa?** Óleos concentrados são mais densos e econômicos — algumas gotas bastam. São também a escolha clássica para quem busca perfumes sem etanol, como em contextos religiosos ou para peles sensíveis.\n\n**O que muda na prática:** Aplique attar no pulso, atrás das orelhas e na nuca sem esfregar. Como não há álcool para evaporar, o aroma surge gradualmente e pode durar o dia inteiro — e até manchar tecidos claros, exigindo cuidado na aplicação [3]."
    ),
    "P1-04-o-processo-de-maceracao": (
        "O Processo de Maceração",
        "O Processo de Maceração: Por que os perfumes artesanais e árabes melhoram (e amadurecem) com o tempo no frasco",
        "Por que os perfumes artesanais e árabes melhoram (e amadurecem) com o tempo no frasco",
        "Perfumistas árabes e artesanais sabem: um perfume recém-envasado não é o mesmo meses depois. A maceração é o período em que a mistura de essências, álcool e água se harmoniza. Este livro explica o que acontece quimicamente nesse processo e como você pode acelerá-lo — ou estragá-lo.",
        "A maceração é uma das etapas mais mal compreendidas da perfumaria. Entender por que um frasco melhora com o tempo permite comprar com antecedência, armazenar corretamente e reconhecer quando uma fragrância atingiu — ou passou — seu ponto ideal.",
        "Maceração é o descanso da mistura perfumada após o envasamento, período em que as moléculas de essência se dissolvem completamente e os acordes se equilibram [1]. Em perfumes artesanais, o processo pode durar de semanas a meses, e muitos artesãos consideram que a fragrância só está pronta após esse amadurecimento [2].\n\n**Por que importa?** Durante a maceração, notas de saída se suavizam, o álcool perde o impacto inicial e a projeção se torna mais coesa. Por isso, frascos de uma mesma leva podem cheirar diferentes em momentos distintos.\n\n**O que muda na prática:** Guarde o frasco em local escuro, fresco e sem oscilações de temperatura. Gire a tampa ocasionalmente para oxigenar sem agitar. Perfumes árabes e artesanais costumam revelar seu potencial máximo entre três e seis meses de maceração [3]."
    ),
    "P1-05-edp-vs-perfume-solido": (
        "Eau de Parfum vs. Perfume Sólido",
        "Eau de Parfum vs. Perfume Sólido: Conheça formatos alternativos e portáteis de fragrâncias",
        "Conheça formatos alternativos e portáteis de fragrâncias",
        "Nem toda fragrância mora em um frasco de vidro com borrifador. O perfume sólido — base de cera e óleos — é um formato antigo que voltou com força, enquanto o EDP segue como padrão de mercado. Este livro compara os dois formatos sob todos os ângulos práticos.",
        "EDP e perfume sólido não competem: complementam-se. O primeiro entrega projeção e ritual; o segundo, discrição, portabilidade e controle absoluto da aplicação. Conhecer as diferenças permite usar cada formato no momento certo.",
        "O Eau de Parfum (EDP) é a concentração mais vendida do mundo, com 15% a 20% de essência em base alcoólica, projetado para projetar por horas [1]. O perfume sólido, por sua vez, é produzido com cera (geralmente de candelilla ou cera de abelha), óleo de coco ou jojoba e essências, sem álcool [2].\n\n**Por que importa?** O sólido viaja sem restrições de líquidos, não derrama e permite aplicar com precisão cirúrgica. A desvantagem é a projeção curta e a intensidade menor em comparação ao EDP.\n\n**O que muda na prática:** Use o sólido para retoques discretos, escritório e viagens; reserve o EDP para ocasiões que pedem presença. Muitos apreciadores combinam os dois: EDP de manhã e sólido para renovação ao longo do dia [3]."
    ),
    "P1-06-notas-acordes-piramide-olfativa": (
        "Notas, Acordes e Pirâmide Olfativa",
        "Notas, Acordes e Pirâmide Olfativa: Como ler a evolução de um perfume da abertura até o fundo",
        "Como ler a evolução de um perfume da abertura até o fundo",
        "Todo perfume conta uma história em três atos: as notas de saída, que chegam primeiro; o coração, que sustenta a identidade; e o fundo, que permanece na pele. Este livro ensina a ler essa evolução — a pirâmide olfativa — e a interpretar qualquer fragrância com o vocabulário dos perfumistas.",
        "A pirâmide olfativa não é apenas uma ferramenta de marketing: é um mapa da evolução temporal de uma fragrância. Saber lê-la transforma a experiência de usar perfume e permite comparar, descrever e escolher com precisão.",
        "A pirâmide olfativa organiza as notas de um perfume por volatilidade. As notas de saída (topo) são moléculas leves e cítricas que evaporam nos primeiros 15 minutos; as de coração formam o corpo da fragrância por até 4 horas; e as de fundo, pesadas e resinosas, permanecem por horas ou dias [1]. Acordes são combinações de duas ou mais notas que criam uma impressão única, como o acorde fougère [2].\n\n**Por que importa?** Julgar um perfume pelos primeiros minutos é o erro mais comum: a abertura pode ser agressiva e o coração, sublime — ou o contrário.\n\n**O que muda na prática:** Ao testar, espere pelo menos 30 minutos e avalie em três momentos: abertura, coração e fundo. Anote cada fase em um caderno olfativo e compare fragrâncias na mesma etapa de evolução [3]."
    ),
    "P1-07-familias-olfativas-descomplicadas": (
        "Famílias Olfativas Descomplicadas",
        "Famílias Olfativas Descomplicadas: Descubra se você é do time Cítrico, Amadeirado, Oriental, Floral ou Fougère",
        "Descubra se você é do time Cítrico, Amadeirado, Oriental, Floral ou Fougère",
        "Cítrico, floral, amadeirado, oriental, fougère, chipre — as famílias olfativas são o mapa mais antigo da perfumaria. Este livro traduz essa classificação para o dia a dia e ajuda você a descobrir qual território combina com a sua personalidade e o seu estilo.",
        "As famílias olfativas não são caixas rígidas, mas territórios com fronteiras fluidas. Conhecê-las permite pedir recomendações precisas, entender o que você já gosta e ampliar o repertório com descobertas seguras.",
        "As famílias olfativas foram sistematizadas pela perfumaria francesa no século XX para organizar a crescente variedade de criações [1]. As principais são: cítrica (limão, bergamota, neroli), floral (rosa, jasmim, tuberosa), amadeirada (sândalo, cedro, vetiver), oriental (âmbar, baunilha, especiarias), fougère (lavanda, musgo, cumarina) e chipre (bergamota, musgo de carvalho, patchouli) [2].\n\n**Por que importa?** Cada família tende a funcionar melhor em certas estações e ocasiões: cítricos brilham no calor, orientais aquecem o inverno, florais dominam o dia a dia.\n\n**O que muda na prática:** Teste um representante de cada família em fitas olfativas, lado a lado, e anote qual despertou reação. Esse exercício simples constrói seu mapa olfativo pessoal em poucas semanas [3]."
    ),
    "P1-08-materias-primas-naturais-vs-sinteticas": (
        "Matérias-Primas Naturais vs. Sintéticas",
        "Matérias-Primas Naturais vs. Sintéticas: O papel da biotecnologia e dos florais sintéticos na perfumaria moderna",
        "O papel da biotecnologia e dos florais sintéticos na perfumaria moderna",
        "Óleo de rosa de Taif ao lado de moléculas criadas em laboratório: a perfumaria moderna transita entre o natural e o sintético com mais nuances do que a maioria imagina. Este livro desfaz a dicotomia simplista e mostra o papel da biotecnologia, dos sintéticos e da sustentabilidade nas fragrâncias atuais.",
        "Natural não é sinônimo automático de melhor, e sintético não é sinônimo de inferior. A perfumaria contemporânea combina ambos por razões de sustentabilidade, consistência e criatividade — e entender essa síntese é essencial para avaliar qualquer fragrância.",
        "Matérias-primas naturais são extraídas de plantas, animais e minerais — como o sândalo, o jasmim e o almíscar —, enquanto as sintéticas são criadas em laboratório, como o calone (nota aquática) e o Iso E Super (nota amadeirada) [1]. A biotecnologia entrou no setor produzindo moléculas idênticas às naturais por fermentação, como o vetiver e o sândalo sustentáveis [2].\n\n**Por que importa?** Muitos florais naturais são caríssimos e instáveis; os sintéticos garantem consistência e preço acessível. A pressão por sustentabilidade — e a escassez de espécies — empurra a indústria para alternativas biotecnológicas.\n\n**O que muda na prática:** Avalie a fragrância pelo resultado, não pelo rótulo. Perfumes com boa base sintética podem ter fixação superior a naturais mal extraídos — e o oposto também é verdade [3]."
    ),
    "P1-09-o-valor-do-artesanal": (
        "O Valor do Artesanal",
        "O Valor do Artesanal: O que diferencia uma produção em pequena escala da perfumaria industrial de massa",
        "O que diferencia uma produção em pequena escala da perfumaria industrial de massa",
        "Pequenas casas de perfumaria criam lotes limitados, com matérias-primas selecionadas e tempo de maceração generoso; a indústria de massa prioriza escala, consistência e custo. Este livro investiga o que realmente muda entre esses dois mundos — e o que você está pagando (ou economizando) em cada um.",
        "O artesanal não é automaticamente superior, mas entrega algo que a indústria raramente oferece: exclusividade, cuidado e narrativa. Saber reconhecer o valor real de cada produção permite decisões de compra mais conscientes e prazerosas.",
        "A perfumaria artesanal opera em pequena escala: lotes limitados, matérias-primas selecionadas, maceração prolongada e controle manual de cada etapa [1]. A industrial, por sua vez, prioriza reprodutibilidade, prazo e custo, usando bases padronizadas e aceleração química de processos [2].\n\n**Por que importa?** O artesanal frequentemente usa essências naturais de alta qualidade e permite que o perfumista aceite variações de lote — uma riqueza que a indústria elimina por design.\n\n**O que muda na prática:** Ao escolher artesanal, espere diferenças entre lotes, preço mais alto e disponibilidade limitada. Ao escolher industrial, espere consistência total e menor custo. O ideal é ter ambos no guarda-roupa olfativo [3]."
    ),
    "P1-10-testando-perfumes-corretamente": (
        "Testando Perfumes Corretamente",
        "Testando Perfumes Corretamente: O guia definitivo de como usar as fitas olfativas (blotters) e a pele sem saturar o olfato",
        "O guia definitivo de como usar as fitas olfativas (blotters) e a pele sem saturar o olfato",
        "Nariz entupido, fitas amassadas, decisão errada: testar perfumes é uma habilidade que quase ninguém domina. Este livro ensina o protocolo completo — do blotter à pele — para avaliar fragrâncias com precisão e sem fadiga olfativa.",
        "Testar perfume é um exercício técnico que se aprende. Com os protocolos certos de fita, pele, tempo e higiene do nariz, você passa a escolher fragrâncias com confiança, economiza dinheiro e reduz drasticamente o risco de arrependimento.",
        "O blotter (fita olfativa) é a ferramenta padrão de avaliação: papel poroso que recebe o perfume e permite cheirar sem contaminar a pele [1]. O protocolo correto envolve borrifar a fita a 10 centímetros, aguardar 30 segundos para o álcool evaporar e cheirar em ondas, com pausas e recheiradas de café ou pele limpa entre amostras [2].\n\n**Por que importa?** O olfato satura em minutos: avaliar mais de quatro ou cinco fragrâncias seguidas compromete o julgamento. A pele, por sua vez, revela o verdadeiro comportamento do perfume, pois reage com o pH individual.\n\n**O que muda na prática:** Divida a avaliação em duas etapas: triagem em blotters (até cinco) e teste final na pele (no máximo duas). Anote horários e reavalie a cada 30 minutos [3]."
    ),

    # ═══════════════ SÉRIE P2 — O UNIVERSO DA PERFUMARIA ÁRABE E ORIENTAL ═══════════════
    "P2-01-a-anatomia-do-oud": (
        "A Anatomia do Oud",
        "A Anatomia do Oud: Desvendando a madeira mais nobre, preciosa e misteriosa do Oriente Médio",
        "Desvendando a madeira mais nobre, preciosa e misteriosa do Oriente Médio",
        "O oud — ou agarwood — é a matéria-prima mais cara e enigmática da perfumaria mundial. Nascido da infecção de uma árvore, esse óleo denso e resinoso é o coração do luxo árabe. Este livro desvenda sua origem, seus perfis olfativos e os desafios de um mercado dominado pela escassez.",
        "O oud é mais que um ingrediente: é um símbolo de status, tradição e misticismo. Compreender sua anatomia — da árvore ao óleo, do cru ao cozido — permite apreciar, escolher e pagar o preço justo por uma das matérias-primas mais raras do planeta.",
        "O oud é produzido a partir da madeira da árvore Aquilaria infectada por um fungo, que reage criando uma resina escura e aromática chamada agarwood [1]. O óleo é extraído por destilação a vapor e classificado por origem (Cambodia, Índia, Malásia), idade e intensidade resinosa — fatores que podem elevar o preço a dezenas de milhares de dólares por quilo [2].\n\n**Por que importa?** O perfil olfativo do oud varia do doce e balsâmico ao animal e medicinal, e é um dos ingredientes mais duradouros da perfumaria.\n\n**O que muda na prática:** Ao comprar, desconfie de preços muito baixos: boa parte do oud comercial é sintética ou diluída. Cheire o cru na pele e avalie a evolução por horas antes de investir [3]."
    ),
    "P2-02-rosa-de-taif-acafrao-e-especiarias": (
        "Rosa de Taif, Açafrão e Especiarias",
        "Rosa de Taif, Açafrão e Especiarias: Os pilares aromáticos das criações árabes de luxo",
        "Os pilares aromáticos das criações árabes de luxo",
        "Rosa de Taif, açafrão, cardamomo, açúcar queimado: a perfumaria árabe constrói suas obras-primas sobre um punhado de ingredientes icônicos. Este livro apresenta cada um desses pilares, seu cultivo, sua extração e o papel que desempenham nas criações de luxo do Oriente Médio.",
        "A rosa de Taif e o açafrão são a assinatura da perfumaria árabe de luxo: ingredientes raros, caros e carregados de significado cultural. Conhecê-los em profundidade é a chave para decifrar o estilo oriental e reconhecer criações autênticas.",
        "A rosa de Taif, cultivada nas montanhas da Arábia Saudita, produz um dos absolutos mais apreciados da perfumaria, com notas de mel, especiarias e geleia de rosa [1]. O açafrão — a especiaria mais cara do mundo — traz um toque metálico, couro e medicinal às composições árabes de luxo, frequentemente combinado a cardamomo, noz-moscada e pimenta [2].\n\n**Por que importa?** Esses ingredientes definem o DNA olfativo árabe: rico, denso, especiado e imediatamente reconhecível.\n\n**O que muda na prática:** Ao avaliar uma criação árabe, procure a interação rosa–açafrão no coração e a progressão para fundos ambarados. Criações autênticas preservam essas notas sem mascará-las com açúcar [3]."
    ),
    "P2-03-o-encanto-do-ambar-e-das-resinas": (
        "O Encanto do Âmbar e das Resinas",
        "O Encanto do Âmbar e das Resinas: Como notas balsâmicas e resinas densas criam rastros magnéticos",
        "Como notas balsâmicas e resinas densas criam rastros magnéticos",
        "Âmbar, benjoim, olíbano, mirra: as resinas são os materiais que conferem profundidade, calor e aquele rastro inconfundível aos perfumes orientais. Este livro explica o que é o acorde âmbar, como as resinas são coletadas e por que elas fixam tão bem.",
        "O âmbar e as resinas são a espinha dorsal da perfumaria oriental: sem eles, não há calor, não há profundidade, não há rastro. Entender esses materiais revela por que certas fragrâncias parecem envolver quem está ao redor.",
        "O acorde âmbar — um dos mais antigos da perfumaria — combina baunilha, benjoim, ládano e estoraque para criar um efeito quente, doce e envolvente [1]. As resinas, como olíbano e mirra, são exsudadas de árvores e destiladas em absolutos densos e balsâmicos, usados tanto em perfumes quanto em incensos religiosos [2].\n\n**Por que importa?** Moléculas pesadas e de baixa volatilidade — típicas das resinas — ancoram a fragrância na pele e geram o rastro (sillage) longo característico dos orientais.\n\n**O que muda na prática:** Teste resinas puras em fitas para treinar o nariz: olíbano, mirra e benjoim têm personalidades muito distintas. Em composições, procure a harmonia entre o âmbar doce e a secura das resinas [3]."
    ),
    "P2-04-mistura-de-culturas": (
        "Mistura de Culturas",
        "Mistura de Culturas: Como a perfumaria ocidental e a oriental se fundem nas tendências globais atuais",
        "Como a perfumaria ocidental e a oriental se fundem nas tendências globais atuais",
        "Casas francesas usando oud, casas árabes criando florais ocidentais: as fronteiras da perfumaria nunca estiveram tão porosas. Este livro analisa como a fusão entre Ocidente e Oriente define as tendências globais atuais e cria novas estéticas olfativas.",
        "A fusão cultural é o motor criativo da perfumaria contemporânea. Compreender como técnicas e ingredientes atravessam fronteiras permite antecipar tendências e apreciar criações híbridas com repertório.",
        "Historicamente, a perfumaria ocidental priorizou flores, frescor e simetria, enquanto a oriental apostou em densidade, especiarias e longevidade [1]. A partir dos anos 2000, o oud invadiu o mercado ocidental de nicho, e casas árabes passaram a dominar a estética gourmand ocidental — criando um vocabulário híbrido [2].\n\n**Por que importa?** Essa mistura gerou os chamados \"orientais modernos\": fragrâncias com coração floral ocidental e fundo ambarado/oud oriental, que dominam o mercado de luxo.\n\n**O que muda na prática:** Ao explorar tendências, teste criações híbridas com atenção à proporção: o equilíbrio entre frescor e densidade define o sucesso da fusão [3]."
    ),
    "P2-05-camadas-olfativas-layering": (
        "Camadas Olfativas (Layering)",
        "Camadas Olfativas (Layering): O ritual árabe de combinar dois ou mais perfumes para criar uma assinatura única",
        "O ritual árabe de combinar dois ou mais perfumes para criar uma assinatura única",
        "No Oriente Médio, usar um único perfume é incomum: a tradição combina camadas de fragrâncias para construir assinaturas complexas e pessoais. Este livro ensina o ritual do layering — da escolha das bases ao protocolo de aplicação — com regras práticas para não errar.",
        "O layering é uma das tradições mais sofisticadas da perfumaria árabe — e uma das mais mal executadas no Ocidente. Dominar as regras de combinação transforma dois ou três frascos comuns em um sistema infinito de assinaturas pessoais.",
        "Layering é a arte de sobrepor duas ou mais fragrâncias para criar um efeito único. A tradição árabe recomenda combinar um óleo corporal ou attar de base com um perfume de cobertura, respeitando famílias complementares: amadeirado com oriental, floral com âmbar [1]. A regra de ouro é a hierarquia: a fragrância mais intensa define o coração, e as demais enriquecem os detalhes [2].\n\n**Por que importa?** Feito certo, o layering cria rastro personalizado e durabilidade superior — feito errado, gera uma mistura turva e enjoativa.\n\n**O que muda na prática:** Comece combinando fragrâncias da mesma família. Aplique a base nos pontos de pulso e a cobertura nas roupas ou nuca. Anote as combinações que funcionaram e as que falharam [3]."
    ),
    "P2-06-perfumes-para-ambientes-bakhoor": (
        "Perfumes para Ambientes e Roupas (Bakhoor)",
        "Perfumes para Ambientes e Roupas (Bakhoor e Bukhoor): A tradição de perfumar o lar e os tecidos com fumaça aromática",
        "A tradição de perfumar o lar e os tecidos com fumaça aromática",
        "O bakhoor — madeiras e resinas perfumadas queimadas em incensários — é o ritual de hospitalidade e acolhimento do mundo árabe. Este livro explora a tradição de perfumar casas, roupas e cabelos com fumaça aromática e como incorporá-la ao cotidiano.",
        "O bakhoor é cultura viva: receber visitas com a casa perfumada é um gesto de honra no Oriente Médio. Compreender a tradição e seus protocolos permite recriar essa experiência de acolhimento em qualquer lar.",
        "Bakhoor são lascas de madeira — geralmente oud — embebidas em óleos e resinas aromáticas, queimadas em um incensário (mabkhara) para perfumar ambientes, roupas e até cabelos [1]. O ritual acompanha recepções, celebrações e orações, e cada região tem suas receitas características [2].\n\n**Por que importa?** A fumaça adere aos tecidos de forma duradoura, criando uma assinatura de lar que permanece por dias.\n\n**O que muda na prática:** Para reproduzir o ritual, use um incensário elétrico ou aceso com brasas, passe a fumaça sob as roupas no cabide e ventile o ambiente após 15 minutos. Em espaços pequenos, o bakhoor pode ser intenso demais — use com parcimônia [3]."
    ),
    "P2-07-almiscar-branco-vs-negro": (
        "Almíscar Branco vs. Almíscar Negro",
        "Almíscar (Musk) Branco vs. Almíscar Negro: Entenda as nuances e a sensualidade dessas notas na perfumaria oriental",
        "Entenda as nuances e a sensualidade dessas notas na perfumaria oriental",
        "O almíscar é a nota mais sensual da perfumaria oriental — e a mais mal compreendida. Branco, negro, cinza, floral: cada variação conta uma história diferente. Este livro compara os almíscares e ensina a reconhecer suas nuances na prática.",
        "O almíscar atravessou a história da perfumaria: proibido em sua forma animal, renasceu em versões sintéticas e florais. Dominar a diferença entre branco e negro — e seus intermediários — é essencial para entender a sensualidade oriental.",
        "Historicamente, o almíscar era extraído da glândula do cervo-almiscareiro, prática hoje proibida e substituída por moléculas sintéticas e vegetais [1]. O almíscar branco é limpo, suave e levemente adocicado — associado a roupas lavadas e pele limpa —, enquanto o almíscar negro (ou animal) é denso, terroso e intensamente sensual, com notas de couro e suor [2].\n\n**Por que importa?** O branco domina o mercado de beleza ocidental; o negro, o luxo árabe. Ambos potencializam outras notas e são fixadores naturais de composições.\n\n**O que muda na prática:** Compare em fitas: branco evoca limpeza, negro evoca pele e profundidade. Criações árabes costumam combiná-los com âmbar e oud para sensualidade máxima [3]."
    ),
    "P2-08-a-magia-do-mel-e-dos-frutados": (
        "A Magia do Mel e dos Frutados Orientais",
        "A Magia do Mel e dos Frutados Orientais: Como as notas adocicadas ganham sofisticação nas mãos dos perfumistas árabes",
        "Como as notas adocicadas ganham sofisticação nas mãos dos perfumistas árabes",
        "Doce não é sinônimo de infantil: no mundo árabe, o mel, os frutos secos e os frutados densos ganham camadas de especiarias, resinas e madeiras. Este livro explora como os perfumistas orientais transformam açúcar em sofisticação.",
        "A perfumaria árabe prova que o doce pode ser adulto, profundo e luxuoso. Entender as técnicas que elevam notas adocicadas — do mel ao damasco — revela uma das faces mais ricas da estética oriental.",
        "O mel é um dos materiais mais antigos da perfumaria, usado como doce e fixador. Na tradição árabe, ele aparece ao lado de tâmaras, damasco, figo e frutas secas, temperados com açafrão, cardamomo e resinas para evitar o efeito enjoativo [1]. Os frutados orientais, como o damasco turco e o figo preto, são densos e quase balsâmicos, diferente dos frutados aquáticos ocidentais [2].\n\n**Por que importa?** A sofisticação vem do contraste: o doce oriental nunca fica sozinho — sempre carrega um contrapeso especiado, ambarado ou amadeirado.\n\n**O que muda na prática:** Ao avaliar gourmands árabes, procure a tensão entre doce e seco. Se um perfume doce não tem contrapeso, provavelmente é uma interpretação ocidental do estilo [3]."
    ),
    "P2-09-frascos-de-colecao": (
        "Frascos de Coleção",
        "Frascos de Coleção: A importância do design, do vidro pesado e dos detalhes metálicos na experiência do luxo árabe",
        "A importância do design, do vidro pesado e dos detalhes metálicos na experiência do luxo árabe",
        "Na perfumaria árabe, o frasco não é um recipiente: é parte da experiência. Vidro pesado, tampas metálicas, dourados, pedras e motivos islâmicos transformam cada lançamento em objeto de desejo. Este livro analisa o design como linguagem do luxo oriental.",
        "O frasco é o primeiro capítulo do perfume. No luxo árabe, o design comunica status, história e a origem das matérias-primas — e entender essa linguagem enriquece tanto a compra quanto a coleção.",
        "A estética dos frascos árabes reflete a cultura do luxo: vidro encorpado e escuro (frequentemente âmbar ou preto, que protegem o conteúdo da luz), tampas metálicas douradas ou prateadas, relevos, arabescos e pedras decorativas [1]. A escolha do vidro pesado não é acidental: transmite solidez e valor, e protege os óleos sensíveis da degradação luminosa [2].\n\n**Por que importa?** Para colecionadores, o frasco é parte do patrimônio; para marcas, é a assinatura visual que distingue o luxo oriental no mercado global.\n\n**O que muda na prática:** Ao colecionar, preserve os frascos da luz e guarde as caixas originais — elas valorizam o conjunto. Avalie o vidro escuro como sinal de cuidado com o conteúdo [3]."
    ),
    "P2-10-guia-de-pronuncia-e-nomes": (
        "Guia de Pronúncia e Nomes",
        "Guia de Pronúncia e Nomes: O significado por trás dos termos em árabe mais comuns nos rótulos de perfumes",
        "O significado por trás dos termos em árabe mais comuns nos rótulos de perfumes",
        "Oud, bakhoor, attar, mukhallat, taif, musk: os rótulos de perfumes árabes são repletos de termos que poucos sabem pronunciar ou traduzir. Este livro é o guia definitivo para decifrar nomes e significados — e para entender o que cada termo promete no frasco.",
        "Entender o vocabulário árabe da perfumaria não é pedantismo: é a chave para comprar com segurança e apreciar a cultura por trás dos rótulos. Cada termo carrega informação sobre origem, material e tradição.",
        "Termos essenciais: oud (madeira de agarwood), attar ou ittar (perfume sem álcool), bakhoor (incenso de madeira e resinas), mukhallat (mistura, combinação de vários perfumes), musk (almíscar), taif (referência à rosa cultivada na cidade de Taif) e mabkhara (incensário) [1]. A pronúncia segue o árabe moderno: \"oud\" soa como \"uud\", e \"attar\" como \"át-tar\" [2].\n\n**Por que importa?** Rótulos árabes autênticos usam esses termos com precisão; falsificações costumam empregá-los de forma genérica apenas para parecer orientais.\n\n**O que muda na prática:** Antes de comprar, verifique se o termo corresponde ao conteúdo: um \"mukhallat\" deve ser realmente uma mistura complexa, e um \"attar\" não deve conter álcool [3]."
    ),

    # ═══════════════ SÉRIE P3 — SAZONALIDADE, CLIMA E OCASIÕES ═══════════════
    "P3-01-o-guarda-roupa-olfativo": (
        "O Guarda-Roupa Olfativo",
        "O Guarda-Roupa Olfativo: Como escolher o perfume ideal para cada uma das quatro estações do ano",
        "Como escolher o perfume ideal para cada uma das quatro estações do ano",
        "Assim como o guarda-roupa de roupas, o guarda-roupa olfativo muda com as estações: cítricos e aquáticos no verão, orientais e gourmands no inverno. Este livro ensina a montar uma coleção equilibrada para o ano inteiro.",
        "Um guarda-roupa olfativo bem planejado tem um frasco para cada estação e ocasião. Compreender a lógica por trás dessa curadoria permite aproveitar cada fragrância no momento em que ela brilha.",
        "O clima afeta diretamente a performance dos perfumes: o calor acelera a evaporação das notas de saída e amplifica a projeção, enquanto o frio retém as moléculas pesadas e suaviza o rastro [1]. Por isso, verão pede frescor (cítricos, aquáticos, verdes) e inverno pede calor (orientais, gourmands, ambarados) [2].\n\n**Por que importa?** Usar um oriental denso sob 35°C pode resultar em enjoo — e um cítrico leve no inverno pode simplesmente desaparecer.\n\n**O que muda na prática:** Monte o guarda-roupa com, no mínimo, um frasco por estação, e teste cada fragrância na temperatura em que pretende usá-la [3]."
    ),
    "P3-02-perfumes-no-calor-extremo-do-brasil": (
        "Perfumes no Calor Extremo do Brasil",
        "Perfumes no Calor Extremo do Brasil: Quais fragrâncias árabes e orientais sobrevivem (e brilham) nas altas temperaturas",
        "Quais fragrâncias árabes e orientais sobrevivem (e brilham) nas altas temperaturas",
        "O Brasil é um país de calor intenso — e a perfumaria árabe, famosa pela densidade, parece desafiar essa realidade. Este livro mostra quais criações orientais realmente funcionam no calor tropical e como adaptar as demais.",
        "Não é preciso abandonar o universo árabe no calor brasileiro: a chave está na seleção de composições leves dentro desse estilo e na adaptação da aplicação. Saber escolher transforma o calor em aliado da projeção.",
        "No calor extremo, a evaporação é acelerada: notas de saída cítricas explodem, e fundos pesados podem saturar [1]. Algumas criações árabes são naturalmente adaptáveis — florais frescos com rosa e bergamota, cítricos orientais com leve toque ambarado — enquanto outras, como ouds densos, exigem aplicação mínima [2].\n\n**Por que importa?** O mercado brasileiro, com temperaturas médias altas, valoriza fragrâncias versáteis que não abafam no calor — e a perfumaria árabe percebeu esse movimento, criando linhas mais frescas.\n\n**O que muda na prática:** No calor, aplique em pontos discretos, evite roupas e use versões menores de concentração. Teste a fragrância por horas sob temperatura real antes de comprar [3]."
    ),
    "P3-03-conforto-para-dias-frios": (
        "Conforto para Dias Frios",
        "Conforto para Dias Frios: Notas aconchegantes, gourmands e especiadas perfeitas para o outono e inverno",
        "Notas aconchegantes, gourmands e especiadas perfeitas para o outono e inverno",
        "No frio, o perfume vira um abraço: notas de baunilha, âmbar, especiarias e madeiras aquecem o corpo e criam uma aura de conforto. Este livro mapeia as famílias e notas perfeitas para o outono e o inverno.",
        "O inverno é a estação dos perfumes densos e envolventes. Entender quais notas aquecem — e como elas se comportam no frio — permite construir uma coleção de conforto que dura o dia inteiro.",
        "No frio, a pele contrai e evapora menos, favorecendo moléculas pesadas: âmbar, baunilha, gourmands (caramelo, chocolate, café), especiarias (canela, cardamomo, cravo) e madeiras cremosas [1]. Essas notas criam o efeito aconchego — o perfume parece envolver quem está próximo [2].\n\n**Por que importa?** A fixação no frio é mais longa, mas a projeção é menor: perfumes que no verão seriam sufocantes tornam-se equilibrados e sofisticados.\n\n**O que muda na prática:** Aproveite o inverno para usar os frascos mais densos da coleção. Borrife em roupas e cachecóis com cuidado, pois alguns gourmands mancham tecidos claros [3]."
    ),
    "P3-04-a-scent-signature": (
        "A Scent Signature (Assinatura Olfativa)",
        "A Scent Signature (Assinatura Olfativa): Como encontrar a fragrância que fará as pessoas lembrarem de você",
        "Como encontrar a fragrância que fará as pessoas lembrarem de você",
        "Existem perfumes que as pessoas reconhecem antes de ver quem os usa. A assinatura olfativa é essa marca pessoal: uma fragrância que dialoga com a sua química, o seu estilo e a sua história. Este livro guia essa busca — que pode levar anos, mas transforma a relação com o perfume.",
        "A assinatura olfativa não se escolhe em uma tarde: ela se constrói. O processo envolve autoconhecimento, paciência e método — e o resultado é uma identidade que acompanha você em todas as ocasiões.",
        "Uma assinatura olfativa é a combinação de uma fragrância com a química corporal de quem a usa, criando um resultado único e reconhecível [1]. Perfumistas recomendam testar candidatas por períodos prolongados — dias a semanas — antes de decidir, pois o olfato se adapta e revela apenas com o tempo [2].\n\n**Por que importa?** A assinatura cria memória: as pessoas passam a associar seu cheiro à sua presença, um dos vínculos sociais mais poderosos.\n\n**O que muda na prática:** Escolha até três candidatas e alterne-as em períodos de duas semanas. Anote reações de outras pessoas e a sua própria satisfação. A vencedora vira sua assinatura [3]."
    ),
    "P3-05-perfumes-para-o-ambiente-de-trabalho": (
        "Perfumes para o Ambiente de Trabalho",
        "Perfumes para o Ambiente de Trabalho: O limite entre marcar presença e invadir o espaço alheio no escritório",
        "O limite entre marcar presença e invadir o espaço alheio no escritório",
        "No escritório, o perfume é uma declaração — e um risco. Um rastro intenso pode encantar uma reunião e irritar o colega ao lado. Este livro estabelece o protocolo olfativo profissional: como marcar presença sem invadir o espaço de ninguém.",
        "O ambiente de trabalho exige a mais rigorosa etiqueta olfativa: discrição é poder. Dominar as regras de projeção, intensidade e escolha permite usar perfume profissionalmente sem gerar desconforto.",
        "Estudos comportamentais indicam que aromas intensos em espaços fechados podem causar desconforto, alergias e até reduzir a produtividade de colegas [1]. No escritório, recomenda-se projeção curta e notas limpas: cítricos suaves, florais leves, fougères discretos — evitando gourmands densos e ouds poderosos [2].\n\n**Por que importa?** A regra de ouro é: a fragrância deve ser percebida apenas em um braço de distância. Se colegas comentam seu perfume ao chegar, está forte demais.\n\n**O que muda na prática:** Aplique até duas borrifadas em pontos cobertos. No trabalho, menos é sempre mais: o objetivo é presença sutil, não performance de palco [3]."
    ),
    "P3-06-encontros-romanticos": (
        "Encontros Românticos",
        "Encontros Românticos: Quais acordes despertam atração e criam intimidade olfativa",
        "Quais acordes despertam atração e criam intimidade olfativa",
        "O olfato é o sentido mais ligado à emoção e à memória — e, portanto, à atração. Certos acordes criam intimidade, aquecimento e proximidade. Este livro explora a química da sedução olfativa e os perfumes que funcionam em encontros.",
        "A perfumaria romântica é um território sensorial à parte: notas que aproximam, que convidam ao contato e que ficam na memória de quem sentiu. Conhecê-las dá a você uma ferramenta sutil e poderosa.",
        "A pesquisa sobre aroma e atração sugere que fragrâncias com notas de baunilha, âmbar, almíscar e especiarias doces tendem a ser percebidas como quentes e convidativas, enquanto notas verdes e aquáticas podem criar distância [1]. O almíscar, em particular, tem associação histórica com feromônios e sensualidade [2].\n\n**Por que importa?** Em encontros, o perfume funciona como trilha sonora da proximidade: intenso demais sufoca, sutil demais se perde.\n\n**O que muda na prática:** Para encontros, escolha fragrâncias de projeção média e grande profundidade olfativa — algo que convide a se aproximar. Aplique nos pontos quentes do corpo e evite excessos [3]."
    ),
    "P3-07-eventos-formais-e-noites-de-gala": (
        "Eventos Formais e Noites de Gala",
        "Eventos Formais e Noites de Gala: Fragrâncias imponentes que exigem elegância e sofisticação",
        "Fragrâncias imponentes que exigem elegância e sofisticação",
        "Uma noite de gala pede um perfume à altura: denso, elegante e memorável, capaz de atravessar horas de eventos. Este livro define o protocolo olfativo dos momentos formais — do vestido de noite ao smoking.",
        "O perfume de gala é um traje olfativo: ele precisa de presença sem gritar, complexidade sem confusão. Dominar a escolha para eventos formais garante que sua fragrância seja parte da elegância da noite.",
        "Eventos formais pedem concentrações altas e composições estruturadas: orientais clássicos, chipres densos, ouds refinados e florais opulentos com fundo ambarado [1]. O protocolo é aplicação generosa, mas em pontos estratégicos — pulsos, nuca, atrás das orelhas — e renovação discreta durante a noite [2].\n\n**Por que importa?** Em ambientes climatizados e longos, o perfume precisa de projeção controlada e fixação de horas: é o cenário dos Extraits e dos ouds de alta qualidade.\n\n**O que muda na prática:** Teste a fragrância escolhida em um evento anterior. Para noites formais, prefira frascos concentrados e evite aplicações de última hora sobre roupas delicadas [3]."
    ),
    "P3-08-pratica-esportiva-e-dias-casuais": (
        "Prática Esportiva e Dias Casuais",
        "Prática Esportiva e Dias Casuais: Opções leves, limpas e revigorantes para momentos de descontração",
        "Opções leves, limpas e revigorantes para momentos de descontração",
        "Academia, trilha, praia, domingo em casa: os momentos casuais pedem fragrâncias que acompanham o movimento sem atrapalhar. Este livro define o perfil olfativo ideal para esportes e lazer — leve, limpo e revigorante.",
        "O perfume esportivo é um estado de espírito: frescor, energia e discrição. Escolher bem para o lazer e a prática esportiva evita desconforto e permite usar fragrância em qualquer circunstância.",
        "Para atividade física, o perfil ideal é o aquático-cítrico: notas de sal marinho, menta, bergamota e almíscar limpo, que refrescam sem abafar durante o suor [1]. A concentração deve ser leve — Eau de Toilette ou Cologne — e a aplicação, discreta, pois o calor corporal intensifica qualquer perfume durante o exercício [2].\n\n**Por que importa?** Fragrâncias pesadas misturadas ao suor podem criar percepção desagradável; as leves e limpas, ao contrário, mantêm a sensação de frescor.\n\n**O que muda na prática:** Para treinos, aplique em tecidos de algodão ou em pontos cobertos, e reaplique após o banho. Dias casuais aceitam um pouco mais de presença, mas mantenha a leveza [3]."
    ),
    "P3-09-transicao-de-estacao": (
        "Transição de Estação",
        "Transição de Estação: Como adaptar o seu armário de perfumes quando o clima começa a mudar",
        "Como adaptar o seu armário de perfumes quando o clima começa a mudar",
        "O fim do verão não pede o fim do seu perfume favorito: pede adaptação. Nas transições de estação, a temperatura oscila e os perfumes se comportam de formas surpreendentes. Este livro ensina a gerenciar a troca do guarda-roupa olfativo sem desperdício.",
        "A transição entre estações é o momento mais delicado do guarda-roupa olfativo: o clima instável exige flexibilidade. Saber adaptar, misturar e rotacionar evita compras por impulso e prolonga a vida útil da coleção.",
        "Durante a transição, manhãs frias e tardes quentes desafiam qualquer fragrância: o mesmo perfume pode abafar ao meio-dia e sumir à noite [1]. A estratégia é a rotação: manter os frescos da estação anterior para as tardes quentes e introduzir gradualmente os densos para as manhãs frias [2].\n\n**Por que importa?** Comprar por impulso na transição gera frascos usados uma única vez. A rotação consciente aproveita o que já existe e revela novas combinações.\n\n**O que muda na prática:** Organize a coleção por estação de uso e, na transição, alterne os dois grupos. Teste as fragrâncias em horários diferentes do dia antes de decidir [3]."
    ),
    "P3-10-viagens-e-aromas": (
        "Viagens e Aromas",
        "Viagens e Aromas: Como escolher o perfume perfeito para levar nas suas férias de verão ou inverno",
        "Como escolher o perfume perfeito para levar nas suas férias de verão ou inverno",
        "Viajar com perfume é escolher uma companhia aromática para cada destino: praia, montanha, cidade europeia ou deserto. Este livro orienta a seleção de fragrâncias para férias — considerando clima, restrições de transporte e memórias.",
        "O perfume de viagem precisa ser versátil, compacto e apropriado ao destino. Escolher bem transforma cada viagem em uma experiência completa — e cada retorno, em memória olfativa duradoura.",
        "A seleção para viagem considera três fatores: o clima do destino (calor tropical pede frescor; inverno europeu, calor), a versatilidade (poucos frascos para muitas ocasiões) e as restrições de transporte (líquidos em bagagem de mão limitados a 100 ml) [1]. Decants e perfumes sólidos resolvem o problema de espaço [2].\n\n**Por que importa?** O aroma passa a integrar a memória da viagem: anos depois, o perfume traz de volta o destino inteiro.\n\n**O que muda na prática:** Leve um decant do seu favorito e uma amostra de algo novo. Ao voltar, adquira a fragrância que marcou a viagem para fixar a memória [3]."
    ),

    # ═══════════════ SÉRIE P4 — APLICAÇÃO, CONSERVAÇÃO E CUIDADOS ═══════════════
    "P4-01-a-arte-da-aplicacao": (
        "A Arte da Aplicação",
        "A Arte da Aplicação: Onde e como aplicar o perfume para maximizar a projeção e a durabilidade",
        "Onde e como aplicar o perfume para maximizar a projeção e a durabilidade",
        "Aplicar perfume parece simples — e por isso quase todo mundo erra. A localização, a distância do borrifador, a quantidade e a técnica determinam projeção e durabilidade. Este livro ensina o protocolo completo de aplicação, do pulso às roupas.",
        "A aplicação é a última etapa da perfumaria — e a mais negligenciada. Dominar a técnica transforma a performance de qualquer fragrância e evita os erros que matam a evolução de um perfume.",
        "A aplicação ideal depende de pontos de pulso quentes (pulsos, pescoço, atrás das orelhas, nuca), onde a temperatura corporal acelera a liberação das moléculas [1]. A distância recomendada é de 15 a 20 centímetros do borrifador, em movimentos que permitem o perfume assentar na pele, nunca esfregado [2].\n\n**Por que importa?** Esfregar os pulsos quebra as moléculas por fricção e destrói a evolução da pirâmide. Aplicar em roupas, por sua vez, fixa mais, mas impede a interação com a pele.\n\n**O que muda na prática:** Para máxima performance, combine pontos de pulso e uma borrifada sobre a roupa (com cuidado com tecidos claros). Ajuste a quantidade à concentração: Extrait pede menos que EDT [3]."
    ),
    "P4-02-hidratacao-e-performance": (
        "Hidratação e Performance",
        "Hidratação e Performance: Como a pele hidratada retém muito melhor as moléculas de perfume",
        "Como a pele hidratada retém muito melhor as moléculas de perfume",
        "A pele seca evapora perfume em minutos; a hidratada segura a fragrância por horas. Este livro explica a ciência por trás dessa diferença e ensina a construir uma rotina de hidratação que potencializa qualquer perfume.",
        "A hidratação é o segredo de performance mais subestimado da perfumaria. Uma rotina simples de hidratação transforma a durabilidade de todos os seus perfumes — sem trocar nenhum frasco.",
        "Moléculas perfumadas são lipofílicas: aderem melhor a superfícies oleosas. A pele hidratada (e levemente oleosa) retém essas moléculas por mais tempo, enquanto a pele seca as perde rapidamente por evaporação [1]. Estudos mostram ganhos significativos de fixação em peles hidratadas [2].\n\n**Por que importa?** O truque dos apreciadores experientes é simples: hidratar com loção neutra (sem perfume) antes da aplicação. A base oleosa segura as moléculas e reduz a evaporação.\n\n**O que muda na prática:** Aplique um hidratante sem fragrância nos pontos de pulso e aguarde secar antes de borrifar. Evite loções perfumadas, que conflitam com o perfume [3]."
    ),
    "P4-03-os-erros-mais-comuns": (
        "Os Erros Mais Comuns",
        "Os Erros Mais Comuns: Por que esfregar os pulsos estraga a evolução de uma fragrância",
        "Por que esfregar os pulsos estraga a evolução de uma fragrância",
        "Esfregar os pulsos, borrifar no ar e atravessar a nuvem, aplicar dezenas de vezes: a lista de erros de aplicação é longa e universal. Este livro cataloga os equívocos mais comuns, explica por que cada um prejudica o perfume e oferece a correção imediata.",
        "Corrigir erros de aplicação é a forma mais rápida de melhorar a experiência com perfumes que você já possui. Cada hábito ruim tem uma explicação técnica — e uma solução simples.",
        "O erro número um é esfregar os pulsos: a fricção aquece e quebra as moléculas das notas de saída, acelerando a evaporação e achatando a pirâmide olfativa [1]. Outros erros frequentes incluem borrifar no ar e atravessar a nuvem (desperdiça e não fixa), aplicar em roupas sujas de perfume anterior e exagerar na quantidade [2].\n\n**Por que importa?** Cada erro tem custo real: desperdício de perfume, fixação reduzida e distorção da fragrância que você escolheu.\n\n**O que muda na prática:** Depois de borrifar no pulso, apenas toque um pulso no outro — sem esfregar. Aplique de perto, em pontos quentes, e respeite a concentração [3]."
    ),
    "P4-04-onde-guardar-seus-perfumes": (
        "Onde Guardar Seus Perfumes",
        "Onde Guardar Seus Perfumes: Como a luz, o calor e a umidade do banheiro podem destruir a sua coleção",
        "Como a luz, o calor e a umidade do banheiro podem destruir a sua coleção",
        "O banheiro é o pior lugar da casa para guardar perfume — e é onde quase todo mundo guarda. Luz, calor e umidade degradam as essências em meses. Este livro define o protocolo de armazenamento que protege sua coleção por anos.",
        "Armazenar corretamente é a forma mais barata de preservar o valor dos seus perfumes. Entender os três inimigos — luz, calor e umidade — permite escolher o local ideal e prolongar a vida útil de qualquer fragrância.",
        "A luz (especialmente ultravioleta) acelera a oxidação das moléculas aromáticas; o calor aumenta a volatilização; e a umidade do banheiro contamina o frasco e altera a composição [1]. O ambiente ideal é escuro, seco e com temperatura estável entre 15°C e 22°C [2].\n\n**Por que importa?** Um frasco guardado no banheiro pode perder cor, aroma e fixação em 6 a 12 meses — enquanto o mesmo frasco em local adequado dura anos.\n\n**O que muda na prática:** Guarde na embalagem original ou em local escuro (gaveta, armário, caixa). Mantenha as tampas bem fechadas e longe de janelas e aquecedores [3]."
    ),
    "P4-05-frascos-na-geladeira": (
        "Frascos na Geladeira?",
        "Frascos na Geladeira?: Mitos e verdades sobre a conservação de perfumes raros e artesanais",
        "Mitos e verdades sobre a conservação de perfumes raros e artesanais",
        "Geladeira protege perfume? A resposta é: depende. Para frascos fechados, o frio retarda a degradação; para abertos, pode causar condensação e alterar a composição. Este livro separa os mitos das verdades sobre a conservação refrigerada.",
        "A geladeira é uma ferramenta útil, mas com regras claras. Entender quando ela ajuda — e quando prejudica — protege tanto frascos raros quanto os artesanais delicados.",
        "O frio retarda reações químicas de oxidação, o que faz da geladeira um aliado para frascos fechados, raros ou que serão guardados por anos [1]. Para frascos em uso, porém, o problema é a condensação: a mudança de temperatura cria água no interior, que contamina a essência [2].\n\n**Por que importa?** A oscilação térmica é mais prejudicial que a temperatura em si. O perfume não deve \"sofrer\" idas e vindas entre frio e ambiente.\n\n**O que muda na prática:** Refrigere apenas frascos lacrados e devolva-os à geladeira rapidamente. Perfumes em uso devem ficar em local escuro e estável, sem mudanças bruscas de temperatura [3]."
    ),
    "P4-06-decants-e-amostras": (
        "Decants e Amostras",
        "Decants e Amostras: A melhor forma de testar novos aromas sem investir em um frasco grande fechado",
        "A melhor forma de testar novos aromas sem investir em um frasco grande fechado",
        "Investir em um frasco grande de um perfume desconhecido é uma aposta cara. Os decants — porções menores transferidas para frascos de viagem — permitem testar com racionalidade. Este livro ensina a usar decants e amostras como estratégia de descoberta.",
        "Decants e amostras transformam a compra de perfume em ciência: testes prolongados antes do investimento, portabilidade e zero desperdício. Dominar essa prática é a maior economia do apreciador.",
        "Decant é a transferência de perfume de um frasco original para um frasco menor (geralmente 5 a 30 ml), permitindo testar por semanas sem comprar o frasco inteiro [1]. A prática é comum entre colecionadores e lojas de nicho, e reduz drasticamente o risco de compra errada [2].\n\n**Por que importa?** O nariz muda de opinião com o tempo e o clima: só o uso prolongado revela o verdadeiro caráter de uma fragrância.\n\n**O que muda na prática:** Sempre que possível, compre decants antes de frascos grandes. Teste em ciclos de uso real — trabalho, calor, frio — antes de decidir. Frascos de viagem são ideais para levar no dia a dia [3]."
    ),
    "P4-07-perfume-vence": (
        "Perfume Vence?",
        "Perfume Vence?: Como identificar quando uma fragrância oxidou ou perdeu as propriedades originais",
        "Como identificar quando uma fragrância oxidou ou perdeu as propriedades originais",
        "Perfume não tem data de validade como alimento, mas tem vida útil — e ela termina. A oxidação altera cor, aroma e performance. Este livro ensina a identificar os sinais de que uma fragrância venceu e o que fazer com frascos degradados.",
        "Saber reconhecer um perfume oxidado evita decepções e preserva a saúde da coleção. Com as técnicas certas de inspeção, você decide o que ainda tem valor e o que deve ser descartado.",
        "A vida útil de um perfume varia de 3 a 10 anos, dependendo da qualidade das matérias-primas e do armazenamento [1]. Sinais de oxidação: mudança de cor (escurecimento), aroma metálico ou azedo, perda das notas de saída e alteração da fixação [2].\n\n**Por que importa?** Notas cítricas e verdes degradam mais rápido; ouds, âmbar e almíscares resistem por décadas. Um frasco escurecido não é necessariamente estragado — mas o aroma decide.\n\n**O que muda na prática:** Ao suspeitar, compare com um decant novo da mesma fragrância. Se o aroma estiver alterado, use para ambientes ou descarte. Nunca misture um frasco oxidado com um novo [3]."
    ),
    "P4-08-cuidados-com-tecidos": (
        "Cuidados com Tecidos",
        "Cuidados com Tecidos: Como perfumar roupas de linho, algodão e lã sem manchar as peças",
        "Como perfumar roupas de linho, algodão e lã sem manchar as peças",
        "Perfume na roupa fixa por dias — mas pode manchar, desbotar e alterar a textura dos tecidos. Linho, algodão e lã reagem de formas diferentes. Este livro ensina a perfumar cada tecido com segurança.",
        "Perfumar tecidos é uma técnica à parte: os ganhos de fixação são enormes, mas os riscos de mancha e dano também. Conhecer os cuidados por tecido protege suas roupas favoritas.",
        "O álcool dos perfumes pode manchar e desbotar tecidos sintéticos e escuros; o linho e o algodão aceitam perfume com mais segurança, mas podem amarelar com o tempo [1]. A lã retém aroma por muito tempo e exige menos quantidade, enquanto seda e tecidos claros devem ser evitados [2].\n\n**Por que importa?** A fixação em tecidos supera a da pele: camisas e cachecóis perfumados mantêm o aroma por dias — o sonho e o pesadelo da perfumaria.\n\n**O que muda na prática:** Borrife a 20 centímetros em forros internos, costuras ou cabides, e aguarde secar antes de vestir. Teste sempre em uma área discreta primeiro [3]."
    ),
    "P4-09-o-olfato-cansa": (
        "O Olfato Cansa",
        "O Olfato Cansa: Como resolver a fadiga olfativa quando você deixa de sentir o seu próprio perfume",
        "Como resolver a fadiga olfativa quando você deixa de sentir o seu próprio perfume",
        "Você aplicou o perfume há uma hora e não sente mais nada — mas os outros sentem. A fadiga olfativa é um fenômeno neurológico, não um defeito da fragrância. Este livro explica como o nariz se adapta e como gerenciar a percepção.",
        "A fadiga olfativa explica por que o nariz se acostuma ao próprio perfume — e por que reaplicar compulsivamente é o pior erro. Entender o mecanismo devolve o controle sobre a percepção e o consumo.",
        "A fadiga olfativa (adaptação sensorial) ocorre quando o cérebro deixa de registrar estímulos constantes para preservar sensibilidade a novos odores [1]. O seu perfume não sumiu: o seu nariz o classificou como \"ruído de fundo\" — e os outros continuam sentindo [2].\n\n**Por que importa?** Reaplicar para \"recuperar\" a percepção gera excesso e pode saturar o ambiente para os outros.\n\n**O que muda na prática:** Para resetar a percepção, cheire café em grão, pele limpa ou saia para o ar fresco. Confie nos outros: se ninguém comenta, a fragrância está discreta — não ausente [3]."
    ),
    "P4-10-viagens-de-aviao": (
        "Viagens de Avião",
        "Viagens de Avião: Como transportar seus frascos de vidro e óleos concentrados com segurança",
        "Como transportar seus frascos de vidro e óleos concentrados com segurança",
        "Cabin pressure, restrições de líquidos, vidro frágil, óleos que vazam: viajar com perfume exige estratégia. Este livro define o protocolo seguro de transporte aéreo — da bagagem de mão ao despacho.",
        "Transportar perfume em avião é uma combinação de regras de segurança, física de pressão e cuidado com o conteúdo. Dominar o protocolo evita perdas, vazamentos e problemas na alfândega.",
        "Em bagagem de mão, líquidos são limitados a 100 ml por recipiente, dentro de saco plástico transparente [1]. Na bagagem despachada, frascos grandes são permitidos, mas devem ser protegidos contra impacto e variação de pressão, que pode causar vazamento [2].\n\n**Por que importa?** A pressurização da cabine não destrói o perfume, mas o impacto e a vibração do transporte podem quebrar vidros e arrancar tampas.\n\n**O que muda na prática:** Use decants para a mão e frascos originais com tampa vedada (fita ou saco plástico) no despacho. Envolva o vidro em plástico bolha e tecidos. Óleos concentrados seguem as mesmas regras de líquidos [3]."
    ),

    # ═══════════════ SÉRIE P5 — COMPORTAMENTO, PSICOLOGIA DOS AROMAS E ESTILO ═══════════════
    "P5-01-a-psicologia-dos-aromas": (
        "A Psicologia dos Aromas",
        "A Psicologia dos Aromas: Como o cheiro influencia o seu humor, sua confiança e sua autoestima",
        "Como o cheiro influencia o seu humor, sua confiança e sua autoestima",
        "O aroma não é apenas decoração: é química que conversa com o cérebro. Notas cítricas despertam, lavanda acalma, âmbar aquece. Este livro explora a psicologia dos aromas e como usar o perfume como ferramenta de bem-estar e confiança.",
        "O perfume é uma das ferramentas mais acessíveis de regulação emocional. Entender o impacto psicológico das notas permite usar fragrâncias intencionalmente — para acordar, concentrar, relaxar ou ganhar coragem.",
        "O sistema olfativo é o único sentido diretamente conectado ao sistema límbico, a região cerebral das emoções e memórias [1]. Estudos mostram que cítricos elevam o estado de alerta e o humor, lavanda e camomila reduzem o estresse, e notas ambaradas aumentam a sensação de calor e conforto [2].\n\n**Por que importa?** O efeito é real e mensurável: fragrâncias podem alterar frequência cardíaca, percepção de dor e até desempenho em tarefas.\n\n**O que muda na prática:** Monte um arsenal emocional: um cítrico para manhãs, um floral para o dia a dia e um oriental para momentos de confiança. Use o perfume como âncora de estados desejados [3]."
    ),
    "P5-02-memoria-olfativa": (
        "Memória Olfativa",
        "Memória Olfativa: Por que um determinado cheiro é capaz de nos transportar instantaneamente para o passado",
        "Por que um determinado cheiro é capaz de nos transportar instantaneamente para o passado",
        "Um cheiro pode trazer de volta uma avó, uma cidade, um amor — em um instante, com uma intensidade que nenhuma foto alcança. A memória olfativa é o fenômeno mais poderoso do cérebro humano. Este livro explora a ciência e as histórias por trás dela.",
        "A memória olfativa é um superpoder humano: um gatilho sensorial que resgata emoções e cenários com precisão brutal. Compreender o fenômeno muda a forma como escolhemos e vivemos nossos perfumes.",
        "O chamado \"fenômeno Proust\" descreve como odores disparam memórias autobiográficas com riqueza emocional incomparável [1]. Isso ocorre porque o bulbo olfativo conecta-se diretamente à amígdala e ao hipocampo, centros de emoção e memória [2].\n\n**Por que importa?** Perfumes criam âncoras: a fragrância do primeiro encontro, da casa da infância ou da viagem perfeita carrega a emoção associada por décadas.\n\n**O que muda na prática:** Use o perfume intencionalmente em momentos importantes: ele se tornará o guardião daquela memória. Ao escolher um novo perfume, considere que ele poderá marcar um período inteiro da sua vida [3]."
    ),
    "P5-03-perfumes-compartilhados-gender-neutral": (
        "Perfumes Compartilhados (Gender-Neutral)",
        "Perfumes Compartilhados (Gender-Neutral): Como a perfumaria árabe quebra barreiras de gênero com notas complexas",
        "Como a perfumaria árabe quebra barreiras de gênero com notas complexas",
        "A divisão entre perfume masculino e feminino é uma convenção recente e ocidental. A perfumaria árabe sempre foi, em grande parte, gender-neutral: ouds, âmbares e rosas usados por todos. Este livro explora essa tradição e o movimento unissex contemporâneo.",
        "O gênero do perfume é uma construção cultural, não química. A tradição árabe — e o movimento moderno de nicho — provam que notas complexas funcionam em qualquer pele, independentemente do rótulo.",
        "Historicamente, a perfumaria árabe não separou fragrâncias por gênero: ouds, rosas e almíscares eram (e são) usados indistintamente [1]. A segmentação masculino/feminino é uma invenção do marketing ocidental do século XX, baseada em normas sociais — não em propriedades das notas [2].\n\n**Por que importa?** Perfumes \"masculinos\" e \"femininos\" compartilham a maioria das matérias-primas. A percepção muda com a pele de quem usa e com as associações culturais.\n\n**O que muda na prática:** Escolha pelo nariz, não pela prateleira. Teste fragrâncias de todas as seções: muitas criações árabes densas são naturalmente compartilhadas e brilham em peles de qualquer gênero [3]."
    ),
    "P5-04-construindo-uma-colecao-enxuta": (
        "Construindo uma Coleção Enxuta (Wardrobe)",
        "Construindo uma Coleção Enxuta (Wardrobe): O conceito de ter poucos frascos, mas versáteis e de alta qualidade",
        "O conceito de ter poucos frascos, mas versáteis e de alta qualidade",
        "Em vez de uma prateleira de frascos meia-uso, a filosofia wardrobe propõe poucos perfumes, cada um com papel definido: dia, noite, verão, inverno, trabalho. Este livro ensina a construir uma coleção enxuta, versátil e de alta qualidade.",
        "A coleção enxuta é uma curadoria, não uma acumulação. Menos frascos, escolhidos com critério, entregam mais satisfação e menos desperdício — e cada perfume ganha o uso que merece.",
        "O conceito de wardrobe (guarda-roupa) olfativo preconiza de 5 a 8 frascos, cada um cobrindo um cenário: trabalho, casual, formal, calor, frio e assinatura pessoal [1]. A regra é a versatilidade: cada frasco deve combinar com vários contextos e roupas [2].\n\n**Por que importa?** Coleções grandes tendem a frascos esquecidos que oxidam antes do uso. A curadoria enxuta maximiza o retorno de cada compra.\n\n**O que muda na prática:** Liste seus cenários de uso e mapeie os frascos atuais. Identifique buracos e preencha com calma, um frasco de cada vez. Prefira decants para validar antes do frasco grande [3]."
    ),
    "P5-05-presentes-inesqueciveis": (
        "Presentes Inesquecíveis",
        "Presentes Inesquecíveis: Como escolher um perfume às cegas para surpreender alguém especial",
        "Como escolher um perfume às cegas para surpreender alguém especial",
        "Presentear perfume é arriscado: gosto olfativo é íntimo e imprevisível. Mas com método — pesquisa, sinais e decants disfarçados — é possível acertar em cheio. Este livro define o protocolo do presente olfativo inesquecível.",
        "O perfume é um dos presentes mais pessoais que existem — e o mais fácil de errar. Com as técnicas certas de investigação e apresentação, o risco vira oportunidade de acertar profundamente.",
        "A escolha às cegas depende de sinais: perfumes que a pessoa já usa, famílias preferidas, notas citadas e até a personalidade percebida [1]. Quando não há sinais, o presente seguro é um conjunto de decants — uma caixa de descoberta que mostra cuidado sem impor um frasco [2].\n\n**Por que importa?** O perfume presenteado certo torna-se parte da identidade da pessoa — e do vínculo entre vocês.\n\n**O que muda na prática:** Investigue discretamente a rotina olfativa da pessoa. Se a dúvida persistir, presenteie uma coleção de amostras selecionadas e a promessa de comprar o frasco do favorito [3]."
    ),
    "P5-06-a-industria-do-marketing-olfativo": (
        "A Indústria do Marketing Olfativo",
        "A Indústria do Marketing Olfativo: Como grandes marcas usam fragrâncias para contar histórias",
        "Como grandes marcas usam fragrâncias para contar histórias",
        "Por trás de cada lançamento há uma narrativa: o \"oud de uma caravana\", a \"rosa colhida ao amanhecer\". O marketing olfativo é uma indústria de storytelling que transforma química em desejo. Este livro decifra as estratégias das grandes marcas.",
        "Entender o marketing olfativo é o antídoto para a compra por impulso. Quando você reconhece a narrativa, consegue separar a história da qualidade real — e decidir com o nariz, não com o anúncio.",
        "O marketing de perfumes combina storytelling (origem das matérias-primas, herança da casa), design de frasco e comunicação aspiracional para construir desejo [1]. Termos como \"oud precioso\" e \"rosa de Taif\" agregam valor percebido mesmo quando as matérias-primas reais são sintéticas ou rastreadas [2].\n\n**Por que importa?** O preço de um perfume inclui a narrativa: casas de nicho cobram pela história tanto quanto pela composição.\n\n**O que muda na prática:** Leia o rótulo como história, mas avalie pelo nariz. Teste a fragrância sem olhar o frasco ou o nome para neutralizar o viés do marketing [3]."
    ),
    "P5-07-sustentabilidade-e-consumo-consciente": (
        "Sustentabilidade e Consumo Consciente",
        "Sustentabilidade e Consumo Consciente: O valor das marcas artesanais de produção local e limitada",
        "O valor das marcas artesanais de produção local e limitada",
        "O perfumista artesanal colhe, destila e envasia perto de casa; a indústria global importa, extrai e padroniza. A sustentabilidade entrou na perfumaria pelos dois lados. Este livro explora o valor das marcas locais, limitadas e responsáveis.",
        "O consumo consciente de perfumes é uma escolha política e ambiental: apoiar marcas locais reduz pegada de carbono, preserva espécies e mantém tradições vivas. Entender o impacto de cada frasco transforma o colecionador em curador responsável.",
        "A perfumaria sustentável enfrenta dilemas reais: a demanda por sândalo e oud pressiona espécies ameaçadas, enquanto a biotecnologia oferece alternativas sem extração predatória [1]. Marcas artesanais locais reduzem transporte, apoiam comunidades e respeitam ciclos de colheita [2].\n\n**Por que importa?** O maior impacto ambiental da perfumaria está nas matérias-primas e no frasco — vidro pesado, tampa metálica e excesso de embalagem contam tanto quanto a essência.\n\n**O que muda na prática:** Prefira marcas com rastreabilidade declarada, refis e frascos reutilizáveis. Investigue a origem do oud e do sândalo antes de comprar [3]."
    ),
    "P5-08-o-prazer-do-colecionismo": (
        "O Prazer do Colecionismo",
        "O Prazer do Colecionismo: Por que nos apaixonamos por buscar frascos raros e exclusivos",
        "Por que nos apaixonamos por buscar frascos raros e exclusivos",
        "Colecionar perfumes é caçar: leilões, lotes limitados, versões antigas de fórmulas descontinuadas. A busca pelo frasco raro move uma comunidade global de apaixonados. Este livro explora a psicologia do colecionismo olfativo e como praticá-lo com saúde.",
        "O colecionismo é uma das formas mais intensas de relação com a perfumaria — e também uma das mais propensas a excessos. Entender seus mecanismos permite colecionar com prazer, estratégia e equilíbrio.",
        "O colecionador de perfumes busca raridade (fórmulas descontinuadas, lotes limitados), história (frascos vintage) e exclusividade (lançamentos de nicho em edições numeradas) [1]. O prazer está tanto na caçada quanto na posse — um padrão clássico de colecionismo, com forte componente emocional e comunitário [2].\n\n**Por que importa?** O mercado de perfumes vintage e raros cresce, com leilões e comunidades dedicadas à preservação de fórmulas históricas.\n\n**O que muda na prática:** Defina limites claros de orçamento e espaço. Priorize frascos que você vai usar e compartilhar, não apenas guardar. Documente sua coleção com fichas de compra e avaliação [3]."
    ),
    "P5-09-autenticidade-vs-copias": (
        "Autenticidade vs. Cópias",
        "Autenticidade vs. Cópias: Como identificar a qualidade de matérias-primas e fugir de produtos falsificados",
        "Como identificar a qualidade de matérias-primas e fugir de produtos falsificados",
        "O mercado de perfumes falsificados movimenta bilhões — e as cópias de qualidade enganam até entendidos. Este livro ensina a identificar autenticidade, avaliar a qualidade real das matérias-primas e proteger sua compra.",
        "Autenticidade é uma questão de informação: selos, lotes, embalagens e — acima de tudo — o comportamento olfativo. Saber verificar evita prejuízo financeiro e garante a experiência real da fragrância.",
        "Falsificações modernas copiam embalagens com precisão crescente, mas raramente reproduzem o aroma completo: usam matérias-primas baratas que achatam a evolução e reduzem a fixação [1]. Indicadores de autenticidade incluem número de lote e código de barras verificáveis, textura do frasco, tampa e o comportamento do perfume na pele [2].\n\n**Por que importa?** O perfume falso não é só decepção: pode conter solventes e alergênicos fora de controle de qualidade.\n\n**O que muda na prática:** Compre apenas de revendedores oficiais ou autorizados. Compare o frasco com fotos oficiais e desconfie de preços muito abaixo do mercado. Teste o aroma contra um decant confiável [3]."
    ),
    "P5-10-do-hobby-a-paixao": (
        "Do Hobby à Paixão",
        "Do Hobby à Paixão: Como treinar o seu nariz para identificar notas isoladas como um perfumista profissional",
        "Como treinar o seu nariz para identificar notas isoladas como um perfumista profissional",
        "O nariz de um perfumista não nasce pronto: é treinado. Identificar notas isoladas — rosa, patchouli, âmbar — é uma habilidade que se constrói com método. Este livro é o programa de treinamento olfativo que transforma o hobby em paixão profissional.",
        "O treinamento olfativo é acessível a qualquer pessoa com paciência: kits de notas, prática sistemática e registro diário. Transformar o nariz em instrumento é a maior recompensa da perfumaria — e o primeiro passo para criar.",
        "Perfumistas treinam o nariz com kits de matérias-primas isoladas, praticando identificação às cegas e construindo um vocabulário olfativo preciso [1]. O método inclui associação (cheirar e nomear), comparação (notas lado a lado) e memória (registrar cada experiência) [2].\n\n**Por que importa?** Estudos mostram que o treino olfativo aumenta a sensibilidade e a capacidade de discriminação ao longo de semanas — o nariz é um músculo cognitivo.\n\n**O que muda na prática:** Monte um kit com 10 a 15 notas essenciais (rosa, jasmim, lavanda, bergamota, patchouli, vetiver, sândalo, âmbar, baunilha, almíscar). Pratique 15 minutos diários, às cegas, e registre em um diário olfativo [3]."
    ),
}

# Auto-gerar lista completa de slugs
SLUGS_PERFUMARIA = list(LIVROS_PERFUMARIA.keys())
