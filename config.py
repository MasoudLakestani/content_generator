from fastapi import FastAPI
from routers import users, article
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify domains of clients allowed to access, or use '*' for open access
    allow_credentials=True,
    allow_methods=["*"],  # Specify which methods can be used to access the resource, or use '*' for all
    allow_headers=["*"],  # Specify which headers can be used when making a request
)
app.include_router(users.router)
app.include_router(article.router)