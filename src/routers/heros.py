from fastapi import APIRouter, status
from sqlmodel import select

from core.database import AsyncSessionDep
from tables import Hero

router = APIRouter(tags=["database"])


@router.get("/heros")
async def get_heros(async_session: AsyncSessionDep):
    results = await async_session.exec(statement=select(Hero))
    heros = results.all()
    return heros


@router.post("/heros")
async def post_hero(hero: Hero, async_session: AsyncSessionDep):
    async_session.add(hero)
    return hero


@router.get("/heros/{id}")
async def get_hero(id: int, async_session: AsyncSessionDep):
    hero = await async_session.get_one(Hero, id)
    return hero


@router.put("/heros/{id}")
async def put_hero(id: int, hero: Hero, async_session: AsyncSessionDep):
    current_hero = await async_session.get_one(Hero, id)
    current_hero.id = hero.id
    current_hero.name = hero.name
    current_hero.age = hero.age
    current_hero.secret_name = hero.secret_name
    await async_session.merge(current_hero)
    return current_hero


@router.delete("/heros/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hero(id: int, async_session: AsyncSessionDep):
    hero = await async_session.get_one(Hero, id)
    await async_session.delete(hero)
