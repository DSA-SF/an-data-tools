from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Member(Base):
    __tablename__ = "member"
    action_network_id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(63))
    last_name: Mapped[str] = mapped_column(String(63))
    email: Mapped[str] = mapped_column(String(127))
    
    def __repr__(self) -> str:
        return f"<Member {self.first_name} {self.last_name}>"
