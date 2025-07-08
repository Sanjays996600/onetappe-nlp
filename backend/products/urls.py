from fastapi import APIRouter
from .views import router as products_router

router = APIRouter()

# Include the products router
router.include_router(products_router)