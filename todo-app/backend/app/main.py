from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine, Base
from app.db.models import User, Task  # noqa: F401 — needed for table creation
from app.api.routes import auth, tasks, sharing

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo App API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(sharing.router)


@app.get("/health")
def health():
    return {"status": "ok"}
