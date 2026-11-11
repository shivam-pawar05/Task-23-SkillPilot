import os
import psycopg2

def connect():
    return psycopg2.connect(
        host=os.getenv("PGHOST","localhost"),
        port=os.getenv("PGPORT","5432"),
        dbname=os.getenv("PGDATABASE","inventory_db"),
        user=os.getenv("PGUSER","postgres"),
        password=os.getenv("PGPASSWORD",""),
        connect_timeout=5
    )
