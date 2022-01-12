"""init

Revision ID: d554df3dfa50
Revises: 
Create Date: 2022-01-12 02:58:06.183075

"""
from alembic import op
import sqlalchemy as sa
from src.models.content_types import ContentTypes


# revision identifiers, used by Alembic.
revision = 'd554df3dfa50'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'blog',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('publish_date', sa.DateTime, nullable=False)
    )
    op.create_table(
        'content',
        sa.Column('blog_id', sa.Integer, sa.ForeignKey("blog.id"), primary_key=True),
        sa.Column('position', sa.Integer, primary_key=True),
        sa.Column('type', sa.Enum(ContentTypes), nullable=False),
        sa.Column('value', sa.String, nullable=False)
    )


def downgrade():
    op.drop_table('blog')
    op.drop_table('content')
