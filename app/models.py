
from xmlrpc.client import Boolean
from sqlalchemy import TIMESTAMP, BigInteger, Column, ForeignKey, Integer, String, Boolean, text
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    rating = Column(Integer, nullable=True, server_default='0')
    published = Column(Boolean,server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), 
    nullable=False, server_default=text('NOW()'))
    postid = Column(BigInteger, nullable=False, unique=True)
    userid =  Column(BigInteger, 
            ForeignKey("users.userid", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    userid = Column(BigInteger, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), 
                nullable=False, server_default=text('NOW()'))

class Vote(Base):
    __tablename__ = 'votes'
    userid = Column(BigInteger, ForeignKey('users.userid', ondelete="CASCADE"), primary_key=True)
    postid = Column(BigInteger, ForeignKey('posts.postid', ondelete="CASCADE"), primary_key=True)