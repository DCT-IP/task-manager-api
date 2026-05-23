from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://api_user:1234@localhost:3306/taskdb"

engine = create_engine(
    DATABASE_URL,
    echo=True,   # helps debug SQL
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()