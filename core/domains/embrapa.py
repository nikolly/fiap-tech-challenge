from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse
from core.functions.functions import config_selenium, get_link_csv, prepare_data, insert_data, normalize_product_names
from fastapi import HTTPException
from sqlalchemy import MetaData
from connection.database import connect_database


def process_data(category: str, sub_category: str = None):
    # Connecting to database
    engine, session = connect_database()
    
    try:
        # Retrieve the defined tables
        metadata = MetaData(bind=engine)
        metadata.reflect(bind=engine)
        md_header = metadata.tables['product']
        if category == '03':
            md_header = metadata.tables['farming_items']
        md_quantities = metadata.tables['quantities']
    except KeyError as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Error retrieving tables from the database")
    
    # Configuring Selenium and retrieving data from a CSV file
    driver = config_selenium()
    separator = '\t' if category == '03' else ';'
    dataframe = prepare_data(get_link_csv(driver,category, sub_category), separator)
    driver.quit()

    for index, row in dataframe.iterrows():
        # Calling the insert_data function to save product and its quantities in database
        insert_data(session, md_header, md_quantities, row,    
                    category, sub_category if sub_category else '00')
    
    try:
        session.commit()
    except SQLAlchemyError as e:
        print(f"Error committing transaction: {str(e)}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Error saving data to the database")
                
    session.commit()
    session.close()
    
    # Changing the index to improve the data output
    if 'control' in dataframe.columns:
        dataframe.set_index('control', inplace=True)
           
    # Returning the data in JSON format
    return JSONResponse(content=dataframe.to_dict(orient='index'), 
                        status_code=200, 
                        headers={"Content-Type": "application/json"})


def process_data_importation_exportation(category: str, sub_category: str = None):
    # Connecting to database
    engine, session = connect_database()
    
    try:
        # Retrieve the defined tables
        metadata = MetaData(bind=engine)
        metadata.reflect(bind=engine)
        md_header = metadata.tables['country']
        md_imp_exp = metadata.tables['importation_exportation']
    except KeyError as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Error retrieving tables from the database")
    
    # Configuring Selenium and retrieving data from a CSV file
    driver = config_selenium()
    dataframe = prepare_data(get_link_csv(driver, category, sub_category), use_name_normalization=False)
    driver.quit()

    for index, row in dataframe.iterrows():
        # Calling the insert_data function to save product and its quantities in database
        insert_data(session, md_header, md_imp_exp, row, category, sub_category)
    
    try:
        session.commit()
    except SQLAlchemyError as e:
        print(f"Error committing transaction: {str(e)}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Error saving data to the database")
                
    session.commit()
    session.close()
    
    # Changing the index to improve the data output
    if 'control' in dataframe.columns:
        dataframe.set_index('control', inplace=True)
    
    dataframe.fillna('null', inplace=True)
    
    # Returning the data in JSON format
    return JSONResponse(content=dataframe.to_dict(orient='index'), 
                        status_code=200, 
                        headers={"Content-Type": "application/json"})
    