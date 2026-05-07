from app.core.database import SessionLocal
from app.models.db_models import Query, Task, Result


class DBService:

    @staticmethod
    def save_query(session_id, query_text):
        print("Saving query:", query_text)
        db = SessionLocal()
        q = Query(session_id=session_id, query_text=query_text)
        db.add(q)
        db.commit()
        db.commit()
        print("Committed to DB")   # 👈 ADD
        db.refresh(q)
        db.close()
        return q.id

    @staticmethod
    def save_task(query_id, task_text):
        db = SessionLocal()
        t = Task(query_id=query_id, task_text=task_text)
        db.add(t)
        db.commit()
        db.refresh(t)
        db.close()
        return t.id

    @staticmethod
    def save_result(task_id, result_text):
        db = SessionLocal()
        r = Result(task_id=task_id, result_text=result_text)
        db.add(r)
        db.commit()
        db.close()

    # 🔥 NEW — FETCH HISTORY
    @staticmethod
    def get_session_history(session_id):
        db = SessionLocal()
        queries = db.query(Query).filter(Query.session_id == session_id).all()
        db.close()

        return [q.query_text for q in queries]