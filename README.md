# Database Practical

## Launching PostgreSQL for local use

This requires [`docker`](https://www.docker.com/) [to be installed](https://docs.docker.com/engine/install/) and available on `PATH`

```bash
docker compose up -d
```

Database name and access credentials can be found in the [`docker-compose.yaml`](./docker-compose.yaml) file, but they're listed here for visibility
(just know that this is not the ultimate source of truth):
```
Username: postgres
Password: postgres
Database: database
Hostname: localhost
Port:     5432
```
Therefore the so-called connection string would be constructed as follows:
```
postgres://postgres:postgres@localhost:5432/database
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

## A note for the security minded

Yes, the access credentials are exposed and committed to this public repository, however,
this is intended only for local use and there is no sensitive data in the database anyway,
therefore, this is fine.
