from fastapi import FastAPI
from routers import users, article


app = FastAPI()
app.include_router(users.router)
app.include_router(article.router)