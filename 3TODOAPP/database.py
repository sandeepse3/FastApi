from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker

# postgresql://<username>:<password>@localhost:<port>/<database>
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:ai@localhost:5432/todoapp"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
 # Establishing the connection to the database and create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

if __name__ == "__main__":
    try:
        db = SessionLocal()
        db.execute(text("SELECT * FROM users;"))
        print("Database connection successful!")
    except Exception as e:
        print("Database connection failed:", e)
    finally:
        db.close()
