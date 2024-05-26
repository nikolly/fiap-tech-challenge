from fastapi import FastAPI

import api.router as router
from connection.database import create_tables
from fastapi.openapi.utils import get_openapi
from sqlalchemy import create_engine


def init_app():
    app = FastAPI()

    engine = create_engine('sqlite:///embrapa.db')
    create_tables(engine)

    router.init_app(app)

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Embrapa API",
            version="1.0.0",
            description="This is the API documentation for the Embrapa project. It provides endpoints for processing production data, import/export data, and more. The Embrapa project aims to provid a platform for data analysis and collaboration.",
            routes=app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema
    
    app.openapi = custom_openapi


    return app
