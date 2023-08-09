from fastapi import APIRouter

from routes import balances

router = APIRouter()
router.include_router(balances.router)
