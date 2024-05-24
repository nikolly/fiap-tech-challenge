from fastapi import FastAPI

import api.router as router
from connection.database import create_tables
from sqlalchemy import create_engine


def init_app():
    app = FastAPI()

    engine = create_engine('sqlite:///embrapa.db')
    create_tables(engine)

    router.init_app(app)

    return app
