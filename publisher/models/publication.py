from sqlalchemy import Table, Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from models import mapper_registry


publication_table = Table(
    "publisher_publication",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False
    ),
    Column("user_id", Integer, nullable=False),
    Column("url", String, nullable=False),
    Column("type", String, nullable=False),
    Column("believed_count", Integer, default=0, nullable=False),
    Column("disbelieved_count", Integer, default=0, nullable=False),
    Column(
        "created_at", DateTime(timezone=True), server_default=func.now(), nullable=False
    ),
    Column(
        "updated_at",
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    ),
)


class Publication:
    pass


publication_mapper = mapper_registry.map_imperatively(
    Publication,
    publication_table,
    properties={"votes": relationship("Vote", back_populates="publication")},
)
