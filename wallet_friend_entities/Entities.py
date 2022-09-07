"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, BigInteger, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    """
    User class is used to store user minimum information in order to
    use upper-classes methods/functions that require role validations.
    """

    __tablename__ = 't_user'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    pwd_hash = Column(String(256), nullable=False)
    creation_datetime = Column(DateTime, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    token = Column(String(256), nullable=True)
    enabled = Column(Boolean, nullable=False)
    # ===Role relationship===
    # M to M.
    roles = relationship('Role', secondary='t_user_role', back_populates='users')


class Role(Base):
    """
     Role class defines what permissions users actually have.
     """
    __tablename__ = 't_role'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    name = Column(String(45), nullable=False, unique=True)
    description = Column(String(150), nullable=True)
    # ===Permissions relationship===
    # M to M.
    permissions = relationship('Permission', secondary='t_role_permission', back_populates='roles')
    # ===Users relationship===
    # M to M.
    users = relationship('User', secondary='t_user_role', back_populates='roles')


class Permission(Base):
    __tablename__ = 't_permission'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    name = Column(String(50), nullable=False, unique=True)
    roles = relationship('Role', secondary='t_role_permission', back_populates='permissions')


"""
User-Role intermediate table.
"""


class UserRole(Base):
    __tablename__ = 't_user_role'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    user_id = Column(BigInteger, ForeignKey('t_user.id'))
    role_id = Column(BigInteger, ForeignKey('t_role.id'))


"""
Role-Permission intermediate table.
"""


class RolePermission(Base):
    __tablename__ = 't_role_permission'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    role_id = Column(BigInteger, ForeignKey('t_role.id'))
    permission_id = Column(BigInteger, ForeignKey('t_permission.id'))



