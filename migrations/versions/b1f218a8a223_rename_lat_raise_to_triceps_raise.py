"""rename lat raise to triceps raise

Revision ID: b1f218a8a223
Revises: c452f7059586
Create Date: 2024-11-03 11:18:49.916423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1f218a8a223'
down_revision = 'c452f7059586'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
        UPDATE exercise_type 
        SET name = 'Dumbbell Triceps Raise' 
        WHERE name = 'Dumbbell Lat Raise';
    """)


def downgrade():
    op.execute("""
        UPDATE exercise_type 
        SET name = 'Dumbbell Lat Raise' 
        WHERE name = 'Dumbbell Triceps Raise';
    """)