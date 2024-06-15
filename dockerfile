FROM python:3.12-alpine

# Install necessary packages
RUN apt-get update && apt-get install -y libssl-dev

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

# Copy the rest of the code
COPY . /app/content_generator

# Enable the venv
ENV PATH="/root/.local/bin:$PATH"

# Run the main.py
CMD ["python", "main.py"]
