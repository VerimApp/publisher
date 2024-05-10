from dependency_injector.wiring import Provide, inject
from sqlalchemy.ext.asyncio import AsyncSession

from protobufs.compiled import publisher_pb2_grpc
from protobufs.compiled.publisher_pb2 import (
    PublicationResponse,
    PublicationsSelectionResponse,
)
from protobufs.compiled.auth_pb2 import (
    Empty,
)
from schemas import (
    CreatePublicationSchema,
    VoteSchema,
)
from config.di import Container
from services.publications import ICreatePublication
from services.votes import IVote
from services.repo import IPublicationRepo
from utils.decorators import handle_grpc_request_error, inject_session


class GRPCPublisher(publisher_pb2_grpc.PublisherServicer):
    @handle_grpc_request_error(PublicationResponse)
    @inject_session
    @inject
    async def publications_create(
        self,
        request,
        context,
        session: AsyncSession,
        service: ICreatePublication = Provide[Container.create_publication],
    ):
        publication = await service(
            session=session,
            user_id=request.user_id,
            schema=CreatePublicationSchema(url=request.url),
        )
        return PublicationResponse(
            id=publication.id,
            url=publication.url,
            type=publication.type,
            believed_count=publication.believed_count,
            disbelieved_count=publication.disbelieved_count,
            created_at=publication.created_at,
            believed=None,
        )

    @handle_grpc_request_error(PublicationsSelectionResponse)
    @inject_session
    @inject
    async def publications_selection(
        self,
        request,
        context,
        session: AsyncSession,
        repo: IPublicationRepo = Provide[Container.publication_repo],
    ):
        selection = await repo.selection(
            session=session,
            user_id=request.user_id,
            size=request.size,
            page=request.page,
        )
        return PublicationsSelectionResponse(
            items=[
                PublicationResponse(
                    id=publication.id,
                    url=publication.url,
                    type=publication.type,
                    believed_count=publication.believed_count,
                    disbelieved_count=publication.disbelieved_count,
                    created_at=str(publication.created_at),
                    believed=publication.believed,
                )
                for publication in selection.__dict__["items"]
            ],
            total=selection.__dict__["total"],
            page=selection.__dict__["page"],
            size=selection.__dict__["size"],
            pages=selection.__dict__["pages"],
        )

    @handle_grpc_request_error(Empty)
    @inject_session
    @inject
    async def publications_vote(
        self,
        request,
        context,
        session: AsyncSession,
        service: IVote = Provide[Container.create_vote],
    ):
        await service(
            session=session,
            user_id=request.user_id,
            publication_id=request.publication_id,
            schema=VoteSchema(believed=request.believed),
        )
        return Empty()
