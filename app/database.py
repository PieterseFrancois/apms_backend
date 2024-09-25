from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker
from sqlalchemy_utils import database_exists, create_database

# Load database URL from environment variables
DATABASE_URL = config("DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a base class for declarative class definitions
mapper_registry = registry()
Base = mapper_registry.generate_base()

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def initialise_database() -> None:
    """
    Initializes the database by creating tables.
    Checks if the database exists and creates it if it doesn't.
    """
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
