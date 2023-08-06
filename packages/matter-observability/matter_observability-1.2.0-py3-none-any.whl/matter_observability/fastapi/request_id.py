import logging
from contextvars import ContextVar

from starlette.requests import Request

_request_id_ctx_var: ContextVar[str] = ContextVar("request_id", default="")


def get_request_id() -> str:
    return _request_id_ctx_var.get()


class RequestIdLogFilter(logging.Filter):
    def filter(self, record):
        request_id = get_request_id()
        record.request_id = request_id
        return True


async def process_request_id(request: Request, call_next):
    # this header is being injected by ISTIO
    request_id = request.headers.get("x-request-id")
    _request_id_ctx_var.set(request_id)
    return await call_next(request)
