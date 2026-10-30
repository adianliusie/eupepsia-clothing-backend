# Eupepsia orders backend

Internal order-tracking API. Python 3.12 on AWS Lambda via SAM, MongoDB Atlas via MongoEngine.

## Setup

```bash
conda activate eupepsia                       # python 3.12 env with deps installed
cp .env.example .env                          # then fill in MONGODB_URI
```

## Run locally

Needs Docker running.

```bash
make layer        # once, and again whenever requirements.txt changes
make up           # http://localhost:8001
```

## Deploy

```bash
make layer
sam deploy --config-env dev --profile happyblacksheep \
  --parameter-overrides "MongoDbUri=<atlas uri> DbName=eupepsia-dev"
```

Dev API: https://4uqxfo1oof.execute-api.us-east-1.amazonaws.com/Prod (stack `eupepsia-orders-dev`, us-east-1).

## Endpoints

| Method | Path | Body |
|---|---|---|
| GET | `/catalogue` | – (products, colours, sizes, statuses for the form) |
| POST | `/orders` | `{first_name, last_name, items: [{style, colour, size, quantity}], notes?}` |
| GET | `/orders` | query, all optional: `status` (csv, default `pending,processing`, or `all`), `q` (name or order no.), `customer_id`, `order_number` (prefix), `type`, `fabric`, `style`, `colour`, `size`, `from`/`to` (YYYY-MM-DD), `sort` (`-created_at`, `order_number`, `total`, `status`), `page`, `page_size` (≤200). Returns `{items, page, page_size, total}`. Two or more item filters must match the same item. |
| GET | `/orders/{id}` | – |
| PATCH | `/orders/{id}/status` | `{status}` |
| GET | `/users` | – |

Responses are `{success, message, data}`.
