
from sqlalchemy.orm import sessionmaker, scoped_session
from base import Base
from topic_model import Topic_model
from contextlib import contextmanager


class TopicDAO:
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

    def add_item(self, id: str, user_topic:str, created_at:int, updated_at:int, topic_status:str, topic_id:str):
        with self.session_scope() as session:
            topic_model = Topic_model(id = id, user_topic = user_topic, created_at = created_at, updated_at = updated_at, topic_status = topic_status, topic_id = topic_id)
            session.add(topic_model)
            session.commit()
            #add print
            session.explunge_all()
            return topic_model
    def update_item(self, id:str, user_topic:str, created_at:int, updated_at:int, topic_status:str, topic_id:str):
        with self.session_scope() as session:
            topic_model = session.query(Topic_model).filter_by(id=id).first()
            if topic_model:
                if id is not None:
                    topic_model.id = id
                if user_topic is not None:
                    topic_model.user_topic = user_topic
                if created_at is not None:
                    topic_model.created_at = created_at
                if updated_at is not None:
                    topic_model.updated_at = updated_at
                if topic_status is not None:
                    topic_model.topic_status = topic_status
                if topic_id is not None:
                    topic_model.topic_id = topic_id
                session.commit()
                return topic_model
            else:
                print(f"topic with id={id} not found in the database.")
            return topic_model
    def delete_item(self, id:str):
        with self.session_scope() as session:
            topic_model = session.query(Topic_model).filter_by(id=id).first()
            session.delete(topic_model)
            session.commit()
            session.explunge_all()
    def get_by_id(self, id: str):
        with self.session_scope() as session:
            topic_model = session.query(Topic_model).filter_by(id=id).first()
            return topic_model if topic_model else None