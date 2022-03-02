from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Sequence, CheckConstraint, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func, expression
from sqlalchemy.orm import relationship
import uuid

from app.models import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer,  Sequence('pk_user_id'), primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    creation_time = Column(DateTime(timezone=True), server_default=func.now())
    validated = Column(Boolean, server_default=expression.false(), nullable=False)
    validate_time = Column(DateTime(timezone=True), onupdate=func.now())
    active = Column(Boolean, server_default=expression.false(), nullable=False)

    games = relationship("Game", back_populates="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return f"id: {self.id or None}, username: {self.username}," \
               f" email: {self.email}, password: {self.password}"


class Game(Base):
    __tablename__ = 'games'
    __table_args__ = (
        CheckConstraint("status = 'active' OR status = 'done'", name='ch_status'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    is_hot_seat = Column(Boolean, nullable=False)
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    status = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=expression.text('now()'))

    user = relationship("User", back_populates='games', uselist=False, cascade='delete')


class DifficultyLevel(Base):
    __tablename__ = 'difficulty_levels'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    algorithm_depth = Column(Integer, nullable=False)


class GomokuAlgorithm(Base):
    __tablename__ = 'gomoku_algorithms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class Rule(Base):
    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)


class GameSettings(Base):
    __tablename__ = 'game_settings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.id', ondelete='CASCADE'), primary_key=True)
    difficulty_id = Column(Integer, ForeignKey('difficulty_levels.id', ondelete='CASCADE'))
    rule_id = Column(Integer, ForeignKey('rules.id', ondelete='CASCADE'))
    algorithm_id = Column(Integer, ForeignKey('gomoku_algorithms.id', ondelete='CASCADE'))
    is_debug = Column(Boolean, nullable=False, default=False)
    field_map = Column(String, nullable=False, default="default")
    dice_colors = Column(String, nullable=False, default="blue:yellow")


class History(Base):
    __tablename__ = 'games_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.id', ondelete='CASCADE'), primary_key=True)
    winner = Column(String, nullable=False)
    result = Column(String, nullable=False)
    move_count = Column(Integer, nullable=False)
