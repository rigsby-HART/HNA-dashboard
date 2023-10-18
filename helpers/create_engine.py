# Engine will be created here.  It's shared throughout all of the processes, so it makess no sense to remake an engine for EACH page
import pandas as pd
from sqlalchemy import create_engine
engine_2021 = create_engine('sqlite:///sources//hart2021.db')
# Importing income data

df_income = pd.read_sql_table('income', engine_2021.connect())

# Importing partners data

df_partners = pd.read_sql_table('partners', engine_2021.connect())