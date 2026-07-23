from async_fastapi_jwt_auth import AuthJWT
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.api.v1.user import router as user_router
from app.core.jwt import JWTSettings
from app.ioc.container import create_container


async def lifespan(app: FastAPI):
    AuthJWT.load_config(JWTSettings)
    container = create_container()
    setup_dishka(container, app)
    yield
    await container.close()


app = FastAPI(
    title='Workflow Automation',
    docs_url='/api/workflow-automation/openapi',
    openapi_url='/api/workflow-automation/openapi.json',
    lifespan=lifespan,
)

app.include_router(user_router, prefix='/api/user', tags=['user'])
