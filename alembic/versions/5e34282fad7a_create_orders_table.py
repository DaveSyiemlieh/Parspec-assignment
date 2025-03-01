"""create orders table

Revision ID: 5e34282fad7a
Revises: 
Create Date: 2025-03-02 00:10:06.506565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger

# revision identifiers, used by Alembic.
revision: str = '5e34282fad7a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

tablename = "order"
trigger_function = PGFunction(  # Remove this from upcoming migrations
    schema="public",
    signature="set_updated_at()",  # Can be reused for any table with column updated_at
    definition="""
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at := now();
    return NEW;
END;
$$ language 'plpgsql'
""",
)
trigger = PGTrigger(  # This is required whenever you create a new table with updated_at
    schema="public",
    signature=f"{tablename}_set_updated_at_on_update",
    on_entity=tablename,
    definition=f"""
       BEFORE UPDATE ON {tablename}
	FOR EACH ROW
	EXECUTE PROCEDURE set_updated_at();
    """,
)

def upgrade() -> None:
    op.create_table(
        tablename,
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('item_ids', sa.String(50), nullable=False),
        sa.Column('total_amount', sa.Integer, nullable=False),
        sa.Column('status', sa.String(15), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now()),
        sa.Column('processing_time', sa.Integer, nullable=True),
    )

    op.create_entity(trigger_function)
    op.create_entity(trigger)


def downgrade() -> None:
    op.drop_entity(trigger)
    op.drop_table(tablename)
    op.drop_entity(trigger_function)
