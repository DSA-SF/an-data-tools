from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
import config

engine = create_engine(config.POSTGRES_URL)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Member(Base):
    __tablename__ = "member"
    action_network_id: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(63), nullable=True)
    last_name: Mapped[str] = mapped_column(String(63), nullable=True)
    email: Mapped[str] = mapped_column(String(127), unique=True)
    
    def __repr__(self) -> str:
        return f"<Member {self.first_name} {self.last_name}>"


class Action(Base):
    __tablename__ = "action"
    action_network_id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(nullable=True)
    created_date_iso: Mapped[str] = mapped_column()
    modified_date_iso: Mapped[str] = mapped_column()
    browser_url: Mapped[str] = mapped_column()
    start_date_iso: Mapped[str] = mapped_column(nullable=True)
    location: Mapped[str] = mapped_column(nullable=True)
