"""
@author: "Arnoldo J. González Quesada".
Github username: "ArnoldG6".
Contact me via "arnoldgq612@gmail.com".
GPL-3.0 license ©2022
"""
import pydantic
from sqlalchemy import Column, String, DateTime, ForeignKey, BigInteger, Boolean,create_engine
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

# Warning!: Run only once when you need to create the DB.
db_string = "postgresql://e89db34874f8a3e18aff2c149d35eed83b50bcce294983021855fd751a7" \
            ":57dc776594d12466b45b1765c001fb390cecd0ba03f91506b00d7a2e42e@localhost:5432" \
            "/d453b9b4c616f9899e4fa08a8f726cbcbbc1b898318b62d2c5af23098c57"
db = create_engine(db_string)
Base.metadata.create_all(db, Base.metadata.tables.values())