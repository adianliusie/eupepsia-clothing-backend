# CLAUDE.md

Internal order-tracking API for Eupepsia (Happy Black Sheep). Python 3.12, AWS Lambda via SAM, MongoDB Atlas.

- `conda activate eupepsia` before running Python.
- Entry: `services/src/app.py` (Powertools `APIGatewayRestResolver`). Routers in `routers/`, MongoEngine docs in `models.py`, request bodies in `schema.py`.
- `catalogue.py` is the source of truth for styles, prices, sizes, colours. It mirrors the "Eupepsia Timeless Collection" spreadsheet. Orders snapshot `unit_price` at creation, so changing prices never rewrites history.
- Collections: `users` (first/last name only, unique with a case-insensitive collation; accounts later), `orders` (items embedded, `unit_price` snapshotted), `counters` (per-month order-number sequence).
- `GET /orders` is the admin query: filters, sort, offset paging, all done in Mongo (see README). Item filters use `$elemMatch` when two or more are set.
- No auth yet. CORS is wildcard.
- Only env vars: `MONGODB_URI`, `DB_NAME`. Deploy with the `happyblacksheep` AWS profile (us-east-1). Dev API: https://4uqxfo1oof.execute-api.us-east-1.amazonaws.com/Prod Never use credentials or services from other repos.
