import os
from src.errors.types.domain_error import DomainError
from src.validators.models.QueryValidation import QueryValidation
from src.infra.openai_api.openai_response_creator import OpenAIResponseCreator
from src.infra.openai_api.settings.openai_api_connection_handler import OpenAIAPIConnectionHandler

from src.config.logger_config import setup_logger
logger = setup_logger(name="OpenAIAPIConnectionHandler")


class QueryValidator:
    def __init__(self) -> None:
        self.prompt_id = str(os.getenv('PROMPT_QUERY_VALIDATION_ID'))

    async def validate(self, query: str) -> QueryValidation:
        logger.info("    Validando query recebida por requsição...")
        if await self.is_inappropriate_query(query=query):
            query_validation = QueryValidation(
                scope="off_topic",
                category="other",
                confidence=1.0,
                reasons="Conteúdo moderado/indevido.",
                action="reject")

            raise DomainError(message=f'A query enviada possui conteúdo indevido/impróprio para o contexto desta aplicação.',
                              body=query_validation.model_dump())
        logger.info(
            "    A query recebida é apropriada para o contexto da aplicação!")

        logger.info(
            "    Verificando se a query recebida possui relação de contexto válida para esta aplicação...")
        query_validation = await OpenAIResponseCreator().create(
            prompt_id=self.prompt_id, variables={"query": query}, text_format=QueryValidation)

        if query_validation.action == "reject":
            raise DomainError(message=f'A query enviada não possui relação de contexto para desta aplicação.',
                              body=query_validation.model_dump())

        logger.info(
            "    A query possui relação de contexto válida para esta aplicação! Query validada com sucesso!")

        return query_validation

    @classmethod
    async def is_inappropriate_query(cls, query: str) -> bool:
        logger.info(
            "    Verificando se a query recebida é inapropriada para o contexto da aplicação...")
        async with OpenAIAPIConnectionHandler() as openai:
            try:
                query_moderation = await openai.client.moderations.create(model="omni-moderation-latest", input=query)
            except Exception:
                logger.exception(
                    f'    Exceção ao avaliar se a query é própira/imprópria para o contexto da aplicação.')
                raise

            return query_moderation.results[0].flagged
