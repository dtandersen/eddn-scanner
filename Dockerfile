FROM ghcr.io/astral-sh/uv:python3.11-alpine

RUN mkdir /app
WORKDIR /app
COPY . /app
RUN uv sync --locked
CMD ["uv", "run", "scan.py"]
