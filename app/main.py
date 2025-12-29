from fastapi import FastAPI, Response

from app.api.v1 import user
from app.core.config import config
from app.core.logging import setup_logging
from app.db.schema import Base, engine

setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.app_name)


# Register routes
app.include_router(user.router, prefix="/api/v1")


@app.get("/")
async def read_root():
    return Response("Uvicorn server is running!\nFastAPI app is up and ready.\nEnjoy!")
