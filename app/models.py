from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import JSON as GenericJSON
from app.database import Base

class Textbook(Base):
    __tablename__ = "textbooks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)

    chunks = relationship("Chunk", back_populates="textbook", cascade="all, delete-orphan")

class Chunk(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    textbook_id = Column(Integer, ForeignKey("textbooks.id"), nullable=False)
    text = Column(Text, nullable=False)

    textbook = relationship("Textbook", back_populates="chunks")
    lesson = relationship("Lesson", back_populates="chunk", uselist=False, cascade="all, delete-orphan")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(Integer, ForeignKey("chunks.id"), nullable=False)
    lesson_json = Column(GenericJSON, nullable=False)

    chunk = relationship("Chunk", back_populates="lesson")
