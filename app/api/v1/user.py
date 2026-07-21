from fastapi import APIRouter

router = APIRouter()

@router.post(
    '/filling-user-data',
    summary='Filling user related data in order to create their profile.',
    description='**Filling user related data in order to create their profile.**',
)
async def filling_user_anketa_data():
    return {'status': 'ok'}
