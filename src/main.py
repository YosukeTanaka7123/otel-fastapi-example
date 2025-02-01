from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy.orm.exc import NoResultFound
from starlette.requests import Request

from core.lifespan import lifespan
from routers import heros, posts

app = FastAPI(lifespan=lifespan)


@app.exception_handler(NoResultFound)
async def not_found_exception_handler(request: Request, exception: NoResultFound):
    return JSONResponse(status_code=404, content={"message": "Not Found"})


@app.get("/")
async def health():
    return {"Health": "OK"}


app.include_router(heros.router)
app.include_router(posts.router)
