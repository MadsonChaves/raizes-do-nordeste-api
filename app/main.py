
from fastapi import FastAPI
from sqlalchemy import text

from app.database.connection import engine
from app.routers.users import router as users_router
from app.routers.units import router as units_router
from app.routers.products import router as products_router
from app.routers.stocks import router as stocks_router
from app.routers.orders import router as orders_router
from app.routers.payments import router as payments_router
from app.routers.stock_movements import router as stock_movements_router
from app.routers import loyalty

app = FastAPI(
    title="Raízes do Nordeste API",
    description="API para gerenciamento da rede de lanchonetes Raízes do Nordeste.",
    version="1.0.0"
)


# Registra as rotas de usuários
app.include_router(users_router)

# Registra as rotas de unidades
app.include_router(units_router)

# Registra as rotas de produtos
app.include_router(products_router)

# Registra as rotas de estoque
app.include_router(stocks_router)

# Registra as rotas de pedidos
app.include_router(orders_router)

# Registra as rotas de pagamentos
app.include_router(payments_router)

# Registra as rotas de movimentações de estoque
app.include_router(stock_movements_router)

# Registra as rotas de fidelidade
app.include_router(loyalty.router)

@app.get("/")
def inicio():
    with engine.connect() as conexao:
        conexao.execute(text("SELECT 1"))

    return {
        "mensagem": "API Raízes do Nordeste funcionando!",
        "banco": "Conexão realizada com sucesso!"
    }
