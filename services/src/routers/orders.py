import re
from datetime import datetime

from aws_lambda_powertools.event_handler.api_gateway import Router
from bson import ObjectId
from bson.errors import InvalidId
from mongoengine.queryset.visitor import Q

from src.catalogue import PRODUCTS, Status, styles_matching
from src.models import Order, OrderItem, User
from src.schema import CreateOrderIn, UpdateStatusIn
from src.utils.responses import error, success

router = Router()

OPEN_STATUSES = [Status.PENDING.value, Status.PROCESSING.value]
SORTS = {"created_at", "order_number", "total", "status"}
MAX_PAGE_SIZE = 200


def _customers_for(orders: list[Order]) -> dict:
    ids = {o.customer_id for o in orders}
    return {u.id: u for u in User.objects(id__in=list(ids))} if ids else {}


@router.post("")
def create_order(body: CreateOrderIn):
    customer = User.find_or_create(body.first_name, body.last_name)
    items = [
        OrderItem(style=i.style.value, colour=i.colour, size=i.size.value,
                  quantity=i.quantity, unit_price=PRODUCTS[i.style]["price"],
                  note=(i.note or "").strip() or None)
        for i in body.items
    ]
    order = Order(
        order_number=Order.next_order_number(),
        customer_id=customer.id,
        items=items,
        total=sum(i.unit_price * i.quantity for i in items),
        notes=body.notes,
    ).save()
    return success(201, order.to_json(customer))


@router.get("")
def list_orders():
    """Query orders. All params optional and ANDed.

    status=pending,processing (default) | all      q=<name or order number>
    customer_id=<id>   order_number=<prefix>        type=Cardigan   fabric=wool
    style=HBS-WL-C31[,HBS-CT-C31]   colour=029278   size=M       from=2026-10-01  to=2026-10-31
    sort=-created_at (created_at|order_number|total|status, leading - = desc; status sorts in workflow order)
    page=1  page_size=50 (max 200)
    """
    p = router.current_event.query_string_parameters or {}

    # --- status
    status = p.get("status", ",".join(OPEN_STATUSES))
    if status == "all":
        query = Q()
    else:
        wanted = [s for s in status.split(",") if s]
        bad = [s for s in wanted if s not in {x.value for x in Status}]
        if bad:
            return error(400, f"Unknown status '{bad[0]}'")
        query = Q(status__in=wanted)

    # --- customer / order number / free text
    if cid := p.get("customer_id"):
        try:
            query &= Q(customer_id=ObjectId(cid))
        except InvalidId:
            return error(400, "Invalid customer_id")
    if prefix := p.get("order_number"):
        query &= Q(order_number__istartswith=prefix)
    if q := p.get("q", "").strip():
        rx = re.compile(re.escape(q), re.IGNORECASE)
        users = User.objects(Q(first_name=rx) | Q(last_name=rx)).only("id")
        ids = [u.id for u in users]
        # whole-name search: "ada love"
        parts = q.split()
        if len(parts) >= 2:
            fr, lr = re.compile(re.escape(parts[0]), re.I), re.compile(re.escape(" ".join(parts[1:])), re.I)
            ids += [u.id for u in User.objects(first_name=fr, last_name=lr).only("id")]
        query &= Q(order_number__icontains=q) | Q(customer_id__in=ids)

    # --- items: style / type / fabric / colour / size. Two or more => must be on the same item.
    item: dict = {}
    if codes := [s for s in p.get("style", "").split(",") if s]:
        known = {s.value for s in PRODUCTS}
        if bad := [s for s in codes if s not in known]:
            return error(400, f"Unknown style '{bad[0]}'")
        item["style"] = codes[0] if len(codes) == 1 else {"$in": codes}
    elif p.get("type") or p.get("fabric"):
        codes = styles_matching(p.get("type"), p.get("fabric"))
        if not codes:
            return error(400, "No garments match that type/fabric")
        item["style"] = {"$in": codes}
    if colour := p.get("colour"):
        item["colour"] = colour
    if size := p.get("size"):
        item["size"] = size
    if len(item) == 1:
        k, v = next(iter(item.items()))
        query &= Q(__raw__={f"items.{k}": v})
    elif item:
        query &= Q(__raw__={"items": {"$elemMatch": item}})

    # --- date range
    for key, op in (("from", "created_at__gte"), ("to", "created_at__lte")):
        if val := p.get(key):
            try:
                query &= Q(**{op: datetime.fromisoformat(val)})
            except ValueError:
                return error(400, f"Invalid {key} date, use YYYY-MM-DD")

    # --- sort + page
    sort = p.get("sort", "-created_at")
    if sort.lstrip("-") not in SORTS:
        return error(400, f"Unknown sort '{sort}'")
    try:
        page = max(1, int(p.get("page", 1)))
        page_size = min(MAX_PAGE_SIZE, max(1, int(p.get("page_size", 50))))
    except ValueError:
        return error(400, "page and page_size must be integers")

    # Status sorts in workflow order (pending → … → cancelled), not alphabetically.
    order_field = sort.replace("status", "status_rank")

    qs = Order.objects(query)
    total = qs.count()
    orders = list(qs.order_by(order_field, "-_id").skip((page - 1) * page_size).limit(page_size))
    customers = _customers_for(orders)
    return success(200, {
        "items": [o.to_json(customers.get(o.customer_id)) for o in orders],
        "page": page,
        "page_size": page_size,
        "total": total,
    })


@router.get("/<order_id>")
def get_order(order_id: str):
    order = _find(order_id)
    if not order:
        return error(404, "Order not found")
    return success(200, order.to_json(User.objects(id=order.customer_id).first()))


@router.patch("/<order_id>/status")
def update_status(order_id: str, body: UpdateStatusIn):
    order = _find(order_id)
    if not order:
        return error(404, "Order not found")
    order.status = body.status.value
    order.save()
    return success(200, order.to_json(User.objects(id=order.customer_id).first()))


def _find(order_id: str) -> Order | None:
    try:
        return Order.objects(id=ObjectId(order_id)).first()
    except InvalidId:
        return None


