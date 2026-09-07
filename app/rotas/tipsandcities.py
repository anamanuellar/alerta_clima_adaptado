from app.modelos.tipsandcities import Tips, City
from frontend.tipsandcities import TipsandCities
from fastapi.exceptions import HTTPException
from functools import lru_cache
from fastapi import APIRouter, Depends
from typing import List

router = APIRouter(prefix="/api/v1")

@lru_cache
def getTipsandCities():
    return TipsandCities()

@router.get(
                "/tips", 
                response_model=Tips, 
                summary="Obtém dicas de clima", 
                response_description="3 dicas de clima para cada tipo de dica"                
)
async def getTips(tipsandcities: TipsandCities = Depends(getTipsandCities)) -> Tips:

    try:
        return tipsandcities.getTips()
    
    except Exception:
        raise HTTPException(status_code=500, detail="Não foi possível obter as dicas de clima. Reinicie a aplicação")
    

@router.get(
            "/cities", 
            response_model=List[City], 
            summary="Obtém cidades e suas siglas de estado", 
            response_description="Lista de cidades e seus atributos"        
)
async def getCities(tipsandcities: TipsandCities = Depends(getTipsandCities)) -> List[City]:

    try:
        return tipsandcities.getCities()
    
    except Exception:
        raise HTTPException(status_code=500, detail="Não foi possível obter as cidades. Reinicie a aplicação")
    
