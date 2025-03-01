from fastapi import APIRouter
from .etiqueta.router import router as etiqueta_router

router = APIRouter()
router.include_router(etiqueta_router, prefix="/etiqueta", tags=["Etiqueta"])
