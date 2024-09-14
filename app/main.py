import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routes.apis import router as api_router
from app.core import constants, env


def get_application() -> FastAPI:
    application = FastAPI(
        title=env.PROJECT_NAME,
        debug=env.DEBUG,
        version=env.VERSION,
        openapi_url=(
            f"{constants.API_PREFIX}/openapi.json"
            if env.ENV in ("local", "dev")
            else None
        ),
        docs_url=(
            f"{constants.API_PREFIX}/docs" if env.ENV in ("local", "dev") else None
        ),
        redoc_url=(
            f"{constants.API_PREFIX}/redoc" if env.ENV in ("local", "dev") else None
        ),
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=env.ALLOWED_HOSTS.split(",") if env.ALLOWED_HOSTS else ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(api_router, prefix=constants.API_PREFIX)

    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=env.PORT,
        headers=[("server", "task-orbit")],
    )
