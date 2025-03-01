from pydantic import BaseModel
from typing import List

class StatusCount(BaseModel):
    pending_count: int
    processing_count: int
    completed_count: int

class MetricsResponse(BaseModel):
    total_orders: int
    average_processing_time: Decimal
    status_counts: StatusCount