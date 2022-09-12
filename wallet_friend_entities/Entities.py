"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import pydantic
from sqlalchemy import Column, String, DateTime, ForeignKey, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


@pydantic.dataclasses.dataclass
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
    enabled = Column(Boolean, nullable=False)
    token = Column(String(256), nullable=True)
    # ===Role relationship===
    # M to M.
    roles = relationship('Role', secondary='t_user_role', back_populates='users')


@pydantic.dataclasses.dataclass
class Role(Base):
    """
     Role class defines what permissions users actually have.
     """
    __tablename__ = 't_role'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    name = Column(String(45), nullable=False, unique=True)
    description = Column(String(150), nullable=True)
    creation_datetime = Column(DateTime, nullable=False)
    # ===Permissions relationship===
    # M to M.
    permissions = relationship('Permission', secondary='t_role_permission', back_populates='roles')
    # ===Users relationship===
    # M to M.
    users = relationship('User', secondary='t_user_role', back_populates='roles')

    def dict_rep(self):
        result = self.__dict__
        result["permissions"] = self.permissions
        return result


@pydantic.dataclasses.dataclass
class Permission(Base):
    __tablename__ = 't_permission'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    creation_datetime = Column(DateTime, nullable=False)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(150), nullable=True)
    roles = relationship('Role', secondary='t_role_permission', back_populates='permissions')


class UserRole(Base):
    """
    User-Role intermediate table.
    """
    __tablename__ = 't_user_role'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    user_id = Column(BigInteger, ForeignKey('t_user.id'))
    role_id = Column(BigInteger, ForeignKey('t_role.id'))


class RolePermission(Base):
    """
    Role-Permission intermediate table.
    """
    __tablename__ = 't_role_permission'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    role_id = Column(BigInteger, ForeignKey('t_role.id'))
    permission_id = Column(BigInteger, ForeignKey('t_permission.id'))


