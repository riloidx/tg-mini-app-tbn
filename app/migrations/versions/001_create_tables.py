"""create_tables

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('telegram_id', sa.BigInteger(), nullable=False),
        sa.Column('first_name', sa.Text(), nullable=True),
        sa.Column('last_name', sa.Text(), nullable=True),
        sa.Column('username', sa.Text(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('last_seen_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('last_test_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('telegram_id')
    )

    # Create questions table
    op.create_table('questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('number', sa.Integer(), nullable=False),
        sa.Column('text', sa.Text(), nullable=False),
        sa.Column('category', sa.Text(), nullable=False),
        sa.Column('max_points', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.CheckConstraint("category IN ('happiness','selfreal','freedom')", name='check_category'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('number')
    )

    # Create results table
    op.create_table('results',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('taken_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('total_score', sa.Integer(), nullable=False),
        sa.Column('happiness_score', sa.Integer(), nullable=False),
        sa.Column('selfreal_score', sa.Integer(), nullable=False),
        sa.Column('freedom_score', sa.Integer(), nullable=False),
        sa.Column('happiness_pct', sa.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column('selfreal_pct', sa.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column('freedom_pct', sa.DECIMAL(precision=5, scale=2), nullable=False),
        sa.Column('version', sa.Text(), nullable=False),
        sa.Column('meta', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    # Create question_options table
    op.create_table('question_options',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=True),
        sa.Column('label', sa.Text(), nullable=False),
        sa.Column('points', sa.Integer(), nullable=False),
        sa.Column('sort_index', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('question_options')
    op.drop_table('results')
    op.drop_table('questions')
    op.drop_table('users')