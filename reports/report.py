from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import os

VIZ_DIR = os.path.join(os.path.dirname(__file__), "..", "visualization")

def generate_report(results, df=None):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    REPORT_PATH = os.path.join(os.path.dirname(__file__), f"report_{timestamp}.pdf")

    doc = SimpleDocTemplate(REPORT_PATH, pagesize=letter,
                            leftMargin=0.75*inch, rightMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story  = []

    title_style = ParagraphStyle("title", parent=styles["Title"],
                                 fontSize=20, textColor=colors.HexColor("#1a3c5e"),
                                 spaceAfter=6, alignment=TA_CENTER)
    date_style  = ParagraphStyle("date", parent=styles["Normal"],
                                 fontSize=9, textColor=colors.grey,
                                 spaceAfter=20, alignment=TA_CENTER)

    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Performance Analysis Report", title_style))
    story.append(Paragraph(datetime.now().strftime("%B %d, %Y"), date_style))
    story.append(Spacer(1, 0.2*inch))

    def section(title):
        s = ParagraphStyle("sec", parent=styles["Heading2"],
                           fontSize=12, textColor=colors.HexColor("#1a3c5e"),
                           spaceBefore=14, spaceAfter=6)
        story.append(Paragraph(title, s))

    # ── Dataset Summary ───────────────────────────────────────────────────
    if df is not None:
        section("Dataset Summary")
        summary_data = [
            ["Total Records", str(len(df))],
            ["Total Columns", str(len(df.columns))],
            ["Columns", ", ".join(df.columns.tolist())],
        ]
        ts = Table(summary_data, colWidths=[2.5*inch, 4.5*inch])
        ts.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (0, -1), colors.HexColor("#f0f4f8")),
            ("FONTNAME",      (0, 0), (0, -1), "Helvetica-Bold"),
            ("GRID",          (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("ALIGN",         (0, 0), (-1, -1), "LEFT"),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ]))
        story.append(ts)
        story.append(Spacer(1, 0.15*inch))

    # ── Network Health Score (only if present) ────────────────────────────
    if results.get("network_health_score") is not None:
        section("Network Health Score")
        score = results.get("network_health_score", 0)
        color = "#27ae60" if score >= 70 else ("#f39c12" if score >= 50 else "#e74c3c")
        t = Table([["Metric", "Score"], ["Overall Network Health", f"{score} / 100"]],
                  colWidths=[3.5*inch, 2*inch])
        t.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0), colors.HexColor("#1a3c5e")),
            ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
            ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BACKGROUND",    (0, 1), (-1, 1), colors.HexColor(color)),
            ("TEXTCOLOR",     (0, 1), (-1, 1), colors.white),
            ("FONTNAME",      (0, 1), (-1, 1), "Helvetica-Bold"),
            ("FONTSIZE",      (0, 1), (-1, 1), 13),
            ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
            ("GRID",          (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("TOPPADDING",    (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ]))
        story.append(t)
        story.append(Spacer(1, 0.15*inch))

    # ── Key Performance Metrics — auto from df ────────────────────────────
    section("Key Performance Metrics")

    if df is not None:
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        numeric_cols = [c for c in numeric_cols if "id" not in c.lower()]

        table_data = [["Metric", "Mean", "Min", "Max", "Std Dev"]]
        for col in numeric_cols:
            table_data.append([
                col.replace("_", " ").title(),
                f"{df[col].mean():.4f}",
                f"{df[col].min():.4f}",
                f"{df[col].max():.4f}",
                f"{df[col].std():.4f}",
            ])

        t2 = Table(table_data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
        t2.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0), colors.HexColor("#1a3c5e")),
            ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
            ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.HexColor("#f0f4f8"), colors.white]),
            ("ALIGN",         (1, 0), (-1, -1), "CENTER"),
            ("GRID",          (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t2)
    else:
        # fallback if no df passed — use whatever is in results
        table_data = [["Metric", "Value"]]
        for key, val in results.items():
            try:
                table_data.append([key.replace("_", " ").title(), f"{float(val):.4f}"])
            except (TypeError, ValueError):
                pass
        t2 = Table(table_data, colWidths=[3.5*inch, 2*inch])
        t2.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0), colors.HexColor("#1a3c5e")),
            ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
            ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.HexColor("#f0f4f8"), colors.white]),
            ("ALIGN",         (1, 0), (1, -1), "CENTER"),
            ("GRID",          (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t2)

    story.append(Spacer(1, 0.15*inch))

    # ── Alerts (only if WSN-specific keys exist) ──────────────────────────
    hl = results.get("high_latency_count")
    lp = results.get("low_pdr_count")
    ce = results.get("critical_energy_count")

    if any(x is not None for x in [hl, lp, ce]):
        section("Network Alerts")
        def status(count): return "Warning" if count > 0 else "OK"
        alert_rows = [["Alert Type", "Node Count", "Status"]]
        if hl is not None:
            alert_rows.append(["High Latency (> 150ms)", str(hl), status(hl)])
        if lp is not None:
            alert_rows.append(["Low PDR (< 0.8)", str(lp), status(lp)])
        if ce is not None:
            alert_rows.append(["Critical Energy (> 4J)", str(ce), status(ce)])

        t3 = Table(alert_rows, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        t3.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0), colors.HexColor("#1a3c5e")),
            ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
            ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS",(0, 1), (-1, -1), [colors.HexColor("#fff3cd"), colors.white]),
            ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
            ("GRID",          (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("TOPPADDING",    (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(t3)
        story.append(Spacer(1, 0.2*inch))

    # ── Charts (only if they exist) ───────────────────────────────────────
    chart_files = [f for f in os.listdir(VIZ_DIR) if f.endswith(".png")] if os.path.exists(VIZ_DIR) else []
    if chart_files:
        section("Analysis Charts")
        for fname in sorted(chart_files):
            fpath = os.path.join(VIZ_DIR, fname)
            caption = fname.replace(".png", "").replace("_", " ").title()
            story.append(Paragraph(caption, styles["Italic"]))
            story.append(Image(fpath, width=6*inch, height=2.8*inch))
            story.append(Spacer(1, 0.15*inch))

    doc.build(story)
    print(f"  Report saved → {REPORT_PATH}")