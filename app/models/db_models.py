from sqlalchemy import Column, Integer, Text, ForeignKey
from app.core.database import Base


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Text)   # ✅ for memory
    query_text = Column(Text)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    query_id = Column(Integer, ForeignKey("queries.id"))
    task_text = Column(Text)


class Result(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    result_text = Column(Text)
    
print("MODEL LOADED WITH SESSION_ID")