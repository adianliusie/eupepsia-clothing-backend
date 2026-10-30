from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
from aws_lambda_powertools.event_handler.api_gateway import RequestValidationError
from aws_lambda_powertools.utilities.typing import LambdaContext
from mongoengine import connect
from mongoengine.connection import ConnectionFailure, get_connection

from src.catalogue import catalogue_json
from src.config import settings
from src.routers import orders, users
from src.utils.responses import error, success

logger = Logger()

# No auth yet and no cookies, so a wildcard origin is fine for an internal tool.
app = APIGatewayRestResolver(cors=CORSConfig(allow_origin="*"), enable_validation=True)
app.include_router(orders.router, prefix="/orders")
app.include_router(users.router, prefix="/users")


@app.get("/catalogue")
def get_catalogue():
    return success(200, catalogue_json())


@app.exception_handler(RequestValidationError)
def on_validation_error(exc: RequestValidationError):
    details = "; ".join(
        f"{'.'.join(str(p) for p in e.get('loc', []))}: {e.get('msg')}" for e in exc.errors()
    )
    return error(422, f"Invalid request: {details}")


@app.exception_handler(Exception)
def on_unhandled(exc: Exception):
    logger.exception("Unhandled error")
    return error(500, "Internal error")


def connect_db() -> None:
    try:
        get_connection()
    except ConnectionFailure:
        connect(settings.DB_NAME, host=settings.MONGODB_URI, tz_aware=True)


@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    connect_db()
    return app.resolve(event, context)
