
import uvicorn
from fastapi import FastAPI

from config.config import get_settings
from database import Base, engine
from handlers.auth import router as auth_router
from handlers.books import router as books_router
from handlers.users import router as users_router

from handlers.favourite import router as favourite_router
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(books_router)
app.include_router(users_router)
app.include_router(favourite_router)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
