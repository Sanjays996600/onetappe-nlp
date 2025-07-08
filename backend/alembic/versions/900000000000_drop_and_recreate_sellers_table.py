"""drop and recreate sellers table to fix enum type issue

Revision ID: 900000000000
Revises: 780887b65afe
Create Date: 2025-06-27 21:00:00.000000

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '900000000000'
down_revision = '780887b65afe'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    if conn.dialect.has_table(conn, 'sellers'):
        op.drop_table('sellers')
    op.create_table(
        'sellers',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('pincode', sa.String(), nullable=False),
        sa.Column('business_hours', sa.String(), nullable=True),
    )
    op.create_index(op.f('ix_sellers_id'), 'sellers', ['id'], unique=False)

def downgrade():
    conn = op.get_bind()
    if conn.dialect.has_table(conn, 'sellers'):
        op.drop_index(op.f('ix_sellers_id'), table_name='sellers')
        op.drop_table('sellers')
    op.create_table(
        'sellers',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('pincode', sa.String(), nullable=False),
        sa.Column('business_hours', sa.String(), nullable=True),
    )
    op.create_index(op.f('ix_sellers_id'), 'sellers', ['id'], unique=False)