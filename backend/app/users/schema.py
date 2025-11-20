from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr


class UsuarioCriar(UsuarioBase):
    senha: str


class UsuarioPublico(UsuarioBase):
    id: int
    criado_em: datetime
    model_config = ConfigDict(from_attributes=True)
