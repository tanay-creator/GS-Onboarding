from collections.abc import Callable
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        start = time.perf_counter()
        ts = datetime.now(timezone.utc).isoformat()
        method = request.method
        path = request.url.path
        query = request.url.query
        client = request.client.host if request.client else "_"
        ua = request.headers.get("user-agent", "_")

        #Incoming log
        logger.info(
            "REQ ts =%s method =%s paht =%s%s client=%s ua=%s,
            ts, method, path, f"?{query}" if query else "", client, ua 
        )

        try:
            response: Response = await call_next(request)
        except Exception:
            #Log exceptions with duration, then re-raise
            dur_ms = (time.perf_counter() - start) * 1000
            logger.exception(
                "ERR method =%s path=%s duration_ms=%.2f", method, path, dur_ms
            )
            raise

            #Outgoing log
        dur_ms = (time.perf_counter()-start) * 1000
        logger.info(
            "RES method =%s path=%s status=%s duration_ms=%.2f",
            method, path, response.status_code, dur_ms
        )
        return response
        return response
