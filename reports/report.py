from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_report(results):
    c = canvas.Canvas("reports/report.pdf", pagesize=letter)

    y = 750
    for key, value in results.items():
        c.drawString(100, y, f"{key}: {value:.2f}")
        y -= 20

    c.save()