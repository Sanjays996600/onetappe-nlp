from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ProductSerializer(BaseModel):
    """Serializer for product data validation"""
    product_name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")
    stock: int = Field(..., description="Product stock quantity")
    description: Optional[str] = Field(None, max_length=300, description="Product description")
    
    @field_validator('product_name')
    def validate_product_name(cls, v):
        if not v or not v.strip():
            raise ValueError('product_name cannot be empty')
        return v
    
    @field_validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('price must be greater than 0')
        return v
    
    @field_validator('stock')
    def validate_stock(cls, v):
        if v < 0:
            raise ValueError('stock must be greater than or equal to 0')
        return v