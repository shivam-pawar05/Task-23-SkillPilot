import argparse,sys,psycopg2
from inventory import operations as op

p=argparse.ArgumentParser(description="PostgreSQL CLI Inventory Manager")
s=p.add_subparsers(dest="cmd",required=True)
s.add_parser("init-db"); s.add_parser("list")
a=s.add_parser("add"); a.add_argument("--name",required=True); a.add_argument("--quantity",required=True,type=int); a.add_argument("--price",required=True,type=float)
g=s.add_parser("get"); g.add_argument("--id",required=True,type=int)
u=s.add_parser("update"); u.add_argument("--id",required=True,type=int); u.add_argument("--name"); u.add_argument("--quantity",type=int); u.add_argument("--price",type=float)
d=s.add_parser("delete"); d.add_argument("--id",required=True,type=int)
x=p.parse_args()
try:
    if x.cmd=="init-db": op.init_db()
    elif x.cmd=="list": op.list_all()
    elif x.cmd=="add": op.add(x.name,x.quantity,x.price)
    elif x.cmd=="get": op.get(x.id)
    elif x.cmd=="update": op.update(x.id,x.name,x.quantity,x.price)
    elif x.cmd=="delete": op.delete(x.id)
except ValueError as e: print("Input error:",e,file=sys.stderr); sys.exit(2)
except psycopg2.OperationalError: print("Connection failed. Check PostgreSQL and PG* environment settings.",file=sys.stderr); sys.exit(1)
except psycopg2.Error as e: print("Database error:",e,file=sys.stderr); sys.exit(1)
