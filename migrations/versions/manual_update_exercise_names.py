"""update exercise names

Revision ID: manual_update_exercise_names
Revises: YOUR_LAST_REVISION_ID
Create Date: 2024-03-11 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# revision identifiers, used by Alembic.
revision = 'manual_update_exercise_names'
down_revision = None  # Get this from your last migration file
branch_labels = None
depends_on = None

def upgrade():
    exercises = table('exercise',
        column('exercise_type', sa.String)
    )
    
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
    exercises = table('exercise',
        column('exercise_type', sa.String)
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