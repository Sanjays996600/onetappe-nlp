from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import pytz
from models.base import Order, Product
from auth.dependencies import get_current_user, require_role
from backend.database import get_db
import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Define IST timezone for reuse
IST_TZ = pytz.timezone('Asia/Kolkata')

router = APIRouter(
    prefix="/seller/orders",
    tags=["reports"],
    dependencies=[Depends(require_role("seller"))]
)


def get_date_range(range_type: str):
    """Helper function to calculate date range based on type
    
    Returns date range in UTC for database queries, but calculates based on IST timezone
    
    Args:
        range_type: Either a predefined range ('today', 'yesterday', 'this-week', 'this-month') or
                   a custom date range in format 'YYYY-MM-DD,YYYY-MM-DD'
    """
    # Check if this is a custom date range (format: 'YYYY-MM-DD,YYYY-MM-DD')
    if ',' in range_type:
        try:
            # Split the range into start and end dates
            start_date_str, end_date_str = range_type.split(',')
            
            # Parse the dates (assuming they're in UTC)
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').replace(tzinfo=pytz.UTC)
            # Set end date to end of day (23:59:59.999999)
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(
                hour=23, minute=59, second=59, microsecond=999999, tzinfo=pytz.UTC
            )
            
            return start_date, end_date
        except (ValueError, TypeError) as e:
            # If there's an error parsing the custom range, fall back to today
            print(f"Error parsing custom date range: {e}")
    
    # Get current time in IST
    ist_now = datetime.now(pytz.UTC).astimezone(IST_TZ)
    today = ist_now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    if range_type == "today":
        start_date = today
        end_date = today + timedelta(days=1) - timedelta(microseconds=1)
    elif range_type == "yesterday":
        # Start from yesterday
        yesterday = today - timedelta(days=1)
        start_date = yesterday
        end_date = yesterday + timedelta(days=1) - timedelta(microseconds=1)
    elif range_type == "this-week":
        # Start from Monday of current week
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=7) - timedelta(microseconds=1)
    elif range_type == "this-month":
        # Start from first day of current month
        start_date = today.replace(day=1)
        # Go to first day of next month and subtract 1 microsecond
        if today.month == 12:
            end_date = today.replace(year=today.year+1, month=1, day=1) - timedelta(microseconds=1)
        else:
            end_date = today.replace(month=today.month+1, day=1) - timedelta(microseconds=1)
    else:  # Default to today
        start_date = today
        end_date = today + timedelta(days=1) - timedelta(microseconds=1)
    
    # Convert back to UTC for database queries
    start_date_utc = start_date.astimezone(pytz.UTC)
    end_date_utc = end_date.astimezone(pytz.UTC)
    
    return start_date_utc, end_date_utc


def generate_pdf_report(orders: List[dict], seller_info: dict, date_range: str):
    """Generate PDF report using ReportLab"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Add title
    title_style = styles["Title"]
    title = Paragraph(f"Sales Report", title_style)
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
    seller_text += f"Date Range: {date_range} [IST]<br/>"
    
    # Get current time in IST for the report
    ist_now = datetime.now(pytz.UTC).astimezone(IST_TZ)
    seller_text += f"Generated on: {ist_now.strftime('%Y-%m-%d %H:%M:%S')} [IST]"
    
    elements.append(Paragraph(seller_text, seller_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Summary statistics
    total_sales = sum(order.get('price', 0) * order.get('quantity', 0) for order in orders)
    total_orders = len(orders)
    
    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
        spaceAfter=12
    )
    summary_text = f"<b>Total Sales:</b> ${total_sales:.2f}<br/>"
    summary_text += f"<b>Total Orders:</b> {total_orders}"
    elements.append(Paragraph(summary_text, summary_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Create table for orders
    if orders:
        data = [["Order ID", "Product", "Quantity", "Price", "Total", "Date"]]
        for order in orders:
            price = order.get('price', 0)
            quantity = order.get('quantity', 0)
            total = price * quantity
            
            # Convert order date from UTC to IST for display
            order_date = order.get('date', datetime.now(pytz.UTC))
            if order_date.tzinfo is None:
                # If date has no timezone info, assume it's UTC
                order_date = order_date.replace(tzinfo=pytz.UTC)
            
            # Convert to IST
            order_date_ist = order_date.astimezone(IST_TZ)
            date_str = order_date_ist.strftime('%Y-%m-%d')
            
            data.append([
                order.get('id', 'N/A'),
                order.get('product', 'N/A'),
                quantity,
                f"${price:.2f}",
                f"${total:.2f}",
                date_str
            ])
        
        # Create the table
        table = Table(data, colWidths=[0.8*inch, 2*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1*inch])
        
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
    else:
        elements.append(Paragraph("No orders found for the selected period.", styles["Normal"]))
    
    # Build the PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()


@router.get("/report")
async def get_order_report(
    type: str = Query("pdf", description="Report type (pdf only for now)"),
    range: str = Query("today", description="Date range (today, yesterday, this-week, this-month) or custom range in format 'YYYY-MM-DD,YYYY-MM-DD'"),
    start_date: Optional[str] = Query(None, description="Start date in YYYY-MM-DD format (for custom range)"),
    end_date: Optional[str] = Query(None, description="End date in YYYY-MM-DD format (for custom range)"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate a sales report for the seller"""
    if type != "pdf":
        raise HTTPException(status_code=400, detail="Only PDF reports are supported at this time")
    
    # Get seller ID from authenticated user
    seller_id = current_user.get("id")
    if not seller_id:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    # Handle custom date range from explicit parameters
    if start_date and end_date:
        try:
            # Create a custom range string in the format expected by get_date_range
            custom_range = f"{start_date},{end_date}"
            start_date_obj, end_date_obj = get_date_range(custom_range)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    else:
        # Use the range parameter
        start_date_obj, end_date_obj = get_date_range(range)
    
    # Query orders for this seller within date range
    # Note: This assumes Order model has seller_id field. Adjust as needed.
    orders_query = db.query(Order).filter(
        Order.date >= start_date_obj,
        Order.date <= end_date_obj
    ).all()
    
    # Convert orders to dict for the PDF generator
    orders_data = []
    for order in orders_query:
        # Get product details
        product_name = order.product
        
        # You might need to join with products table to get price
        # This is a simplified example
        orders_data.append({
            "id": order.id,
            "product": product_name,
            "quantity": order.quantity,
            "price": 0.00,  # Replace with actual price from your data model
            "date": order.date
        })
    
    # Generate PDF - Convert UTC dates back to IST for display
    
    # Convert UTC dates to IST for display
    start_date_ist = start_date_obj.astimezone(IST_TZ)
    end_date_ist = end_date_obj.astimezone(IST_TZ)
    
    pdf_data = generate_pdf_report(
        orders=orders_data,
        seller_info=current_user,
        date_range=f"{start_date_ist.strftime('%Y-%m-%d')} to {end_date_ist.strftime('%Y-%m-%d')}"
    )
    
    # Create filename with date range using IST dates
    filename = f"sales_report_{start_date_ist.strftime('%Y%m%d')}_to_{end_date_ist.strftime('%Y%m%d')}_IST.pdf"
    
    # Return PDF as downloadable file
    return Response(
        content=pdf_data,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )