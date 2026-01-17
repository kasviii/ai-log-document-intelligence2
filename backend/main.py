from fastapi import FastAPI
from backend.routes.health import router as health_router
from backend.routes.upload import router as upload_router
from backend.routes.extract import router as extract_router
app = FastAPI(
    title="AI Log & Document Intelligence",
    version="0.1.0"
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(extract_router)
