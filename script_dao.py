from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session
from base import Base
from script_model import Script_model
from contextlib import contextmanager

class ScriptDAO:
    def __init__(self, db_engine, session):
        self.engine = db_engine
        self.session = session

    @contextmanager
    def session_scope(self):
        session = self.session()
        try: 
            yield session
            session.commit()
        except:
            session.rollback()
        finally: 
            session.close()

    def add_item(self, script:str, created_at:int, updated_at:int, topic_status:str, topic_id:str):
        with self.session_scope() as session:
            script_model = Script_model(script = script, created_at = created_at, updated_at = updated_at, topic_status = topic_status, topic_id = topic_id)
            session.add(script_model)
            session.commit()
            session.explunge_all()
    def update_item(self, script:str, created_at:int, updated_at:int, topic_status:str, topic_id:str):
        with self.session_scope() as session:
            script_model = session.query(Script_model).filter_by(script=script).first()
            if script_model:
                if script is not None:
                    script_model.script = script
                if created_at is not None:
                    script_model.created_at = created_at
                if updated_at is not None:
                    script_model.updated_at = updated_at
                if topic_status is not None:
                    script_model.topic_status = topic_status
                if topic_id is not None:
                    script_model.topic_id = topic_id
                session.commit()
            else:
                    print(f"Script with script={script} not found in the database.")
    def delete_item(self, script:str):
        with self.session_scope() as session:
            script_model = session.query(Script_model).filter_by(script=script).first()
            session.delete(script_model)
            session.commit()
            session.explunge_all()
    def get_by_id(self, script: str):
        with self.session_scope() as session:
            script_model = session.query(Script_model).filter_by(script=script).first()
            return script_model if script_model else None