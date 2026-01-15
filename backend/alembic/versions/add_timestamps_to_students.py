"""add timestamps to students

Revision ID: add_timestamps
Revises: 
Create Date: 2026-01-15

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision = 'add_timestamps'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add created_at and updated_at columns to students table
    op.add_column('students', sa.Column('created_at', sa.DateTime(), server_default=func.now(), nullable=True))
    op.add_column('students', sa.Column('updated_at', sa.DateTime(), server_default=func.now(), onupdate=func.now(), nullable=True))


def downgrade():
    # Remove created_at and updated_at columns
    op.drop_column('students', 'updated_at')
    op.drop_column('students', 'created_at')
