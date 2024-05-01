from . import (
    embrapa,
    login
)


def init_app(app):
    app.include_router(embrapa.router)
    app.include_router(login.router)
    