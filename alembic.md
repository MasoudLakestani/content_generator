<!-- make migration -->
alembic revision --autogenerate -m "<message>"

<!-- migrate -->
alembic upgrade head
