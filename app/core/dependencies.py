
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.models.user import User
from app.core.security import verificar_token


bearer_scheme = HTTPBearer()


def get_usuario_logado(
    credenciais: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    token = credenciais.credentials

    dados_token = verificar_token(token)

    if not dados_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado."
        )

    usuario_id = dados_token.get("sub")

    usuario = db.query(User).filter(
        User.id == int(usuario_id)
    ).first()

    if not usuario or not usuario.ativo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado ou inativo."
        )

    return usuario

# Verifica se o usuário possui o perfil necessário
def exigir_perfil(*perfis_permitidos: str):

    def verificar_perfil(
        usuario: User = Depends(get_usuario_logado)
    ):
        if usuario.perfil not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este recurso."
            )

        return usuario

    return verificar_perfil