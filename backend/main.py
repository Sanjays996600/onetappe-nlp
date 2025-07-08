import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.base import SessionLocal
from auth.jwt import create_access_token
from auth.utils import verify_password
from jose import JWTError, jwt
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi.responses import FileResponse
from models.base import SessionLocal
from auth.jwt import create_access_token
from sqlalchemy.orm import Session
from fastapi import APIRouter
from routes import auth, products, reports, invoices
from products.urls import router as products_api_router
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from database import get_db

app = FastAPI()
db = SessionLocal()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_user_by_email(db: Session, email: str):
    return db.execute("SELECT * FROM users WHERE email = :email", {"email": email}).fetchone()

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# Function to get the current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = {"email": email}
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, email=token_data["email"])
    if user is None:
        raise credentials_exception
    return user

# Dependency to require a specific role
async def require_role(required_role: str, user: dict = Depends(get_current_user)):
    if user.role != required_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

# Example usage in a route
@app.get("/admin-only")
async def read_admin_data(user: dict = Depends(lambda: require_role("admin"))):
    return {"message": "This is admin data."}

# Booking model
class Booking(BaseModel):
    buyer_id: str
    seller_id: int
    slot: str

# Create a booking
@app.post("/bookings/")
async def create_booking(booking: Booking):
    with db.begin() as conn:
        conn.execute('INSERT INTO bookings (buyer_id, seller_id, slot) VALUES (:buyer_id, :seller_id, :slot)', booking.dict())
    return {"message": "Booking created successfully"}

# Read all bookings
@app.get("/bookings/")
async def read_bookings():
    with db.begin() as conn:
        result = conn.execute('SELECT * FROM bookings')
        bookings = result.fetchall()
    return {"bookings": bookings}

# Update a booking
@app.put("/bookings/{booking_id}")
async def update_booking(booking_id: int, booking: Booking):
    with db.begin() as conn:
        conn.execute('UPDATE bookings SET buyer_id = :buyer_id, seller_id = :seller_id, slot = :slot WHERE id = :id', {**booking.dict(), "id": booking_id})
    return {"message": "Booking updated successfully"}

# Delete a booking
@app.delete("/bookings/{booking_id}")
async def delete_booking(booking_id: int):
    with db.begin() as conn:
        conn.execute('DELETE FROM bookings WHERE id = :id', {"id": booking_id})
    return {"message": "Booking deleted successfully"}

@app.get("/")
def root():
    return {"message": "One Tappe backend is running 🎉"}

@app.post("/api/login")
async def login(token: str):
    # Example token validation logic
    if token == "valid-token":
        return {"success": True}
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/api/reports")
async def get_reports():
    # Path to the report file
    report_path = "./reports/sample_report.pdf"
    if os.path.exists(report_path):
        return FileResponse(path=report_path, filename="report.pdf", media_type='application/pdf')
    else:
        raise HTTPException(status_code=404, detail="Report not found")

admin_router = APIRouter(prefix="/admin", dependencies=[Depends(lambda: require_role("admin"))])
seller_router = APIRouter(prefix="/seller", dependencies=[Depends(lambda: require_role("seller"))])

@admin_router.get("/dashboard")
async def admin_dashboard():
    return {"message": "Welcome to the admin dashboard."}

@seller_router.get("/dashboard")
async def seller_dashboard():
    return {"message": "Welcome to the seller dashboard."}

@seller_router.get("/orders")
async def get_seller_orders():
    return {"orders": "Mock orders data for seller"}

@seller_router.get("/inventory")
async def get_seller_inventory():
    return {"inventory": "Mock inventory data for seller"}

from whatsapp_webhook import router as whatsapp_router

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(reports.router)
app.include_router(invoices.router)
app.include_router(admin_router)
app.include_router(seller_router)
app.include_router(whatsapp_router)
app.include_router(products_api_router)

if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)

# Update Uvicorn command in Dockerfile to remove reload flag
