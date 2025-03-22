from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.models.database import create_tables, create_admin, drop_tables
from backend.routes.admin import router as admin_router
from backend.routes.authorization import router as token_router
from backend.routes.lobby import router as lobby_router
from backend.routes.queue import router as queue_router
from backend.routes.users import router as users_router
from backend.routes.websocket import router as websocket_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_tables()
    await create_admin()
    yield
    await drop_tables()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(token_router)

app.include_router(admin_router)

app.include_router(users_router)
app.include_router(queue_router)

app.include_router(lobby_router)
app.include_router(websocket_router)
