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
            cur.execute(
                query=SQL("INSERT INTO {table_name} VALUES ({values})").format(
                    table_name=Identifier(table_name),
                    values=SQL(", ").join(map(Placeholder, row.keys())),
                ),
                params=row,
            )


def main():
    with psycopg.connect(CONNECTION_STRING) as conn:
        for table_name in INSERTION_ORDER:
            insert_table(conn, table_name)


if __name__ == "__main__":
    main()
