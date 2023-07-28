from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from base import Base
# ADD RELATIONSHIPS

class Script_model(Base):

    __tablename__ = "script_table"
    script = Column(String(50), primary_key = True, nullable=False) #change to script_id
    created_at = Column(Integer)
    updated_at = Column(Integer)
    topic_status = Column(String(20))
    topic_id = Column(String(50))
    topic_rel = relationship("Topic_model", back_populates= "script_rel")



