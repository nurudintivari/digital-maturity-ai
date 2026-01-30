from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from datetime import datetime

# ===== REGISTRACIJA UNICODE FONT-A (SIGURNO) =====
pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))

# ===== BENCHMARK =====
BENCHMARK = {
    "IT infrastruktura": 3.8,
    "Procesna digitalizacija": 3.5,
    "Podaci i analitika": 3.4,
    "Cyber bezbjednost": 3.9,
    "Digitalne kompetencije": 3.6
}

def generate_pdf(
    kompanija,
    indeks,
    nivo,
    dimenzije,
    filename="izvjestaj_digitalne_zrelosti.pdf"
):
    doc = SimpleDocTemplate(filename)

    # ===== STILOVI SA UNICODE FONTOM =====
    style_title = ParagraphStyle(
        name="Title",
        fontName="HeiseiKakuGo-W5",
        fontSize=16,
        spaceAfter=14
    )

    style_normal = ParagraphStyle(
        name="Normal",
        fontName="HeiseiKakuGo-W5",
        fontSize=10,
        spaceAfter=6
    )

    style_header = ParagraphStyle(
        name="Header",
        fontName="HeiseiKakuGo-W5",
        fontSize=12,
        spaceAfter=10
    )

    sadrzaj = []

    # NASLOV
    sadrzaj.append(Paragraph(
        "Izvještaj o digitalnoj zrelosti kompanije",
        style_title
    ))

    # OSNOVNE INFORMACIJE
    sadrzaj.append(Paragraph(
        f"Kompanija: {kompanija}", style_normal
    ))
    sadrzaj.append(Paragraph(
        f"Datum: {datetime.now().strftime('%d.%m.%Y')}", style_normal
    ))
    sadrzaj.append(Paragraph(
        f"Indeks digitalne zrelosti: {indeks}", style_normal
    ))
    sadrzaj.append(Paragraph(
        f"Nivo digitalne zrelosti: {nivo}", style_normal
    ))
    sadrzaj.append(Spacer(1, 12))

    # ===== TABELA =====
    sadrzaj.append(Paragraph(
        "Poređenje sa referentnim benchmarkom",
        style_header
    ))

    tabela_podaci = [
        ["Dimenzija", "Vaša ocjena", "Benchmark industrije"]
    ]

    for dim, val in dimenzije.items():
        tabela_podaci.append([
            dim,
            f"{round(val, 2)}",
            f"{BENCHMARK.get(dim, 'N/A')}"
        ])

    tabela = Table(tabela_podaci, colWidths=[220, 120, 160])
    tabela.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "HeiseiKakuGo-W5"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
    ]))

    sadrzaj.append(tabela)
    sadrzaj.append(Spacer(1, 14))

    # ===== INTERPRETACIJA =====
    sadrzaj.append(Paragraph(
        "Interpretacija rezultata",
        style_header
    ))

    for dim, val in dimenzije.items():
        ref = BENCHMARK.get(dim, 0)
        if val >= ref:
            txt = f"{dim}: rezultat je u skladu ili iznad prosjeka industrije."
        else:
            txt = f"{dim}: rezultat je ispod prosjeka industrije – preporučuje se unapređenje."
        sadrzaj.append(Paragraph(txt, style_normal))

    doc.build(sadrzaj)
    return filename
