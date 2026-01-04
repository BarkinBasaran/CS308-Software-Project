from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime

def generate_invoice_pdf(order, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    elements = []
    styles = getSampleStyleSheet()
    
    # ChipMaster Header
    header_style = ParagraphStyle(
        'Header', parent=styles['Heading1'], fontSize=28, alignment=TA_CENTER, textColor=colors.HexColor('#ff5e62'), spaceAfter=8, spaceBefore=0, fontName='Helvetica-Bold'
    )
    elements.append(Paragraph("ChipMaster", header_style))
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'], fontSize=13, alignment=TA_CENTER, textColor=colors.HexColor('#292929'), spaceAfter=18, spaceBefore=0, fontName='Helvetica-Bold'
    )
    elements.append(Paragraph("Small Chips, Big Impact", subtitle_style))

    # Invoice Title
    invoice_title_style = ParagraphStyle(
        'InvoiceTitle', parent=styles['Heading2'], fontSize=20, alignment=TA_CENTER, textColor=colors.HexColor('#222'), spaceAfter=18, fontName='Helvetica-Bold'
    )
    elements.append(Paragraph(f"INVOICE #{order.id}", invoice_title_style))

    # Order & Customer Info Table
    info_data = [
        [
            Paragraph('<b>Order Date:</b>', styles['Normal']), order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            Paragraph('<b>Status:</b>', styles['Normal']), order.status.title()
        ],
        [
            Paragraph('<b>Payment Method:</b>', styles['Normal']), order.payment_method,
            Paragraph('<b>Customer:</b>', styles['Normal']), order.user.username
        ],
        [
            Paragraph('<b>Delivery Address:</b>', styles['Normal']), order.delivery_address,
            Paragraph('<b>Billing Address:</b>', styles['Normal']), order.billing_address
        ]
    ]
    info_table = Table(info_data, colWidths=[1.3*inch, 2.2*inch, 1.3*inch, 2.2*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f7f7f7')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, 2), (-1, 2), 1, colors.HexColor('#ff5e62')),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 18))

    # Order Items Table
    items_data = [[
        Paragraph('<b>Product</b>', styles['Normal']),
        Paragraph('<b>Quantity</b>', styles['Normal']),
        Paragraph('<b>Unit Price</b>', styles['Normal']),
        Paragraph('<b>Total</b>', styles['Normal'])
    ]]
    for item in order.order_items:
        items_data.append([
            item.product.name,
            str(item.quantity),
            f"${float(item.unit_price):.2f}",
            f"${float(item.total_price):.2f}"
        ])
    items_table = Table(items_data, colWidths=[3*inch, inch, inch, inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ff5e62')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f7f7f7')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#222')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ff5e62')),
    ]))
    elements.append(items_table)
    elements.append(Spacer(1, 18))

    # Totals Table
    subtotal = float(order.total_price)
    tax = subtotal * 0.18
    total = subtotal * 1.18
    total_data = [
        [Paragraph('<b>Subtotal:</b>', styles['Normal']), f"${subtotal:.2f}"],
        [Paragraph('<b>Tax (18%):</b>', styles['Normal']), f"${tax:.2f}"],
        [Paragraph('<b>Total:</b>', styles['Normal']), f"${total:.2f}"]
    ]
    total_table = Table(total_data, colWidths=[4.2*inch, 1.1*inch])
    total_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 2), (0, 2), colors.HexColor('#ff5e62')),
        ('TEXTCOLOR', (1, 2), (1, 2), colors.HexColor('#ff5e62')),
    ]))
    elements.append(total_table)
    elements.append(Spacer(1, 24))

    # Thank you / Footer
    thank_style = ParagraphStyle(
        'ThankYou', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, textColor=colors.HexColor('#292929'), spaceAfter=8, spaceBefore=0, fontName='Helvetica-Oblique'
    )
    elements.append(Paragraph("Thank you for shopping with ChipMaster!", thank_style))
    footer_style = ParagraphStyle(
        'Footer', parent=styles['Normal'], fontSize=9, alignment=TA_CENTER, textColor=colors.HexColor('#888'), spaceAfter=0, spaceBefore=8, fontName='Helvetica'
    )
    elements.append(Paragraph("© 2025 ChipMaster. All rights reserved.", footer_style))

    # Generate PDF
    doc.build(elements) 