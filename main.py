from fastapi import FastAPI, Depends
from pydantic import BaseModel

#---------------------------- Models ----------------------------#
class CreateOrderRequest(BaseModel):
    user_id: int
    order_id: int
    item_ids: str
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



#----------------------- DB Model & Session -----------------------#
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
from sqlalchemy.sql import func
from datetime import datetime

db = sa.create_engine("postgresql+psycopg2://order:pg@db:5432/order")
Session = sessionmaker(bind=db)
Base = declarative_base()

class Order(Base):
    __tablename__ = "order"
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int]
    item_ids: Mapped[str]
    total_amount: Mapped[int]
    status: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    processing_time: Mapped[int]
#------------------------------------------------------------------#



#---------------------------- APIs --------------------------------#
app = FastAPI()

db_session = None
@app.post("/order")
def create_orders(req: CreateOrderRequest):
    order = Order(
        id = req.order_id,
        user_id = req.user_id,
        item_ids = req.item_ids,
        total_amount = req.total_amount,
        status = "PENDING",
    )
    with Session() as session:
        session.add(order)
        session.commit()
    
    return {"content": "Order created successfully"}


@app.get("/user/{user_id}/orders")
def orders_status(user_id: int):
    stmt = sa.select(Order).where(Order.user_id == user_id)
    order_list = []
    for order in Session().scalars(stmt):
        print(order)
        order_list.append({
            "id": order.id,
            "status": order.status
        })
    return {"content": order_list}


@app.get("/metrics")
def metrics():
    with Session() as session:
        order_info = session.query(func.count().label("total_orders"), func.avg(Order.processing_time).label("average_processing_time")).first()
        order_by_status = session.query(func.count().label("count"), Order.status).group_by(Order.status).all()
        
        pending_count = 0
        processing_count = 0
        completed_count = 0
        for sc in order_by_status:
            if sc.status == 'PENDING':
                pending_count = sc.count if sc.count != None else 0
            elif sc.status == 'PROCESSING':
                processing_count = sc.count if sc.count != None else 0
            else:
                completed_count = sc.count if sc.count != None else 0

    return MetricsResponse(
        total_orders = order_info.total_orders,
        average_processing_time = order_info.average_processing_time if order_info.average_processing_time != None else 0,
        status_counts = StatusCount(
            pending_count = pending_count,
            processing_count = processing_count,
            completed_count = completed_count
        )
    )
#------------------------------------------------------------------#

