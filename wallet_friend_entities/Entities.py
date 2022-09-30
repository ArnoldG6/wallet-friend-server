"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import enum

import pydantic
from sqlalchemy import Column, String, DateTime, ForeignKey, BigInteger, Boolean, Numeric, Enum
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
    roles = relationship('Role', secondary='t_user_role', back_populates='users', lazy='subquery')
    # ===Account relationship===
    # O to M.
    account = relationship("Account", back_populates="parent")


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
    permissions = relationship('Permission', secondary='t_role_permission', back_populates='roles', lazy='subquery')
    # ===Users relationship===
    # M to M.
    users = relationship('User', secondary='t_user_role', back_populates='roles', lazy='subquery')

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
    roles = relationship('Role', secondary='t_role_permission', back_populates='permissions', lazy='subquery')


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


class Account(Base):
    """
        Account class is used to store user information related to the money that is entered or withdrew,
        also works as link between user and movement class.
    """

    __tablename__ = 't_account'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    creation_datetime = Column(DateTime, nullable=False)
    total_balance = Column(Numeric, nullable=False)
    # ===User relationship===
    # M to O.
    owner_username = Column(String(100), ForeignKey("t_user.username"), nullable=False)
    owner = relationship("User", back_populates="children")
    # ===Movement relationship===
    # M to M.
    movements = relationship("Movement", secondary='t_account_movement', back_populates='accounts', lazy='subquery')
    # ===Bag relationship===
    # O to M.
    bags = relationship("Bag", back_populates="parent")


class Movement(Base):
    """
        Movement class stores every transaction,
        it can be a deposit or a withdrawal of money to the user account.
    """

    __tablename__ = 't_movement'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    creation_datetime = Column(DateTime, nullable=False)
    name = Column(String(50), nullable=False)
    description = Column(String(50))
    amount = Column(Numeric, nullable=False)
    available_amount = Column(Numeric, nullable=False)
    # ===Account relationship===
    # M to M.
    account = relationship('Account', secondary='t_account_movement', back_populates='movements', lazy='subquery')
    # ===Bag relationship===
    # M to M.
    bag = relationship('Bag', secondary='t_bag_movement', back_populates='movements', lazy='subquery')
    # ===RecurrentMovement relationship===
    # Inheritance.
    __mapper_args__ = {
        "polymorphic_on": "movement_type",
    }


class TemporaryType(enum.Enum):
    monthly = "Monthly"
    weekly = "Weekly"
    biweekly = "Biweekly"
    daily = "Daily"


class RecurrentMovement(Movement):
    """
        RecurrentMovement class stores a recurrent transaction,
        it can be a deposit or a withdrawal of money to the user account.
    """
    __tablename__ = 't_recurrentMovement'  # Indexed.
    temporary_type = Column(Enum(TemporaryType))
    end_date = Column(DateTime, nullable=False)
    __mapper_args__ = {
        "polymorphic_identity": "movement",
    }
    # Applying Inheritance is missing to do


class Bag(Base):
    """
        Bag class stores a list of movements
    """

    __tablename__ = 't_bag'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    balance = Column(Numeric, nullable=False)
    goal_balance = Column(Numeric, nullable=False)
    end_date = Column(DateTime, nullable=False)
    # ===Account relationship===
    # M to O.
    account_id = Column(BigInteger, ForeignKey("t_account.id"), nullable=False)
    account = relationship("Account", back_populates="children")
    # ===Movement relationship===
    # M to M.
    movements = relationship("Movement", secondary='t_bag_movement', back_populates='bags', lazy='subquery')


class BagMovement(Base):
    """
    Bag-Movement intermediate table.
    """
    __tablename__ = 't_bag_movement'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    bag_id = Column(BigInteger, ForeignKey('t_bag.id'))
    movement_id = Column(BigInteger, ForeignKey('t_movement.id'))


class AccountMovement(Base):
    """
    Account-Movement intermediate table.
    """
    __tablename__ = 't_account_movement'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    account_id = Column(BigInteger, ForeignKey('t_bag.id'))
    movement_id = Column(BigInteger, ForeignKey('t_movement.id'))
