"""Add mobile_number column to students table

Revision ID: add_mobile_number
Revises: add_timestamps
Create Date: 2026-01-15

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic
revision = 'add_mobile_number'
down_revision = 'add_timestamps'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add mobile_number column to students table after email"""
    op.execute("ALTER TABLE students ADD COLUMN mobile_number VARCHAR(20) NULL COMMENT 'Student''s mobile phone number' AFTER email")


def downgrade() -> None:
    """Remove mobile_number column from students table"""
    op.drop_column('students', 'mobile_number')
