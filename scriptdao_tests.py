import os
import pytest
from script_dao import ScriptDAO
from sqlalchemy import create_engine
from script_model import Script_model
from sqlalchemy.orm import sessionmaker, scoped_session
from base import Base

@pytest.fixture(scope="session")
def script_db_engine():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="session")
def script_db_session(script_db_engine): 
    Session = sessionmaker(bind=script_db_engine)
    return scoped_session(Session)

@pytest.fixture
def script_dao(script_db_session):
    return ScriptDAO(None, script_db_session)

class TestScriptDAO:
    def test_add_item(self, script_dao):
        script_dao.add_item("script1", 1234567890, 1234567891, "Active", "ABC123")
        with script_dao.session_scope() as session:
            script_model = session.query(Script_model).filter_by(script="script1").first()

            assert script_model.script == "script1"
            assert script_model.created_at == 1234567890
            assert script_model.updated_at == 1234567891
            assert script_model.topic_status == "Active"
            assert script_model.topic_id == "ABC123"

    def test_update_item(self, script_dao):
        script_dao.add_item("script1", 1234567890, 1234567891, "Active", "ABC123")
        script_dao.update_item("script2", None, None, "Updated", None)
        with script_dao.session_scope() as session:
            script_model = session.query(Script_model).filter_by(script="script2").first()
            assert script_model.script == "script2"
            assert script_model.topic_status == "Updated"

    def test_delete_item(self, script_dao):
        script_dao.add_item("script1", 1234567890, 1234567891, "Active", "ABC123")
        script_dao.delete_item("script1")
        script_model = script_dao.get_by_id("script1")
        assert script_model is None

    def test_get_by_id(self, script_dao):
        script_dao.add_item("script1", 1234567890, 1234567891, "Active", "ABC123")
        with script_dao.session_scope() as session:
            script_model = session.query(Script_model).filter_by(script="script2").first()
            assert script_model.script == "script1"
            assert script_model.created_at == 1234567890
            assert script_model.updated_at == 1234567891
            assert script_model.topic_status == "Active"
            assert script_model.topic_id == "ABC123"



        