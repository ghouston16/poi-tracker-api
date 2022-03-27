"""create pois table

Revision ID: f0b6eb23553e
Revises: 
Create Date: 2022-02-23 00:28:23.210418

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "f0b6eb23553e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "pois",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade():
    op.drop_table("pois")
    pass
