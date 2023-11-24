import datetime
from sqlalchemy import (
    Date,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import config

engine = create_engine(config.POSTGRES_URL)
Session = sessionmaker(bind=engine)

if config.DEV_DISABLE_FOREIGN_KEY_CHECKS:
    ForeignKey = lambda *args, **kwargs: None


class Base(DeclarativeBase):
    pass


class Member(Base):
    __tablename__ = "member"
    action_network_id: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(63), nullable=True)
    last_name: Mapped[str] = mapped_column(String(63), nullable=True)
    email: Mapped[str] = mapped_column(String(127), unique=True)
    phone: Mapped[str] = mapped_column(String(31), nullable=True)
    dsa_chapter: Mapped[str] = mapped_column(String(63), nullable=True)
    is_union_member: Mapped[bool] = mapped_column(nullable=True)
    is_student: Mapped[bool] = mapped_column(nullable=True)
    join_date: Mapped[datetime.date] = mapped_column(Date(), nullable=True)
    lapse_date: Mapped[datetime.date] = mapped_column(Date(), nullable=True)
    membership_type: Mapped[str] = mapped_column(String(63), nullable=True)
    national_in_good_standing: Mapped[bool] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"<Member {self.first_name} {self.last_name}>"


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    member_action_network_id: Mapped[str] = mapped_column(
        ForeignKey("member.action_network_id")
    )
    line1: Mapped[str] = mapped_column(nullable=True)
    line2: Mapped[str] = mapped_column(nullable=True)
    city: Mapped[str] = mapped_column(nullable=True)
    state: Mapped[str] = mapped_column(nullable=True)
    postal_code: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    primary: Mapped[bool] = mapped_column()


class Phone(Base):
    __tablename__ = "phone"
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    member_action_network_id: Mapped[str] = mapped_column(
        ForeignKey("member.action_network_id")
    )
    number: Mapped[str] = mapped_column()
    number_type: Mapped[str] = mapped_column()
    primary: Mapped[bool] = mapped_column()


class Email(Base):
    __tablename__ = "email"
    member_action_network_id: Mapped[str] = mapped_column(
        ForeignKey("member.action_network_id")
    )
    address: Mapped[str] = mapped_column(primary_key=True)
    primary: Mapped[bool] = mapped_column()
    status: Mapped[str] = mapped_column()


class Action(Base):
    __tablename__ = "action"
    action_network_id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    created_ts: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    modified_ts: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    browser_url: Mapped[str] = mapped_column()
    start_ts: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    location: Mapped[str] = mapped_column(nullable=True)


class Attendance(Base):
    __tablename__ = "attendance"
    action_network_id: Mapped[str] = mapped_column(primary_key=True)
    member_action_network_id: Mapped[str] = mapped_column(
        ForeignKey("member.action_network_id")
    )
    action_action_network_id: Mapped[str] = mapped_column(
        ForeignKey("action.action_network_id")
    )
    created_ts: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("member_action_network_id", "action_action_network_id"),
    )


class Tag(Base):
    __tablename__ = "tag"
    action_network_id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()


class Tagging(Base):
    __tablename__ = "tagging"
    action_network_id: Mapped[str] = mapped_column(primary_key=True)
    member_action_network_id: Mapped[str] = mapped_column(
        ForeignKey("member.action_network_id")
    )
    tag_action_network_id: Mapped[str] = mapped_column(
        ForeignKey("tag.action_network_id")
    )
    created_ts: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    modified_ts: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        # You would think this is unique, but it's not from the AN API.
        # UniqueConstraint("member_action_network_id", "tag_action_network_id"),
    )
