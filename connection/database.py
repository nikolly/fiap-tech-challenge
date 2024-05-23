from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey, Date, UniqueConstraint, inspect
from sqlalchemy.dialects.sqlite import TEXT
import uuid
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException


def drop_tables(engine, metadata):
    """Excluir todas as tabelas no banco de dados."""
    inspector = inspect(engine)
    for table_name in inspector.get_table_names():
        table = Table(table_name, metadata, autoload_with=engine)
        table.drop(engine)
        

def connect_database():
    try:
        engine = create_engine('sqlite:///embrapa.db')
        Session = sessionmaker(bind=engine)
        session = Session()
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    return engine,session
        
        
def create_tables(engine):
    """
    Create tables in the database.

    Args:
        engine (sqlalchemy.engine.Engine): The database engine.

    Returns:
        None
    """
    metadata = MetaData()

    product = Table('product', metadata,
        Column('name', String, primary_key=True),
        Column('dtcriation', Date, default='CURRENT_DATE')
    )

    farming_items = Table('farming_items', metadata,
        Column('name', String, primary_key=True),
        Column('dtcriation', Date, default='CURRENT_DATE')
    )

    quantities = Table('quantities', metadata,
        Column('id', TEXT, primary_key=True, default=lambda: str(uuid.uuid4())),
        Column('product', TEXT, ForeignKey('product.name'), nullable=True), # The column is nullable because the data can be related to a product or a farming item
        Column('farming_item', TEXT, ForeignKey('farming_items.name'), nullable=True),
        Column('year', Integer),
        Column('quantity', Integer),
        Column('subcategory', String),
        Column('dtcriation', Date, default='CURRENT_DATE'),
        UniqueConstraint('product', 'year', name='uq_product_year'),
        UniqueConstraint('farming_item', 'year', 'subcategory', name='uq_farming_item_year_subcategory')
    )

    country = Table('country', metadata,
        Column('id', TEXT, primary_key=True, default=lambda: str(uuid.uuid4())),
        Column('name', String, unique=True),
        Column('dtcriation', Date, default='CURRENT_DATE')
    )

    importation_exportation = Table('importation_exportation', metadata,
        Column('id', TEXT, primary_key=True, default=lambda: str(uuid.uuid4())),
        Column('id_country', TEXT, ForeignKey('country.id')),
        Column('year', Integer),
        Column('value', Integer),
        Column('category', String),
        Column('subcategory', String),
        Column('dtcriation', Date, default='CURRENT_DATE'),
        UniqueConstraint('id_country', 'year', 'category')
    )

    # Criar todas as tabelas no banco de dados
    metadata.create_all(engine)
