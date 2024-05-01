import pandas as pd
from core.functions.functions import config_selenium, get_csv
import sqlite3
from fastapi import HTTPException


def get_data():
    driver=config_selenium()
    
    # csv_production = get_csv(driver,'02')
    
    # csv_processing_vinifera = get_csv(driver,'03')
    # csv_processing_american_and_hybrid = get_csv(driver,'03','02')
    # csv_processing_table_grapes = get_csv(driver,'03','03')
    # csv_processing_unclassified = get_csv(driver,'03','04')
    
    csv_sales = get_csv(driver,'04')
    
    # csv_import_table_wines = get_csv(driver,'05')
    # csv_import_sparkling_wines = get_csv(driver,'05', '02')
    # csv_import_fresh_grapes = get_csv(driver,'05', '03')
    # csv_import_raisins = get_csv(driver,'05', '04')
    # csv_import_grape_juice = get_csv(driver,'05', '05')
    
    # csv_export_table_grapes = get_csv(driver,'06')
    # csv_export_sparkling_wines = get_csv(driver,'06', '02')
    # csv_export_fresh_grapes = get_csv(driver,'06', '03')
    # csv_export_grape_juice = get_csv(driver,'06', '04')
        
    driver.quit()
    
    try:
        df = pd.read_csv(csv_sales, sep='\t')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=("An error occurred while reading the data."))
    
    for item in df:
        print(item)
    
    # Conectar ao banco de dados SQLite
    # conn = sqlite3.connect('dados.db')

    # # Salvar o DataFrame no banco de dados SQLite
    # df.to_sql('tabela_dados', conn, if_exists='replace', index=False)

    # # Fechar a conexão com o banco de dados
    # conn.close()
    return df
