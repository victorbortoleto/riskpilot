from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)


def _money(value):
    try:
        return f"${float(value):,.2f}"
    except Exception:
        return "$0.00"


def _percent(value):
    try:
        return f"{float(value):.2f}%"
    except Exception:
        return "0.00%"


def _safe(value):
    if value is None:
        return "-"
    return str(value)


def build_pdf_report(
    language,
    title,
    subtitle,
    file_name,
    prop_mode,
    account_size,
    metrics,
    scores,
    prop_status,
    insights,
    diagnosis_items,
    alerts,
    trades_df,
):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.4 * cm,
        leftMargin=1.4 * cm,
        topMargin=1.3 * cm,
        bottomMargin=1.3 * cm,
    )

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="RiskTitle",
            parent=styles["Title"],
            fontSize=24,
            leading=30,
            textColor=colors.HexColor("#0F172A"),
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="RiskSubtitle",
            parent=styles["BodyText"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#475569"),
            spaceAfter=14,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#0F172A"),
            spaceBefore=14,
            spaceAfter=8,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Small",
            parent=styles["BodyText"],
            fontSize=8,
            leading=11,
            textColor=colors.HexColor("#334155"),
        )
    )

    story = []

    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    story.append(Paragraph("RiskPilot", styles["RiskTitle"]))
    story.append(Paragraph(subtitle, styles["RiskSubtitle"]))

    header_data = [
        ["Report", title],
        ["File", _safe(file_name)],
        ["Prop Firm Mode", _safe(prop_mode)],
        ["Account Size", _money(account_size)],
        ["Generated At", generated_at],
    ]

    header_table = Table(header_data, colWidths=[4.0 * cm, 12.0 * cm])
    header_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#0F172A")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("PADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(header_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Performance Overview", styles["Section"]))

    performance = [
        ["Metric", "Value"],
        ["Net P&L", _money(metrics.get("net_pnl", 0))],
        ["Winrate", _percent(metrics.get("winrate", 0))],
        ["Profit Factor", f"{float(metrics.get('profit_factor', 0)):.2f}"],
        ["Max Drawdown", _money(metrics.get("max_drawdown", 0))],
        ["Total Trades", _safe(metrics.get("total_trades", 0))],
        ["Average Win", _money(metrics.get("average_win", 0))],
        ["Average Loss", _money(metrics.get("average_loss", 0))],
        ["Max Win Streak", _safe(metrics.get("max_win_streak", 0))],
        ["Max Loss Streak", _safe(metrics.get("max_loss_streak", 0))],
    ]

    table = Table(performance, colWidths=[8.0 * cm, 8.0 * cm])
    table.setStyle(_standard_table_style())
    story.append(table)

    story.append(Paragraph("Risk Scores", styles["Section"]))

    risk_score, consistency_score, account_health, behavior_score = scores

    score_data = [
        ["Score", "Value"],
        ["Risk Score", f"{risk_score}/100"],
        ["Consistency Score", f"{consistency_score}/100"],
        ["Account Health", f"{account_health}/100"],
        ["Behavior Score", f"{behavior_score}/100"],
    ]

    table = Table(score_data, colWidths=[8.0 * cm, 8.0 * cm])
    table.setStyle(_standard_table_style())
    story.append(table)

    story.append(Paragraph("Prop Firm Control", styles["Section"]))

    approval, daily_remaining, dd_remaining, target_distance, violation_score = prop_status

    prop_data = [
        ["Metric", "Value"],
        ["Approval Probability", f"{approval}/100"],
        ["Daily Loss Remaining", _money(daily_remaining)],
        ["Max Drawdown Remaining", _money(dd_remaining)],
        ["Target Distance", _money(target_distance)],
        ["Violation Risk", f"{violation_score}/100"],
    ]

    table = Table(prop_data, colWidths=[8.0 * cm, 8.0 * cm])
    table.setStyle(_standard_table_style())
    story.append(table)

    story.append(Paragraph("Automatic Insights", styles["Section"]))

    insight_rows = [["Insight", "Value", "Result"]]
    for item in insights:
        insight_rows.append([
            _safe(item.get("label")),
            _safe(item.get("value")),
            _safe(item.get("result")),
        ])

    table = Table(insight_rows, colWidths=[5.2 * cm, 5.2 * cm, 5.2 * cm])
    table.setStyle(_standard_table_style())
    story.append(table)

    story.append(PageBreak())

    story.append(Paragraph("Operational Diagnosis", styles["Section"]))

    for item in diagnosis_items:
        story.append(Paragraph(f"• {item}", styles["Small"]))
        story.append(Spacer(1, 5))

    story.append(Paragraph("Risk Alerts", styles["Section"]))

    for alert in alerts:
        story.append(Paragraph(f"• {alert}", styles["Small"]))
        story.append(Spacer(1, 5))

    story.append(Paragraph("Trade Sample", styles["Section"]))

    sample = trades_df.copy().head(25)

    columns = [col for col in ["date", "asset", "side", "quantity", "net_pnl"] if col in sample.columns]

    trade_rows = [columns]

    for _, row in sample.iterrows():
        trade_rows.append([_safe(row.get(col)) for col in columns])

    if len(trade_rows) > 1:
        table = Table(trade_rows, repeatRows=1)
        table.setStyle(_standard_table_style(font_size=7))
        story.append(table)
    else:
        story.append(Paragraph("No trades available.", styles["Small"]))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Generated by RiskPilot - Trading Risk Analytics", styles["Small"]))

    doc.build(story)

    buffer.seek(0)
    return buffer.getvalue()


def _standard_table_style(font_size=8):
    return TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0F172A")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), font_size),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#CBD5E1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]
    )
