from pathlib import Path
from decimal import Decimal, InvalidOperation
from .db import connect

def price_value(value):
    try: p=Decimal(str(value))
    except (InvalidOperation,ValueError): raise ValueError("Price must be numeric.")
    if not p.is_finite() or p < 0: raise ValueError("Price must be non-negative.")
    return p

def init_db():
    sql=(Path(__file__).resolve().parent.parent/"sql"/"schema.sql").read_text()
    with connect() as c:
        with c.cursor() as q: q.execute(sql)
    print("Inventory table created/verified.")

def add(name,qty,price):
    if not name.strip() or qty<0: raise ValueError("Name is required and quantity cannot be negative.")
    with connect() as c:
        with c.cursor() as q:
            q.execute("INSERT INTO inventory_items(name,quantity,price) VALUES(%s,%s,%s) RETURNING item_id",(name.strip(),qty,price_value(price)))
            print("Added item ID:",q.fetchone()[0])

def list_all():
    with connect() as c:
        with c.cursor() as q:
            q.execute("SELECT item_id,name,quantity,price FROM inventory_items ORDER BY item_id")
            rows=q.fetchall()
    if not rows: print("Inventory is empty."); return
    print(f"{'ID':<6}{'NAME':<25}{'QUANTITY':>10}{'PRICE':>12}")
    for r in rows: print(f"{r[0]:<6}{r[1][:24]:<25}{r[2]:>10}{r[3]:>12.2f}")

def get(item_id):
    with connect() as c:
        with c.cursor() as q:
            q.execute("SELECT item_id,name,quantity,price FROM inventory_items WHERE item_id=%s",(item_id,))
            r=q.fetchone()
    print(r if r else "Item not found.")

def update(item_id,name,qty,price):
    if name is None and qty is None and price is None: raise ValueError("Provide a field to update.")
    if name is not None and not name.strip(): raise ValueError("Name cannot be empty.")
    if qty is not None and qty<0: raise ValueError("Quantity cannot be negative.")
    p=price_value(price) if price is not None else None
    with connect() as c:
        with c.cursor() as q:
            q.execute("""UPDATE inventory_items SET name=COALESCE(%s,name),
              quantity=COALESCE(%s,quantity),price=COALESCE(%s,price),
              updated_at=CURRENT_TIMESTAMP WHERE item_id=%s""",
              (name.strip() if name is not None else None,qty,p,item_id))
            changed=q.rowcount
    print("Item updated." if changed else "Item not found.")

def delete(item_id):
    with connect() as c:
        with c.cursor() as q:
            q.execute("DELETE FROM inventory_items WHERE item_id=%s",(item_id,))
            changed=q.rowcount
    print("Item deleted." if changed else "Item not found.")
