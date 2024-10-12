from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    TIMESTAMP,
    ForeignKey,
    DateTime,
)
from sqlalchemy.dialects.mysql import VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import current_timestamp

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)
    last_login = Column(TIMESTAMP)

    messages = relationship("Message", back_populates="user")
    roles = relationship("UserRole", back_populates="user")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message_text = Column(String, nullable=False)
    sent_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")
    conversation = relationship("Conversation", back_populates="messages")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    is_group = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    messages = relationship("Message", back_populates="conversation")


class ConversationParticipant(Base):
    __tablename__ = "conversation_participants"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    joined_at = Column(TIMESTAMP, default=current_timestamp)

    conversation = relationship("Conversation")
    user = relationship("User")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    role_name = Column(VARCHAR(50), unique=True, nullable=False)

    users = relationship("UserRole", back_populates="role")


class UserRole(Base):
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role_id = Column(Integer, ForeignKey("roles.id"))
    assigned_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    added_at = Column(TIMESTAMP, default=current_timestamp)

    user = relationship("User", foreign_keys=[user_id])

    contact_user = relationship("User", foreign_keys=[contact_user_id])

