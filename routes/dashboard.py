from fastapi import APIRouter
from fastapi.responses import JSONResponse
from database.metrics import get_metrics

router = APIRouter()


@router.get("/metrics")
def metrics():
    return JSONResponse(content=get_metrics())
