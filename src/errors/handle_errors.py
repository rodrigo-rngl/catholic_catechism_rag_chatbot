from datetime import datetime
from src.config.logger_config import setup_logger
from src.errors.types.domain_error import DomainError
from src.errors.types.validation_domain_error import ValidationDomainError
from src.validators.models.HttpRequest import HttpRequestOut
from src.validators.models.HttpResponse import HttpResponse

logger = setup_logger(name="handle_errors")


def handle_errors(http_request: HttpRequestOut, error: Exception) -> HttpResponse:
    end_time = datetime.now(tz=http_request.created_in.tzinfo)
    took_ms = int((end_time - http_request.created_in).total_seconds() * 1000)

    if isinstance(error, ValidationDomainError):
        logger.error(error.message)
        return HttpResponse(id=http_request.id,
                            status_code=error.status_code,
                            created_in=http_request.created_in,
                            took_ms=took_ms,
                            query=http_request.query,
                            top_k=http_request.top_k,
                            body={
                                "error": [{
                                    "title": error.name,
                                    "detail": error.message,
                                    "validation_errors": error.body
                                }]
                            })

    if isinstance(error, DomainError):
        logger.error(error.message)
        return HttpResponse(id=http_request.id,
                            status_code=error.status_code,
                            created_in=http_request.created_in,
                            took_ms=took_ms,
                            query=http_request.query,
                            top_k=http_request.top_k,
                            body={
                                "error": [{
                                    "title": error.name,
                                    "detail": error.message,
                                    "query_validation": error.body
                                }]
                            })

    logger.exception(
        f"Exceção ao gerar resposta à requsição: {http_request.id}")
    return HttpResponse(id=http_request.id,
                        status_code=500,
                        created_in=http_request.created_in,
                        took_ms=took_ms,
                        query=http_request.query,
                        top_k=http_request.top_k,
                        body={
                            "error": [{
                                "title": "Server Error",
                                "detail": "Interval Server Error"
                            }]
                        })
