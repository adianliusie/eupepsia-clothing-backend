from aws_lambda_powertools.event_handler.api_gateway import Router

from src.models import User
from src.utils.responses import success

router = Router()


@router.get("")
def list_users():
    return success(200, [u.to_json() for u in User.objects.order_by("last_name", "first_name")])
