# pylint: disable=missing-docstring

import re
from os import environ as env
from warnings import warn

from fastapi import APIRouter, FastAPI


class BaseURL(FastAPI):
    '''
    Inherited from FastAPI class ReDoc have a predefined router to documentation from redoc library.

    Classic OpenAPI documentation can be activated through environment variable $SIMPLE_DOC.
    This variable is a higher priority that the class argument. But if $SIMPLE_DOC will set a similar
    redoc argument then the variable will be ignored.

    Args:

        title: Name of API.

        description: Short description of API. It would be used markdown.

        version: Version of API service (container/server/etc). It's not an API specification version.

        contact: Support team contacts. Have to has name and email in dictionary format.

        base_url: Path prefix.

        debug: Debugging flag.

        **kw: Additional arguments from FastAPI class.
    '''

    def __init__(
        self,
        title: str,
        description: str,
        version: str,
        contact: dict,
        base_url: str | None = None,
        debug: bool = False,
        **kw
    ):

        debug = bool(env.get('DEBUG_API', debug))  # env vars have priority

        pattern = re.compile(r'^\/[\-a-zA-Z0-9\(\)\_\+\.\#\?\&\=]+(\/[\-a-zA-Z0-9\(\)\_\+\.\#\?\&\=]+)*$')
        path = str(base_url or env.get('BASE_URL', ''))

        if not re.match(pattern, path) and path != '':
            warn('Wrong BASE_URL value! $BASE_URL will used as "" value.')
            path = ''

        redoc_url = path if path != '' else '/'
        openapi_url = f'{path}/openapi.json' if path != '' else '/openapi.json'

        super().__init__(
            title=title,
            description=description,
            version=version,
            contact=contact,
            redoc_url=redoc_url,
            openapi_url=openapi_url,
            debug=debug,
            **kw
        )

        self._base_router = APIRouter(prefix=path)

        self.include_router(self._base_router)

    def add2base(self, router: APIRouter):
        '''
        Added router behind `BASE_URL` path.

        Args:
            router: Instance of defined router.
        '''

        self._base_router.include_router(router)
        self.include_router(self._base_router)
