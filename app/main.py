from fastapi import FastAPI, Depends
from .models import CreateOrderRequest, MetricsResponse, StatusCount
from .order_repository import OrderRepository

app = FastAPI()

# Ideally, route-logic would be kept in a route-directory but to simplify the submission of the assignment,
# the logic will be placed in 1 file
@app.post("/order")
def create_orders(req: CreateOrderRequest, session: Depends(psl_session)):
    # Create order
    # Offload processing to queue
    order_repository = OrderRepository(session)

    order_respository.create_order(req)
    
    return {"content": "Ordering..."}


@app.get("{user_id}/orders")
def orders_status(user_id: int, session: Depends(psl_session)):
    # Get all orders for user
    return {"content": f"Order status for {user_id=}"}


@app.get("/metrics")
def metrics(session: Depends(psl_session)):
    #   - Total number of orders processed.
    #   - Average processing time for orders.
    #   - Count of orders in each status -
    #     - Pending, 
    #     - Processing, 
    #     - Completed

    return MetricsResponse(
        total_orders = 0
        average_processing_time =0
        status_counts = StatusCount(
            pending_count: int
            processing_count: int
            completed_count: int
        )
    )