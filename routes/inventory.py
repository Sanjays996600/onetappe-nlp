from fastapi import APIRouter, Depends, HTTPException, status, Query, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from models.base import Product
from auth.dependencies import get_current_user, require_role
from backend.database import get_db
import io
from datetime import datetime
import pytz
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Define IST timezone for reuse
IST_TZ = pytz.timezone('Asia/Kolkata')

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    dependencies=[Depends(require_role("seller"))]
)

class InventoryUpdateRequest(BaseModel):
    product_id: int
    stock: int

@router.get("/", response_model=List[dict])
async def get_inventory(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.seller_id == current_user.get("sub")).all()
    return [{"id": p.id, "name": p.name, "stock": p.stock} for p in products]

@router.post("/update")
async def update_stock(update_request: InventoryUpdateRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == update_request.product_id, Product.seller_id == current_user.get("sub")).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Validate that stock is not negative
    if update_request.stock < 0:
        return {"error": "Quantity cannot be negative."}
    
    # Handle zero/blank quantity with a default value of 0
    stock_value = update_request.stock if update_request.stock is not None else 0
    
    product.stock = stock_value
    db.commit()
    return {"reply": f"📦 Stock for Product ID {update_request.product_id} updated to {stock_value} units."}


def generate_inventory_pdf_report(products: List[dict], seller_info: dict):
    """Generate PDF inventory report using ReportLab"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Add title
    title_style = styles["Title"]
    title = Paragraph(f"Inventory Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.25*inch))
    
    # Add seller info
    seller_style = ParagraphStyle(
        'SellerInfo',
        parent=styles['Normal'],
        fontSize=10,
        leading=12
    )
    seller_text = f"Seller: {seller_info.get('email', 'Unknown')}<br/>"
    
    # Get current time in IST for the report
    ist_now = datetime.now(pytz.UTC).astimezone(IST_TZ)
    seller_text += f"Generated on: {ist_now.strftime('%Y-%m-%d %H:%M:%S')} [IST]"
    
    elements.append(Paragraph(seller_text, seller_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Summary statistics
    total_products = len(products)
    total_stock = sum(product.get('stock', 0) for product in products)
    low_stock_count = sum(1 for product in products if product.get('stock', 0) < 10)  # Assuming 10 is low stock threshold
    out_of_stock = sum(1 for product in products if product.get('stock', 0) == 0)
    
    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        spaceAfter=12
    )
    summary_text = f"<b>Total Products:</b> {total_products}<br/>"
    summary_text += f"<b>Total Stock Units:</b> {total_stock}<br/>"
    summary_text += f"<b>Low Stock Items:</b> {low_stock_count}<br/>"
    summary_text += f"<b>Out of Stock Items:</b> {out_of_stock}"
    elements.append(Paragraph(summary_text, summary_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Create table for inventory
    if products:
        data = [["Product ID", "Product Name", "Stock", "Status"]]
        for product in products:
            stock = product.get('stock', 0)
            
            # Determine status based on stock level
            if stock == 0:
                status = "Out of Stock"
            elif stock < 10:  # Assuming 10 is low stock threshold
                status = "Low Stock"
            else:
                status = "In Stock"
            
            data.append([
                product.get('id', 'N/A'),
                product.get('name', 'N/A'),
                stock,
                status
            ])
        
        # Create the table
        table = Table(data, colWidths=[0.8*inch, 3*inch, 0.8*inch, 1.2*inch])
        
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
            
            # Add color coding for status
            status_col = 3
            status = data[i][status_col]
            if status == "Out of Stock":
                table_style.add('TEXTCOLOR', (status_col, i), (status_col, i), colors.red)
            elif status == "Low Stock":
                table_style.add('TEXTCOLOR', (status_col, i), (status_col, i), colors.orange)
        
        table.setStyle(table_style)
        elements.append(table)
    else:
        elements.append(Paragraph("No products found in inventory.", styles["Normal"]))
    
    # Build the PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


@router.get("/report")
async def get_inventory_report(
    type: str = Query("pdf", description="Report type (pdf only for now)"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate an inventory report for the seller"""
    if type != "pdf":
        raise HTTPException(status_code=400, detail="Only PDF reports are supported at this time")
    
    # Get seller ID from authenticated user
    seller_id = current_user.get("id")
    if not seller_id:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # Query products for this seller
    products = db.query(Product).filter(Product.seller_id == current_user.get("sub")).all()
    
    # Convert products to dict for the PDF generator
    products_data = []
    for product in products:
        products_data.append({
            "id": product.id,
            "name": product.name,
            "stock": product.stock
        })
    
    # Generate PDF
    pdf_data = generate_inventory_pdf_report(
        products=products_data,
        seller_info=current_user
    )
    
    # Get current time in IST for filename
    ist_now = datetime.now(pytz.UTC).astimezone(IST_TZ)
    
    # Create filename with current date
    filename = f"inventory_report_{ist_now.strftime('%Y%m%d')}_IST.pdf"
    
    # Return PDF as downloadable file
    return Response(
        content=pdf_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )