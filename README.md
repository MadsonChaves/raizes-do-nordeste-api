# Raízes do Nordeste API

## 1. Sobre o projeto

A Raízes do Nordeste API é um projeto desenvolvido como atividade prática de Back-end. Seu objetivo é construir uma API REST para gerenciar operações de um sistema de vendas de produtos alimentícios, incluindo usuários, unidades, produtos, estoque, pedidos, pagamentos e fidelidade.

A aplicação foi desenvolvida utilizando Python e FastAPI, com persistência de dados por meio do SQLAlchemy e banco de dados SQLite.

## 2. Funcionalidades implementadas

- Cadastro e autenticação de usuários.
- Autenticação utilizando tokens JWT.
- Controle de acesso por perfil de usuário.
- Gerenciamento de unidades.
- Cadastro e consulta de produtos.
- Controle de estoque por produto.
- Registro de entradas e saídas de estoque.
- Histórico de movimentações de estoque.
- Criação e consulta de pedidos.
- Processamento simulado de pagamentos.
- Programa de fidelidade com acúmulo de pontos.

## 3. Tecnologias utilizadas

- Python 3.14
- FastAPI
- SQLAlchemy
- SQLite
- Alembic
- JWT
- Postman


## 4. Como executar o projeto

### 4.1. Pré-requisitos

- Python 3.14 instalado.
- Visual Studio Code ou outro editor de código.
- Terminal PowerShell.

### 4.2. Ativar o ambiente virtual

Na pasta principal do projeto, execute:

    .\.venv\Scripts\Activate.ps1

### 4.3. Aplicar as migrações do banco de dados

Com o ambiente virtual ativado, execute:

    alembic upgrade head

### 4.4. Iniciar a API

Execute o comando:

    python -m uvicorn app.main:app --reload

A API estará disponível em:

http://127.0.0.1:8000

### 4.5. Documentação Swagger

Para visualizar e testar os endpoints, acesse:

http://127.0.0.1:8000/docs


## 5. Testes da API

Os testes foram elaborados utilizando o Postman, com o objetivo de verificar o funcionamento dos endpoints, as regras de negócio e os controles de acesso da aplicação.

A coleção contém 12 cenários de teste:

| ID | Cenário |
|---|---|
| T01 | Login com sucesso |
| T02 | Login com senha incorreta |
| T03 | Acesso sem token |
| T04 | Cliente sem permissão para criar unidade |
| T05 | Consultar perfil do usuário |
| T06 | Listar produtos |
| T07 | Consultar fidelidade |
| T08 | Cliente sem permissão para criar produto |
| T09 | Criar pedido com sucesso |
| T10 | Pagamento recusado |
| T11 | Cliente sem permissão para alterar produto |
| T12 | Cliente não pode consultar pedido de outro usuário |

### 5.1. Coleção Postman

O arquivo da coleção está disponível na pasta `tests`:

`Testes - Raizes do Nordeste API.postman_collection.json`

Para executar os testes:

1. Inicie a API.
2. Abra o Postman.
3. Importe o arquivo JSON da coleção.
4. Realize os logins necessários para obter os tokens de autenticação.
5. Execute as requisições na ordem dos cenários.

Os resultados esperados incluem respostas de sucesso e respostas de erro, conforme as regras de autorização e validação da API.


## 6. Estrutura do projeto

O projeto está organizado em módulos, separando as responsabilidades da aplicação para facilitar a manutenção, a organização e a evolução do sistema.

### 6.1. Organização das pastas

- **app/:** contém o código principal da aplicação.
- **core/:** concentra configurações e dependências essenciais, incluindo autenticação e controle de acesso.
- **database/:** contém os recursos relacionados à conexão e ao acesso ao banco de dados.
- **models/:** define os modelos das entidades e tabelas do banco de dados.
- **routers/:** contém as rotas e os endpoints da API.
- **schemas/:** define os esquemas utilizados na validação e na estruturação dos dados recebidos e enviados pela API.
- **services/:** reúne os serviços e regras de processamento da aplicação.
- **migrations/:** armazena os arquivos utilizados pelo Alembic para controlar as alterações na estrutura do banco de dados.
- **migrations/versions/:** armazena as versões das migrações.
- **tests/:** contém a coleção de testes da API criada no Postman.

### 6.2. Principais arquivos

- **main.py:** inicializa a aplicação FastAPI e registra os roteadores.
- **env.py:** configura o ambiente de execução das migrações do Alembic.
- **script.py.mako:** modelo utilizado na geração dos arquivos de migração.
- **alembic.ini:** arquivo de configuração do Alembic.
- **raizes.db:** banco de dados SQLite utilizado pela aplicação.
- **teste.py:** arquivo Python utilizado para testes.
- **README.md:** documentação principal do projeto.
- **.venv/:** ambiente virtual Python utilizado para isolar as dependências do projeto.

### 6.3. Árvore de diretórios

    Trabalho-Backend/
    ├── app/
    │   ├── core/
    │   ├── database/
    │   ├── models/
    │   ├── routers/
    │   ├── schemas/
    │   ├── services/
    │   ├── __init__.py
    │   └── main.py
    ├── migrations/
    │   ├── versions/
    │   ├── env.py
    │   └── script.py.mako
    ├── tests/
    │   └── Testes - Raizes do Nordeste API.postman_collection.json
    ├── .venv/
    ├── alembic.ini
    ├── raizes.db
    ├── README.md
    └── teste.py


## 7. Segurança da aplicação

A API possui mecanismos de segurança para proteger os dados e controlar o acesso aos recursos.

As principais medidas implementadas são:

- **Autenticação JWT:** utilização de tokens para identificar os usuários autenticados.
- **Hash de senhas:** as senhas são armazenadas de forma protegida, utilizando Argon2.
- **Controle de acesso por perfil:** determinadas operações são restritas a usuários com perfil de gerente ou administrador.
- **Proteção de pedidos:** cada usuário pode consultar somente os próprios pedidos.
- **Validação de dados:** utilização de schemas para validar as informações recebidas pela API.


## 8. Regras de negócio

A aplicação possui regras de negócio para garantir a integridade das operações realizadas.

- **Usuários:** o acesso aos recursos é controlado de acordo com o perfil do usuário.
- **Produtos:** cada produto está vinculado a uma unidade.
- **Estoque:** não é permitido realizar saídas em quantidade superior ao saldo disponível.
- **Movimentações:** as entradas e saídas de estoque são registradas no histórico.
- **Pedidos:** não é permitido repetir o mesmo produto em um pedido.
- **Pedidos:** a criação de um pedido verifica a disponibilidade dos produtos e do estoque.
- **Pagamentos:** o pagamento aprovado altera o status do pedido para pago.
- **Pagamentos:** o pagamento recusado provoca a devolução das quantidades reservadas ao estoque.
- **Fidelidade:** pagamentos aprovados geram pontos para o usuário.

## 9. Observação sobre pagamentos

O módulo de pagamentos utiliza uma simulação para representar o processamento de transações.

A API permite informar se um pagamento foi aprovado ou recusado, possibilitando testar os diferentes fluxos do sistema.

Essa implementação tem finalidade acadêmica e não realiza transações financeiras reais, pois não está integrada a um gateway de pagamento.