from pydantic import BaseModel
from typing import List

class CreateOrderRequest(BaseModel):
    user_id: int
    order_id: int
    item_ids: List
    total_amount: int