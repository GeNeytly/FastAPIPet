import asyncio

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from core.models import User, Post, Profile, Order, Product
from core.models import db_helper


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    result: Result = await session.execute(stmt)
    user = result.scalar_one_or_none()
    # print(user)
    return user


async def get_post_by_id(session: AsyncSession, post_id: int) -> Post:
    post = await session.get(Post, post_id)
    return post


async def delete_post_by_id(session: AsyncSession, post: Post) -> None:
    await session.delete(post)
    await session.commit()


async def get_profile_by_user_id(session: AsyncSession, user_id: int) -> Profile | None:
    stmt = select(Profile).where(Profile.user_id == user_id)
    result: Result = await session.execute(stmt)
    profile = result.scalar_one_or_none()
    print(profile)
    return profile


async def show_user_with_profiles(session: AsyncSession) -> list[User]:
    stmt = select(User).options(joinedload(User.profile))
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    users_with_prof = []

    for user in users:
        print(user)
        if user.profile is not None:
            users_with_prof.append(user)

    return users_with_prof


async def get_users_with_posts(session: AsyncSession) -> list[User]:
    stmt = select(User).options(selectinload(User.posts))
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    users_with_posts = []

    for user in users:
        if user.posts is not None:
            users_with_posts.append(user)

    return list(users_with_posts)


async def get_posts_with_user(session: AsyncSession) -> list[Post]:
    stmt = select(Post).options(joinedload(Post.user)).order_by(Post.id)
    posts = await session.scalars(stmt)
    return list(posts)


async def get_users_with_post_and_profile(session: AsyncSession) -> list[User]:
    stmt = (
        select(User)
        .options(selectinload(User.posts), joinedload(User.profile))
        .order_by(User.id)
    )
    users = await session.scalars(stmt)
    return list(users)


async def get_profile_with_users_and_user_posts(session: AsyncSession) -> list[Profile]:
    stmt = (
        select(Profile)
        .join(Profile.user)
        .options(joinedload(Profile.user).selectinload(User.posts))
        .order_by(Profile.id)
        .where(User.username == "User1")
    )
    profiles = await session.scalars(stmt)
    return list(profiles)


# OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
# OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO


async def create_obj(session: AsyncSession, model, **kwargs):
    obj = model(**kwargs)
    session.add(obj)
    await session.commit()
    return obj


async def get_all_objs_of_model(session: AsyncSession, model, **kwargs) -> list:
    stmt = select(model).filter_by(**kwargs)
    objs = await session.scalars(stmt)
    return list(objs)


async def get_one_obj_of_model(session: AsyncSession, model, **kwargs):
    stmt = select(model).filter_by(**kwargs)
    res = await session.execute(stmt)
    return res.scalar_one_or_none()


async def demo_m2m(session: AsyncSession):
    # order = await create_order(session=session, promocode="Legendary Promo")
    # await create_obj(
    #     session, Product, name="Last Elem", description="Cool prod", price=1229
    # )
    # order1 = await get_one_obj_of_model(session=session, model=Order, id=1)
    # order2 = await get_one_obj_of_model(session=session, model=Order, id=2)
    # products = await get_all_objs_of_model(session=session, model=Product)
    # order1 = await session.scalar(
    #     select(Order).filter_by(id=order1.id).options(selectinload(Order.products))
    # )
    # print("-" * 15)
    # print(order1.products)
    # order1.products.append(products[0])
    # order1.products.append(products[1])
    # print("-" * 15)
    # await session.commit()
    # print("-" * 15)
    # order1 = await session.scalar(
    #     select(Order).filter_by(id=1).options(selectinload(Order.products))
    # )
    print("-" * 15)
    # print(order1.products)
    # print(*products, sep="\n")


async def main():
    async with db_helper.session_factory() as session:
        res = await get_users_with_post_and_profile(session)
        print(res)
        print(type(res))


if __name__ == "__main__":
    asyncio.run(main())
