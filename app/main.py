from fastapi import FastAPI, Depends
# from order_repository import OrderRepository
from pydantic import BaseModel
from typing import List

#---------------------------- Models ----------------------------#
class CreateOrderRequest(BaseModel):
    user_id: int
    order_id: int
    item_ids: List
    total_amount: int

class StatusCount(BaseModel):
    pending_count: int
    processing_count: int
    completed_count: int

class MetricsResponse(BaseModel):
    total_orders: int
    average_processing_time: float
    status_counts: StatusCount
#------------------------------------------------------------------#


#---------------------------- APIs --------------------------------#
app = FastAPI()

db_session = None
@app.post("/order")
def create_orders(req: CreateOrderRequest):
    # Create order
    # Offload processing to queue``
    # order_repository = OrderRepository(db_session)
    # order_respository.create_order(req)
    
    return {"content": "Ordering 2..."}


@app.get("{user_id}/orders")
def orders_status(user_id: int):
    # Get all orders for user
    return {"content": f"Order status for {user_id=}"}


@app.get("/metrics")
def metrics():
    #   - Total number of orders processed.
    #   - Average processing time for orders.
    #   - Count of orders in each status -
    #     - Pending, 
    #     - Processing, 
    #     - Completed

    return MetricsResponse(
        total_orders = 0,
        average_processing_time = 0,
        status_counts = StatusCount(
            pending_count = 0,
            processing_count = 0,
            completed_count = 0
        )
    )
#------------------------------------------------------------------#

