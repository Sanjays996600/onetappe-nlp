from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from database import get_db
from models.base import Product
from .serializers import ProductSerializer

router = APIRouter(
    prefix="/products",
    tags=["products"],
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Any])
async def create_product(product: ProductSerializer, db: Session = Depends(get_db)):
    """
    Create a new product
    
    This endpoint allows sellers to add new products to their inventory via:
    - WhatsApp chatbot command
    - Seller dashboard form
    
    Args:
        product: Validated product data
        db: Database session
        
    Returns:
        JSON response with success message and product ID
    """
    try:
        # Create new product instance
        new_product = Product(
            name=product.product_name,
            description=product.description,
            price=product.price,
            stock=product.stock,
            # Note: seller_id would be set from authentication in a real implementation
            # For now, we'll set a default seller_id of 1
            seller_id=1  # Setting a default seller_id to avoid NULL constraint errors
        )
        
        # Add to database and commit
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        
        # Return success response
        return {
            "success": True,
            "message": "Product added successfully",
            "product_id": new_product.id
        }
    except Exception as e:
        # Rollback in case of error
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create product: {str(e)}"
        )