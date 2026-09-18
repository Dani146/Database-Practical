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

## Running SQL queries

The standard way to do this from the command line would follow this template
```bash
docker compose exec --user postgres postgres psql -d database -c "<query>"
```

For example:
```bash
docker compose exec --user postgres postgres psql -d database -c "SELECT * FROM ai_tool"
```

Alternatively you can use a management tool like [`pgAdmin`](https://www.pgadmin.org/) (which can
also be [launched using `docker`](https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html#examples)
if you don't wish to install it otherwise)

## Danger: deleting the database

This can be useful in the case you update the schema in `schema/init.sql`, because it only runs on an empty
database. Currently there is no migration mechanism in place for that, so the easiest way is to simply
delete the volume where the data is stored (the `-v` switch below) and then recreate it (see above for
[Launching PostgreSQL for local use](#launching-postgresql-for-local-use)).

```bash
docker compose down -v
```
