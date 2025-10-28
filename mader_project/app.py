from http import HTTPStatus
from fastapi import FastAPI

from mader_project.routes import auth, users, novelists, books
from mader_project.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(books.router)
app.include_router(novelists.router)

@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def read_root():
    return {'message': 'Hello World!'}