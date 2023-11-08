# Engine will be created here.  It's shared throughout all the processes, so it makess no sense to remake an
# engine for EACH page

# I like type hinting, makes the IDE a lot smarter: try Pycharm Community if you aren't using one
from typing import Dict, List

import pandas as pd
import sqlalchemy.engine
from sqlalchemy import create_engine
import os

from sources.previous_years.year_data import year_data

# All years imported here, modify the years imported using the json listed below
data_path = "sources/previous_years/"
engine_list: Dict[int, sqlalchemy.engine.Engine] = {}
for year, file_name in year_data:
    file_path = os.path.join(data_path, file_name)
    if os.path.isfile(file_path):
        engine_list[year] = create_engine(f'sqlite:///sources//previous_years//{file_name}')

# Importing income data
default_year = 2021
# This stuff should be the same every year (unless places change which I cannot think of a good idea to fix it)
engine_current = engine_list[default_year] # Current Year

# Importing Projection Data

updated_csd_current = pd.read_sql_table('csd_hh_projections', engine_current.connect())  # CSD level projections
updated_cd_current = pd.read_sql_table('cd_hh_projections', engine_current.connect())  # CD level projections

# Importing Geo Code Information

df_geo_list = pd.read_sql_table('geocodes', engine_current.connect())
df_region_list = pd.read_sql_table('regioncodes', engine_current.connect())
df_province_list = pd.read_sql_table('provincecodes', engine_current.connect())
df_region_list.columns = df_geo_list.columns
df_province_list.columns = df_geo_list.columns
mapped_geo_code = pd.read_sql_table('geocodes_integrated', engine_current.connect())

# Repeat the data processing for each year
income_partners_year: Dict[int, pd.DataFrame] = {}
income_indigenous_year: Dict[int, pd.DataFrame] = {}
updated_csd_year: Dict[int, pd.DataFrame] = {}
updated_cd_year: Dict[int, pd.DataFrame] = {}
mapped_geo_code_year: Dict[int, pd.DataFrame] = {}
for year in engine_list.keys():
    income_category = pd.read_sql_table('income', engine_list[year].connect())
    income_category = income_category.drop(['Geography'], axis=1)
    income_category = income_category.rename(columns={'Formatted Name': 'Geography'})

    df_partners = pd.read_sql_table('partners', engine_list[year].connect())
    df_ind = pd.read_sql_table('indigenous', engine_list[year].connect())

    income_partners_year[year] = income_category.merge(df_partners, how='left', on='Geography')
    income_indigenous_year[year] = income_category.merge(df_ind, how='left', on='Geography')
    updated_csd_year[year] = pd.read_sql_table('csd_hh_projections', engine_list[year].connect())
    updated_cd_year[year] = pd.read_sql_table('cd_hh_projections', engine_list[year].connect())
    mapped_geo_code_year[year] = pd.read_sql_table('geocodes_integrated', engine_list[year].connect())

