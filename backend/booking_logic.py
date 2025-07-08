import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Booking(Base):
    __tablename__ = 'bookings'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    buyer_id = Column(String, nullable=False)
    seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=False)
    slot = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    seller = relationship('Seller')