from datetime import datetime
from src.database import Base

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, MetaData, TIMESTAMP, Table


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name_ru = Column(String(50), unique=True)
    name_en = Column(String(50), unique=True)
    name_uz = Column(String(50), unique=True)

    def __repr__(self):
        return f'<Role {self.name_ru}>'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))
    registered_on = Column(TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'
