from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)


class UserRole(Base):
    __tablename__ = "user_roles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role_id = Column(Integer, ForeignKey("roles.role_id"), primary_key=True)
    assigned_at = Column(TIMESTAMP, default=current_timestamp)

    user = relationship("UserDB", back_populates="roles")
    role = relationship("Role", back_populates="users")


class Contacts(Base):
    __tablename__ = "contacts"

    contact_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    added_at = Column(TIMESTAMP, default=current_timestamp)

    user = relationship("UserDB", foreign_keys=[user_id])
    contact_user = relationship("UserDB", foreign_keys=[contact_user_id])


class Files(Base):
    __tablename__ = "files"

    file_id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.message_id"), nullable=False)
    file_url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    uploaded_at = Column(TIMESTAMP, default=current_timestamp)

    message = relationship("Messages", back_populates="files")
