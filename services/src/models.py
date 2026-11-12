"""MongoEngine documents. Two collections: users and orders."""

from datetime import UTC, datetime

from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    FloatField,
    IntField,
    ObjectIdField,
    StringField,
)
from mongoengine.connection import get_db

from src.catalogue import STATUS_RANK, Status


def now() -> datetime:
    return datetime.now(UTC)


CI = {"locale": "en", "strength": 2}


class User(Document):
    # Case-insensitive collation: "ada lovelace" and "Ada Lovelace" are one user.
    meta = {
        "collection": "users",
        "indexes": [{"fields": ["first_name", "last_name"], "unique": True, "collation": CI}],
    }

    first_name = StringField(required=True)
    last_name = StringField(required=True)
    created_at = DateTimeField(default=now)
    # later: email, password_hash, role ...

    @classmethod
    def find_or_create(cls, first_name: str, last_name: str) -> "User":
        first, last = first_name.strip(), last_name.strip()
        user = cls.objects(first_name=first, last_name=last).collation(CI).first()
        if user:
            return user
        return cls(first_name=first, last_name=last).save()

    def to_json(self) -> dict:
        return {"id": str(self.id), "first_name": self.first_name, "last_name": self.last_name}


class OrderItem(EmbeddedDocument):
    style = StringField(required=True)       # Style value, e.g. HBS-WL-C31
    colour = StringField(required=True)      # mill code
    size = StringField(required=True)
    quantity = IntField(required=True, min_value=1)
    unit_price = FloatField(required=True)   # snapshotted from PRODUCTS at order time
    note = StringField()                     # optional, per item


class Order(Document):
    meta = {
        "collection": "orders",
        "indexes": [{"fields": ["order_number"], "unique": True}, "status", "-created_at"],
    }

    order_number = StringField(required=True)
    customer_id = ObjectIdField(required=True)
    status = StringField(required=True, choices=[s.value for s in Status], default=Status.PENDING.value)
    # Position of `status` in the workflow so sorting by status follows it. Set in save(); a bulk
    # QuerySet.update(status=...) must set it too (STATUS_RANK), and scripts/migrate_status.py backfills it.
    status_rank = IntField()
    items = EmbeddedDocumentListField(OrderItem, required=True)
    total = FloatField(required=True)
    notes = StringField()
    created_at = DateTimeField(default=now)
    updated_at = DateTimeField(default=now)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        self.status_rank = STATUS_RANK[self.status]
        return super().save(*args, **kwargs)

    @staticmethod
    def next_order_number() -> str:
        """EUP-YYMM-NNN, sequence resets each month. Atomic via a counters collection."""
        key = now().strftime("%y%m")
        doc = get_db()["counters"].find_one_and_update(
            {"_id": f"orders-{key}"}, {"$inc": {"seq": 1}}, upsert=True, return_document=True
        )
        return f"EUP-{key}-{doc['seq']:03d}"

    def to_json(self, customer: User | None = None) -> dict:
        return {
            "id": str(self.id),
            "order_number": self.order_number,
            "customer": customer.to_json() if customer else {"id": str(self.customer_id)},
            "status": self.status,
            "items": [
                {"style": i.style, "colour": i.colour, "size": i.size,
                 "quantity": i.quantity, "unit_price": i.unit_price,
                 "line_total": i.unit_price * i.quantity, "note": i.note}
                for i in self.items
            ],
            "total": self.total,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
