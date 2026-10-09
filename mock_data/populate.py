import csv
from pathlib import Path

import psycopg
from psycopg.sql import SQL, Identifier, Placeholder

DATA_DIRECTORY = Path(__file__).resolve().parent / "data"

CONNECTION_STRING = "postgres://postgres:postgres@localhost:5432/database"
INSERTION_ORDER = [
    "company",
    "department",
    "role",
    "employee",
    "job_offer",
    "ai_tool",
    "ai_usage",
]


def insert_table(conn: psycopg.Connection, table_name: str):
    with conn.cursor() as cur, (DATA_DIRECTORY / f"{table_name}.csv").open() as file:
        reader = csv.DictReader(file)

        for row in reader:
            # the id column is auto-incremented and does not allow setting a value, overriding is
            # possible, but would require manually changing the increment value for the table
            insert_keys = list(row.keys())[1:]
            cur.execute(
                query=SQL("INSERT INTO {table_name} ({keys}) VALUES ({values})").format(
                    table_name=Identifier(table_name),
                    keys=SQL(", ").join(map(Identifier, insert_keys)),
                    values=SQL(", ").join(map(Placeholder, insert_keys)),
                ),
                params=row,
            )


def main():
    with psycopg.connect(CONNECTION_STRING) as conn:
        for table_name in INSERTION_ORDER:
            insert_table(conn, table_name)


if __name__ == "__main__":
    main()
