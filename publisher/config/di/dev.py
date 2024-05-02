from dependency_injector import containers, providers

import auth_pb2_grpc
from auth_grpc_typed import AuthStub
from config import settings
from config.celery import app as _celery_app
from config.db import Database
from config.grpc import GRPCConnection

from services.publications import CreatePublication
from services.votes import Vote
from repo import PublicationRepo, VoteRepo


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["grpc_services"], modules=["config.celery", "grpc_services.publisher"]
    )

    celery_app = providers.Object(_celery_app)

    _auth_grpc = providers.Singleton(
        GRPCConnection,
        host=settings.AUTH_GRPC_HOST,
        port=settings.AUTH_GRPC_PORT,
        stub=auth_pb2_grpc.AuthStub,
    )
    auth_grpc = providers.Singleton(AuthStub, connection=_auth_grpc)

    db = providers.Singleton(Database, db_url=settings.DATABASE_URL)

    publication_repo = providers.Singleton(
        PublicationRepo, session_factory=db.provided.session
    )
    _vote_repo = providers.Singleton(VoteRepo, session_factory=db.provided.session)

    create_publication = providers.Singleton(CreatePublication, repo=publication_repo)
    create_vote = providers.Singleton(
        Vote, repo=_vote_repo, publication_repo=publication_repo
    )
