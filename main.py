from fastapi import FastAPI
from routers.parts import router as parts_router

app = FastAPI(title="hermes-auto-parts-api", version="0.1.0")
app.include_router(parts_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
