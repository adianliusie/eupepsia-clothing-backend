from aws_lambda_powertools.event_handler import Response, content_types


def success(status: int, data=None, message: str = "ok") -> Response:
    return Response(status_code=status, content_type=content_types.APPLICATION_JSON,
                    body={"success": True, "message": message, "data": data})


def error(status: int, message: str) -> Response:
    return Response(status_code=status, content_type=content_types.APPLICATION_JSON,
                    body={"success": False, "message": message, "data": None})
