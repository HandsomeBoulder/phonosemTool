from fastapi import Depends
from sqlalchemy import create_engine, JSON
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, sessionmaker, Session
import json
from typing import Literal
from typing import Annotated

from settings import settings

engine = create_engine(f"sqlite:///{settings.database_name}.db")

session_factory = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)

def get_session():
    """Needed for FastApi dependecy injection."""
    with session_factory() as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

class Base(DeclarativeBase):
    pass

class EnglishWiktionary(Base):
    __tablename__ = "english_wiktionary"

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str]
    pos: Mapped[str]
    entry: Mapped[dict] = mapped_column(JSON)

class RussianWiktionary(Base):
    __tablename__ = "russian_wiktionary"

    id: Mapped[int] = mapped_column(primary_key=True)
    word: Mapped[str]
    pos: Mapped[str]
    entry: Mapped[dict] = mapped_column(JSON)

Base.metadata.create_all(engine)

def fill_wiktionary(language: Literal['russian', 'english']):
    """Заполнить таблицу данными из wiktionary."""
    with session_factory() as session:
        file = settings.english_wiktionary if language == 'english' else settings.russian_wiktionary
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                entry: dict = json.loads(line)
                word = entry.get("word")
                pos = entry.get("pos")
                if not (word and pos): continue
                if language == 'russian': db_entry = RussianWiktionary(word=word, entry=entry, pos=pos)
                else: db_entry = EnglishWiktionary(word=word, entry=entry, pos=pos)
                session.add(db_entry)
        session.commit()
        