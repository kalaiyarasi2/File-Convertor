from fastapi import FastAPI
from controllers.converter_controller import router as converter_router
from database.db import init_db

app = FastAPI(title="Universal Format Converter API")

# Create DB tables on startup
init_db()

app.include_router(converter_router, prefix="", tags=["Format Converter"])


@app.get("/")
def health_check():
    return {"status": "running", "message": "Universal Format Converter API"}

