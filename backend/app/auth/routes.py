from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import Token
from app.database import pegar_sessao
from app.security import (
    criar_token_acesso, 
    criar_token_refresh,  # ← NOVO
    pegar_usuario_atual, 
    verificar_senha,
    verificar_token_refresh  # ← NOVO
)
from app.users.models import Usuario
from app.users.schema import UsuarioPublico  # ← Para retornar dados do usuário


router_auth = APIRouter(prefix="/auth", tags=["Autenticação"])

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]
Sessao = Annotated[AsyncSession, Depends(pegar_sessao)]
UsuarioAtual = Annotated[Usuario, Depends(pegar_usuario_atual)]


@router_auth.post("/token", response_model=Token)
async def login_token_acesso(
    response: Response,  # ← ADICIONADO para definir cookies
    form_data: OAuth2Form, 
    sessao: Sessao
):
    """
    Login - retorna access_token e define refresh_token em cookie HTTP-only
    """
    # Busca usuário pelo email
    usuario = await sessao.scalar(
        select(Usuario).where(Usuario.email == form_data.username)
    )

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, 
            detail="Senha ou email incorreto"
        )

    # Verifica senha
    if not verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, 
            detail="Senha ou email incorreto"
        )

    # Cria os DOIS tokens
    token_acesso = criar_token_acesso(dados={"sub": usuario.email})
    token_refresh = criar_token_refresh(dados={"sub": usuario.email})  # ← NOVO

    # Define refresh token em cookie HTTP-only (SEGURO!)
    response.set_cookie(
        key="refresh_token",
        value=token_refresh,
        httponly=True,  # JavaScript não pode acessar
        secure=False,  # Mude para True em produção com HTTPS
        samesite="lax",  # Proteção CSRF
        max_age=60 * 60 * 24 * 7,  # 7 dias
        path="/"
    )

    # Retorna apenas o access token (refresh fica no cookie)
    return {
        "access_token": token_acesso, 
        "token_type": "bearer"
    }


@router_auth.post("/refresh_token", response_model=Token)
async def refresh_acesso_token(
    response: Response,
    sessao: Sessao,
    refresh_token: str | None = Cookie(None)  # ← LÊ do cookie HTTP-only
):
    """
    Renova o access token usando o refresh token do cookie
    
    Este endpoint é chamado automaticamente pelo frontend quando o access token expira
    """
    if not refresh_token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Refresh token não encontrado"
        )

    # Verifica e decodifica o refresh token
    email = verificar_token_refresh(refresh_token)

    if not email:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Refresh token inválido ou expirado"
        )

    # Busca usuário no banco
    usuario = await sessao.scalar(
        select(Usuario).where(Usuario.email == email)
    )

    if not usuario:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Usuário não encontrado"
        )

    # Cria novos tokens (rotação de tokens para segurança)
    novo_token_acesso = criar_token_acesso(dados={"sub": usuario.email})
    novo_token_refresh = criar_token_refresh(dados={"sub": usuario.email})

    # Atualiza o cookie com novo refresh token
    response.set_cookie(
        key="refresh_token",
        value=novo_token_refresh,
        httponly=True,
        secure=False,  # True em produção
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
        path="/"
    )

    return {
        "access_token": novo_token_acesso,
        "token_type": "bearer"
    }


@router_auth.post("/logout")
async def logout(response: Response):
    """
    Logout - remove o refresh token do cookie
    """
    response.delete_cookie(
        key="refresh_token",
        path="/"
    )
    return {"mensagem": "Logout realizado com sucesso"}


@router_auth.get("/me", response_model=UsuarioPublico)
async def verificar_login(usuario: UsuarioAtual):
    """
    Retorna dados do usuário atual
    
    Este endpoint é usado pelo frontend para:
    1. Verificar se o usuário está autenticado
    2. Buscar dados do usuário após login/refresh
    """
    return usuario