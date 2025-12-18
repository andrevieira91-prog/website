"""Gera um relatório PDF automático para o projeto "Calculadora de Juros Compostos".

Gera imagens dos cenários de teste, salva CSVs e compõe um PDF com capa, descrição,
resultados e comparação entre cenários.

Uso: python exercicios_flet/calculadora_juros/generate_report.py

Dependências: reportlab, matplotlib
"""

import os
from datetime import datetime

import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def calcular_historico(capital_inicial: float, aporte_mensal: float, taxa_anual_pct: float, anos: float):
    meses = int(round(anos * 12))
    taxa_mensal = taxa_anual_pct / 100 / 12

    saldos = []
    saldo = float(capital_inicial)
    for m in range(1, meses + 1):
        saldo = saldo * (1 + taxa_mensal)
        saldo += aporte_mensal
        saldos.append(saldo)

    resumo_anual = []
    for y in range(1, int(anos) + 1):
        idx = y * 12 - 1
        if idx < len(saldos):
            resumo_anual.append((y, saldos[idx]))

    return saldos, resumo_anual


OUTPUT_PDF = "AndreMoisesVieiraDaSilvaMuller_ProjetoFinalFlet.pdf"
OUT_DIR = "exercicios_flet/calculadora_juros/reports"
os.makedirs(OUT_DIR, exist_ok=True)

SCENARIOS = {
    "Padrão": {"capital": 1000, "aporte": 100, "taxa": 5, "periodo": 10},
    "Sem aporte": {"capital": 1000, "aporte": 0, "taxa": 5, "periodo": 10},
    "Com aporte e taxa maior": {"capital": 1000, "aporte": 200, "taxa": 7, "periodo": 20},
}


def plot_save(saldos, filename):
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.plot(range(1, len(saldos) + 1), saldos, linewidth=2)
    ax.set_xlabel("Mês")
    ax.set_ylabel("Saldo (R$)")
    ax.grid(alpha=0.25)
    plt.tight_layout()
    fig.savefig(filename, dpi=150)
    plt.close(fig)


def save_csv(saldos, filename):
    import csv
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Mes", "Saldo (R$)"])
        for i, s in enumerate(saldos, start=1):
            writer.writerow([i, f"{s:.2f}"])


def generate_pdf(report_path, author_name="Andre Moisés Vieira da Silva Müller"):
    c = canvas.Canvas(report_path, pagesize=A4)
    width, height = A4

    # Capa
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 40 * mm, "Calculadora de Juros Compostos")
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 50 * mm, f"Aluno: {author_name}")
    c.drawCentredString(width / 2, height - 60 * mm, f"Data: {datetime.now().strftime('%Y-%m-%d')}")
    c.showPage()

    # Sumário e descrição
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, height - 20 * mm, "1. Descrição do Projeto")
    c.setFont("Helvetica", 10)
    text = c.beginText(20 * mm, height - 30 * mm)
    text.textLines([
        "Aplicação em Flet que calcula a evolução de um investimento com aportes mensais e",
        "capitalização mensal. Este relatório apresenta cenários de teste, gráficos e arquivos CSV gerados.",
    ])
    c.drawText(text)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(20 * mm, height - 70 * mm, "Requisitos implementados:")
    c.setFont("Helvetica", 10)
    text = c.beginText(20 * mm, height - 78 * mm)
    text.textLines([
        "- Entradas: capital inicial, aporte mensal, taxa anual (%), período (anos)",
        "- Cálculo mês a mês com capitalização mensal",
        "- Gráfico da evolução gerado por matplotlib",
        "- Tabela anual com saldos ao final de cada ano",
        "- Exportação para CSV (arquivo no diretório do projeto)",
    ])
    c.drawText(text)
    c.showPage()

    # Cenários
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, height - 20 * mm, "2. Cenários e resultados")

    y = height - 30 * mm

    for title, params in SCENARIOS.items():
        saldos, resumo = calcular_historico(params["capital"], params["aporte"], params["taxa"], params["periodo"])
        final = saldos[-1] if saldos else params["capital"]
        total_aportes = params["aporte"] * int(round(params["periodo"] * 12))
        juros = final - params["capital"] - total_aportes

        # salvar imagem e csv
        img_path = os.path.join(OUT_DIR, f"{title.replace(' ', '_')}.png")
        csv_path = os.path.join(OUT_DIR, f"{title.replace(' ', '_')}.csv")
        plot_save(saldos, img_path)
        save_csv(saldos, csv_path)

        # adicionar texto e imagem
        c.setFont("Helvetica-Bold", 12)
        c.drawString(20 * mm, y, f"Cenário: {title}")
        y -= 8 * mm
        c.setFont("Helvetica", 10)
        c.drawString(22 * mm, y, f"Parâmetros: capital={params['capital']}, aporte={params['aporte']}, taxa={params['taxa']}%, período={params['periodo']} anos")
        y -= 6 * mm
        c.drawString(22 * mm, y, f"Saldo final: R$ {final:,.2f}    |    Total aportado: R$ {total_aportes:,.2f}    |    Juros: R$ {juros:,.2f}")
        y -= 8 * mm

        # inserir imagem
        c.drawImage(img_path, 22 * mm, y - 50 * mm, width=160 * mm, height=40 * mm)
        y -= 56 * mm

        # referência ao CSV
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(22 * mm, y, f"CSV gerado: {csv_path}")
        y -= 10 * mm

        if y < 70 * mm:
            c.showPage()
            y = height - 30 * mm

    # análise comparativa (simples)
    c.showPage()
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, height - 20 * mm, "3. Análise comparativa")
    c.setFont("Helvetica", 10)

    lines = []
    # ordenar por saldo final
    results = []
    for title, params in SCENARIOS.items():
        saldos, _ = calcular_historico(params["capital"], params["aporte"], params["taxa"], params["periodo"])
        final = saldos[-1] if saldos else params["capital"]
        results.append((title, final))
    results.sort(key=lambda x: x[1], reverse=True)

    for r in results:
        lines.append(f"{r[0]} -> Saldo final: R$ {r[1]:,.2f}")

    text = c.beginText(20 * mm, height - 40 * mm)
    text.textLines(lines)
    c.drawText(text)

    c.showPage()
    c.save()


if __name__ == "__main__":
    print("Gerando relatório... (pode demorar alguns segundos)")
    generate_pdf(os.path.join(OUT_DIR, OUTPUT_PDF))
    print("Relatório gerado em:", os.path.join(OUT_DIR, OUTPUT_PDF))
