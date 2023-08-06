
import os
from datetime import datetime, tzinfo
from configparser import ConfigParser
from markupsafe import escape
from markdown import markdown


class MultiLanger:
    DEFAULT_SECTION = 'default'
    LANG = 'lang'
    LANG_FULL_NAME = 'lang_full_name'

    def __init__(self, lang_source_dir: str, def_lang='en', ext='.ini', auto_markdown=True):
        """
        This class creates a datastructure of all translations available, so you can switch the language easily,
        and get the correct translation.

        the translations are in Config files (ini files), each file for a language, all files in the same directory and has the same file extension (ex: .ini),
        every translation file must respect the following syntax:

        - has a section named $cls.DEFAULT_SECTION
        - has a key in that section named $cls.LANG
        - the value of $cls.LANG is the name of the translation (file name doesn't affect)

        by default the ext is '.ini', you can change that in argument $ext
        also the default language is 'en', you can change that also in $lang
        :param lang_source_dir: the source directory of all translation files
        :param def_lang: specify a default language, en by default
        :param ext: the extension of target files, .ini by default
        :param auto_markdown: to markdown translation results automatically
        """
        self._lang = def_lang.lower()
        self._groups = {}
        self._langs = []
        self._auto_markdown = auto_markdown
        self._load_from_dir(lang_source_dir, ext)

    @property
    def lang(self):
        return self._lang

    @property
    def auto_markdown(self):
        return self._auto_markdown

    def _load_from_file(self, file_name: str):
        """
        load data to ConfigParser
        extract the value of key $cls.LANG from section $cls.DEFAULT_SECTION
        loop all sections, add section to self.groups as key: <dict>
        loop the section values, add each value to previous key as $lang: the value
        :param file_name: target file
        :return:
        """
        parser = ConfigParser()
        parser.read(file_name)
        # try to get the default section ($DEFAULT_SECTION), if failed error and exit
        try:
            default_section = parser[self.DEFAULT_SECTION]
        except KeyError:
            raise KeyError(f'A translation file "{file_name}" must have the [{self.DEFAULT_SECTION}] Section!')
        else:
            # when $DEFAULT_SECTION section is there, try to get the value of $cls.LANG key, if can't error and exit
            try:
                lang = default_section[self.LANG]
            except KeyError:
                raise KeyError(f'A translation file must have a "lang" key in [{self.DEFAULT_SECTION}] Section!')
            else:
                lang = lang.lower()  # lowering the lang is important
                for section in parser.sections():
                    for key, value in parser[section].items():
                        section = section.lower()  # important
                        # > make sure to create the group as dict before trying to access it (if not been made in passed loops)
                        if self._groups.get(section, None) is None:  # this should return a dict object if $section exists
                            self._groups[section] = {}
                        # > also create the current key in the group if isn't exist
                        if self._groups[section].get(key, None) is None:
                            self._groups[section][key] = {}
                        # < now we made sure that the group is there, also the key, and we have the lang,
                        # > last thing to do is saving the translation value under the $lang language
                        self._groups[section][key][lang] = value
                # finally register this lang in self._langs
                self._langs.append(lang)

    def _load_from_dir(self, source: str, ext='.ini'):
        """
        get all files with $ext from $source directory
        loop them all passing each one to _load_from_file
        :param source: directory
        :param ext: files ext, default '.ini', you can leave it empty string ''
        :return:
        """
        for name in os.listdir(source):
            right_name = os.path.join(source, name)
            if os.path.isfile(right_name) and os.path.splitext(name)[1] == ext:
                self._load_from_file(right_name)

    def _get_translation(self, key: str, group_name: str = None, default: str = None):
        """
        return the translation value for the given key, in the selected language
        :param key: the key of needed translation
        :param group_name: if the key isn't in the default group, specify where it is
        :param default: when no translation key was found, return this instead
        :return:
        """
        # all translations have a default group
        group_name = self.DEFAULT_SECTION if group_name is None else group_name
        # try to get the group by name if exists, if not error and exit or return default
        try:
            group: dict = self._groups[group_name.lower()]
        except KeyError:
            if default is not None:
                return default
            raise KeyError(f'There is No Group or Section named "{group_name}"! if you modified your lag-files recently restart your server!')
        else:
            # now we have the group dictionary,
            # we can go with getting the translations from it, if no one exits error and exit or return default
            try:
                translations: dict = group[key.lower()]
            except KeyError:
                if default is not None:
                    return default
                raise NameError(f'There is No Item named "{key}" in {group_name} group! if you modified your lag-files recently restart your server!')
            else:
                # now we have the translations of the target key, the only thing left is returning it in the selected language
                ln = self._lang  # the selected language
                if ln in translations.keys():  # if it exists
                    value = translations[ln]  # return the translation
                    return value
                else:  # if the language doesn't exist, return the default value if specified or choose the first language's
                    if default is not None:
                        return default
                    ln = list(translations.keys())[0]
                    value = translations[ln]
                    return value

    def __repr__(self):
        return f'<MultiLanger {self._lang} / {len(self._langs)}>'

    def __call__(self, key: str, group: str = None, default: str = None, markdowned=None):
        result = self._get_translation(key, group, default)
        # > when the markdown is selected, do
        if self._auto_markdown or markdowned:
            return markdown(escape(result))[3:-4]  # [3:-4] to escape the <p> ... </p>
        else:
            return result

    def change_lang(self, new_lang: str):
        new_lang = new_lang.lower()
        if new_lang in self._langs:
            self._lang = new_lang
        else:
            raise ValueError(f'This language is not available "{new_lang}".')

    def available_langs(self, with_descriptions=True):
        """
        returns all available languages, with or without descriptions
        :param with_descriptions: if you don't want descriptions, make this False
        :return: list of langs or tuple of (lang, description)
        """
        if not with_descriptions:
            return self._langs
        else:
            # > loop all self._langs, and for each, do get $self.LANG_FULL_NAME from $DEFAULT_SECTION group,
            # > if $self.LANG_FULL_NAME doesn't exist for current lang, return empty dict, so you will get None from it eventually.
            return [(lng, self._groups[self.DEFAULT_SECTION].get(self.LANG_FULL_NAME, {}).get(lng)) for lng in self._langs]

    @property
    def langs_count(self):
        return len(self._langs)

    def datetime_now_formatted(self, tz: tzinfo = None):
        """
        returns the datetime as string in the selected language's format
        :param tz: the time zone as object <datetime.tzinfo>
        :return: str
        """
        frmt = self.date_time_format
        return datetime.now(tz).strftime(frmt)

    @property
    def date_time_format(self):
        lng = self._lang  # get selected lang
        # > return an empty dict when no 'date_format' key is available,to return None afterwards
        frmt = self._groups[self.DEFAULT_SECTION].get('date_format', {}).get(lng)
        # > when frmt is None, means there is no target key on file, or the selected lang has no source file
        if frmt is None:
            frmt = '%Y-%m-%d %H:%M:%S'
        return frmt

    def set_auto_markdown(self, value: bool):
        self._auto_markdown = bool(value)

    # > TODO: temporary method, remove on production
    def prettify(self, p=False):
        import json
        r = json.dumps(self._groups, indent=4, ensure_ascii=False)
        if p:
            print(r)
        return r
