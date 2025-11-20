from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, ExpiredSignatureError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import pegar_sessao
from app.users.models import Usuario
from app.settings import Configuracoes

configuracoes = Configuracoes() # type: ignore

pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def criar_token_acesso(dados: dict):
    """
    Cria um access token JWT com vida curta
    """
    codificar = dados.copy()
    expiracao = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=configuracoes.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    codificar.update({
        "exp": expiracao,
        "type": "access"  # ← ADICIONADO: Identifica como access token
    })
    jwt_codificado = encode(
        codificar, configuracoes.SECRET_KEY, algorithm=configuracoes.ALGORITHM
    )
    return jwt_codificado


def criar_token_refresh(dados: dict):
    """
    Cria um refresh token JWT com vida longa (7 dias)
    """
    codificar = dados.copy()
    expiracao = datetime.now(tz=ZoneInfo("UTC")) + timedelta(days=7)
    codificar.update({
        "exp": expiracao,
        "type": "refresh"  # ← NOVO: Identifica como refresh token
    })
    jwt_codificado = encode(
        codificar, configuracoes.SECRET_KEY, algorithm=configuracoes.ALGORITHM
    )
    return jwt_codificado


def verificar_token_refresh(token: str) -> str | None:
    """
    Verifica e decodifica um refresh token
    Retorna o email do usuário ou None se inválido
    """
    try:
        payload = decode(
            token, configuracoes.SECRET_KEY, algorithms=[configuracoes.ALGORITHM]
        )
        email: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        # Verifica se é realmente um refresh token
        if email is None or token_type != "refresh":
            return None
            
        return email
    except (DecodeError, ExpiredSignatureError):
        return None


def pegar_senha_criptografada(senha: str):
    return pwd_context.hash(senha)


def verificar_senha(senha: str, senha_criptografada: str):
    return pwd_context.verify(senha, senha_criptografada)


async def pegar_usuario_atual(
    sessao: AsyncSession = Depends(pegar_sessao), 
    token: str = Depends(oauth2_scheme)
):
    execoes_credenciais = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Suas credenciais não são válidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            token, configuracoes.SECRET_KEY, algorithms=[configuracoes.ALGORITHM]
        )
        sub_email = payload.get("sub")
        token_type = payload.get("type")  # ← NOVO
        
        if not sub_email:
            raise execoes_credenciais
        
        # ← NOVO: Verifica se é um access token
        if token_type != "access":
            raise execoes_credenciais

    except DecodeError:
        raise execoes_credenciais
    except ExpiredSignatureError:
        raise execoes_credenciais

    usuario = await sessao.scalar(select(Usuario).where(Usuario.email == sub_email))

    if not usuario:
        raise execoes_credenciais

    return usuario