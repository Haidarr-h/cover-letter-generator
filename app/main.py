from fastapi import FastAPI
from app.api import routes
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host = "0.0.0.0",
        port = 8000,
        reload = True
    )