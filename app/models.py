from xmlrpc.client import Boolean
from sqlalchemy import TIMESTAMP, BigInteger, Column, Integer, String, Boolean, text
from .database import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    rating = Column(Integer, nullable=True, server_default='0')
    published = Column(Boolean,server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
    nullable=False, server_default=text('NOW()'))
    postid = Column(BigInteger, nullable=False)

