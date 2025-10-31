import re
from typing import List
from src.validators.models.Payload import Payload


class CatechismPageContentSplitter:
    def __init__(self) -> None:
        self.payloads_list: List[Payload] = []

    def split(self, elements: List[str]) -> None:
        current_part = ""
        current_section = ""
        current_chapter = ""
        current_article = ""
        current_paragraphs_group = ""
        current_internal_section = ""
        current_subsection = ""

        self.n_splitted_paragraphs = 0

        self.paragraph_id = 0

        self.__buffer_paragraph = ""
        self.__buffer_localization = {}

        self.__incorrect_paragraphs_number_dict = {1495: 1498,
                                                   2117: 2217,
                                                   1439: 2439}

        i = 0
        n_elements = len(elements)

        while i < n_elements:
            text = elements[i]
            cleaned_text = self.__clean_text(text)

            if not cleaned_text:
                i += 1
                continue

            if self.__start_referencies_section(cleaned_text):
                self.__create_payloads()
                break

            if self.__is_part(cleaned_text):
                current_part = cleaned_text

                name_part = self.__clean_text(elements[i + 1])
                if name_part and current_part != 'PRÓLOGO':
                    current_part = cleaned_text + ' - ' + name_part
                    i += 1

                current_section = ""
                current_chapter = ""
                current_article = ""
                current_paragraphs_group = ""
                current_internal_section = ""
                current_subsection = ""

                self.__create_payloads()

                i += 1
                continue

            if self.__is_section(cleaned_text):
                current_section = cleaned_text

                name_section = self.__clean_text(elements[i + 1])
                if name_section and current_section != 'INTRODUÇÃO':
                    current_section = current_section + ' - ' + name_section
                    i += 1

                current_chapter = ""
                current_article = ""
                current_paragraphs_group = ""
                current_internal_section = ""
                current_subsection = ""

                self.__create_payloads()

                i += 1
                continue

            if self.__is_chapter(cleaned_text):
                current_chapter = cleaned_text

                name_chapter = self.__clean_text(elements[i + 1])
                if name_chapter:
                    current_chapter = current_chapter + ' - ' + name_chapter
                    i += 1

                current_article = ""
                current_paragraphs_group = ""
                current_internal_section = ""
                current_subsection = ""

                self.__create_payloads()

                i += 1
                continue

            if self.__is_article(cleaned_text):
                current_article = cleaned_text

                name_article = self.__clean_text(elements[i + 1])
                if name_article:
                    current_article = current_article + ' - ' + name_article
                    i += 1

                current_paragraphs_group = ""
                current_internal_section = ""
                current_subsection = ""

                self.__create_payloads()

                i += 1
                continue

            if self.__is_paragraphs_group(cleaned_text):
                current_paragraphs_group = cleaned_text

                name_paragraphs_group = self.__clean_text(elements[i + 1])
                if name_paragraphs_group:
                    current_paragraphs_group = current_paragraphs_group + ' - ' + name_paragraphs_group
                    i += 1

                current_internal_section = ""
                current_subsection = ""

                self.__create_payloads()

                i += 1
                continue

            if self.__is_internal_section(cleaned_text):
                current_internal_section = cleaned_text

                current_subsection = ""

                self.__create_payloads()

                i += 1
                continue

            if self.__is_subsection(cleaned_text):
                current_subsection = cleaned_text

                self.__create_payloads()

                i += 1
                continue

            if self.__is_paragraph(cleaned_text):
                self.__buffer_localization_is_not_empty()
                self.__create_payloads()

                self.__buffer_paragraph = cleaned_text
                self.__buffer_localization = {
                    "PART": current_part,
                    "SECTION": current_section,
                    "CHAPTER": current_chapter,
                    "ARTICLE": current_article,
                    "PARAGRAPHS_GROUP": current_paragraphs_group,
                    "INTERNAL_SECTION": current_internal_section,
                    "THEMATIC_SUBSECTION": current_subsection
                }

                splited_text = self.__split_topic_text(text=cleaned_text)
                self.paragraph_id = int(splited_text[0].strip())

                if self.paragraph_id == 750:
                    print("")

                self.n_splitted_paragraphs += 1

                i += 1
                continue

            if self.__buffer_paragraph:
                self.__buffer_paragraph += ' ' + cleaned_text
                i += 1
                continue

            self.__restart_buffers()
            i += 1

    @classmethod
    def __clean_text(cls, text: str) -> str:
        return text.replace('\xa0', ' ').strip()

    @classmethod
    def __is_part(cls, text: str) -> bool:
        return bool(re.match(r'^(?:PRÓLOGO|(?:PRIMEIRA|SEGUNDA|TERCEIRA|QUARTA)\s+PARTE)$', text.strip(), re.IGNORECASE))

    @classmethod
    def __is_section(cls, text: str) -> bool:
        return bool(re.match(r'^(?:INTRODUÇÃO|(?:PRIMEIRA|SEGUNDA)\s+SECÇÃO)$', text.strip(), re.IGNORECASE))

    @classmethod
    def __is_chapter(cls, text: str) -> bool:
        return bool(re.match(r'^CAP[IÍ]TULO\s+(PRIMEIRO|SEGUNDO|TERCEIRO|QUARTO)$', text.strip(), re.IGNORECASE))

    @classmethod
    def __is_article(cls, text: str) -> bool:
        return bool(re.match(r'^ARTIGO \d+', text.strip(), re.IGNORECASE) or text == "<<AMEN>>")

    @classmethod
    def __is_paragraphs_group(cls, text: str) -> bool:
        return bool(re.match(r'^PARÁGRAFO \d+', text.strip(), re.IGNORECASE))

    @classmethod
    def __is_internal_section(cls, text: str) -> bool:
        return bool(re.match(r'^[IVXLCDM]+\.\s', text.strip()) or text == "Resumindo:")

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

    def __is_paragraph(self, text: str) -> bool:
        if not self.__is_topic(text=text):
            return False

        splited_text = self.__split_topic_text(text=text)

        text_id = int(splited_text[0].strip())

        if text_id < self.paragraph_id and text_id in self.__incorrect_paragraphs_number_dict:
            text_id = self.__incorrect_paragraphs_number_dict[text_id]

        return bool(self.paragraph_id is not None and text_id > self.paragraph_id)

    def __start_referencies_section(self, text: str) -> bool:
        if text in ['Notas', 'CREDO', 'OS DEZ MANDAMENTOS']:
            return True
        if not self.__is_topic(text):
            return False

        splited_text = self.__split_topic_text(text=text)

        text_id = int(splited_text[0])
        pattern = r'^(?:[IVXLCDM]+)\b|(?:Cf)|(?:CatRom)|(?:Santo)|(?:São)'

        return bool(self.paragraph_id is not None and text_id < self.paragraph_id and re.match(pattern, splited_text[1].strip()))

    def __restart_buffers(self) -> None:
        self.__buffer_paragraph = ""
        self.__buffer_localization = dict()

    def __create_payloads(self) -> None:
        if self.__buffer_paragraph and self.__buffer_localization:
            payload = Payload(
                text=self.__buffer_paragraph,
                localization=self.__buffer_localization
            )

            self.payloads_list.append(payload)
        self.__restart_buffers()

    def __buffer_localization_is_not_empty(self) -> None:
        if self.__buffer_localization != {} and all(valor == "" for valor in self.__buffer_localization.values()):
            raise ValueError(
                f'Os valores de localização do parágrafo buffer {self.paragraph_id} estão vazios.')
