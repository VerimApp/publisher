from sqlalchemy import Table, Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from models import mapper_registry

from .publication import publication_table


vote_table = Table(
    "publisher_vote",
    mapper_registry.metadata,
    Column(
        "id", Integer, primary_key=True, unique=True, autoincrement=True, nullable=False
    ),
    Column(
        "publication_id",
        Integer,
        ForeignKey(publication_table.c.id, ondelete="CASCADE"),
        nullable=False,
    ),
    Column("user_id", Integer, nullable=False),
    Column("believed", Boolean, nullable=True),
)


class Vote:
    pass


vote_mapper = mapper_registry.map_imperatively(
    Vote,
    vote_table,
    properties={"publication": relationship("Publication", back_populates="votes")},
)
