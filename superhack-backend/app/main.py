from fastapi import FastAPI
from app.routers import user
from app.routers import health

app = FastAPI(title="SuperHack Backend", docs_url="/docs")

app.include_router(user.router)
app.include_router(health.router)
