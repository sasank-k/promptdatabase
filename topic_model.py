from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from base import Base

class Topic_model(Base):

    __tablename__ = 'topic_table'

    id = Column(String(50), primary_key=True)
    user_topic = Column(String(50), nullable=False)
    created_at = Column(Integer)
    updated_at = Column(Integer)
    topic_status = Column(String(20))
    topic_id = Column(String(50))
    script_rel = relationship("Script_model", back_populates="topic_rel")



