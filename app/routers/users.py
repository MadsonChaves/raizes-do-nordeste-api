
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import exigir_perfil
from app.core.dependencies import get_usuario_logado
from app.database.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.core.security import gerar_hash, verificar_senha, criar_token

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"]
)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_usuario(
    usuario: UserCreate,
    db: Session = Depends(get_db)
):
    # Verifica se o e-mail já está cadastrado
    usuario_existente = db.query(User).filter(
        User.email == usuario.email
    ).first()

    if usuario_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado."
        )

    # Cria o usuário
    novo_usuario = User(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash(usuario.senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return novo_usuario

@router.post("/login")
def login(
    usuario: UserLogin,
    db: Session = Depends(get_db)
):
    # Procura o usuário pelo e-mail
    usuario_encontrado = db.query(User).filter(
        User.email == usuario.email
    ).first()

    # Verifica se o usuário existe e se a senha está correta
    if not usuario_encontrado or not verificar_senha(
        usuario.senha,
        usuario_encontrado.senha_hash
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos."
        )

    # Gera o token JWT
    token = criar_token({
        "sub": str(usuario_encontrado.id),
        "perfil": usuario_encontrado.perfil
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def obter_usuario_logado(
    usuario: User = Depends(get_usuario_logado)
):
    return {
        "id": usuario.id,
        "nome": usuario.nome,
        "email": usuario.email,
        "perfil": usuario.perfil
    }

@router.get("/area-gerencial")
def area_gerencial(
    usuario: User = Depends(
        exigir_perfil("gerente", "administrador")
    )
):
    return {
        "mensagem": "Acesso autorizado à área gerencial!",
        "usuario": usuario.nome,
        "perfil": usuario.perfil
    }