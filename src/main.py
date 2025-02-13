from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import NoResultFound
from starlette.requests import Request

from core.lifespan import lifespan
from core.logging import getLogger, setup_otel_fastapi_logging
from core.opentelemetry import setup_opentelemetry
from routers import heros, posts

# アプリケーション起動時にログ設定を行う
setup_otel_fastapi_logging()

logger = getLogger(__name__)


app = FastAPI(lifespan=lifespan)

setup_opentelemetry(app)


@app.exception_handler(NoResultFound)
async def not_found_exception_handler(request: Request, exception: NoResultFound):
    logger.exception("NoResultFound Error")
    return JSONResponse(status_code=404, content={"message": "Not Found"})


@app.get("/")
async def health():
    return {"Health": "OK"}


app.include_router(heros.router)
app.include_router(posts.router)
