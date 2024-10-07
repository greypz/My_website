from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.Base import Base

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="messages")
    project = Column(Integer, default=1)  # New column for project identifier

    def __repr__(self):
        return f"<Message(content={self.content}, user_id={self.user_id}, project={self.project})>"

