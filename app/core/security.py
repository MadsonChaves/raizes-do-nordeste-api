
import os
from dotenv import load_dotenv
from pwdlib import PasswordHash

import jwt
from datetime import datetime, timedelta, timezone


load_dotenv()

CHAVE_SECRETA = os.getenv("JWT_SECRET_KEY")

if not CHAVE_SECRETA:
    raise RuntimeError("A chave secreta JWT não foi configurada no arquivo .env")

ALGORITMO = "HS256"
TEMPO_EXPIRACAO = 30

password_hash = PasswordHash.recommended()


# Transforma a senha em um hash
def gerar_hash(senha: str) -> str:
    return password_hash.hash(senha)


# Verifica se a senha corresponde ao hash
def verificar_senha(senha: str, senha_hash: str) -> bool:
    return password_hash.verify(senha, senha_hash)


# Gera um token de autenticação
def criar_token(dados: dict):
    dados_token = dados.copy()
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=TEMPO_EXPIRACAO)
    dados_token.update({"exp": expiracao})

    token = jwt.encode(
        dados_token,
        CHAVE_SECRETA,
        algorithm=ALGORITMO
    )

    return token


# Decodifica e valida um token de autenticação
def verificar_token(token: str):
    try:
        dados = jwt.decode(
            token,
            CHAVE_SECRETA,
            algorithms=[ALGORITMO]
        )
        return dados

    except jwt.InvalidTokenError:
        return None
