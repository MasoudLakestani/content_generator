FROM python:3.12-alpine

WORKDIR /app

RUN pip install poetry

COPY ./poetry.lock ./pyproject.toml /app/

# Don't create a virtualenv
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-root 

# Copy the rest of the code
COPY . /app

WORKDIR /app/content_generator

# Enable the venv
ENV PATH="/root/.local/bin:$PATH"

# Run the spiders
CMD ["sh", "-c", "python main.py"]

