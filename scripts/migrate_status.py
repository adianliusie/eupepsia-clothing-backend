"""One-off: rename status "sent" to "delivered" and fill `status_rank` on every order.

Safe to re-run. Reads MONGODB_URI / DB_NAME from .env (the same database the deployed API uses).
Needs only pymongo + python-dotenv; the status order comes from the catalogue.

    python3 scripts/migrate_status.py           # dry run: counts only, writes nothing
    python3 scripts/migrate_status.py --apply   # write
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "services"))
from src.catalogue import STATUS_RANK  # noqa: E402  (after the path setup)

load_dotenv(root / ".env")
db_name = os.environ.get("DB_NAME", "eupepsia-dev")
orders = MongoClient(os.environ["MONGODB_URI"])[db_name]["orders"]
apply = "--apply" in sys.argv

print(f"db={db_name}  orders={orders.count_documents({})}")
for d in sorted(orders.aggregate([{"$group": {"_id": "$status", "n": {"$sum": 1}}}]), key=lambda d: str(d["_id"])):
    print(f"  {d['_id']}: {d['n']}")

steps = [({"status": "sent"}, {"$set": {"status": "delivered"}}, 'status "sent" -> "delivered"')]
steps += [({"status": s}, {"$set": {"status_rank": r}}, f"status_rank={r} for {s}") for s, r in STATUS_RANK.items()]

for flt, update, what in steps:
    if apply:
        print(f"{what}: {orders.update_many(flt, update).modified_count} updated")
    else:
        print(f"{what}: {orders.count_documents(flt)} would match")

if not apply:
    print("Dry run. Re-run with --apply to write.")
