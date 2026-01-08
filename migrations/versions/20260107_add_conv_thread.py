"""
Add conversation_id (thread) to AIConversation for chat threads
Revision ID: 20260107_add_conv_thread
Revises: 
Create Date: 2026-01-07
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260107_add_conv_thread'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('ai_conversations', sa.Column('conversation_id', sa.Integer(), nullable=True))
    op.create_index('ix_ai_conversations_conversation_id', 'ai_conversations', ['conversation_id'])

def downgrade():
    op.drop_index('ix_ai_conversations_conversation_id', table_name='ai_conversations')
    op.drop_column('ai_conversations', 'conversation_id')
