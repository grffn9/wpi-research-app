"""add last_notif_time

Revision ID: a1b2c3d4e5f6
Revises: ef3d4953cf26
Create Date: 2025-12-11 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = 'ef3d4953cf26'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('faculty', sa.Column('last_notif_time', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('faculty', 'last_notif_time')
