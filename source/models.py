from sqlalchemy import Column, Integer, String, Text, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
#
#
# class Character(Base):
#     __tablename__ = 'character'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(200), nullable=False)
#     description = Column(Text, nullable=True)
#
#     def __repr__(self):
#         return f"<Character(id={self.id}, name='{self.name}', description='{self.description}')>"

metadata = MetaData()

# Define the characters table
characters = Table(
    'characters',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(200), nullable=False),
    Column('description', Text, nullable=True)
)
