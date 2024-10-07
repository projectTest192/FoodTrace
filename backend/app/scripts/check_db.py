import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(BACKEND_DIR))

from sqlalchemy import inspect
from app.db.session import engine

def check_tables():
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print("\nDatabase tables:")
    for table in tables:
        print(f"- {table}")
        columns = inspector.get_columns(table)
        for column in columns:
            print(f"  • {column['name']}: {column['type']}")

if __name__ == "__main__":
    check_tables() 