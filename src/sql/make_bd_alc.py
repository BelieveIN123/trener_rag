# create_db.py

from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    Enum,
    Boolean,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# 1. Объявляем базовый класс для всех моделей
Base = declarative_base()

# 2. Определяем модели (таблицы) согласно схеме

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String, unique=True, nullable=False)  # ID в мессенджере
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    timezone = Column(String, nullable=True)  # Например, "Europe/Amsterdam"

    # Связи (необязательно, но удобно)
    goals = relationship("Goal", back_populates="user", cascade="all, delete-orphan")
    strengths_weaknesses = relationship(
        "StrengthWeakness", back_populates="user", cascade="all, delete-orphan"
    )
    conversations = relationship(
        "Conversation", back_populates="user", cascade="all, delete-orphan"
    )
    progress_entries = relationship(
        "ProgressEntry", back_populates="user", cascade="all, delete-orphan"
    )


class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)  # Текст цели
    description = Column(Text, nullable=True)  # Дополнительные детали
    start_date = Column(Date, default=datetime.utcnow, nullable=False)
    target_date = Column(Date, nullable=True)
    status = Column(
        Enum("active", "paused", "achieved", "dropped", name="goal_status"),
        default="active",
        nullable=False,
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="goals")
    progress_entries = relationship(
        "ProgressEntry", back_populates="goal", cascade="all, delete-orphan"
    )


class StrengthWeakness(Base):
    __tablename__ = "strengths_weaknesses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(
        Enum("strength", "weakness", name="sw_type"),
        nullable=False,
    )  # "strength" или "weakness"
    value = Column(String, nullable=False)  # Например, "усидчивость", "прокрастинация"
    source = Column(
        Enum("self", "gpt", name="sw_source"),
        default="self",
        nullable=False,
    )  # "self" (пользователь выбрал) или "gpt" (пометка модели)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="strengths_weaknesses")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message_from = Column(
        Enum("user", "bot", name="msg_from"), nullable=False
    )  # "user" или "bot"
    message_text = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    used_for_gpt = Column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="conversations")


class ProgressEntry(Base):
    __tablename__ = "progress_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    goal_id = Column(Integer, ForeignKey("goals.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, default=datetime.utcnow, nullable=False)
    status = Column(String, nullable=False)  # Краткий статус: "день 1/30: изучил 20 слов"
    notes = Column(Text, nullable=True)  # Детали, затруднения, достижения

    user = relationship("User", back_populates="progress_entries")
    goal = relationship("Goal", back_populates="progress_entries")


# 3. Функция для создания базы и всех таблиц
def init_db(db_path: str = "sqlite:///app.db"):
    """
    Создаёт SQLite-файл (app.db) и все таблицы, описанные в моделях.
    Если файл уже существует и таблицы созданы — ничего не поменяется.
    """
    engine = create_engine(db_path, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    return engine


if __name__ == "__main__":
    # Запускаем инициализацию БД
    engine = init_db()
    print("База данных и таблицы успешно созданы (SQLite).")
