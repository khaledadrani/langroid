from sqlalchemy import Table, Column, Integer, String, Text
from sqlalchemy.orm import registry
from sqlalchemy.sql import text
from sqlalchemy import create_engine, MetaData

from source.config import DataBaseConfig

metadata = MetaData()

# Define the characters table
characters = Table(
    'characters',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(200), nullable=False),
    Column('description', Text, nullable=True)
)

# Create an engine to connect to the database
engine = create_engine(DataBaseConfig().db_url, echo=True)
metadata.create_all(engine)


# Define the Character class to map to the characters table
class Character:
    def __init__(self, name, description=None):
        self.name = name
        self.description = description


mapper_registry = registry()

mapper_registry.map_imperatively(Character, characters)


# Insert a method to insert data into the characters table
def insert_character(name, description=None):
    with engine.connect() as conn:
        stmt = characters.insert().values(name=name, description=description)
        conn.execute(stmt)
        conn.commit()


# Define a function to retrieve all characters
def get_all_characters():
    with engine.connect() as conn:
        stmt = text("SELECT * FROM characters")
        result = conn.execute(stmt)
        return result.fetchall()


# Test the implementation
if __name__ == "__main__":
    # Insert some sample data
    insert_character("Gandalf", "A wise wizard")
    insert_character("Frodo", "A hobbit on a quest")

    # Retrieve all characters
    characters = get_all_characters()
    for character in characters:
        print(character)
