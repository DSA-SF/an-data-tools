from db import Base, engine
"""Script to create DB tables

The main script drops and recreates all tables, so only use this if needed while developing"""

Base.metadata.create_all(engine)
