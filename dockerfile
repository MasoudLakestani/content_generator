FROM python:3.12-alpine

# Install necessary packages including dependencies for Gunicorn
RUN apk update && apk add --no-cache libressl-dev gcc libc-dev

# Set the working directory
WORKDIR /app/content_generator

# Install poetry
RUN pip install poetry

# Copy only the poetry files first to leverage Docker caching
COPY ./poetry.lock ./pyproject.toml /app/content_generator/

# Don't create a virtualenv
ENV POETRY_VIRTUALENVS_CREATE=false

# Install dependencies
RUN poetry install --no-root

# Install Gunicorn
RUN pip install gunicorn

# Copy the rest of the code
COPY . /app/content_generator

# Set the command to use Gunicorn with Uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "12", "--bind", "0.0.0.0:443", "--keyfile", "/etc/letsencrypt/live/parsllm.ir/privkey.pem", "--certfile", "/etc/letsencrypt/live/parsllm.ir/fullchain.pem", "config:app"]
