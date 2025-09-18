# FROM python:3.13-slim-bookworm

# ENV PYTHONUNBUFFERED=1

# RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# ADD https://astral.sh/uv/0.7.19/install.sh /uv-installer.sh

# RUN sh /uv-installer.sh && rm /uv-installer.sh

# ENV PATH="/root/.local/bin/:$PATH"

# WORKDIR /app

# COPY uv.lock .

# COPY pyproject.toml .

# RUN uv sync --locked

# COPY . .

# EXPOSE 8001

# # CMD ["uv", "run", "fastapi", "dev", "main.py", "--host=0.0.0.0", "--port=8001"]
# CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]  

FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Install uv
ADD https://astral.sh/uv/0.7.19/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /app

# Copy dependency files first (these change less frequently)
COPY uv.lock pyproject.toml ./

# Install dependencies - this layer will be cached unless uv.lock or pyproject.toml change
RUN uv sync --locked

# Copy the rest of the application code (this changes more frequently)
COPY . .

EXPOSE 8001

# CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
CMD ["uv", "run", "fastapi", "dev", "main.py", "--host=0.0.0.0", "--port=8001"]
