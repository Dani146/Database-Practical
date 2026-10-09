import csv
import sqlite3
from pathlib import Path

import psycopg

DATA_DIRECTORY = Path(__file__).resolve().parent

CONNECTION_STRING = "postgres://postgres:postgres@localhost:5432/database"


def process_jobs(pg_conn: psycopg.Connection):
    con = sqlite3.connect(":memory:")

    cur = con.cursor()
    cur.execute("CREATE TABLE jobs(title, company, location, remote, posted)")

    rows = list(csv.reader((DATA_DIRECTORY / "jobs.csv").open()))[1:]
    cur.executemany("INSERT INTO jobs VALUES (?, ?, ?, ?, ?)", rows)
    con.commit()

    companies = cur.execute("SELECT DISTINCT company FROM jobs").fetchall()
    roles = cur.execute("SELECT DISTINCT title FROM jobs").fetchall()

    with pg_conn.cursor() as pg_cur:
        pg_cur.executemany("INSERT INTO company (name) VALUES (%s)", companies)
        pg_cur.executemany("INSERT INTO role (name) VALUES (%s)", roles)
        pg_conn.commit()

        for company_id, name in pg_cur.execute(
            "SELECT company_id, name FROM company"
        ).fetchall():
            pg_cur.execute(
                "INSERT INTO department (name, company_id) VALUES (%s, %s)",
                params=(name, company_id),
            )
        pg_conn.commit()

        company_to_id = dict(
            pg_cur.execute("SELECT name, company_id FROM company").fetchall()
        )
        role_to_id = dict(pg_cur.execute("SELECT name, role_id FROM role").fetchall())
        offers = [
            (company_to_id[company], role_to_id[title], posted)
            for title, company, posted in cur.execute(
                "SELECT title, company, posted FROM jobs WHERE posted != ''"
            )
        ]

        pg_cur.executemany(
            "INSERT INTO job_offer (department_id, role_id, publication_date) VALUES (%s, %s, %s)",
            offers,
        )
        pg_conn.commit()


def process_ai_tools(pg_conn: psycopg.Connection):
    con = sqlite3.connect(":memory:")

    cur = con.cursor()
    cur.execute(
        "CREATE TABLE ai_tools(name, category, pricing, description, website, review_url, slug)"
    )

    rows = list(csv.reader((DATA_DIRECTORY / "ai-tools.csv").open()))[1:]
    cur.executemany("INSERT INTO ai_tools VALUES (?, ?, ?, ?, ?, ?, ?)", rows)
    con.commit()

    tool_names = cur.execute("SELECT DISTINCT name FROM ai_tools").fetchall()

    with pg_conn.cursor() as pg_cur:
        pg_cur.executemany("INSERT INTO ai_tool (name) VALUES (%s)", tool_names)
        pg_conn.commit()


def main():
    with psycopg.connect(CONNECTION_STRING) as conn:
        process_jobs(conn)
        process_ai_tools(conn)


if __name__ == "__main__":
    main()
