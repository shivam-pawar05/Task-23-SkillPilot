# Python PostgreSQL CLI Inventory Manager
A command-line CRUD inventory app using Python argparse and psycopg2.

## Setup
1. Create database: `CREATE DATABASE inventory_db;`
2. Create/activate venv: `python -m venv venv` then activate it.
3. Install: `pip install -r requirements.txt`
4. Set PGHOST, PGPORT, PGDATABASE, PGUSER and PGPASSWORD environment variables.
5. Initialize: `python main.py init-db`

## Commands
`python main.py add --name "Keyboard" --quantity 25 --price 799.50`
`python main.py list`
`python main.py get --id 1`
`python main.py update --id 1 --quantity 30`
`python main.py delete --id 1`

Run `python main.py --help` for help. Credentials are read from environment
variables. Each write uses a transaction and rolls back on errors. Do not commit
passwords to GitHub.
