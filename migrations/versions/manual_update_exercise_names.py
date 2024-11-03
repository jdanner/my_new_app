"""update exercise names

Revision ID: manual_update_exercise_names
Revises: YOUR_LAST_REVISION_ID
Create Date: 2024-03-11 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'manual_update_exercise_names'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # First create the exercise table if it doesn't exist
    op.create_table(
        'exercise',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('exercise_type', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Then define the table for updates
    exercises = sa.table('exercise',
        sa.column('exercise_type', sa.String)
    )
    
    # Now do the updates
    op.execute(
        exercises.update().where(
            exercises.c.exercise_type == 'Bench Press'
        ).values(
            exercise_type = 'Dumbbell Chest Press'
        )
    )
    
    op.execute(
        exercises.update().where(
            exercises.c.exercise_type == 'Barbell Row'
        ).values(
            exercise_type = 'Rows'
        )
    )

def downgrade():
    exercises = sa.table('exercise',
        sa.column('exercise_type', sa.String)
    )
    
    op.execute(
        exercises.update().where(
            exercises.c.exercise_type == 'Dumbbell Chest Press'
        ).values(
            exercise_type = 'Bench Press'
        )
    )
    
    op.execute(
        exercises.update().where(
            exercises.c.exercise_type == 'Rows'
        ).values(
            exercise_type = 'Barbell Row'
        )
    )

    # Drop the table in downgrade if needed
    op.drop_table('exercise')