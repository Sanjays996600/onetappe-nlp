from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from models.base import Order, Product
from auth.dependencies import get_current_user, require_role
from backend.database import get_db
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

router = APIRouter(
    prefix="/seller/invoices",
    tags=["invoices"],
    dependencies=[Depends(require_role("seller"))]
)


def generate_invoice_pdf(order_data: dict, seller_info: dict, customer_info: dict):
    """
    Generate PDF invoice using ReportLab
    
    This function properly handles discount calculations by applying discounts to the subtotal
    before calculating tax.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Add title
    title_style = styles["Title"]
    title = Paragraph(f"Invoice", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.25*inch))
    
    # Add invoice number and date
    invoice_style = ParagraphStyle(
        'InvoiceInfo',
        parent=styles['Normal'],
        fontSize=10,
        leading=12
    )
    invoice_text = f"Invoice #: {order_data.get('id', 'N/A')}<br/>"
    invoice_text += f"Date: {datetime.now().strftime('%Y-%m-%d')}<br/>"
    elements.append(Paragraph(invoice_text, invoice_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add seller info
    seller_style = ParagraphStyle(
        'SellerInfo',
        parent=styles['Normal'],
        fontSize=10,
        leading=12
    )
    seller_text = f"<b>Seller:</b><br/>"
    seller_text += f"{seller_info.get('name', 'Unknown')}<br/>"
    seller_text += f"{seller_info.get('email', '')}<br/>"
    elements.append(Paragraph(seller_text, seller_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add customer info
    customer_style = ParagraphStyle(
        'CustomerInfo',
        parent=styles['Normal'],
        fontSize=10,
        leading=12
    )
    customer_text = f"<b>Customer:</b><br/>"
    customer_text += f"{customer_info.get('name', 'Unknown')}<br/>"
    customer_text += f"{customer_info.get('email', '')}<br/>"
    elements.append(Paragraph(customer_text, customer_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Create table for order items
    data = [["Product", "Quantity", "Unit Price", "Total"]]
    
    # Calculate subtotal
    subtotal = 0
    for item in order_data.get('items', []):
        price = item.get('price', 0)
        quantity = item.get('quantity', 0)
        item_total = price * quantity
        subtotal += item_total
        
        data.append([
            item.get('product', 'N/A'),
            quantity,
            f"${price:.2f}",
            f"${item_total:.2f}"
        ])
    
    # Create the table
    table = Table(data, colWidths=[2.5*inch, 1*inch, 1.25*inch, 1.25*inch])
    
    # Add style to the table
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    
    # Add zebra striping
    for i in range(1, len(data)):
        if i % 2 == 0:
            table_style.add('BACKGROUND', (0, i), (-1, i), colors.white)
    
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 0.25*inch))
    
    # Add summary with proper discount and tax calculation
    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=10,
        alignment=2,  # Right alignment
        leading=14,
        spaceAfter=12
    )
    
    # Get discount information
    discount_percent = order_data.get('discount_percent', 0)
    discount_amount = order_data.get('discount_amount', 0)
    
    # Calculate discount - FIXED: Apply discount to subtotal, not after tax
    if discount_percent > 0:
        discount = subtotal * (discount_percent / 100)
    else:
        discount = discount_amount
    
    # Calculate discounted subtotal
    discounted_subtotal = subtotal - discount
    
    # Calculate tax on the discounted subtotal
    tax_rate = order_data.get('tax_rate', 0)
    tax = discounted_subtotal * (tax_rate / 100)
    
    # Calculate total
    total = discounted_subtotal + tax
    
    # Create summary text
    summary_text = f"<b>Subtotal:</b> ${subtotal:.2f}<br/>"
    if discount > 0:
        if discount_percent > 0:
            summary_text += f"<b>Discount ({discount_percent}%):</b> -${discount:.2f}<br/>"
        else:
            summary_text += f"<b>Discount:</b> -${discount:.2f}<br/>"
    summary_text += f"<b>Tax ({tax_rate}%):</b> ${tax:.2f}<br/>"
    summary_text += f"<b>Total:</b> ${total:.2f}"
    
    elements.append(Paragraph(summary_text, summary_style))
    
    # Add footer with terms
    elements.append(Spacer(1, 0.5*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        alignment=1  # Center alignment
    )
    footer_text = "Thank you for your business!<br/>"
    footer_text += "Terms and conditions apply."
    elements.append(Paragraph(footer_text, footer_style))
    
    # Build the PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


@router.get("/{order_id}")
async def get_invoice(
    order_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate an invoice PDF for a specific order"""
    # Get seller ID from authenticated user
    seller_id = current_user.get("id")
    if not seller_id:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # Query the order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Get product details
    product = db.query(Product).filter(Product.name == order.product).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Prepare order data for the invoice generator
    order_data = {
        "id": order.id,
        "items": [
            {
                "product": order.product,
                "quantity": order.quantity,
                "price": product.price
            }
        ],
        "tax_rate": 10,  # Example tax rate, could be fetched from settings
        "discount_percent": 0,  # Default to no discount
        "discount_amount": 0
    }
    
    # Check if there's a discount query parameter
    discount_percent = 0
    discount_amount = 0
    
    # Example customer info (in a real app, this would come from the database)
    customer_info = {
        "name": order.buyer,
        "email": "customer@example.com"
    }
    
    # Generate PDF
    pdf_data = generate_invoice_pdf(
        order_data=order_data,
        seller_info=current_user,
        customer_info=customer_info
    )
    
    # Create filename
    filename = f"invoice_{order.id}_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    # Return PDF as downloadable file
    return Response(
        content=pdf_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.get("/{order_id}/with-discount")
async def get_invoice_with_discount(
    order_id: int,
    discount_type: str = Query("percent", description="Type of discount: 'percent' or 'amount'"),
    discount_value: float = Query(0, description="Discount value (percentage or fixed amount)"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate an invoice PDF for a specific order with a discount applied"""
    # Get seller ID from authenticated user
    seller_id = current_user.get("id")
    if not seller_id:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # Query the order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Get product details
    product = db.query(Product).filter(Product.name == order.product).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Prepare order data for the invoice generator
    order_data = {
        "id": order.id,
        "items": [
            {
                "product": order.product,
                "quantity": order.quantity,
                "price": product.price
            }
        ],
        "tax_rate": 10,  # Example tax rate, could be fetched from settings
        "discount_percent": 0,
        "discount_amount": 0
    }
    
    # Apply discount based on type
    if discount_type == "percent":
        order_data["discount_percent"] = discount_value
    else:  # amount
        order_data["discount_amount"] = discount_value
    
    # Example customer info (in a real app, this would come from the database)
    customer_info = {
        "name": order.buyer,
        "email": "customer@example.com"
    }
    
    # Generate PDF
    pdf_data = generate_invoice_pdf(
        order_data=order_data,
        seller_info=current_user,
        customer_info=customer_info
    )
    
    # Create filename
    discount_info = f"{discount_value}{'percent' if discount_type == 'percent' else 'amount'}"
    filename = f"invoice_{order.id}_{discount_info}_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    # Return PDF as downloadable file
    return Response(
        content=pdf_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )