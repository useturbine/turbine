from datetime import datetime
from turbine.config import config
import uuid
from turbine.schemas import PipelineSchemaGet, IndexSchemaGet
from logging import getLogger
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.types import UUID
from sqlalchemy.dialects.postgresql import JSONB
from typing import Optional


logger = getLogger(__name__)
engine = create_engine(config.database_url, pool_pre_ping=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    clerk_id: Mapped[Optional[str]] = mapped_column(unique=True)
    api_key: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID, unique=True, default=uuid.uuid4
    )
    deleted: Mapped[bool] = mapped_column(default=False)
    internal: Mapped[bool] = mapped_column(default=False)


class Index(Base):
    __tablename__ = "indexes"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
    name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    embedding_model: Mapped[dict] = mapped_column(JSONB)
    vector_database: Mapped[dict] = mapped_column(JSONB)
    deleted: Mapped[bool] = mapped_column(default=False)

    def dump(self):
        return IndexSchemaGet(
            **{
                "id": str(self.id),
                "name": self.name,
                "embedding_model": self.embedding_model,
                "vector_database": self.vector_database,
            }
        )


class Pipeline(Base):
    __tablename__ = "pipelines"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)
    name: Mapped[str]
    index_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("indexes.id"))
    data_source: Mapped[dict] = mapped_column(JSONB)
    deleted: Mapped[bool] = mapped_column(default=False)

    def dump(self):
        return PipelineSchemaGet(
            **{
                "id": str(self.id),
                "name": self.name,
                "data_source": self.data_source,
                "index_id": self.index_id,
            }
        )
