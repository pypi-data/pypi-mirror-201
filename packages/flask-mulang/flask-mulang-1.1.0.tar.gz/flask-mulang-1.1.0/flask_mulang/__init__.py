
import os
from .flask_multilananger import MultiLanger as _MultiLanger
from flask import Flask as _Flask, g as _g, request as _request, flash, make_response, redirect


class MuLang(_MultiLanger):
    COOKIE_KEY = "lang"
    CONTEXT_VARIABLE = '_'
    DEFAULT_LANG = "en"

    def __init__(self, app: _Flask = None, languages_folder: str = None, def_lang=DEFAULT_LANG, ext='.ini', auto_markdown=True):
        """
        this class doesn't initialize the instance if the $app argument is not a valid flask application, instead,
        it holds all the arguments in self._kwargs, so you can later do call self.init_app(app: Flask) with passing the app,
        so then it initializes
        :param app: valid Flask app
        :param languages_folder: the source directory of lang files
        :param def_lang: default lang
        :param ext: extension of lang files
        :param auto_markdown: to auto markdown values, you can choose for each value later
        """
        # > default to false now
        self._initialized = False
        # > hold the app
        self.app = app
        # > hold all arguments to use now or later
        self._kwargs = dict(languages_folder=languages_folder, def_lang=def_lang, ext=ext, auto_markdown=auto_markdown)
        # > check if the app is a valid Flask instance
        if isinstance(self.app, _Flask):
            # > initialize the app, by calling the initializer method
            self.init_app(self.app, **self._kwargs)

    def init_app(self, app: _Flask = None, languages_folder: str = None, def_lang=DEFAULT_LANG, ext='.ini', auto_markdown=True):
        """
        call this method to initialize the instance
        :param app: valid Flask app
        :param languages_folder: the source directory of lang files
        :param def_lang: default lang
        :param ext: extension of lang files
        :param auto_markdown: to auto markdown values, you can choose for each value later
        :return: None
        """
        self.DEFAULT_LANG = def_lang if def_lang else self.DEFAULT_LANG
        # > check if already initialized before doing it
        if self._initialized:
            raise Exception('Cannot have Mulang() instance initialized more than once.')
        # > check if the $app argument is valid Flask
        if isinstance(app, _Flask):
            # > get the languages_folder to be within the app root path
            root_lang_source_dir = os.path.join(app.root_path, languages_folder)
            # > initialize MultiLanger with given arguments
            _MultiLanger.__init__(self, root_lang_source_dir, def_lang, ext, auto_markdown)
            # > set self.app to be app, if not already!
            self.app = app

        # > register instance to jinja and g
        @app.context_processor
        def inject_user():
            """
            the name $self.CONTEXT_VARIABLE as jinja2 variable and also as flask.g attribute, pointing to this instance (self).
            """
            setattr(_g, self.CONTEXT_VARIABLE, self)
            return {
                self.CONTEXT_VARIABLE: self
            }

        # > this is the language handler
        @app.before_request
        def language_handler():
            """
            this method gets the cookie value of current language, and applies it to current session
            :return:
            """
            # > try to get cookie from request
            lang = _request.cookies.get(self.COOKIE_KEY, None)
            # > check if the cookie exists
            if lang is not None:
                # - exists
                try:
                    # > try to change language to current one
                    self.change_lang(lang)
                    # < if any error is happened, means the lang is not available
                except ValueError:
                    # - when error
                    # > fallback to default language
                    self.change_lang(self.DEFAULT_LANG)
                    # > flash a danger message
                    flash(f'Invalid Language: {lang}', 'danger')
                    # > redirect to the requested URL with setting lang to default one
                    resp = make_response(redirect(_request.path))  # - create response
                    resp.set_cookie(self.COOKIE_KEY, self.DEFAULT_LANG)  # - edit response cookies, add lang=DEFAULT_LANG
                    return resp
            else:
                # - when no cookie was found in request
                # > set session lang to default
                self.change_lang(self.DEFAULT_LANG)
                # - don't set any cookie of user's response

    def set_user_language(self, lang: str, redirect_to='/'):
        """
        This method sets the language in the user cookie to $lang and return a redirection response $redirect_to
        :param lang: the lang name 'en', 'ar' or 'ru'
        :param redirect_to: any valid route
        :return:
        """
        resp = make_response(redirect(redirect_to))
        resp.set_cookie(self.COOKIE_KEY, lang)
        return resp

    @property
    def dir(self):
        """
        this property loads the dir key from default section (group) to present the HTML page direction, if there is no dir key, will return 'auto'
        :return: str
        """
        return self('dir', default='auto', markdowned=False)

    def __repr__(self):
        return f"<MuLang lang: {self.lang}>"
