import re
from typing import Union, List
from configparser import  ConfigParser


_STRING_VALUE_REGEX = r'\s*((\'[^\']+\')|("[^"]+"))\s*'


class _FlatTranslationCall:
    REGEX = rf'\({_STRING_VALUE_REGEX}\)'
    type = 'flat'

    def __init__(self, key: str):
        self.key = self._remove_citations(key)

    @classmethod
    def extract_matches(cls, text: str, context_v_name: str = '_'):
        FLAT_PATTERN = context_v_name + cls.REGEX
        flat_pattern = re.compile(FLAT_PATTERN)
        matches_as_obj = []
        for match in flat_pattern.finditer(text):
            matches_as_obj.append(cls.from_match(match))
        return matches_as_obj

    @classmethod
    def from_match(cls, match: re.Match):
        return cls(match.group(1))

    @staticmethod
    def _remove_citations(string: str):
        return string[1:-1]

    def __repr__(self):
        return f'<{self.type.upper()}TranslationCall key: {self.key}>'


class _GroupedTranslationCall(_FlatTranslationCall):
    REGEX = rf'\({_STRING_VALUE_REGEX},{_STRING_VALUE_REGEX}\)'
    type = 'grouped'

    def __init__(self, key: str, group: str):
        super().__init__(key)
        self.group = self._remove_citations(group)

    @classmethod
    def from_match(cls, match: re.Match):
        return cls(match.group(1), match.group(4))


class _ExtendedTranslationCall(_GroupedTranslationCall):
    REGEX = rf'\({_STRING_VALUE_REGEX},{_STRING_VALUE_REGEX},([^(]+)\)'
    type = 'extended'

    def __init__(self, key: str, group: str, other_args: str):
        super().__init__(key, group)
        self.other_args = other_args

    @classmethod
    def from_match(cls, match: re.Match):
        return cls(match.group(1), match.group(4), match.group(7))


def _extract_translations(text: str, context_v_name: str = '_'):
    flat = _FlatTranslationCall.extract_matches(text, context_v_name)
    grouped = _GroupedTranslationCall.extract_matches(text, context_v_name)
    extended = _ExtendedTranslationCall.extract_matches(text, context_v_name)
    return flat + grouped + extended  # list


def _create_lang_file(symbol: str, name: str, translations: List[Union[_FlatTranslationCall, _GroupedTranslationCall, _ExtendedTranslationCall]]):
    """
    this method creates a **language file** with sections and keys also default values, processed from **$translations**;

    language file is an INI file **.ini** will be added as file extension, the name of the file is **$symbol**;

    if the file already exists, the process will abort with **FileExistsError**

    :param symbol: Unique language presentation code, (will be used to gain access to, so it is important)
    :param name: Human readable name of language to indentify on the web page
    :param translations: the translation used in a template file, get them with **extract_translations()**
    :return: created file name
    """
    # > set universal constants
    DEFAULT_SECTION = 'default'
    LANG = 'lang'
    FULL_NAME = 'full_name'
    # > create ini parser
    parser = ConfigParser()
    # > setting language default values
    parser.add_section(DEFAULT_SECTION)
    parser.set(DEFAULT_SECTION, LANG, symbol)
    parser.set(DEFAULT_SECTION, FULL_NAME, name)
    parser.set(DEFAULT_SECTION, 'date_format', '%%Y-%%m-%%d %%H:%%M:%%S')
    # > setting input translation keys with capitalized default values
    for trans in translations:  # - loop all translations
        try:
            # > if translation is not valid type
            if not isinstance(trans, (_FlatTranslationCall, _GroupedTranslationCall, _ExtendedTranslationCall)):
                raise TypeError(f'instance of type: {type(trans)} is not a valid translation.')
            # > flat ones in default section (group)
            if trans.type == 'flat':
                section_of_trans = DEFAULT_SECTION
            # > others on their section (group)
            else:
                section_of_trans = trans.group
            # > if the section doesn't exist create it
            if not parser.has_section(section_of_trans):
                parser.add_section(section_of_trans)
            # > add the key, and give it a default value = its name capitalized
            parser.set(section_of_trans, trans.key, trans.key.replace('_', ' ').title())
        except TypeError:
            pass
    # > saving file, using 'x' mode (if exists error will be raised)
    new_file_name = f'{symbol}.ini'
    with open(new_file_name, 'x') as file:
        parser.write(file, True)
        return new_file_name


def generate(source_template_file: str, lang_code: str, lang_name: str, context_name: str = '_'):
    """
    Generates translation file from html/jinja2 template

    :param source_template_file: the template file path
    :param lang_code: Unique language presentation code, (will be used to gain access to, so it is important)
    :param lang_name: Human readable name of language to indentify on the web page
    :param context_name: jinja2 context variable name used in the template, "_" by default
    :return: the name of generated file
    """
    with open(source_template_file, 'r') as source_file:
        extracted_translations = _extract_translations(source_file.read(), context_name)
        return _create_lang_file(lang_code, lang_name, extracted_translations)
