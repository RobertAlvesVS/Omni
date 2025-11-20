from datetime import datetime
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import func
from app.database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True)
    criado_em: Mapped[datetime] = mapped_column(server_default=func.now())
