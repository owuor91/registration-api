"""baseline

Revision ID: 3496f3637a61
Revises: 
Create Date: 2020-06-21 00:23:48.884280

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '3496f3637a61'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'students',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(), nullable=False),
        sa.Column('last_name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('phone_number', sa.String(), nullable=False),
        sa.Column('sex', sa.String(), nullable=False)
    )


def downgrade():
    op.drop_table('students')
