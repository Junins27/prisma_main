from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (KeepTogether, Paragraph, SimpleDocTemplate,
                                Spacer, Table, TableStyle, PageBreak)

OUTPUT = Path("output/pdf/resumo-desenvolvimento-prisma.pdf")

NAVY = colors.HexColor("#13171B")
SLATE = colors.HexColor("#242A30")
GOLD = colors.HexColor("#D1A45B")
PAPER = colors.HexColor("#F7F4EE")
MUTED = colors.HexColor("#6B6D70")
LINE = colors.HexColor("#D9D9D6")


def paragraph(text, style):
    return Paragraph(text, style)


def build():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=1.8 * cm, leftMargin=1.8 * cm,
        topMargin=1.7 * cm, bottomMargin=1.6 * cm,
        title="Resumo de desenvolvimento - Prisma",
        author="Prisma",
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitlePrisma", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=25, leading=29, textColor=NAVY, spaceAfter=7,
    ))
    styles.add(ParagraphStyle(
        name="Kicker", parent=styles["BodyText"], fontName="Helvetica-Bold",
        fontSize=8, leading=11, textColor=GOLD, uppercase=True, tracking=1.1,
    ))
    styles.add(ParagraphStyle(
        name="SectionPrisma", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=14, leading=18, textColor=NAVY, spaceBefore=16, spaceAfter=7,
    ))
    styles.add(ParagraphStyle(
        name="BodyPrisma", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=9.5, leading=14, textColor=SLATE, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="SmallPrisma", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=8.2, leading=11.5, textColor=MUTED,
    ))
    styles.add(ParagraphStyle(
        name="CardTitle", parent=styles["BodyText"], fontName="Helvetica-Bold",
        fontSize=10, leading=13, textColor=NAVY, spaceAfter=3,
    ))
    styles.add(ParagraphStyle(
        name="FooterPrisma", parent=styles["BodyText"], fontName="Helvetica",
        fontSize=7.5, leading=10, textColor=MUTED, alignment=TA_CENTER,
    ))

    def footer(canvas, _doc):
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.line(1.8 * cm, 1.15 * cm, A4[0] - 1.8 * cm, 1.15 * cm)
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(MUTED)
        canvas.drawCentredString(A4[0] / 2, .72 * cm, f"PRISMA  |  Resumo de desenvolvimento  |  Página {_doc.page}")
        canvas.restoreState()

    story = []
    story += [
        paragraph("DOCUMENTAÇÃO DE ENTREGA", styles["Kicker"]),
        paragraph("Prisma - resumo de desenvolvimento", styles["TitlePrisma"]),
        paragraph("Portfólio institucional com painel editorial personalizado, persistência em Cloudflare e gestão de conteúdo autorizada.", styles["BodyPrisma"]),
        Spacer(1, 7),
    ]
    banner = Table([[paragraph("<b>STATUS</b><br/>Site publicado e integrado ao Cloudflare Worker", styles["BodyPrisma"]), paragraph("<b>ATUALIZADO EM</b><br/>%s" % date.today().strftime("%d/%m/%Y"), styles["BodyPrisma"]), paragraph("<b>PAINEL</b><br/>/painel/", styles["BodyPrisma"])]], colWidths=[6.2 * cm, 4.7 * cm, 4.9 * cm])
    banner.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), PAPER), ("BOX", (0, 0), (-1, -1), .5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), .5, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 11), ("RIGHTPADDING", (0, 0), (-1, -1), 11),
        ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    story += [banner, Spacer(1, 8)]

    story += [
        paragraph("O que foi construído", styles["SectionPrisma"]),
        paragraph("A Prisma agora opera como um site de portfólio com duas versões visuais (Golden Hour e Solar Editorial), páginas para as frentes de Marketing e Tecnologia, listagem e página individual de cases, formulário de contato e uma área administrativa feita sob medida para a equipe.", styles["BodyPrisma"]),
    ]
    cards = [
        ("Portfólio e cases", "Cases de Marketing e Tecnologia, status de publicação, destaque, página individual, botão externo e galeria com até cinco imagens."),
        ("Imagens com enquadramento", "Cada imagem de case pode ser exibida inteira ou preenchendo o quadro, com ajustes de zoom e ponto focal sem editar o arquivo original."),
        ("Sobre nós", "Três perfis editáveis, com foto, nome, cargo e bio. Um perfil só aparece publicamente depois que tiver nome preenchido."),
        ("Contato", "E-mail, telefone, WhatsApp, disponibilidade, localização, Instagram e LinkedIn aparecem no rodapé quando informados."),
    ]
    card_rows = []
    for left, right in zip(cards[::2], cards[1::2]):
        card_rows.append([
            paragraph(f"<b>{left[0]}</b><br/>{left[1]}", styles["SmallPrisma"]),
            paragraph(f"<b>{right[0]}</b><br/>{right[1]}", styles["SmallPrisma"]),
        ])
    feature_table = Table(card_rows, colWidths=[7.9 * cm, 7.9 * cm], hAlign="LEFT")
    feature_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), .5, LINE), ("INNERGRID", (0, 0), (-1, -1), .5, LINE),
        ("BACKGROUND", (0, 0), (-1, -1), colors.white), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story += [feature_table]

    story += [paragraph("Novas provas de repertório", styles["SectionPrisma"])]
    new_rows = [
        [paragraph("<b>Indicadores por case</b><br/>Até três resultados reais e verificáveis por case. Quando preenchidos, aparecem como impactos na página individual do projeto.", styles["SmallPrisma"]), paragraph("<b>Depoimentos</b><br/>Até três falas com pessoa, cargo ou empresa. Cada item exige acionamento explícito para ser publicado.", styles["SmallPrisma"])],
        [paragraph("<b>Marcas e parceiros</b><br/>Até seis marcas com logo opcional, site e confirmação obrigatória de autorização antes da exibição pública.", styles["SmallPrisma"]), paragraph("<b>Insights da Prisma</b><br/>Até quatro conteúdos com título, categoria, resumo, data e link externo para evidenciar o repertório da equipe.", styles["SmallPrisma"])],
    ]
    new_table = Table(new_rows, colWidths=[7.9 * cm, 7.9 * cm], hAlign="LEFT")
    new_table.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), .5, LINE), ("INNERGRID", (0, 0), (-1, -1), .5, LINE),
        ("BACKGROUND", (0, 0), (-1, -1), PAPER), ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story += [new_table]

    story += [PageBreak(), paragraph("Como administrar", styles["SectionPrisma"])]
    steps = [
        "Acesse <b>/painel/</b> com a senha editorial configurada nos Secrets do Cloudflare.",
        "Em <b>Cases</b>, crie ou edite um case, envie até cinco imagens e, se houver dados aprovados, preencha os impactos e resultados.",
        "Em <b>Sobre nós</b>, preencha os três perfis. A foto é opcional; nome, cargo e bio ficam ao lado dela no site.",
        "Em <b>Dados de contato</b>, atualize os canais exibidos no rodapé.",
        "Em <b>Conteúdos</b>, cadastre depoimentos, marcas e insights. Publique somente o que tiver autorização de uso e dados confirmados.",
    ]
    for number, step in enumerate(steps, 1):
        row = Table([[paragraph(f"{number:02d}", styles["Kicker"]), paragraph(step, styles["BodyPrisma"])]], colWidths=[.75 * cm, 15.05 * cm])
        row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, -1), .35, LINE), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
        story.append(row)

    story += [
        paragraph("Operação editorial", styles["Kicker"]),
        paragraph("Arquitetura e segurança", styles["SectionPrisma"]),
        paragraph("O front-end estático é servido pelo Cloudflare Worker. Dados editoriais são persistidos no banco D1 e imagens ficam no bucket R2. A área administrativa usa sessão assinada e senha mantida exclusivamente em Secrets do Cloudflare; as credenciais não fazem parte do repositório.", styles["BodyPrisma"]),
        paragraph("Princípio editorial adotado: o sistema não inclui cases, resultados, depoimentos, marcas ou conteúdos fictícios. Itens só aparecem no site após preenchimento e, quando aplicável, confirmação de publicação ou autorização.", styles["SmallPrisma"]),
    ]
    story += [
        paragraph("Regras de publicação", styles["SectionPrisma"]),
        paragraph("Valide conteúdo, métricas e autorizações antes de publicar. Resultados devem ser verificáveis; depoimentos precisam de consentimento; marcas só aparecem após a confirmação no painel. O original de cada imagem é preservado no R2 e as credenciais ficam exclusivamente nos Secrets do Cloudflare.", styles["BodyPrisma"]),
    ]
    story += [
        paragraph("Uso recomendado", styles["SectionPrisma"]),
        paragraph("Comece pelos cases e pelos perfis da equipe. Em seguida, publique uma prova de cada vez: um resultado comprovado, um depoimento autorizado, uma marca autorizada e um insight com link. Esse ritmo preserva a credibilidade do portfólio e permite revisar cada bloco antes de ampliar a presença institucional.", styles["BodyPrisma"]),
    ]
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
