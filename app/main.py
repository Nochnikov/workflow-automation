from fastapi import FastAPI

from app.api.v1.user import router as user_router

app = FastAPI(
    title='Workflow Automation',
    docs_url='/api/workflow-automation/openapi',
    openapi_url='/api/workflow-automation/openapi.json',
    # lifespan='off',
)

app.include_router(user_router, prefix='/api/user', tags=['user'])
