# Parspec-assignment

## Pre-requisites:
- Docker
- Pull postgres docker image `docker pull postgres:15`

## Steps to run the app:
- Move to the working directory (i.e. directory containing all the submitted files)
- Run `docker compose build`
- Run `docker-compose up -d`

## API Requests & Responses


1. Create API
### Request Curl
```
curl --location 'http://localhost:8000/order' \
--header 'Content-Type: application/json' \
--data '{
    "user_id": 1,
    "order_id": 1,
    "item_ids": "1,2,3",
    "total_amount": 500
}'
```
### Response
```
{
    "content": "Order created successfully"
}
```


2. Get orders (by user) API
### Request Curl
```
curl --location 'http://localhost:8000/user/1/orders'
```
### Response
```
{
    "content": [
        {
            "id": 1,
            "status": "PENDING"
        }
    ]
}
```
3. Metric API
### Request Curl
```
curl --location 'http://localhost:8000/metrics'
```

### Response
```
{
    "total_orders": 14,
    "average_processing_time": 0.4,
    "status_counts": {
        "pending_count": 2,
        "processing_count": 0,
        "completed_count": 12
    }
}
```

## Design Decisions
1. Put all of the code in 1 file for ease and clarity during submission. Ideally, a cleaner file structure would have been implemented if durectory-info was preservered during file submission
2. Used FastAPI to quickly setup a RESTful API backend server
3. Used PostgresDB as the DB as I have experience with using it
4. Ideally, the metrics API would query some metrics-service such as Prometheus for this kind of info, but for simplicity, a DB query was used instead (Hence the extra columns in the DB)

## Assumptions made
1. Processing time for a message takes 0.2s - 0.5s every time.
2. Processing is synchronous
3. Processing is not I/O bound
4. Get orders API would be specific to a user (based on Amazon's `order` section)
5. Item_ids and User_ids have already been validated and would also be correct