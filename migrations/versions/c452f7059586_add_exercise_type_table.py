"""add exercise type table

Revision ID: c452f7059586
Revises: ce85212bc88e
Create Date: 2024-11-03 10:59:38.224421

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c452f7059586'
down_revision = 'ce85212bc88e'
branch_labels = None
depends_on = None


def upgrade():
    # Add our standard exercises
    op.execute(
        """
        INSERT INTO exercise_type (name) VALUES 
        ('Dumbbell Chest Press'),
        ('Dumbbell Biceps Curl'),
        ('Dumbbell Lat Raise'),
        ('Dumbbell Overhead Press'),
        ('Lat Pulldowns'),
        ('Rows'),
        ('Leg Press'),
        ('Calf Press'),
        ('Leg Curl'),
        ('Face Pulls');
        """
    )
    
    # Modify exercise table
    with op.batch_alter_table('exercise', schema=None) as batch_op:
        batch_op.add_column(sa.Column('exercise_type_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            'fk_exercise_exercise_type',
            'exercise_type',
            ['exercise_type_id'], ['id']
        )
        batch_op.drop_column('exercise_type')


def downgrade():
    with op.batch_alter_table('exercise', schema=None) as batch_op:
        batch_op.add_column(sa.Column('exercise_type', sa.VARCHAR(length=100), nullable=False))
        batch_op.drop_constraint('fk_exercise_exercise_type', type_='foreignkey')
        batch_op.drop_column('exercise_type_id')