import flet as ft
import matplotlib.pyplot as plt
import io
import base64
import csv


def calcular_historico(capital_inicial: float, aporte_mensal: float, taxa_anual_pct: float, anos: float):
    """Calcula o histórico de saldos mensalmente com capitalização mensal.

    Retorna lista de saldos por mês e resumo anual (saldo no final de cada ano).
    """
    meses = int(round(anos * 12))
    taxa_mensal = taxa_anual_pct / 100 / 12

    saldos = []
    saldo = float(capital_inicial)
    for m in range(1, meses + 1):
        # aplicar juros
        saldo = saldo * (1 + taxa_mensal)
        # aporte ao final do mês
        saldo += aporte_mensal
        saldos.append(saldo)

    # resumo anual
    resumo_anual = []
    for y in range(1, int(anos) + 1):
        idx = y * 12 - 1
        if idx < len(saldos):
            resumo_anual.append((y, saldos[idx]))

    return saldos, resumo_anual


def plot_saldos_to_base64(saldos):
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(range(1, len(saldos) + 1), saldos, marker="", linewidth=2)
    ax.set_xlabel("Mês")
    ax.set_ylabel("Saldo (R$)")
    ax.grid(alpha=0.3)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    img_bytes = buf.read()
    img_b64 = base64.b64encode(img_bytes).decode("ascii")
    return img_b64


def main(page: ft.Page):
    page.title = "Calculadora de Juros Compostos"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 900

    # Inputs
    capital = ft.TextField(label="Capital inicial (R$)", value="1000", width=200)
    aporte = ft.TextField(label="Aporte mensal (R$)", value="100", width=200)
    taxa = ft.TextField(label="Taxa anual (%)", value="5", width=200)
    periodo = ft.TextField(label="Período (anos)", value="10", width=200)

    resultado_text = ft.Text(value="Preencha os campos e clique em Calcular", size=14)
    imagem = ft.Image(width=780, height=260)

    tabela = ft.DataTable(columns=[ft.DataColumn(ft.Text("Ano")), ft.DataColumn(ft.Text("Saldo (R$)"))],
                          rows=[],
                          width=780)

    def mostrar_resultados(e=None):
        try:
            c = float(capital.value)
            a = float(aporte.value)
            t = float(taxa.value)
            p = float(periodo.value)
            if c < 0 or a < 0 or t < 0 or p <= 0:
                raise ValueError("Valores devem ser não-negativos e período > 0")
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {err}"))
            page.snack_bar.open = True
            page.update()
            return

        saldos, resumo = calcular_historico(c, a, t, p)
        final = saldos[-1] if saldos else c
        total_aportes = a * int(round(p * 12))
        juros = final - c - total_aportes

        resultado_text.value = f"Saldo final: R$ {final:,.2f}    |    Total aportado: R$ {total_aportes:,.2f}    |    Juros: R$ {juros:,.2f}"

        # atualizar tabela anual
        tabela.rows.clear()
        for ano, saldo in resumo:
            tabela.rows.append(ft.DataRow(cells=[ft.DataCell(ft.Text(str(ano))), ft.DataCell(ft.Text(f"R$ {saldo:,.2f}"))]))

        # plot
        img_b64 = plot_saldos_to_base64(saldos)
        imagem.src_base64 = img_b64

        page.update()

    def export_csv(e=None):
        try:
            c = float(capital.value)
            a = float(aporte.value)
            t = float(taxa.value)
            p = float(periodo.value)
        except Exception as err:
            page.snack_bar = ft.SnackBar(ft.Text(f"Erro: {err}"))
            page.snack_bar.open = True
            page.update()
            return

        saldos, _ = calcular_historico(c, a, t, p)
        filename = "calculadora_juros_result.csv"
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Mes", "Saldo (R$)"])
            for i, s in enumerate(saldos, start=1):
                writer.writerow([i, f"{s:.2f}"])

        page.snack_bar = ft.SnackBar(ft.Text(f"CSV exportado: {filename}"))
        page.snack_bar.open = True
        page.update()

    btn_calcular = ft.ElevatedButton(text="Calcular", on_click=mostrar_resultados)
    btn_export = ft.ElevatedButton(text="Exportar CSV", on_click=export_csv)

    controls = ft.Row([capital, aporte, taxa, periodo, btn_calcular, btn_export], alignment=ft.MainAxisAlignment.START)

    page.add(
        ft.Column([
            ft.Text("Calculadora de Juros Compostos", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("Informe os parâmetros abaixo:", size=12),
            controls,
            ft.Divider(),
            resultado_text,
            imagem,
            ft.Divider(),
            ft.Text("Resumo anual:", weight=ft.FontWeight.BOLD),
            tabela
        ], spacing=12)
    )


if __name__ == "__main__":
    ft.app(target=main)
