"""Build an Excel workbook with analysis tables and a comparison chart."""
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parents[1]
OUT, DATA = ROOT / "outputs", ROOT / "data"


def build():
    OUT.mkdir(exist_ok=True)
    tables = {
        "Offer Data": pd.read_csv(DATA / "offers.csv"),
        "Optimised Basket": pd.read_csv(OUT / "optimised_allocation.csv"),
        "Strategy Compare": pd.read_csv(OUT / "strategy_comparison.csv"),
        "Platform Costs": pd.read_csv(OUT / "platform_cost_breakdown.csv"),
        "Platform Summary": pd.read_csv(OUT / "platform_offer_summary.csv"),
    }
    path = OUT / "Basket_Economics_Dashboard.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for sheet, frame in tables.items():
            frame.to_excel(writer, sheet_name=sheet, index=False)
    wb = load_workbook(path)
    for ws in wb.worksheets:
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for cell in ws[1]:
            cell.font = Font(bold=True, color="FFFFFF")
            cell.fill = PatternFill("solid", fgColor="17365D")
            cell.alignment = Alignment(horizontal="center")
        for column in ws.columns:
            width = min(max(max(len(str(c.value or "")) for c in column) + 2, 12), 34)
            ws.column_dimensions[get_column_letter(column[0].column)].width = width
    ws = wb["Strategy Compare"]
    chart = BarChart(); chart.type = "bar"; chart.style = 10
    chart.title = "Basket Cost by Strategy"; chart.y_axis.title = "Strategy"; chart.x_axis.title = "Cost (INR)"
    chart.add_data(Reference(ws, min_col=2, min_row=1, max_row=ws.max_row), titles_from_data=True)
    chart.set_categories(Reference(ws, min_col=1, min_row=2, max_row=ws.max_row))
    chart.height, chart.width = 8, 15
    ws.add_chart(chart, "G2")
    wb.save(path)
    print(f"Created {path.relative_to(ROOT)}")

if __name__ == "__main__":
    build()
