from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import json
import pandas as pd
import os
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from fastapi import HTTPException
from datetime import date
from sqlalchemy.dialects.sqlite import insert


def config_selenium():
    """
    Configures and returns a Selenium WebDriver instance with headless mode enabled.
    
    Returns:
        webdriver.Chrome: A Chrome WebDriver instance with headless mode enabled.
    """
    try:
        options = Options()
        options.add_argument("--headless")
        
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    except Exception as e:
        print(f"Error configuring Selenium: {str(e)}")
        return None


def get_link_csv(driver, category, sub_option=None):
    """
    Get the download link for a CSV file based on the given category and sub-option.

    Parameters:
    driver (WebDriver): The WebDriver object used to interact with the web page.
    category (str): The item of the menu in the page. The options are:
                    02 - Produção
                    03 - Processamento (Viníferas) / sub_option 02 - Americanas e híbridas / sub_option 03 - Uvas de Mesa / sub_option 04 - Sem classificação
                    04 - Comercialização
                    05 - Importação (Vinhos de Mesa) / sub_option 02 - Espumantes / sub_option 03 - Uvas frescas / sub_option 04 - Uvas passas / sub_option 05 - Suco de uva
                    06 - Exportação (Vinhos de Mesa) / sub_option 02 - Espumantes / sub_option 03 - Uvas frescas / sub_option 04 - Suco de uva
    sub_option (str, optional): The options for each item of the menu. Defaults to None.

    Returns:
    str: The download link for the CSV file.
    """
    # If a sub_option is provided, append it to the category
    if sub_option:
        category += f'&subopcao=subopt_{sub_option}'
    
    # Trying to get the download link from embrapa. If an exception occurs, return the file path in the project
    try:    
        driver.get(f"http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_{category}")
        link_download = driver.find_element(By.CSS_SELECTOR, '.footer_content[href$=".csv"]').get_attribute('href')
    except:
        link_download = os.path.join('embrapa_files', f'{category[:2]}{sub_option}.csv' if sub_option else f'{category}.csv')
        
    return link_download


import pandas as pd

def prepare_data(link_csv, separator=';', use_name_normalization=True):
    """
    Prepare the data from a CSV file for further analysis.

    Args:
        link_csv (str): The path or URL to the CSV file.
        separator (str, optional): The separator used in the CSV file. Defaults to ';'.

    Returns:
        pandas.DataFrame: The prepared DataFrame.

    """
    # Read the CSV file into a DataFrame
    df = pd.read_csv(link_csv, sep=separator, dtype=str)
    
    # Convert column names to lowercase
    df.columns = [col.lower() for col in df.columns]
    
    # Rename the 'cultivar' and 'país' column to 'produto' if it exists
    if 'cultivar' in df.columns:
        df.rename(columns={'cultivar': 'produto'}, inplace=True)
    if 'país' in df.columns:
        df.rename(columns={'país': 'control'}, inplace=True)
    
    # Convert 'produto' column to string type
    if 'produto' in df.columns:
        df['produto'] = df['produto'].astype(str)

    # If 'id' column is missing, read the CSV file again with specified column names
    if not 'id' in df.columns.values:
        return 'not id++++++++++++========================='
        # column_names = ["id", "control", "produto"] + [str(year) for year in range(1970, 2023)]
        # df = pd.read_csv(link_csv, sep=separator, names=column_names)

    for col in df.columns:
        if col.isdigit():
            # updating nan values to 0
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype('int')
    
    # Normalize product names
    if use_name_normalization:
        df = normalize_product_names(df)
    
    return df


def insert_data(session, md_header, md_quantities, row, category, subcategory):
    # Inserting product into the 'product' table
    product_insert = insert(md_header).values(name=row['control']).on_conflict_do_nothing(index_elements=['name'])
    print(f"Inserting header: {row['control']}")
        
    try:
        result = session.execute(product_insert)
    except SQLAlchemyError as e:
        print(f"Error inserting product: {str(e)}")
        session.rollback()
        raise HTTPException(status_code=500, detail="Error inserting the category into the database")
    
    year_columns = [col for col in row.index if col.isdigit()]
    if category == '05' or category == '06':
        for year in year_columns:
            insert_imp_exp(session, md_quantities, row, category, subcategory, year)
    else:
        for year in year_columns:
            insert_quantity(session, md_quantities, row, category, subcategory, year)
            

def insert_imp_exp(session, md_quantities, row, category, subcategory, year):
    if pd.notna(row[str(year)]):
        # Inserting values from importation/exportation into the 'importation_exportation' table
        stmt = insert(md_quantities).values(
                    id=str(uuid4()), 
                    country=row['control'],
                    year=year,
                    value=row[str(year)],
                    category=category,
                    subcategory=subcategory,
                )
        stmt = stmt.on_conflict_do_update(
                    index_elements=['country', 'year', 'category', 'subcategory'],
                    set_=dict(value=row[str(year)], dtcriation=date.today())
                )
        print(f"Inserting value: {row[str(year)]} for the year {year}, country {row['control']}")
                
        try:
            session.execute(stmt)
        except SQLAlchemyError as e:
            print(f"Error inserting quantity: {str(e)}")
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error inserting quantities from {row['produto']} into the database")
    
               
def insert_quantity(session, md_quantities, row, category, subcategory, year):
    if pd.notna(row[str(year)]):
        # Inserting quantities from product into the 'quantities' table
        stmt = insert(md_quantities).values(
                    id=str(uuid4()), 
                    product=row['control'],
                    year=year,
                    quantity=row[str(year)],
                    category=category,
                    subcategory=subcategory,
                )
        stmt = stmt.on_conflict_do_update(
                    index_elements=['farming_item', 'year', 'subcategory'] if category == '03' else ['product', 'year', 'category'],
                    set_=dict(quantity=row[str(year)], dtcriation=date.today())
                )
        print(f"Inserting quantity: {row[str(year)]} for the year {year}, product {row['produto']}")
                
        try:
            session.execute(stmt)
        except SQLAlchemyError as e:
            print(f"Error inserting quantity: {str(e)}")
            session.rollback()
            raise HTTPException(status_code=500, detail=f"Error inserting quantities from {row['produto']} into the database")


def normalize_product_names(df: pd.DataFrame):
    """
    Normalizes product names in a DataFrame by concatenating subcategories with their corresponding main categories.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing product data where main categories are in uppercase and subcategories follow them.
    
    Returns:
    pd.DataFrame: DataFrame with normalized product names.
    """
    # Identify main categories
    print(df['produto'])
    main_categories = df['produto'].str.isupper()

    # Variable to save the last main category used
    prefix = None

    # Modify subcategories to include the main category prefix
    for index, row in df.iterrows():
        if main_categories[index]:
            # Updating the field control with the field produto because sometimes it is NaN
            df.at[index, 'control'] = row['produto']
            # Extract prefix from main category (first letter of each word)
            words = row['produto'].split()
            prefix = "".join([word[0] for word in words]).lower()
            
        else:
            modified_subcategory = f"{prefix}_{row['produto'].strip().replace(' ', '_').lower()}"
            if not prefix:
                modified_subcategory = f"{row['produto'].strip().replace(' ', '_').lower()}"
                
            df.at[index, 'control'] = modified_subcategory
    
    return df


def load_users_from_json(file_path):
    """
    Loads user data from a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: A dictionary containing the user data.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        json.JSONDecodeError: If the JSON file is not valid.

    """
    try:
        with open(file_path, "r") as file:
            users_data = json.load(file)
        return users_data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON file: {file_path}")
        return None
    