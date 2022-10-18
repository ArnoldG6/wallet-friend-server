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
    creation_datetime = Column(DateTime, nullable=False)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    pwd_hash = Column(String(256), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    enabled = Column(Boolean, nullable=False)
    token = Column(String(256), nullable=True)
    # ===Role relationship===
    # Many to many.
    roles = relationship('Role', secondary='t_user_role', back_populates='users', lazy='subquery')
    # ===Account relationship===
    # One to one.
    account = relationship("Account", back_populates="owner", uselist=False)


@pydantic.dataclasses.dataclass
class Role(Base):
    """
     Role class defines what permissions users actually have.
     """
    __tablename__ = 't_role'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    creation_datetime = Column(DateTime, nullable=False)
    name = Column(String(45), nullable=False, unique=True)
    description = Column(String(150), nullable=True)
    # ===Permissions relationship===
    # Many to many.
    permissions = relationship('Permission', secondary='t_role_permission', back_populates='roles', lazy='subquery')
    # ===Users relationship===
    # Many to many.
    users = relationship('User', secondary='t_user_role', back_populates='roles', lazy='subquery')

    def dict_rep(self):
        return self.__dict__ | {"permissions": self.permissions}


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
    # One to one.
    owner_id = Column(BigInteger, ForeignKey("t_user.id"), nullable=False)
    owner = relationship("User", back_populates="account")
    # ===Movement relationship===
    # One to many.
    movements = relationship("Movement", back_populates="account", lazy="subquery")
    # ===FixedMovement relationship===
    # One to many.
    fixed_movements = relationship("FixedMovement", back_populates="account", lazy="subquery", overlaps="movements")
    # ===Bag relationship===
    # One to many.
    bags = relationship("Bag", back_populates="account", lazy="subquery")


class Movement(Base):
    """
        Movement class stores every transaction,
        it can be a deposit or a withdrawal of money to the user account.
    """

    __tablename__ = 't_movement'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    creation_datetime = Column(DateTime, nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(String(200), nullable=True)
    amount = Column(Numeric, nullable=False)
    available_amount = Column(Numeric, nullable=False)
    # ===Account relationship===
    # Many to one.
    account_id = Column(BigInteger, ForeignKey('t_account.id'))
    account = relationship('Account', back_populates='movements', lazy='subquery')
    # ===Bag relationship===
    # M to M.
    bag_movements = relationship("BagMovement", lazy="subquery")
    # ===FixedMovement relationship===
    # Inheritance. Not sure if it is this way
    __mapper_args__ = {
        "polymorphic_identity": "t_movement"
    }


class TemporaryType(enum.Enum):
    monthly = "Monthly"
    weekly = "Weekly"
    biweekly = "Biweekly"
    daily = "Daily"


class FixedMovement(Movement):
    """
        FixedMovement class stores a recurrent transaction,
        it can be a deposit or a withdrawal of money to the user account.
    """
    __tablename__ = 't_fixed_movement'  # Indexed.
    id = Column(BigInteger, ForeignKey('t_movement.id'), primary_key=True, index=True)  # Auto-sequential.
    temporary_type = Column(Enum(TemporaryType))
    repeat_date = Column(DateTime, nullable=False)
    # ===Movement relationship===
    __mapper_args__ = {
        "polymorphic_identity": "t_fixed_movement",
    }


class Bag(Base):
    """
        Bag class stores a list of movements
    """

    __tablename__ = 't_bag'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    creation_datetime = Column(DateTime, nullable=False)
    balance = Column(Numeric, nullable=False)
    goal_balance = Column(Numeric, nullable=False)
    done = Column(Boolean, nullable=False)
    end_date = Column(DateTime, nullable=False)
    # ===Account relationship===
    # Many to one.
    account_id = Column(BigInteger, ForeignKey("t_account.id"), nullable=False)
    account = relationship("Account", back_populates="bags", lazy="subquery")
    history = []


class BagMovement(Base):
    """
    Bag-Movement
    """
    __tablename__ = 't_bag_movement'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    creation_datetime = Column(DateTime, nullable=False)
    bag_id = Column(BigInteger, ForeignKey('t_bag.id'))
    bag = relationship("Bag", lazy="subquery")
    movement_id = Column(BigInteger, ForeignKey('t_movement.id'))
    # movement = relationship("Movement", back_populates="bag_movements", lazy="subquery")
    amount = Column(Numeric, nullable=False)


class HistoricBagMovement(Base):
    __tablename__ = 't_historic_bag_movement'  # Indexed.
    id = Column(BigInteger, primary_key=True, index=True)  # Auto-sequential.
    creation_datetime = Column(DateTime, nullable=False)
    amount = Column(Numeric, nullable=False)
    origin = Column(BigInteger, ForeignKey('t_movement.id'), nullable=False)


# Updated base object for table generation script.
updated_base = Base
