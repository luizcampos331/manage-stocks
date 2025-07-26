from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.presentation.http.controllers.stock_controller import stock_router

router = APIRouter()

router.include_router(stock_router)


@router.get("/", response_class=JSONResponse)
async def root():
    return "API Account Transactions 0.1.0"
