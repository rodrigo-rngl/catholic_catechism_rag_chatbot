import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
from bs4.element import NavigableString, Tag, PageElement
from src.errors.types.content_container_error import ContentContainerError
from src.pipelines.data_ingestion.catechism_page_content_splitter import CatechismPageContentSplitter

from src.config.logger_config import setup_logger
logger = setup_logger(name="CatechismScrapper")


class CatechismScrapper:
    def __init__(self, catechism_page_content_splitter: CatechismPageContentSplitter):
        self.catechism_page_content_splitter = catechism_page_content_splitter
        self.main_url = 'https://www.vatican.va/archive/cathechism_po/index_new/'
        self.main_page = 'prima-pagina-cic_po.html'
        self.buffer_payloads = list()

    def scrape(self) -> List[Dict]:
        page_links = self.__scrape_main_page_links()

        for link in page_links:
            logger.info(f'Raspando a página: {link}')
            response = self.__page_request(page_link=link)
            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')

            content_container = self.__find_content_container(soup=soup)

            page_content = self.__scrape_page_content(
                content_container=content_container)

            payloads = self.catechism_page_content_splitter.split(
                elements=page_content)
            self.buffer_payloads += payloads.copy()

            logger.info(
                f'{len(payloads)} parágrafos do Catecismo foram extraídos e estruturados com sucesso! {len(self.buffer_payloads)} parágrafos ao total.')

        return self.buffer_payloads

    def __scrape_main_page_links(self) -> List[str]:
        response = self.__page_request(page_link=self.main_page)
        html_content = response.text

        soup = BeautifulSoup(html_content, 'html.parser')

        # Lista para armazenar os links de outras páginas, contidas e disponíveis na página principal.
        links = [a_tag.get('href')  # type: ignore
                 for a_tag in soup.find_all('a', href=True) if isinstance(a_tag, PageElement)]

        # Lista com paginas únicas, excluindo páginas intermediárias.
        valids_links = [link for link in links if (
            link.startswith('p')) and ("#" not in link)]  # type: ignore
        unique_links = list(dict.fromkeys(valids_links))

        return unique_links  # type: ignore

    def __page_request(self, page_link: str) -> requests.Response:
        try:
            response = requests.get(self.main_url + page_link, timeout=10)
            response.raise_for_status()  # Lança erro para códigos 4xx ou 5xx automaticamente
            return response
        except Exception as error:
            logger.error(
                f"Erro ao fazer requisição para {self.main_url + page_link}: {error}")
            raise

    @classmethod
    def __find_content_container(cls, soup: BeautifulSoup) -> Tag:
        table_tags = soup.find_all("table")

        if len(table_tags) < 2:
            raise ContentContainerError(
                "Quantidade de table Tags (<table>) insuficientes. No momento em que a aplicação foi desenvolida, todo o conteúdo da página estava contido dentro da segunda Tag <table>.")

        table_tag = table_tags[1]
        tds = table_tag.find_all("td")  # type: ignore

        if len(tds) < 2:
            raise ContentContainerError(
                "Quantidade de td Tags (<td>) insuficientes. No momento em que a aplicação foi desenvolida, todo o conteúdo da página estava contido dentro da segunda Tag <td>.")

        container_tag = tds[1]
        if len(container_tag.find_all("p")) == 0:  # type: ignore
            raise ContentContainerError(
                "Tag <p> não existe. Deve ao menos existe uma Tag <p> para conter o conteúdo da página.")

        return container_tag  # type: ignore

    @classmethod
    def __flush_buffer(cls, buffer: List, page_content: List) -> Tuple[List, List]:
        if buffer:
            # junta tudo num único parágrafo
            buffer = [element.strip() for element in buffer]

            joined = " ".join(buffer).strip()
            if joined:
                page_content.append(joined)
            buffer.clear()

        return buffer, page_content

    def __collect_txt_in_page_element(self, page_element: PageElement, buffer: List, page_content: List) -> Tuple[List, List]:
        # textos "soltos" (fora de <p>) → acumulam no buffer
        if isinstance(page_element, NavigableString):
            txt = page_element.strip()
            if txt:
                buffer.append(txt)
            return buffer, page_content

        # elementos de página que não são do tipo Tag, é ignorado
        if not isinstance(page_element, Tag):
            return buffer, page_content

        # Tags de tipo específicos, são ignorado
        if page_element.name in ("script", "style"):
            return buffer, page_content

        # se for <p>, fecha bloco anterior e adiciona parágrafo
        if page_element.name == "p":
            buffer, page_content = self.__flush_buffer(buffer, page_content)
            txt = page_element.get_text(" ", strip=True)
            if txt:
                page_content.append(txt)
            return buffer, page_content  # não percorre filhos do <p>; já coletou o texto

        # para QUALQUER outra Tag (ex.: blockquote, div, td, etc.), desce recursivamente
        for child in page_element.children:
            buffer, page_content = self.__collect_txt_in_page_element(
                page_element=child, buffer=buffer, page_content=page_content)

        return buffer, page_content

    def __scrape_page_content(self, content_container: Tag):
        page_content = []
        buffer = []  # acumula nós consecutivos fora de <p>

        # percorre apenas os filhos diretos do contêiner
        for child in content_container:
            buffer, page_content = self.__collect_txt_in_page_element(
                page_element=child, buffer=buffer, page_content=page_content)

        # fim do container: fecha último bloco fora de <p>
        __, page_content = self.__flush_buffer(buffer, page_content)

        return page_content
