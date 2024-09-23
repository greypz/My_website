from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError
from models.user import User
from models.message import Message
from models.Base import Base
import psycopg2

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Connection details
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')

# Create connection string without the database name
DATABASE_URL_NO_DB = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/postgres"

# Create connection string with the database name
DATABASE_URL_WITH_DB = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Check if the database exists
try:
    # Try to connect to the database directly
    engine_with_db = create_engine(DATABASE_URL_WITH_DB)
    engine_with_db.connect()
    print(f"Connected to {DATABASE_NAME} database.")

except OperationalError as e:
    # Database does not exist, create it
    if f'database "{DATABASE_NAME}" does not exist' in str(e):
        print(f"Database {DATABASE_NAME} does not exist. Creating the database...")

        # Connect to the PostgreSQL server without specifying a database
        conn = psycopg2.connect(DATABASE_URL_NO_DB)
        conn.autocommit = True
        cursor = conn.cursor()

        # Create the database
        cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")

        # Close the cursor and connection
        cursor.close()
        conn.close()

        print(f"Database {DATABASE_NAME} created successfully.")

        # Reconnect to the newly created database
        engine_with_db = create_engine(DATABASE_URL_WITH_DB)

    else:
        raise

# Create all tables from the Base models
Base.metadata.create_all(engine_with_db)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_with_db)

# Test the session
session = SessionLocal()
session.close()
