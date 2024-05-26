from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from core.functions.functions import config_selenium, get_link_csv, prepare_data, insert_data, get_metadata_and_tables
from fastapi import HTTPException
from connection.database import connect_database
from models.embrapa import ApiResponse, ItemData, YearData
        
        
def process_data(category: str, sub_category: str = None):
    # Connecting to database
    engine, session = connect_database()
    
    try:
        metadata, md_header, md_quantities = get_metadata_and_tables(engine, category)
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving tables from the database: {str(e)}")
    
    # Configuring Selenium and retrieving data from a CSV file
    driver = config_selenium()
    # COnfiguring the separator and the use_name_normalization parameter
    separator = '\t' if category == '03' else ';'
    use_name_normalization=False if category in ['05','06'] else True 
    dataframe = prepare_data(get_link_csv(driver,category, sub_category), separator, use_name_normalization)
    driver.quit()

    for index, row in dataframe.iterrows():
        # Calling the insert_data function to save product and its quantities in database
        insert_data(session, md_header, md_quantities, row,    
                    category, sub_category if sub_category else '00')
    
    try:
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving data to the database: {str(e)}")
    finally:
        session.close()
    
    # Changing the index to improve the data output
    if 'control' in dataframe.columns:
        dataframe.set_index('control', inplace=True)
    
    dataframe.fillna('null', inplace=True)
    
    # Cleaning up the dataframe to avoid duplicate columns
    dataframe = dataframe.loc[:, ~dataframe.columns.str.endswith('.1')]

    data_dict = dataframe.to_dict(orient='index')

    structured_data = [
        ItemData(
            id=row.get('id', ''),
            name=item_name,
            data=[YearData(year=int(year), value=value) for year, value in row.items() if year.isdigit()]
        )
        for item_name, row in data_dict.items()
    ]

    response_data = ApiResponse(items=structured_data)
    
    return JSONResponse(content=response_data.model_dump(), status_code=200, headers={"Content-Type": "application/json"})