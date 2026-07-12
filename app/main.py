from fastapi import FastAPI

app = FastAPI(
    title='Workflow Automation',
    docs_url='/api/workflow-automation/openapi',
    openapi_url='/api/workflow-automation/openapi.json',
    # lifespan='off',
)
