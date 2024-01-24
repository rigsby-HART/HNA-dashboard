import pandas as pd
import numpy as np
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# This file takes in the associated.csv and hart20xx.db
# The purpose is to add in subsidized vs unsubsidized renter data into the owners table in the database
# Both files should be placed in the same directory as this file


# Specify the file path of the CSV file
csv_file = 'data_analysis/renter_owner/subsidized_renters.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file, header=None, encoding='latin-1', dtype=str)

subsidization = [x.strip() for x in df.iloc[0, 1:].unique()]  # [Subsidized housing, Not subsidized housing]
AMHI = [x.strip() for x in df.iloc[1, 1:].unique()]
CHN_status = [x.strip() for x in df.iloc[2, 1:].unique()]

numbers = df.iloc[4:, 1:].replace("x", "0").fillna(0).astype(int)  # Census censors data with 'x'

groups = len(CHN_status) * len(AMHI) * len(subsidization)
subsidized_renters = numbers.iloc[:, 1:groups + 1]

# Create the names of the columns
# The csv has 3 rows for this shit, flatten it

columnName = pd.Series([""] * groups)
index = 0

for subbed in subsidization:
    for income in AMHI:
        for status in CHN_status:
            columnName[index] = f"{subbed}-{income}-{status}"
            index += 1
columnName = columnName.rename({x: (x + 1) for x in range(groups * 2)})
subsidized_renters = subsidized_renters.rename(columns=columnName.to_dict())
subsidized_renters.insert(0, "Geography", df.iloc[4:, 0])
subsidized_renters = subsidized_renters.reset_index(drop=True)

# Create engine
# engine = create_engine(f'sqlite:///sources//previous_years//hart2021.db')
engine = create_engine(f'sqlite:///data_analysis//renter_owner///hart2016.db')
mapped_geo_code = pd.read_sql_table('geocodes_integrated', engine.connect())
partners = pd.read_sql_table('partners', engine.connect())
conn = engine.connect()


def convert_to_name(original_name):
    pattern = r"\(\d+\)"
    code = re.findall(pattern, original_name)[0]
    code = code[1:-1]  # strip brackets
    try:
        geo = mapped_geo_code[mapped_geo_code["Geo_Code"] == int(code)]["Geography"].item()
    except:
        return np.nan
    return geo


subsidized_renters.iat[0, 0] = "Canada"
subsidized_renters.iloc[1:, 0] = subsidized_renters.iloc[1:, 0].apply(convert_to_name)
condition = subsidized_renters.iloc[:, 0].notna()
subsidized_renters = subsidized_renters[condition]
subsidized_renters = subsidized_renters.reset_index(drop=True)
Base = declarative_base()

# 'Percent Non-Binary HH in core housing need'
# Calculate percent of the non-binary ppl in CHN by income category

# Percent of trans HH in CHN

income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']
income_labels = ['Very Low Income', 'Low Income', 'Moderate Income', 'Median Income', 'High Income']
# One for percent of the total population, then one for each income
label = '{household} Percent HH with income {range} of AMHI in core housing need'
subsidized = subbed[0]
unsubsidized = subbed[1]
