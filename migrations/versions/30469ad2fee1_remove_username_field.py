"""remove username field

Revision ID: 30469ad2fee1
Revises: b1f218a8a223
Create Date: 2024-11-10 09:xx:xx.xxxxxx

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30469ad2fee1'
down_revision = 'b1f218a8a223'
branch_labels = None
depends_on = None


def upgrade():
    # Username column is already removed, so we do nothing
    pass


def downgrade():
    # Add the username column back if needed
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=20), nullable=False))
