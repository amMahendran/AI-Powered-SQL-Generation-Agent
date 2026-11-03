from sqlalchemy import create_engine,text
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL=os.getenv("DATABASE_URL")
if not DB_URL:
    raise ValueError("Database URL Error")
else:
    print("Database URL Found")

engine=create_engine(DB_URL,pool_pre_ping=True)

def test_connection():
    with engine.connect() as connection:
        result=connection.execute(text("SELECT version()"))
        print("DATABASE CONNECTION TEST PASSED")
        # print(result.scalar())
test_connection()