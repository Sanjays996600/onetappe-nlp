from alembic import op
import sqlalchemy as sa
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.base import Base, engine

Base.metadata.create_all(bind=engine)

# Migration script for sellers table

def upgrade():
    op.create_table(
        'sellers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('category', sa.String, nullable=False),
        sa.Column('pincode', sa.String, nullable=False),
        sa.Column('business_hours', sa.String)
    )

    op.create_table(
        'bookings',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('buyer_id', sa.String, nullable=False),
        sa.Column('seller_id', sa.Integer, sa.ForeignKey('sellers.id'), nullable=False),
        sa.Column('slot', sa.String, nullable=False),
        sa.Column('timestamp', sa.DateTime, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table('bookings')
    op.drop_table('sellers')