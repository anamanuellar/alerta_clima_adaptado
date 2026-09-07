from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "Relatorio_Tecnico_Desafio_5.pdf"

NAVY = colors.HexColor("#0F172A")
BLUE = colors.HexColor("#0284C7")
CYAN = colors.HexColor("#06B6D4")
PINK = colors.HexColor("#DB2777")
SLATE = colors.HexColor("#475569")
LIGHT = colors.HexColor("#F1F5F9")
BORDER = colors.HexColor("#CBD5E1")
GREEN = colors.HexColor("#15803D")

pdfmetrics.registerFont(TTFont("DejaVu", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CoverTitle",
        parent=styles["Title"],
        fontName="DejaVu-Bold",
        fontSize=27,
        leading=32,
        textColor=NAVY,
        alignment=TA_CENTER,
        spaceAfter=14,
    )
)
styles.add(
    ParagraphStyle(
        name="CoverSubtitle",
        parent=styles["Normal"],
        fontName="DejaVu",
        fontSize=13,
        leading=19,
        textColor=SLATE,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        name="Section",
        parent=styles["Heading1"],
        fontName="DejaVu-Bold",
        fontSize=17,
        leading=21,
        textColor=BLUE,
        spaceBefore=13,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="Subsection",
        parent=styles["Heading2"],
        fontName="DejaVu-Bold",
        fontSize=12,
        leading=15,
        textColor=NAVY,
        spaceBefore=9,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="BodyCustom",
        parent=styles["BodyText"],
        fontName="DejaVu",
        fontSize=9.5,
        leading=14,
        textColor=NAVY,
        spaceAfter=7,
    )
)
styles.add(
    ParagraphStyle(
        name="Small",
        parent=styles["BodyText"],
        fontName="DejaVu",
        fontSize=8,
        leading=11,
        textColor=SLATE,
    )
)
styles.add(
    ParagraphStyle(
        name="Callout",
        parent=styles["BodyText"],
        fontName="DejaVu",
        fontSize=9.5,
        leading=14,
        textColor=NAVY,
        leftIndent=10,
        rightIndent=10,
        spaceBefore=5,
        spaceAfter=5,
    )
)


def p(text, style="BodyCustom"):
    return Paragraph(text, styles[style])


def table(data, widths, header=True):
    result = Table(data, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.45, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if header:
        commands.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "DejaVu-Bold"),
            ]
        )
        if len(data) > 1:
            commands.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]))
    result.setStyle(TableStyle(commands))
    return result


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(1.7 * cm, height - 1.35 * cm, width - 1.7 * cm, height - 1.35 * cm)
    canvas.setFont("DejaVu-Bold", 8)
    canvas.setFillColor(BLUE)
    canvas.drawString(1.7 * cm, height - 1.05 * cm, "INSURMINDS - DESAFIO 5")
    canvas.setFont("DejaVu", 8)
    canvas.setFillColor(SLATE)
    canvas.drawRightString(width - 1.7 * cm, height - 1.05 * cm, "Alerta Clima Seguro")
    canvas.line(1.7 * cm, 1.25 * cm, width - 1.7 * cm, 1.25 * cm)
    canvas.drawString(1.7 * cm, 0.9 * cm, "Grupo 01 - I2A2")
    canvas.drawRightString(width - 1.7 * cm, 0.9 * cm, f"Página {doc.page}")
    canvas.restoreState()


story = [Spacer(1, 3.2 * cm)]
story.extend(
    [
        p("ALERTA CLIMA SEGURO", "CoverTitle"),
        p("Ferramenta inteligente para comunicação proativa com o segurado", "CoverSubtitle"),
        Spacer(1, 1.2 * cm),
        Table(
            [[p("RELATÓRIO TÉCNICO", "Subsection")]],
            colWidths=[9 * cm],
            style=TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                    ("BOX", (0, 0), (-1, -1), 1, CYAN),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("TOPPADDING", (0, 0), (-1, -1), 14),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
                ]
            ),
            hAlign="CENTER",
        ),
        Spacer(1, 2.5 * cm),
        p("Instituto de Inteligência Artificial Aplicada - I2A2", "CoverSubtitle"),
        p("InsurMinds - Grupo 01", "CoverSubtitle"),
        p("Setembro de 2026", "CoverSubtitle"),
        PageBreak(),
    ]
)

story.extend(
    [
        p("1. Visão geral", "Section"),
        p(
            "O Alerta Clima Seguro é um MVP que transforma dados meteorológicos em comunicações "
            "preventivas para segurados. A solução consulta uma fonte pública, reconhece eventos "
            "relevantes, cruza o risco com cidade e tipo de seguro, gera mensagens personalizadas "
            "com IA Generativa e registra uma simulação de envio."
        ),
        p(
            "O objetivo é demonstrar uma abordagem proativa: a interação não começa após um "
            "sinistro, mas antes dele, com recomendações que podem reduzir danos. Todos os segurados "
            "e apólices utilizados são fictícios."
        ),
        p("2. Arquitetura", "Section"),
        table(
            [
                [p("Componente", "Small"), p("Responsabilidade", "Small"), p("Tecnologia", "Small")],
                [p("Coleta", "Small"), p("Consultar previsões de três dias para as cidades monitoradas.", "Small"), p("Open-Meteo / Requests", "Small")],
                [p("Análise", "Small"), p("Transformar códigos WMO e medidas numéricas em eventos relevantes.", "Small"), p("Python / Pydantic", "Small")],
                [p("Decisão", "Small"), p("Selecionar segurados pela cidade e compatibilidade do seguro.", "Small"), p("Regras determinísticas", "Small")],
                [p("Comunicação", "Small"), p("Produzir orientação personalizada e adequada ao risco.", "Small"), p("LangChain / OpenRouter", "Small")],
                [p("Notificação", "Small"), p("Registrar canal, destinatário, conteúdo e status simulado.", "Small"), p("FastAPI / Interface web", "Small")],
            ],
            [3.1 * cm, 8.4 * cm, 4 * cm],
        ),
        p("Fluxo de processamento", "Subsection"),
        table(
            [[p("Open-Meteo", "Small"), p("Eventos", "Small"), p("Regras", "Small"), p("IA", "Small"), p("Envio simulado", "Small")]],
            [3 * cm] * 5,
        ),
        p(
            "A separação permite testar cada etapa isoladamente e substituir a fonte meteorológica, "
            "o conjunto de regras ou o provedor de IA sem reescrever toda a aplicação."
        ),
        PageBreak(),
    ]
)

story.extend(
    [
        p("3. Regras de negócio", "Section"),
        p(
            "As regras são determinísticas para que a decisão de notificar seja explicável. O LLM "
            "não decide quem recebe o alerta; ele atua apenas após a seleção, redigindo a mensagem."
        ),
        table(
            [
                [p("Evento", "Small"), p("Critério", "Small"), p("Seguros elegíveis", "Small")],
                [p("Chuva intensa", "Small"), p("WMO 65/82, chuva >= 30 mm ou >= 20 mm com probabilidade >= 80%.", "Small"), p("Residencial, rural e empresarial", "Small")],
                [p("Granizo", "Small"), p("WMO 96 ou 99.", "Small"), p("Todos os tipos cadastrados", "Small")],
                [p("Vento forte", "Small"), p("Rajadas >= 60 km/h.", "Small"), p("Todos os tipos cadastrados", "Small")],
                [p("Nevoeiro", "Small"), p("WMO 45 ou 48.", "Small"), p("Automóvel", "Small")],
                [p("Tempestade", "Small"), p("WMO 95.", "Small"), p("Todos os tipos cadastrados", "Small")],
            ],
            [3.1 * cm, 7.6 * cm, 4.8 * cm],
        ),
        p(
            "Em todos os casos, a cidade do segurado deve coincidir com a cidade afetada. A "
            "severidade é classificada como moderada, alta ou extrema a partir da intensidade."
        ),
        p("4. Dados fictícios", "Section"),
        p(
            "A base contém seis perfis distribuídos entre Salvador, Curitiba, São Paulo, Rio de "
            "Janeiro, Goiânia e Recife. Cada registro informa nome, coordenadas, tipo de seguro, bem "
            "segurado e canal preferencial. Nenhum dado pessoal real é utilizado."
        ),
        table(
            [
                [p("Exemplo", "Small"), p("Cidade", "Small"), p("Seguro", "Small"), p("Canal", "Small")],
                [p("Mariana Souza", "Small"), p("Salvador", "Small"), p("Residencial", "Small"), p("WhatsApp", "Small")],
                [p("Carlos Mendes", "Small"), p("Curitiba", "Small"), p("Automóvel", "Small"), p("SMS", "Small")],
                [p("Fazenda Boa Vista", "Small"), p("Goiânia", "Small"), p("Rural", "Small"), p("E-mail", "Small")],
            ],
            [4.2 * cm, 3.8 * cm, 3.8 * cm, 3.2 * cm],
        ),
    ]
)

story.extend(
    [
        PageBreak(),
        p("5. Uso de Inteligência Artificial", "Section"),
        p(
            "Após a aplicação das regras, o agente de comunicação recebe nome, cidade, tipo de "
            "seguro, bem protegido, evento, data, severidade e descrição técnica. O prompt orienta "
            "o modelo a escrever em Português do Brasil, sem alarmismo e sem prometer cobertura ou "
            "indenização."
        ),
        p(
            "A mensagem deve conter duas ou três ações preventivas e lembrar o segurado de seguir "
            "os alertas oficiais. Se o provedor estiver indisponível, uma mensagem determinística de "
            "contingência mantém o fluxo funcional e identifica sua origem."
        ),
        p("Exemplos de comunicação", "Subsection"),
        KeepTogether(
            [
                Table(
                    [[p("CHUVA INTENSA - SEGURO RESIDENCIAL", "Small")], [p("Olá, Mariana Souza. Identificamos risco de chuva intensa em Salvador para amanhã. Como você possui seguro residencial, proteja objetos próximos a áreas externas, verifique ralos e evite regiões alagadas. Esta é uma comunicação preventiva; acompanhe os alertas das autoridades locais.", "Callout")]],
                    colWidths=[15.5 * cm],
                    style=TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E0F2FE")), ("BOX", (0, 0), (-1, -1), 0.8, CYAN), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]),
                ),
                Spacer(1, 8),
            ]
        ),
        KeepTogether(
            [
                Table(
                    [[p("GRANIZO - SEGURO AUTOMÓVEL", "Small")], [p("Olá, Carlos Mendes. Há risco de tempestade com granizo em Curitiba. Mantenha o veículo em local coberto, evite estacionar próximo a árvores e, se possível, adie deslocamentos durante o período crítico. Esta é uma comunicação preventiva; siga os alertas oficiais.", "Callout")]],
                    colWidths=[15.5 * cm],
                    style=TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#FCE7F3")), ("BOX", (0, 0), (-1, -1), 0.8, PINK), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]),
                ),
                Spacer(1, 8),
            ]
        ),
        p("6. Demonstração", "Section"),
        p(
            "No modo real, notificações aparecem somente quando a previsão atinge os limites. No "
            "modo demonstrativo, a aplicação ainda consulta a Open-Meteo, mas apresenta três eventos "
            "didáticos identificados como simulados: chuva intensa em Salvador, granizo em Curitiba "
            "e vento forte em Recife. Assim, o avaliador consegue observar todas as etapas."
        ),
    ]
)

story.extend(
    [
        PageBreak(),
        p("7. API e interface", "Section"),
        table(
            [
                [p("Método e rota", "Small"), p("Finalidade", "Small")],
                [p("GET /api/v1/insureds", "Small"), p("Lista os perfis fictícios monitorados.", "Small")],
                [p("POST /api/v1/monitoring/run", "Small"), p("Executa o monitoramento com a previsão real.", "Small")],
                [p("POST /api/v1/monitoring/run?demonstracao=true", "Small"), p("Executa o fluxo completo em modo didático.", "Small")],
                [p("GET /api/v1/current", "Small"), p("Mantém a consulta meteorológica atual por cidade.", "Small")],
                [p("GET /api/v1/forecast", "Small"), p("Mantém a previsão de sete dias por cidade.", "Small")],
            ],
            [6.5 * cm, 9 * cm],
        ),
        p(
            "A interface apresenta botões separados para monitoramento real e demonstração. O "
            "resultado informa quantidade de cidades, segurados, eventos e notificações, seguido dos "
            "cartões com destinatário, seguro, evento, mensagem, canal e status."
        ),
        p("8. Testes e validação", "Section"),
        p(
            "Foram implementados testes automatizados para o código WMO 82, rajadas acima de 60 "
            "km/h, compatibilidade entre evento e seguro e execução completa do cenário "
            "demonstrativo. O teste integrado retornou status HTTP 200, seis segurados analisados, "
            "três eventos, três destinatários e três envios simulados."
        ),
        p("9. Segurança", "Section"),
        p(
            "Credenciais não fazem parte do código-fonte. O repositório inclui apenas um arquivo "
            ".env.example, e o .gitignore exclui o .env real. As chaves devem ser injetadas em tempo "
            "de execução. O segredo de sessão também é configurável por variável de ambiente."
        ),
        p("10. Limitações e evolução", "Section"),
        table(
            [
                [p("Limitação atual", "Small"), p("Evolução possível", "Small")],
                [p("Base fictícia em JSON", "Small"), p("Integração autorizada com cadastro real ou banco de dados.", "Small")],
                [p("Regras didáticas", "Small"), p("Validação com especialistas, apólices e alertas oficiais.", "Small")],
                [p("Execução sob demanda", "Small"), p("Agendamento periódico e prevenção de notificações duplicadas.", "Small")],
                [p("Envio simulado", "Small"), p("Integração futura com provedores de SMS, e-mail, WhatsApp ou push.", "Small")],
            ],
            [6.4 * cm, 9.1 * cm],
        ),
        Spacer(1, 12),
        p(
            "Conclusão: o protótipo demonstra o fluxo completo solicitado, com integração externa, "
            "decisão explicável, personalização por IA, contingência e simulação segura do envio.",
            "Subsection",
        ),
    ]
)


doc = SimpleDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    rightMargin=1.7 * cm,
    leftMargin=1.7 * cm,
    topMargin=1.75 * cm,
    bottomMargin=2.2 * cm,
    title="Alerta Clima Seguro - Relatório Técnico do Desafio 5",
    author="Grupo 01 - InsurMinds/I2A2",
)
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUTPUT)
