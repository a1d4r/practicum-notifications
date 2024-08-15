import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

import config

settings = config.get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.method in ["POST", "PUT", "PATCH"] and "auth" not in request.url.path:
            body = await request.body()
            try:
                json_body = json.loads(body.decode("utf-8"))
                settings.logger.info(
                    f"method: {request.method}; url: {request.url}; body: {json_body};"
                )
            except json.JSONDecodeError:
                settings.logger.info(
                    f"method: {request.method}; url: {request.url}; body: Received non-JSON body;"
                )
        else:
            settings.logger.info(f"method: {request.method}; url: {request.url};")

        try:
            response = await call_next(request)
        except Exception as e:
            settings.logger.error(f"Error processing request: {str(e)}")
            return Response("Internal server error", status_code=500)

        settings.logger.info(f"Response: {response.status_code}")
        return response


app.add_middleware(LoggingMiddleware)

origins = settings.frontend_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def func_start() -> None:
    pass


@app.on_event("shutdown")
async def func_down() -> None:
    pass
