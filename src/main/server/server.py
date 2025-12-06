import json
from uuid import uuid4
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from datetime import datetime, timezone, timedelta
from src.errors.handle_errors import handle_errors
from fastapi.exceptions import RequestValidationError
from src.main.routes.search_routes import search_routes
from src.main.routes.retrieve_routes import retrieve_routes
from src.errors.types.validation_error import ValidationError
from src.validators.models.HttpRequest import HttpRequestValidationError
from src.infra.fastembed_embedder.fastembed_embedder_factory import get_fastembed_hybrid_embedder

load_dotenv()


@asynccontextmanager
async def embedders_inicialization_lifespan(app: FastAPI):
    get_fastembed_hybrid_embedder()
    yield

app = FastAPI(
    title="API RAG do Catecismo da Igreja Católica",
    description="A **API RAG do Catecismo da Igreja Católica** nasceu de uma vontade simples: usar conhecimento em **Engenharia de IA** para ajudar a espalhar a evangelização católica. Ela cria uma curadoria de conteúdos textuais da Igreja voltada para aplicações digitais — especialmente chatbots — utilizando a técnica **RAG** (Retrieval-Augmented Generation) para enriquecer o contexto das solicitações com base no Catecismo.\n\n"
    "Este projeto existe para que comunidades, catequistas, agentes pastorais e curiosos da fé encontrem apoio em momentos de dúvida. Ao disponibilizar um acesso rápido e confiável ao Catecismo, a API pretende apoiar um movimento de evangelização que respeita a tradição e, ao mesmo tempo, dialoga com o mundo digital.\n\n"
    "“Ser cristão, para mim, significa observar o mundo e levar minha alegria e a minha força aos demais.” — **São Carlo Acutis**\n\n"
    "**O que essa API faz exatamente?**\n\n"
    "Até o momento, a API expõe endpoints dedicados:\n"
    "- `POST /hybrid_search`, capaz de receber perguntas catequéticas, validar sua adequação e devolver os parágrafos mais relevantes do Catecismo com localização completa;\n"
    "- `GET /catechism_paragraph/{paragraph_number}` / `POST /catechism_paragraphs`, que permitem recuperar diretamente parágrafos específicos a partir de suas numerações, mantendo a transparência doutrinal.\n\n"
    "**Como a API funciona por trás dos panos?**\n"
    "- O endpoint de busca, ao receber uma requisição, a API verifica se o conteúdo da requisição é compatível com a missão da Igreja e se está expresso com clareza. Caso a pergunta seja inadequada ou fora de escopo, a resposta será um convite a reformular com respeito ou a buscar outro caminho. Se a pergunta for válida, a API vasculha a coleção do Catecismo, organizada com localizações completas (Parte, Seção, Capítulo, Artigo etc.), e entrega os parágrafos mais próximos do questionamento — sempre com contexto e transparência.\n"
    "- Já nos endpoints de recuperação, quando você envia um número de parágrafo, a API localiza e retorna diretamente esse trecho.\n"
    "- O retorno da API também traz um pequeno relatório que explica por que a pergunta foi aceita ou rejeitada, ajudando você a orientar o usuário final com mais empatia e precisão.\n\n"
    "**Recomendações de uso**\n"
    "- Traga todo o contexto possível na sua pergunta; quanto mais detalhes, maior a chance de encontrar trechos que realmente iluminem a questão.\n"
    "- Valores de `top_k` entre 3 e 5 costumam equilibrar profundidade e clareza. Se precisar de múltiplos pontos de vista, experimente 7 ou 8, respeitando o limite de 10.\n"
    "- Se receber uma resposta `207` (ask_clarifying), veja a mensagem e incentive o usuário a reformular a dúvida com mais foco teológico.\n"
    "- Em caso de erro `406` (reject), entenda que o assunto ultrapassa o escopo da fé católica ou contém algo impróprio; cuide para proteger o espaço espiritual que estamos construindo juntos.\n\n"
    "Que esta API ajude você a criar experiências que não apenas respondem perguntas, mas também anunciam a esperança cristã com fidelidade, ternura e responsabilidade. Que Deus te abençoe!\n\n"
    "- **Repositório do Projeto**: [github.com/rodrigo-rngl/catholic_catechism_rag_api](https://github.com/rodrigo-rngl/catholic_catechism_rag_api)\n"
    "- [**AmicusDei** (Assistente Teológico Católico criado a partir desta API)](https://amicusdei.streamlit.app/) \n",
    version="2.0.0",
    lifespan=embedders_inicialization_lifespan
)
app.include_router(search_routes)
app.include_router(retrieve_routes)


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request,
                                           exc: RequestValidationError) -> JSONResponse:
    UTC_MINUS_3 = timezone(timedelta(hours=-3))

    http_request = HttpRequestValidationError(
        id=uuid4(),
        created_in=datetime.now(tz=UTC_MINUS_3)
    )

    validation_error = ValidationError(message="Erro de validação no corpo da requisição.",
                                       body=exc.errors())

    http_response = handle_errors(
        http_request=http_request,
        error=validation_error
    )

    return JSONResponse(status_code=http_response.status_code,
                        content=http_response.model_dump(mode="json"))
