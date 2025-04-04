from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from backend.secure import pwd_context

engine = create_async_engine("sqlite+aiosqlite:///rps_arena.db")
Session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class UserOrm(Model):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]
    role: Mapped[str] = mapped_column(default="user")
    status: Mapped[str] = mapped_column(default="idle")

    rating: Mapped[int] = mapped_column(default=0)
    games_played: Mapped[int] = mapped_column(default=0)
    wins: Mapped[int] = mapped_column(default=0)
    losses: Mapped[int] = mapped_column(default=0)
    ties: Mapped[int] = mapped_column(default=0)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


async def create_admin():
    async with Session() as session:
        result = await session.execute(select(UserOrm).where(UserOrm.role == "admin"))
        admin_user = result.scalar_one_or_none()

        if not admin_user:
            admin_user = UserOrm(
                username="admin",
                password=pwd_context.hash("admin"),
                role="admin"
            )
            session.add(admin_user)
            await session.commit()
