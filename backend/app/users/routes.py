from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import pegar_sessao
from app.security import pegar_senha_criptografada
from app.users.schema import UsuarioCriar, UsuarioPublico
from app.users.models import Usuario


router_user = APIRouter(prefix="/usuario", tags=["Usuario"])
Sessao = Annotated[AsyncSession, Depends(pegar_sessao)]


@router_user.post("/", status_code=HTTPStatus.CREATED, response_model=UsuarioPublico)
async def criar_usuario(usuario: UsuarioCriar, sessao: Sessao):
    db_usuario = await sessao.scalar(
        select(Usuario).where(
            (Usuario.nome == usuario.nome) | (Usuario.email == usuario.email)
        )
    )
    if db_usuario:
        if db_usuario.nome:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Nome de usuario já existe!"
            )
        elif db_usuario.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT, detail="Email já existe!"
            )
    senha_criptografada = pegar_senha_criptografada(usuario.senha)
    db_usuario = Usuario(
        email=usuario.email,
        nome=usuario.nome,
        senha=senha_criptografada,
    )
    sessao.add(db_usuario)
    await sessao.commit()
    await sessao.refresh(db_usuario)

    return db_usuario