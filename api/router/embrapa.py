from fastapi import APIRouter, Depends

from core.domains import embrapa
from security.auth import Auth


router = APIRouter(prefix="/api/embrapa")
auth = Auth()


@router.post("/production", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_production_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process production data.
    """
    return embrapa.process_data(category='02')


@router.post("/sales", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_sales_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process sales data.
    """
    return embrapa.process_data(category='04')


@router.post("/processing/vinifera", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_processing_vinifera_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process vinifera processing data.
    """
    return embrapa.process_data(category='03', sub_category='01')


@router.post("/processing/americanAndHybrid", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_processing_american_hybrid_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process American and Hybrid processing data.
    """
    return embrapa.process_data(category='03', sub_category='02')


@router.post("/processing/tableGrapes", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_processing_table_grapes_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process table grapes processing data.
    """
    return embrapa.process_data(category='03', sub_category='03')


@router.post("/processing/noClassification", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_processing_no_classification_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process no classification processing data.
    """
    return embrapa.process_data(category='03', sub_category='04')


@router.post("/exportation/tableGrapes", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_exportation_table_grapes_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process table grapes exportation data.
    """
    return embrapa.process_data(category='06', sub_category='01')


@router.post("/exportation/sparklingWines", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_exportation_sparkling_wines_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process sparkling wines exportation data.
    """
    return embrapa.process_data(category='06', sub_category='02')


@router.post("/exportation/freshGrapes", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_exportation_fresh_grapes_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process fresh grapes exportation data.
    """
    return embrapa.process_data(category='06', sub_category='03')


@router.post("/exportation/grapeJuice", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_exportation_grape_juice_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process grape juice exportation data.
    """
    return embrapa.process_data(category='06', sub_category='04')


@router.post("/importation/tableGrapes", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_importation_table_grapes_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process table grapes importation data.
    """
    return embrapa.process_data(category='05', sub_category='01')


@router.post("/importation/sparklingWines", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_importation_sparkling_wines_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process sparkling wines importation data.
    """
    return embrapa.process_data(category='05', sub_category='02')


@router.post("/importation/freshGrapes", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_importation_fresh_grapes_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process fresh grapes importation data.
    """
    return embrapa.process_data(category='05', sub_category='03')


@router.post("/importation/raisins", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_importation_raisins_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process raisins importation data.
    """
    return embrapa.process_data(category='05', sub_category='04')


@router.post("/importation/grapeJuice", response_model=embrapa.ApiResponse, tags=["Embrapa"])
def process_importation_grape_juice_data(current_user: str = Depends(auth.get_current_user)):
    """
    Process grape juice importation data.
    """
    return embrapa.process_data(category='05', sub_category='05')
