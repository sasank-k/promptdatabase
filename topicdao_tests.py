import os
import pytest
from topic_dao import TopicDAO
from sqlalchemy import create_engine
from topic_model import Topic_model
from sqlalchemy.orm import sessionmaker, scoped_session
from base import Base

@pytest.fixture(scope="session")
def topic_db_engine():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="session")
def topic_db_session(topic_db_engine): 
    Session = sessionmaker(bind=topic_db_engine)
    return scoped_session(Session)


@pytest.fixture
def topic_dao(topic_db_session):
    return TopicDAO(None, topic_db_session)



class TestTopicDAO:
    def test_add_item(self, topic_dao):
        topic_dao.add_item("1A", "Topic 1", 12345, 123456, "Active", "ABC123")
        with topic_dao.session_scope() as session:
            topic_model = session.query(Topic_model).filter_by(id="1A").first()

            assert topic_model is not None
            assert topic_model.id == "1A"
            assert topic_model.user_topic == "Topic 1"
            assert topic_model.created_at == 12345
            assert topic_model.updated_at == 123456
            assert topic_model.topic_status == "Active"
            assert topic_model.topic_id == "ABC123"
    
    def test_update_item(self, topic_dao):
        topic_dao.add_item("1A", "Topic 1", 12345, 123456, "Active", "ABC123")
        topic_dao.update_item("1A", "Updated Topic", None, 987654, "Updated", None)

        with topic_dao.session_scope() as session:
            topic_model = session.query(Topic_model).filter_by(id="1A").first()
            assert topic_model is not None
            assert topic_model.user_topic == "Updated Topic"
            assert topic_model.created_at == 12345
            assert topic_model.updated_at == 987654
            assert topic_model.topic_status == "Updated"
            assert topic_model.topic_id == "ABC123"

    def test_delete_item(self, topic_dao):
        topic_dao.add_item("1A", "Topic 1", 12345, 123456, "Active", "ABC123")
        topic_dao.delete_item("1A")
        with topic_dao.session_scope() as session:
            topic_model = session.query(Topic_model).filter_by(id="1A").first()
            assert topic_model is None
    def test_get_by_id(self, topic_dao):
        topic_dao.add_item("1A", "Topic 1", 12345, 123456, "Active", "ABC123")
        with topic_dao.session_scope() as session:
            topic = topic_dao.get_by_id("1A")
            assert topic is not None
            assert topic.id == "1A"
            assert topic.user_topic == "Topic 1"
            assert topic.created_at == 12345
            assert topic.updated_at == 123456
            assert topic.topic_status == "Active"
            assert topic.topic_id == "ABC123"