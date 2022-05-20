import datetime
import uuid

import sqlalchemy as sa
from sqlalchemy.ext import declarative
from sqlalchemy.orm import relationship

from pydantic_models import common

Base = declarative.declarative_base()
_uuid = lambda: uuid.uuid4().hex  # noqa future workpiece for function


class Admins(Base):
    __tablename__ = "admins"

    id = sa.Column(
        "id",
        sa.String(48),
        unique=True,
        nullable=False,
        primary_key=True,
        default=_uuid,
    )
    email = sa.Column("email", sa.String(320), unique=True, nullable=False)


class Clients(Base):
    __tablename__ = "clients"

    id = sa.Column(
        "id",
        sa.String(48),
        unique=True,
        nullable=False,
        primary_key=True,
        default=_uuid,
    )
    email = sa.Column("email", sa.String(320), unique=True, nullable=False)
    first_name = sa.Column("first_name", sa.String(255), nullable=False)
    last_name = sa.Column("last_name", sa.String(255), nullable=False)
    birthday = sa.Column("birthday", sa.DATE, nullable=False)
    phone_number = sa.Column("phone_number", sa.VARCHAR(25), nullable=False)
    city = sa.Column("city", sa.VARCHAR(255), nullable=False)  # mb enum?
    address = sa.Column("address", sa.VARCHAR(1023), nullable=False)


class Managers(Base):
    __tablename__ = "managers"

    id = sa.Column(
        "id",
        sa.String(48),
        unique=True,
        nullable=False,
        primary_key=True,
        default=_uuid,
    )
    email = sa.Column("email", sa.String(320), unique=True, nullable=False)
    status = sa.Column("status", sa.Boolean, server_default=sa.text("false"))
    first_name = sa.Column("first_name", sa.String(255), nullable=False)
    last_name = sa.Column("last_name", sa.String(255), nullable=False)
    birthday = sa.Column("birthday", sa.DATE, nullable=False)
    phone_number = sa.Column("phone_number", sa.VARCHAR(25), nullable=False)


class Orders(Base):
    __tablename__ = "orders"

    pk = sa.Column(
        "pk",
        sa.String(48),
        unique=True,
        nullable=False,
        primary_key=True,
        default=_uuid,
    )
    client_id = sa.Column(
        "client_id",
        sa.ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False,
    )
    manager_id = sa.Column(
        "manager_id",
        sa.ForeignKey("managers.id", ondelete="CASCADE"),
        nullable=True,
    )
    order_name = sa.Column("order_name", sa.String(255), nullable=False)
    order_details = sa.Column("order_details", sa.Text, nullable=False)
    order_status = sa.Column("order_status", sa.Enum(common.OrderStatus), nullable=True)
    sphere_type = sa.Column("sphere_type", sa.Enum(common.SphereType), nullable=True)
    created_at = sa.Column("created_at", sa.DateTime, default=datetime.datetime.utcnow)
    updated_at = sa.Column(
        "updated_at", sa.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )

