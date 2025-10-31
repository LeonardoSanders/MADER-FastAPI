# MADER-FastAPI - API de Usuários e Livros

Este projeto consiste em uma API RESTful desenvolvida com FastAPI para gerenciar usuários e a sua relação com livros lidos. A API permite operações CRUD completas para usuários e a associação de livros a eles.

## Tecnologias e Escolhas de Design

A arquitetura do projeto foi pensada para ser moderna, performática e escalável, utilizando tecnologias de ponta do ecossistema Python.

*   **Framework:** **FastAPI** foi escolhido como o framework principal devido ao Curso de FASTAPI do Dunossauro, suporte nativo a programação assíncrona (`async`/`await`), sistema de injeção de dependências e geração automática de documentação interativa (Swagger UI).

*   **Banco de Dados e ORM:** A comunicação com o banco de dados é gerenciada pelo **SQLAlchemy 2.0** em seu modo assíncrono. Essa escolha permite que as operações de I/O com o banco não bloqueiem a thread principal da aplicação, garantindo alta concorrência e performance. O uso de um ORM como o SQLAlchemy abstrai o SQL, aumenta a segurança contra SQL Injection e facilita a manutenção do código.

*   **Validação de Dados:** O **Pydantic** é utilizado para definir os schemas de dados (`request` e `response`). Ele se integra perfeitamente ao FastAPI para validar, serializar e desserializar dados, garantindo que a API receba e retorne apenas dados no formato esperado, além de ser a base para a geração da documentação.

*   **Autenticação e Segurança:** A segurança é implementada com senhas hasheadas (utilizando `passlib`) e um sistema de autenticação baseado em tokens **OAuth2 com JWT**. O FastAPI facilita a implementação desse fluxo, protegendo os endpoints e garantindo que apenas usuários autenticados possam realizar determinadas ações.

*   **Estrutura do Projeto:** O código é organizado de forma modular, separando responsabilidades em diferentes pacotes e módulos:
    *   `routes`: Define os endpoints da API.
    *   `schemas`: Contém os modelos Pydantic para validação de dados.
    *   `models`: Define as tabelas do banco de dados com o SQLAlchemy.
    *   `security`: Funções relacionadas à segurança, como hashing de senhas e geração de tokens.
    *   `dependencies`: Lógica de injeção de dependências, como a obtenção do usuário logado.

*   **Migrações de Banco de Dados:** Para gerenciar as alterações no schema do banco de dados de forma versionada e segura, o projeto utiliza o **Alembic**, a ferramenta de migração oficial do SQLAlchemy.

## Como Executar o Projeto

Siga os passos abaixo para configurar e executar o ambiente de desenvolvimento localmente.

### Pré-requisitos

*   Python 3.10 ou superior
*   Poetry (gerenciador de dependências)
*   Docker e Docker Compose (para o banco de dados)

### 1. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/mader-project.git
cd mader-project
```

### 2. Configurar o Ambiente Virtual e Instalar Dependências

O projeto utiliza o Poetry para gerenciar suas dependências.

```bash
poetry install
```

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto, copiando o exemplo `.env.example`. Preencha as variáveis com as informações do seu ambiente, principalmente as de conexão com o banco de dados.

```bash
cp .env.example .env
```

Exemplo de `.env`:
```ini
DATABASE_URL="postgresql+asyncpg://app_user:app_password@localhost:5432/app_db"
SECRET_KEY="sua-chave-secreta-aqui"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Subir o Banco de Dados (PostgreSQL com Docker)

Para facilitar a configuração, um `docker-compose.yml` é fornecido para iniciar um container com o PostgreSQL.

```bash
docker-compose up -d
```

### 5. Aplicar as Migrações do Banco de Dados

Com o banco de dados em execução, aplique as migrações para criar as tabelas.

```bash
poetry run alembic upgrade head
```

### 6. Executar a Aplicação

Inicie o servidor de desenvolvimento Uvicorn.

```bash
poetry run uvicorn mader_project.main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

### 7. Acessar a Documentação Interativa

Para explorar e testar os endpoints, acesse a documentação gerada automaticamente pelo Swagger UI no seu navegador:

`http://127.0.0.1:8000/docs`