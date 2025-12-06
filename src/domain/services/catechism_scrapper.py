import requests
from typing import List
from bs4 import BeautifulSoup
from src.validators.models.Payload import Payload
from bs4.element import NavigableString, Tag, PageElement
from src.domain.services.catechism_page_content_splitter import CatechismPageContentSplitter

from src.config.logger_config import setup_logger
logger = setup_logger(name="CatechismScrapper")


class CatechismScrapper:
    def __init__(self) -> None:
        self.catechism_page_content_splitter = CatechismPageContentSplitter()
        self.main_url = 'https://www.vatican.va/archive/cathechism_po/index_new/'
        self.main_page = 'prima-pagina-cic_po.html'

    def scrape(self) -> List[Payload]:
        logger.info(
            "Iniciando a raspagem dos parágrafos do catecismo da Igreja Católica...")
        page_links = self.__scrape_main_page_links()

        for link in page_links:
            logger.info(f'Raspando a página: {link}')
            response = self.__page_request(page_link=link)

            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')

            content_container = self.__find_content_container(soup=soup)

            page_content = self.__scrape_page_content(
                content_container=content_container)

            self.catechism_page_content_splitter.split(
                elements=page_content)

            logger.info(
                f'{self.catechism_page_content_splitter.n_splitted_paragraphs} parágrafos do Catecismo foram extraídos e estruturados com sucesso! {len(self.catechism_page_content_splitter.payloads_list)} parágrafos ao total.')

        logger.info(
            "Raspagem dos parágrafos do catecismo da Igreja Católica concluída com sucesso!")
        return self.catechism_page_content_splitter.payloads_list

    def __scrape_main_page_links(self) -> List[str]:
        logger.info(
            "Raspando os links da página principal do site do catecismo da Igreja Católica...")
        response = self.__page_request(page_link=self.main_page)

        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        # Lista para armazenar os links de outras páginas, contidas e disponíveis na página principal.
        links = [a_tag.get('href')
                 for a_tag in soup.find_all('a', href=True) if isinstance(a_tag, Tag)]

        # Lista com paginas únicas, excluindo páginas intermediárias.
        valids_links = [link for link in links if isinstance(link, str) and
                        link.startswith('p') and ("#" not in link)]
        unique_links = list(dict.fromkeys(valids_links))

        return unique_links

    def __page_request(self, page_link: str) -> requests.Response:
        try:
            response = requests.get(self.main_url + page_link, timeout=10)
            return response
        except Exception as exception:
            logger.exception(
                f"Exceção ao enviar requisição para {self.main_url + page_link}: {exception}")
            raise

    @classmethod
    def __find_content_container(cls, soup: BeautifulSoup) -> Tag:
        table_tags = soup.find_all("table")

        if len(table_tags) < 2:
            raise NotImplementedError(
                "Quantidade de table Tags (<table>) insuficientes. No momento em que a aplicação foi desenvolvida, todo o conteúdo da página estava contido dentro da segunda Tag <table>.")

        table_tag = table_tags[1]
        if not isinstance(table_tag, Tag):
            raise TypeError("A table_tag deveria ser do tipo Tag.")

        tds_tags = table_tag.find_all("td")
        if len(tds_tags) < 2:
            raise NotImplementedError(
                "Quantidade de td Tags (<td>) insuficientes. No momento em que a aplicação foi desenvolvida, todo o conteúdo da página estava contido dentro da segunda Tag <td>.")

        content_container_tag = tds_tags[1]
        if not isinstance(content_container_tag, Tag):
            raise TypeError("O content_container_tag deveria ser do tipo Tag.")

        if len(content_container_tag.find_all("p")) == 0 and len(content_container_tag.find_all("font")) == 0:
            raise NotImplementedError(
                "p Tags (<p>) e font Tags (<font>) não existem. No momento em que a aplicação foi desenvolvida, todo o conteúdo da página estava contido dentro de Tags <p> ou Tags <font>.")

        return content_container_tag

    def __flush_the_buffer(self) -> None:
        if self.__buffer:
            buffer = [element.strip() for element in self.__buffer]

            joined = " ".join(buffer).strip()
            if joined:
                self.__page_content.append(joined)

            self.__buffer.clear()

    def __collect_txt_in_page_element(self, page_element: PageElement) -> None:
        # textos "soltos" (fora de <p>) -> acumulam no buffer
        if isinstance(page_element, NavigableString):
            txt = page_element.strip()
            if txt:
                self.__buffer.append(txt)
            return None

        # elementos de página que não são do tipo Tag, é ignorado
        if not isinstance(page_element, Tag):
            return None

        # Tags de tipo específicos, são ignorado
        if page_element.name in ("script", "style"):
            return None

        # se for <p>, fecha bloco anterior e adiciona parágrafo
        if page_element.name == "p":
            txt = page_element.get_text(" ", strip=True)

            if txt in ['A CELEBRAÇÃO DO MISTÉRIO CRISTÃO', 'A VIDA EM CRISTO']:
                self.__page_content.append(txt)
                return None

            self.__flush_the_buffer()

            if txt:
                self.__page_content.append(txt)
                return None  # não percorre filhos do <p>; já coletou o texto

        # para QUALQUER outra Tag (ex.: blockquote, div, td, etc.), desce recursivamente
        for child in page_element.children:
            self.__collect_txt_in_page_element(page_element=child)

    def __scrape_page_content(self, content_container: Tag) -> List[str]:
        self.__page_content: List[str] = []
        self.__buffer: List[str] = []  # acumula nós consecutivos fora de <p>

        # percorre apenas os filhos diretos do contêiner
        for child in content_container:
            self.__collect_txt_in_page_element(page_element=child)

        # fim do container: fecha último bloco fora de <p>
        self.__flush_the_buffer()

        return self.__page_content
