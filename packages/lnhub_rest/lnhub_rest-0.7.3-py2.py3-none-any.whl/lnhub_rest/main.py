import os

import uvicorn
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.middleware.cors import CORSMiddleware

from lnhub_rest.routers import account, ci, dev, instance

root_path = "/" + os.getenv("ROOT_PATH", "")
port = int(os.getenv("PORT", 8000))


app = FastAPI(openapi_prefix=root_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ci.router)
app.include_router(account.router)
app.include_router(instance.router)
app.include_router(dev.router)

client = TestClient(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=port, root_path=root_path)
