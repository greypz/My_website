import logging
from sqlalchemy.orm import sessionmaker
from .__main__ import engine_with_db

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_with_db)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
        print("Transaction committed successfully")
    except Exception as e:
        db.rollback()
        logging.error(f"Transaction rolled back due to: {e}")
        raise
    finally:
        db.close()