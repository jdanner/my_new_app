"""update exercise names

Revision ID: manual_update_exercise_names
Revises: YOUR_LAST_REVISION_ID
Create Date: 2024-03-11 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = 'manual_update_exercise_names'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create user table
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('password_hash', sa.String(length=128), nullable=True),  # Can be null initially
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create workout table
    op.create_table(
        'workout',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False, default=datetime.utcnow),  # Fixed default
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),  # Added CASCADE
        sa.PrimaryKeyConstraint('id')
    )

    # Create exercise table
    op.create_table(
        'exercise',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('workout_id', sa.Integer(), nullable=False),
        sa.Column('exercise_type', sa.String(length=100), nullable=False),
        sa.Column('sets', sa.Integer(), nullable=False),
        sa.Column('reps', sa.Integer(), nullable=False),
        sa.Column('weight', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['workout_id'], ['workout.id'], ondelete='CASCADE'),  # Added CASCADE
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    # Drop tables in correct order (respect foreign keys)
    op.drop_table('exercise')
    op.drop_table('workout')
    op.drop_table('user')