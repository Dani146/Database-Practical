# Database Practical

## Launching PostgreSQL for local use

This requires [`docker`](https://www.docker.com/) [to be installed](https://docs.docker.com/engine/install/) and available on `PATH`

```bash
docker compose up -d
```

## Setting up a Python virtual environment

This requires [`uv`](https://docs.astral.sh/uv/) [to be installed](https://docs.astral.sh/uv/getting-started/installation/) and available on `PATH`

```bash
uv venv --python 3.14
uv pip install -r requirements.txt
```

## Populate the database with mock data

```bash
uv run python mock_data/populate.py
```
