import re
from typing import List, Dict, Any


class CatechismPageContentSplitter:
    def __init__(self):
        self.buffer_paragraph = ""
        self.buffer_metadata = dict()

    def split(self, elements: List[str]) -> List[Dict]:
        current_part = "INTRODUÇÃO"
        current_section = ""
        current_chapter = ""
        current_article = ""
        current_internal_section = ""
        current_subsection = ""
        payloads_list = []
        paragraph_id = 0

        i = 0
        n_elements = len(elements)

        while i < n_elements:
            text = elements[i]
            cleaned_text = self.__clean_text(text)
            if not cleaned_text or cleaned_text in ['Resumindo:']:
                i += 1
                continue

            if self.__is_referencies(cleaned_text, paragraph_id=paragraph_id):
                # Último parágrafo no final da lista
                payloads_list = self.__append_to_payloads_list(
                    payloads_list=payloads_list)
                break

            if self.__is_part(cleaned_text):
                name_part = self.__clean_text(elements[i + 1])
                current_part = cleaned_text
                if cleaned_text != 'INTRODUÇÃO' and name_part:
                    current_part = cleaned_text + ' ' + elements[i + 1]
                    i += 1
                current_section = ""
                current_chapter = ""
                current_article = ""
                current_internal_section = ""
                current_subsection = ""
                payloads_list = self.__append_to_payloads_list(
                    payloads_list=payloads_list)
                i += 1
                continue

            if self.__is_section(cleaned_text):
                name_section = self.__clean_text(elements[i + 1])
                current_section = cleaned_text
                if cleaned_text != 'PRÓLOGO' and name_section:
                    current_section = current_section + ' - ' + name_section
                    i += 1
                current_chapter = ""
                current_article = ""
                current_internal_section = ""
                current_subsection = ""
                payloads_list = self.__append_to_payloads_list(
                    payloads_list=payloads_list)
                i += 1
                continue

            if self.__is_chapter(cleaned_text):
                name_chapter = self.__clean_text(elements[i + 1])
                current_chapter = cleaned_text
                if name_chapter:
                    current_chapter = current_chapter + ' - ' + name_chapter
                    i += 1
                current_article = ""
                current_internal_section = ""
                current_subsection = ""
                payloads_list = self.__append_to_payloads_list(
                    payloads_list=payloads_list)
                i += 1
                continue

            if self.__is_article(cleaned_text):
                name_article = self.__clean_text(elements[i + 1])
                current_article = cleaned_text
                if name_article:
                    current_article = current_article + ' - ' + name_article
                    i += 1
                current_internal_section = ""
                current_subsection = ""
                payloads_list = self.__append_to_payloads_list(
                    payloads_list=payloads_list)
                i += 1
                continue

            if self.__is_internal_section(cleaned_text):
                current_internal_section = cleaned_text
                current_subsection = ""
                payloads_list = self.__append_to_payloads_list(
                    payloads_list=payloads_list)
                i += 1
                continue

            if self.__is_subsection(cleaned_text):
                current_subsection = cleaned_text
                payloads_list = self.__append_to_payloads_list(
                    payloads_list=payloads_list)
                i += 1
                continue

            if self.__is_paragraph(cleaned_text, paragraph_id):
                payloads_list = self.__append_to_payloads_list(
                    payloads_list=payloads_list)

                self.buffer_paragraph = cleaned_text
                self.buffer_metadata = {
                    "PARTE": current_part,
                    "SECÇAO": current_section,
                    "CAPITULO": current_chapter,
                    "ARTIGO": current_article,
                    "SECÇAO_INTERNA": current_internal_section,
                    "SUBSEÇAO_TEMATICA": current_subsection
                }

                splited_text = self.__split_topic_text(text=cleaned_text)
                paragraph_id = int(splited_text[0].strip())
                i += 1
                continue

            if self.buffer_paragraph:
                self.buffer_paragraph += ' ' + cleaned_text
                i += 1
                continue

            self.__restart_buffers()
            i += 1

        return payloads_list

    @classmethod
    def __clean_text(cls, text: str) -> str:
        return text.replace('\xa0', ' ').strip()

    @classmethod
    def __is_part(cls, text: str) -> bool:
        return bool(re.match(r'^(?:INTRODUÇÃO|(?:PRIMEIRA|SEGUNDA|TERCEIRA|QUARTA)\s+PARTE)$', text.strip(), re.IGNORECASE))

    @classmethod
    def __is_section(cls, text: str) -> bool:
        return bool(re.match(r'^(?:PRÓLOGO|(?:PRIMEIRA|SEGUNDA)\s+SECÇÃO)$', text.strip(), re.IGNORECASE))

    @classmethod
    def __is_chapter(cls, text: str) -> bool:
        return bool(re.match(r'^CAP[IÍ]TULO\s+(PRIMEIRO|SEGUNDO|TERCEIRO|QUARTO)$', text.strip(), re.IGNORECASE))

    @classmethod
    def __is_article(cls, text: str) -> bool:
        return bool(re.match(r'^ARTIGO \d+', text.strip(), re.IGNORECASE))

    @classmethod
    def __is_internal_section(cls, text: str) -> bool:
        return bool(re.match(r'^[IVXLCDM]+\.\s', text.strip()))

    @classmethod
    def __is_subsection(cls, text: str) -> bool:
        return text.strip().isupper()

    @classmethod
    def __is_topic(cls, text: str) -> bool:
        return bool(re.match(r'^\d+(?:\s\.|\.\s|\s|\.)', text.strip()))

    @classmethod
    def __split_topic_text(cls, text: str) -> List:
        if (re.match(r'^(\d+\.)', text)):
            splited_text = text.split('.', 1)
            return splited_text
        if (re.match(r'^\d+\s', text)):
            splited_text = text.split(' ', 1)
            return splited_text

        raise ValueError(f'Não foi possível dividir o texto do tópico: {text}')

    def __is_paragraph(self, text: str, paragraph_id: int) -> bool:
        if not self.__is_topic(text=text):
            return False

        splited_text = self.__split_topic_text(text=text)

        text_id = int(splited_text[0].strip())

        if text_id < paragraph_id and text_id == 1495:
            text_id = 1498

        if text_id < paragraph_id and text_id == 2117:
            text_id = 2217

        if text_id < paragraph_id and text_id == 1439:
            text_id = 2439

        return paragraph_id is not None and text_id > paragraph_id

    def __is_referencies(self, text: str, paragraph_id: int) -> bool:
        if text in ['Notas', 'CREDO', 'OS DEZ MANDAMENTOS']:
            return True
        if not self.__is_topic(text):
            return False

        splited_text = self.__split_topic_text(text=text)

        text_id = int(splited_text[0])
        pattern = r'^(?:[IVXLCDM]+)\b|(?:Cf)|(?:CatRom)|(?:Santo)|(?:São)'

        return bool(paragraph_id is not None and text_id < paragraph_id and re.match(pattern, splited_text[1].strip()))

    def __restart_buffers(self) -> None:
        self.buffer_paragraph = ""
        self.buffer_metadata = dict()

    def __append_to_payloads_list(self, payloads_list: List) -> List[Dict[str, Any]]:
        if self.buffer_paragraph and self.buffer_metadata:
            payload = {
                'text': self.buffer_paragraph,
                'metadata': self.buffer_metadata
            }

            payloads_list.append(payload)
        self.__restart_buffers()

        return payloads_list
