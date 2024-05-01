from fastapi import FastAPI

import api.router as router


def init_app():
    app = FastAPI()

    router.init_app(app)

    return app
