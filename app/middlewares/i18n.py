import gettext
from gettext import NullTranslations

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import os
from babel.support import Translations

LOCALES_DIR = os.path.join(os.path.dirname(__file__), "../../locales")
DEFAULT_LOCALE = "pt_BR"  # Default language
SUPPORTED_LOCALES = ["pt_BR", "en"]  # Supported languages


def get_locale(request: Request) -> str:
    """
    Detects the locale from the request headers (Accept-Language) or a query parameter.
    Falls back to the default locale if none is found or supported.
    """
    # Check for a query parameter (e.g., ?lang=pr-br)
    lang_query = request.query_params.get("lang")
    if lang_query and lang_query in SUPPORTED_LOCALES:
        return lang_query

    # Check Accept-Language header
    accept_language = request.headers.get("accept-language")
    if accept_language:
        for language in accept_language.split(","):
            lang_code = language.split(";")[0].strip()
            if lang_code in SUPPORTED_LOCALES:
                return lang_code

    return DEFAULT_LOCALE


def get_translation(locale: str) -> gettext.GNUTranslations:
    """
    Loads the appropriate translation based on the locale.
    """
    try:
        return gettext.translation(
            "messages",
            LOCALES_DIR,
            [locale],
        )
    except FileNotFoundError:
        return gettext.translation(
            "messages",
            LOCALES_DIR,
            [DEFAULT_LOCALE],
        )


class I18nMiddleware(BaseHTTPMiddleware):
    """
    Middleware to set the translation object in the request state.
    """

    async def dispatch(self, request: Request, call_next):
        locale = get_locale(request)
        translation = get_translation(locale)

        request.state.locale = locale
        request.state.translate = translation.gettext

        response = await call_next(request)
        return response
