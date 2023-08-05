# pylint: disable=missing-docstring

from __future__ import annotations

import re
from enum import Enum, unique
from importlib import import_module as im
from os import environ as env
from os import path
from pathlib import Path

import dash_bootstrap_components as dbc
import flask
import requests
from asgiref.wsgi import WsgiToAsgi
from dash import Dash, dcc, html, page_container  # type: ignore
from hypercorn.middleware import AsyncioWSGIMiddleware
from jupyter_dash import JupyterDash

base_url: str = env.get('BASE_URL', None) or env.get('DASH_URL_BASE_PATHNAME', '/')
static_path = path.join(path.dirname(path.abspath(__file__)), 'static')


@unique
class Themes(Enum):
    CERULEAN = 'CERULEAN'
    COSMO = 'COSMO'
    CYBORG = 'CYBORG'
    DARKLY = 'DARKLY'
    FLATLY = 'FLATLY'
    JOURNAL = 'JOURNAL'
    LITERA = 'LITERA'
    LUMEN = 'LUMEN'
    LUX = 'LUX'
    MATERIA = 'MATERIA'
    MINTY = 'MINTY'
    MORPH = 'MORPH'
    PULSE = 'PULSE'
    QUARTZ = 'QUARTZ'
    SANDSTONE = 'SANDSTONE'
    SIMPLEX = 'SIMPLEX'
    SKETCHY = 'SKETCHY'
    SLATE = 'SLATE'
    SOLAR = 'SOLAR'
    SPACELAB = 'SPACELAB'
    SUPERHERO = 'SUPERHERO'
    UNITED = 'UNITED'
    VAPOR = 'VAPOR'
    YETI = 'YETI'
    ZEPHYR = 'ZEPHYR'


class Bootstrapped(Dash):
    '''
    Prepared a plotly dash class which includes:
    - uploaded a Bootstrap theme;
    - uploaded Google fonts: Comfortaa, Montserrat, Roboto and Material & Awesome Icons;
    - setted up responsive metatag.

    Additionally the BootstrappedDash class processed environment variables:
    - BASE_URL: leading part of the path;
    - FAVICON_URL:
    '''

    def __init__(
        self,
        name: str,
        default_theme: Themes = Themes.COSMO,
        store_local: bool = False,
        store_session: bool = False,
        store_memory: bool = False,
        **kw
    ):

        assert re.match(r'^(\/[0-9a-z_\-\.\/]+)*\/$', base_url), f'base_url "{base_url}" isn\'t correct'

        bootstrap_theme = getattr(im('dash_bootstrap_components.themes'), default_theme.value, None)

        self._name = name

        external_scripts = []
        self._external_scripts = getattr(self, '_external_scripts', [])
        self._external_scripts.extend(external_scripts)
        if 'external_scripts' in kw and isinstance(kw['external_scripts'], list):
            self._external_scripts.extend(kw['external_scripts'])
            del kw['external_scripts']

        # An adding corporate styles
        external_stylesheets = [
            {
                'href': 'https://fonts.googleapis.com',
                'rel': 'preconnect'
            },
            {
                'href': 'https://fonts.gstatic.com',
                'rel': 'preconnect',
                'crossorigin': 'crossorigin'
            },
            {
                'href': ''.join([
                    'https://fonts.googleapis.com/css2?',
                    'family=Comfortaa:wght@300;400;600;700&',
                    'family=Montserrat:ital,wght@0,100;0,200;0,400;0,600;1,100;1,200;1,400;1,600&',
                    'family=Roboto:ital,wght@0,100;0,300;0,500;1,100;1,300;1,500&',
                    'display=swap'
                ]),
                'rel': 'stylesheet'
            },
            {
                'href': 'https://fonts.googleapis.com/icon?family=Material+Icons',
                'rel': 'stylesheet'
            },
            {
                'href': 'https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200',  # pylint: disable=line-too-long
                'rel': 'stylesheet'
            }
        ]
        self._external_stylesheets = getattr(self, '_external_stylesheets', [])
        self._external_stylesheets.extend(external_stylesheets)
        self._external_stylesheets.extend([dbc.icons.FONT_AWESOME, dbc.icons.BOOTSTRAP])
        if bootstrap_theme:
            self._external_stylesheets.append(bootstrap_theme)
        if 'external_stylesheets' in kw and isinstance(kw['external_stylesheets'], list):
            self._external_stylesheets.extend(kw['external_stylesheets'])
            del kw['external_stylesheets']

        super().__init__(
            name=re.sub(r'[ ]+', '', name.title()),
            title=name.upper(),
            compress=True,
            use_pages=True,
            url_base_pathname=base_url,
            external_stylesheets=self._external_stylesheets,
            external_scripts=self._external_scripts,
            **kw
        )

        #  Make layout
        self._page = html.Section(
            page_container,
            id='page'
        )

        children = []
        if store_local:
            children.append(dcc.Store(id='store-local', storage_type='local'))
        if store_memory:
            children.append(dcc.Store(id='store-memory', storage_type='memory'))
        if store_session:
            children.append(dcc.Store(id='store-session', storage_type='session'))

        self._system = html.Div(
            children,
            id='system',
            style={'display': 'none'}
        )
        self.layout = html.Div(
            [
                self._system,
                self._page
            ],
            id='root'
        )

        if 'FAVICON_URL' in env and env['FAVICON_URL'] != '':
            # change default favicon
            Path('assets').mkdir(parents=True, exist_ok=True)
            img_data = requests.get(env['FAVICON_URL'], timeout=3).content
            with open('assets/favicon.png', 'wb') as handler:
                handler.write(img_data)
            self._favicon = 'favicon.png'

    @classmethod
    @property
    def theme(cls) -> Themes:
        '''
        An Enum object of themes

        Returns:
            A permitted theme
        '''
        return Themes   # type: ignore

    @property
    def name(self) -> str:
        '''
        Application name

        Returns:
            Application name
        '''

        return self._name


class Servers(Dash):
    '''
    Class Servers provides development & two production async servers with static serving & HTTP/2.
    '''

    def __init__(
        self,
        host: str = '0.0.0.0',
        port: int = 8008,
        **kw
    ):
        super().__init__(**kw)
        self._port = port
        self._host = host

    def debug_server(
        self,
        debug: bool = True,
        **kw
    ):
        '''
        Debug server for development
        '''

        if path.exists(static_path):

            @self.server.route('/static/<resource>')  # type: ignore
            def serve_static(resource):
                '''
                '''
                return flask.send_from_directory(static_path, resource)

        self.run_server(debug=debug, port=self._port, host=self._host, **kw)

    @property
    def async_server(self):
        '''
        Run service as async for working with hypercorn & http/2
        '''

        if path.exists(static_path):

            @self.server.route('/static/<resource>')  # type: ignore
            def serve_static(resource):
                return flask.send_from_directory(static_path, resource)

        return AsyncioWSGIMiddleware(self.server)  # type: ignore

    @property
    def asgi_server(self):
        '''
        Run service as async for working with asgiref package & http/2.
        '''

        if path.exists(static_path):

            @self.server.route('/static/<resource>')  # type: ignore
            def serve_static(resource):
                return flask.send_from_directory(static_path, resource)

        return WsgiToAsgi(self.server)


class PyScript(Dash):
    '''
    Class adds Js & CSS which needed to work PyScript
    '''
    # TODO: Make py-config tag to header
    # TODO: Make py-script tag

    def __init__(
        self,
        **kw
    ):

        # Adding Javascript for PyScript
        external_scripts = external_scripts = [
            {
                'src': 'https://pyscript.net/latest/pyscript.js',
                'crossorigin': 'defer'
            }
        ]
        self._external_scripts = getattr(self, '_external_scripts', None) or []
        self._external_scripts.extend(external_scripts)
        if 'external_scripts' in kw and isinstance(kw['external_scripts'], list):
            self._external_scripts.extend(kw['external_scripts'])

        # An adding corporate styles & PyScript styles
        external_stylesheets = [
            {
                'href': 'https://pyscript.net/latest/pyscript.css',
                'rel': 'stylesheet'
            }
        ]
        self._external_stylesheets = getattr(self, '_external_stylesheets', None) or []
        self._external_stylesheets.extend(external_stylesheets)
        if 'external_stylesheets' in kw and isinstance(kw['external_stylesheets'], list):
            self._external_stylesheets.extend(kw['external_stylesheets'])

        # Adding custom metatag
        meta_tags = []
        self._meta_tags = getattr(self, '_meta_tags', None) or []
        self._meta_tags.extend(meta_tags)
        if 'meta_tags' in kw and kw['meta_tags'] != '':
            self._external_stylesheets.extend(kw['meta_tags'])

        super().__init__(
            url_base_pathname=base_url,
            meta_tags=self._meta_tags,
            external_stylesheets=self._external_stylesheets,
            external_scripts=self._external_scripts,
            **kw
        )


class CoLab(JupyterDash):
    '''
    Make the application with jupyter notebook.

    Run as cell's output or in another tab.
    '''

    def __init__(
        self,
        debug: bool = True,
        host: str = '0.0.0.0',
        port: int = 8008,
        **kw
    ):
        super().__init__(**kw)
        self._debug = debug
        self._port = port
        self._host = host

    def cell(self, **kw):
        '''
        Run Dash inside cell's output
        '''

        self.run_server(
            mode='inline',
            host=self._host,
            port=self._port,
            dev_tools_ui=self._debug,
            debug=self._debug,
            dev_tools_hot_reload=self._debug,
            **kw
        )

    def page(self, **kw):
        '''
        Run application in jupyter session
        '''

        self.run_server(
            mode='jupyterlab',
            host=self._host,
            port=self._port,
            dev_tools_ui=self._debug,
            debug=self._debug,
            dev_tools_hot_reload=self._debug,
            threaded=True,
            **kw
        )

    def stop_jupyter(self):
        '''
        Stop Dash server.
        '''

        self._server_threads[(self._host, self._port)].kill()
