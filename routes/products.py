from backend.database import get_db
# Revert to absolute import for get_db from backend.database
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from models.base import Product
from auth.dependencies import get_current_user, require_role

router = APIRouter(
    prefix="/seller/products",
    tags=["products"],
    dependencies=[Depends(require_role("seller"))]
)

@router.get("/", response_model=List[dict])
async def list_products(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user.get("id")
    products = db.query(Product).filter(Product.seller_id == user_id).all()
    return [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(product: dict, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    new_product = Product(
        seller_id=current_user.get("id"),
        name=product.get("name"),
        description=product.get("description"),
        price=product.get("price"),
        stock=product.get("stock")
    )
    db.add(new_product)
    db.commit()
    return {"message": "Product created successfully"}

@router.put("/{id}")
async def update_product(id: int, product: dict, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_product = db.query(Product).filter(Product.id == id, Product.seller_id == current_user).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.items():
        setattr(existing_product, key, value)
    db.commit()

@router.delete("/products/{product_id}")
async def delete_product(product_id: int, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.seller_id == current_user).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": f"Product with ID {product_id} deleted successfully."}
    db.refresh(existing_product)
    return {"id": existing_product.id, "name": existing_product.name, "price": existing_product.price, "stock": existing_product.stock}

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int, current_user: int = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_product = db.query(Product).filter(Product.id == id, Product.seller_id == current_user).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(existing_product)
    db.commit()
    return

@router.post("/update-stock", status_code=status.HTTP_200_OK)
async def update_stock_by_name(product_data: dict, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update product stock by product name"""
    name = product_data.get("name")
    stock = product_data.get("stock")
    
    if not name or stock is None:
        raise HTTPException(status_code=400, detail="Product name and stock are required")
    
    # Validate that stock is not negative
    if stock < 0:
        return {"error": "Quantity cannot be negative."}
    
    # Find product by name for the current seller
    product = db.query(Product).filter(
        Product.name == name,
        Product.seller_id == current_user.get("id")
    ).first()
    
    if not product:
        raise HTTPException(status_code=404, detail=f"Product '{name}' not found")
    
    # Update stock with proper handling for zero/blank quantity
    stock_value = stock if stock is not None else 0
    product.stock = stock_value
    db.commit()
    
    return {"message": f"Stock updated for {name} to {stock_value} units.", "product": {"id": product.id, "name": product.name, "stock": product.stock}}

@router.get("/low-stock", response_model=List[dict])
async def get_low_stock_products(threshold: int = 5, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get products with stock below the specified threshold"""
    products = db.query(Product).filter(
        Product.seller_id == current_user.get("id"),
        Product.stock < threshold
    ).all()
    
    return [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products]

@router.post("/low-stock", response_model=List[dict])
async def post_low_stock_products(data: dict, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get products with stock below the specified threshold (POST method for NLP integration)"""
    threshold = data.get("threshold", 5)
    products = db.query(Product).filter(
        Product.seller_id == current_user.get("id"),
        Product.stock < threshold
    ).all()
    
    return [{"id": p.id, "name": p.name, "price": p.price, "stock": p.stock} for p in products]

@router.post("/check-stock", status_code=status.HTTP_200_OK)
async def check_product_stock(data: dict, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Check if a specific product is available in inventory"""
    product_name = data.get("name")
    
    if not product_name:
        raise HTTPException(status_code=400, detail="Product name is required")
    
    # Find product by name for the current seller
    product = db.query(Product).filter(
        Product.name.ilike(f"%{product_name}%"),
        Product.seller_id == current_user.get("id")
    ).first()
    
    if not product:
        return {"success": True, "found": False, "message": f"Product '{product_name}' not found"}
    
    return {
        "success": True,
        "found": True,
        "name": product.name,
        "stock": product.stock,
        "price": product.price,
        "id": product.id
    }