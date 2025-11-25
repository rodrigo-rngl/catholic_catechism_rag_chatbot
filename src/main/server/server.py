import json
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from datetime import datetime, timezone, timedelta
from src.errors.handle_errors import handle_errors
from fastapi.exceptions import RequestValidationError
from src.validators.models.HttpRequest import HttpRequestOut
from src.main.routes.hybrid_search_route import hybrid_search_route
from src.errors.types.validation_domain_error import ValidationDomainError
from src.infra.fastembed_embedder.fastembed_embedder_factory import get_fastembed_hybrid_embedder

load_dotenv()


@asynccontextmanager
async def embedders_inicialization_lifespan(app: FastAPI):
    get_fastembed_hybrid_embedder()
    yield

app = FastAPI(
    title="API RAG do Catecismo da Igreja Católica",
    description="A **API RAG do Catecismo da Igreja Católica** nasceu do desejo de unir ciência e fé para servir melhor às pessoas. Foi construída a partir da percepção de que a tecnologia pode iluminar caminhos, levar consolo e orientar quem busca respostas seguras sobre a doutrina católica. É uma ponte entre o Catecismo e quem anseia por formação sólida, acolhedora e fiel.\n\n"

    "Este projeto existe para que comunidades, catequistas, agentes pastorais e curiosos da fé encontrem apoio em momentos de dúvida. Ao disponibilizar um acesso rápido e confiável ao Catecismo, a API pretende apoiar um movimento de evangelização que respeita a tradição e, ao mesmo tempo, dialoga com o mundo digital.\n\n"

    "“Ser cristão, para mim, significa observar o mundo e levar minha alegria e a minha força aos demais.” — **São Carlo Acutis**\n\n"

    "**O que essa API faz exatamente?**\n"
    "\nEla fornece um serviço RAG (Retrieval-Augmented Generation) especializado no Catecismo da Igreja Católica: recebe a sua pergunta, procura os parágrafos do Catecismo mais similares a pergunta, e devolve trechos completos com suas referências (Parte, Seção, Capítulo etc.). Assim, você pode construir respostas catequéticas, chatbots pastorais ou materiais educativos com base textual segura, transparente e pronta para citar.\n\n"

    "**Como a API funciona por traz dos panos?**\n"
    "- Ao receber uma dúvida, a API verifica se o conteúdo é compatível com a missão da Igreja e se está expresso com clareza. Caso a pergunta seja inadequada ou fora de escopo, a resposta será um convite a reformular com respeito ou a buscar outro caminho.\n"
    "- Se a pergunta for válida, a API vasculha a coleção do Catecismo, organizada com localizações completas (Parte, Seção, Capítulo, Artigo etc.), e entrega os parágrafos mais próximos do questionamento — sempre com contexto e transparência.\n"
    "- O retorno também traz um pequeno relatório que explica por que a pergunta foi aceita ou rejeitada, ajudando você a orientar o usuário final com mais empatia e precisão.\n\n"

    "**Recomendações de uso**\n"
    "- Traga todo o contexto possível na sua pergunta; quanto mais detalhes, maior a chance de encontrar trechos que realmente iluminem a questão.\n"
    "- Valores de top_k entre 3 e 5 costumam equilibrar profundidade e clareza. Se precisar de múltiplos pontos de vista, experimente 7 ou 8, respeitando o limite de 10.\n"
    "- Se receber uma resposta 406 (ask_clarifying), veja a mensagem e incentive o usuário a reformular a dúvida com mais foco teológico.\n"
    "- Em caso de erro 422 (reject), entenda que o assunto ultrapassa o escopo da fé católica ou contém algo impróprio; cuide para proteger o espaço espiritual que estamos construindo juntos.\n\n"

    "Que esta API ajude você a criar experiências que não apenas respondem perguntas, mas também anunciam a esperança cristã com fidelidade, ternura e responsabilidade.\n\n"

    "- **Repositório do Projeto**: [github.com/rodrigo-rngl/catholic_catechism_rag_api](https://github.com/rodrigo-rngl/catholic_catechism_rag_api)\n"
    "- [**AmicusDei** (Assistente Teológico Católico criado a partir desta API)](https://amicusdei.streamlit.app/) \n",
    version="1.0.0",
    lifespan=embedders_inicialization_lifespan
)
app.include_router(hybrid_search_route)


@app.exception_handler(RequestValidationError)
async def hybrid_search_request_validation_error_handler(request: Request,
                                                         exc: RequestValidationError) -> JSONResponse:
    raw_body = await request.body()

    payload = {}
    if raw_body:
        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload = {}

    UTC_MINUS_3 = timezone(timedelta(hours=-3))

    http_request = HttpRequestOut.model_construct(id=uuid4(),
                                                  created_in=datetime.now(
                                                      tz=UTC_MINUS_3),
                                                  query=payload.get("query"),
                                                  top_k=payload.get("top_k"))

    validation_error = ValidationDomainError(message="Erro de validação no corpo da requisição.",
                                             body={"error": exc.errors()})

    http_response = handle_errors(
        http_request=http_request,
        error=validation_error
    )

    return JSONResponse(status_code=http_response.status_code,
                        content=http_response.model_dump(mode="json"))
