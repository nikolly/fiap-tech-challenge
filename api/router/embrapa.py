from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi.openapi.utils import get_openapi

from core.domains import embrapa
from security.auth import Auth


router = APIRouter(prefix="/api/embrapa")
auth = Auth()


@router.post("/production")
def process_production_data(current_user: str = Depends(auth.get_current_user)):
    
    return embrapa.process_data(category='02')


@router.post("/sales")
def process_sales_data(current_user: str = Depends(auth.get_current_user)):
    
    return embrapa.process_data(category='04')


@router.post("/processing/vinifera")
def process_processing_data(current_user: str = Depends(auth.get_current_user)):
    
    return embrapa.process_data(category='03', sub_category='01')


@router.post("/processing/americanAndHybrid")
def process_processing_data(current_user: str = Depends(auth.get_current_user)):
    
    return embrapa.process_data(category='03', sub_category='02')


@router.post("/processing/tableGrapes")
def process_processing_data(current_user: str = Depends(auth.get_current_user)):
    
    return embrapa.process_data(category='03', sub_category='03')


@router.post("/processing/noClassification")
def process_processing_data(current_user: str = Depends(auth.get_current_user)):
    
    return embrapa.process_data(category='03', sub_category='04')


@router.post("/exportation")
def process_exportation_data(current_user: str = Depends(auth.get_current_user)):
    
    return embrapa.process_data(category='04')


@router.post("/importation")
def process_importation_data(current_user: str = Depends(auth.get_current_user)):
    
    return embrapa.process_data(category='04')
