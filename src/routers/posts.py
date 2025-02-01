from typing import List

from fastapi import APIRouter

from core.client import AsyncClientDep
from core.config import SettingsDep
from schemas import Post

router = APIRouter(tags=["api"])


@router.get("/posts", tags=["api"], response_model=List[Post])
async def get_posts(async_client: AsyncClientDep, settings: SettingsDep):
    response = await async_client.get(f"{settings.api_url}/posts")
    return response.json()


@router.post("/posts", tags=["api"], response_model=Post)
async def post_post(post: Post, async_client: AsyncClientDep, settings: SettingsDep):
    response = await async_client.post(
        f"{settings.api_url}/posts",
        headers={
            "Content-type": "application/json; charset=UTF-8",
        },
        data=post.model_dump_json(exclude={"id"}),
    )
    return response.json()


@router.get("/posts/{id}", tags=["api"], response_model=Post)
async def get_post(id: int, async_client: AsyncClientDep, settings: SettingsDep):
    response = await async_client.get(f"{settings.api_url}/posts/{id}")
    return response.json()


@router.put("/posts/{id}", tags=["api"], response_model=Post)
async def put_post(
    id: int, post: Post, async_client: AsyncClientDep, settings: SettingsDep
):
    response = await async_client.put(
        f"{settings.api_url}/posts/{id}",
        headers={
            "Content-type": "application/json; charset=UTF-8",
        },
        data=post.model_dump_json(),
    )
    return response.json()


@router.delete("/posts/{id}", tags=["api"])
async def delete_post(id: int, async_client: AsyncClientDep, settings: SettingsDep):
    response = await async_client.delete(f"{settings.api_url}/posts/{id}")
    return response.json()
