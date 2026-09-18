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

## Danger: deleting the database

This can be useful in the case you update the schema in `schema/init.sql`, because it only runs on an empty
database. Currently there is no migration mechanism in place for that, so the easiest way is to simply
delete the volume where the data is stored (the `-v` switch below) and then recreate it (see above for
[Launching PostgreSQL for local use](#launching-postgresql-for-local-use)).

```bash
docker compose down -v
```
