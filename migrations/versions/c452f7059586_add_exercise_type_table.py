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
    # First create the table
    op.create_table('exercise_type',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Then insert the data
    op.execute("INSERT INTO exercise_type (name) VALUES ('Dumbbell Chest Press')")
    op.execute("INSERT INTO exercise_type (name) VALUES ('Dumbbell Biceps Curl')")
    op.execute("INSERT INTO exercise_type (name) VALUES ('Dumbbell Lat Raise')")
    op.execute("INSERT INTO exercise_type (name) VALUES ('Dumbbell Overhead Press')")
    op.execute("INSERT INTO exercise_type (name) VALUES ('Lat Pulldowns')")
    op.execute("INSERT INTO exercise_type (name) VALUES ('Rows')")
    op.execute("INSERT INTO exercise_type (name) VALUES ('Leg Press')")
    op.execute("INSERT INTO exercise_type (name) VALUES ('Calf Press')")
    op.execute("INSERT INTO exercise_type (name) VALUES ('Leg Curl')")
    op.execute("INSERT INTO exercise_type (name) VALUES ('Face Pulls')")
    
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

    op.drop_table('exercise_type')