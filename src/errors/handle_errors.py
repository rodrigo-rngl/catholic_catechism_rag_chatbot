from src.errors.types.bad_query_error import BadQueryError
from src.validators.models.HttpResponse import HttpResponse
from src.errors.types.content_container_error import ContentContainerError
from src.errors.types.collection_not_found_error import CollectionNotFoundError
from src.errors.types.class_not_implemented_error import ClassNotImplementedError
from src.errors.types.points_searcher_not_found_error import PointsSearcherNotFoundError
from src.errors.types.collection_creator_not_found_error import CollectionCreatorNotFoundError

from src.config.logger_config import setup_logger
logger = setup_logger(name="handle_errors")


def handle_errors(error: Exception) -> HttpResponse:
    if isinstance(error, (BadQueryError, ClassNotImplementedError, CollectionCreatorNotFoundError,
                          CollectionNotFoundError, ContentContainerError, PointsSearcherNotFoundError)):
        logger.error(error.message)
        return HttpResponse(
            status_code=error.status_code,
            body={
                "errors": [{
                    "title": error.name,
                    "detail": error.message
                }]
            }
        )

    return HttpResponse(
        status_code=500,
        body={
            "errors": [{
                "title": "Server Error",
                "detail": str(error)
            }]
        }
    )
