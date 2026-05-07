# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# DATABASE_URL = "mysql+pymysql://root:Trilochan%40123@localhost:3306/ai_agent_db"

# engine = create_engine(DATABASE_URL, echo=False)

# SessionLocal = sessionmaker(bind=engine)

# Base = declarative_base()
# print("DB URL:", DATABASE_URL)

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite database
DATABASE_URL = "sqlite:///./ai_agent.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

print("SQLite DB Connected")