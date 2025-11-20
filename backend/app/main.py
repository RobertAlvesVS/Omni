from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from http import HTTPStatus

from fastapi.responses import FileResponse
from app.users.routes import router_user
from app.auth.routes import router_auth
from app.schemas import Mensagem

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL do seu Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router_user)
app.include_router(router_auth)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")

@app.get("/", response_model=Mensagem, status_code=HTTPStatus.OK, tags=["Raiz"])
def raiz():
    return {"mensagem": "Api Online"}
