import pandas as pd
import numpy as np
import re

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy import insert

# This file takes in 2021_Consolidated_trans added.csv and hart2021.db
# The purpose is to add in transgender CHN data into the partners table in the database
# Both files should be placed in the same directory as this file,


# Specify the file path of the CSV file
csv_file = 'data_analysis/2021_Consolidated_trans added.csv'  # Replace with the actual file path

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file, header=None, encoding='latin-1', dtype=str)
minority_status = [x.strip() for x in df.iloc[0, 1:].unique()]
housing_type = [x.strip() for x in df.iloc[1, 1:].unique()]
AMHI = [x.strip() for x in df.iloc[2, 1:].unique()]
CHN_status = [x.strip() for x in df.iloc[3, 1:].unique()]
numbers = df.iloc[4:, 1:].replace("x", "0").fillna(0).astype(int)

# Total households/Transgender households are the last two types
groups = len(CHN_status) * len(AMHI) * len(housing_type)
offset = (len(minority_status) - 2) * groups
transgender_households = numbers.iloc[:, offset:]

# Create the names of the columns
columnName = pd.Series([""] * (groups * 2))
index = 0
for minority in (minority_status[-2:]):
    for housing in housing_type:
        for income in AMHI:
            for status in CHN_status:
                columnName[index] = f"{minority}-{housing}-{income}-{status}"
                index += 1
columnName = columnName.rename({x: (x + offset + 1) for x in range(groups * 2)})
transgender_households = transgender_households.rename(columns=columnName.to_dict())
transgender_households.insert(0, "Geography", df.iloc[4:, 0])
transgender_households = transgender_households.reset_index(drop=True)

# Create engine
# engine = create_engine(f'sqlite:///sources//previous_years//hart2021.db')
engine = create_engine(f'sqlite:///data_analysis//hart2021.db')
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


transgender_households.iat[0, 0] = "Canada"
transgender_households.iloc[1:, 0] = transgender_households.iloc[1:, 0].apply(convert_to_name)
condition = transgender_households.iloc[:, 0].notna()
transgender_households = transgender_households[condition]
transgender_households = transgender_households.reset_index(drop=True)
Base = declarative_base()

# 'Percent Non-Binary HH in core housing need'
# Calculate percent of the non-binary ppl in CHN by income category

# Percent of trans HH in CHN

income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']

output_transgender_label = "Percent of Transgender HH in core housing"

# One for percent of the total population, then one for each income
output_columns = [
                     output_transgender_label,
                     f'{output_transgender_label} with income {income_lv_list[0]} of the AMHI'
                 ] + [
                     f'{output_transgender_label} with income {i} of AMHI' for i in income_lv_list[1:]
                 ]
output_df = pd.DataFrame(columns=output_columns)
total_label, transgender_label = minority_status[-2:]

def add_columns(row):
    # Match row to transgender row
    geo = row["Geography"]
    trans_data = transgender_households[transgender_households["Geography"] == geo]
    # Sometimes it exists in Partners, but not in the other transgender data
    if trans_data.empty:
        row_output = {x: None for x in output_columns}
        return pd.Series(row_output)
    # Naming scheme produces repeated names, so the query for geo returns two series
    trans_data = trans_data.iloc[0] if isinstance(trans_data, pd.DataFrame) else trans_data

    chn_transgender = trans_data[f"{transgender_label}-{housing_type[0]}-{AMHI[0]}-{CHN_status[1]}"]
    total_transgender = trans_data[f"{transgender_label}-{housing_type[0]}-{AMHI[0]}-{CHN_status[0]}"]
    try:
        percent_chn = chn_transgender.item() / total_transgender.item()
    except ZeroDivisionError:
        percent_chn = None
    row_output = {output_columns[0]: percent_chn}
    for index, income_lvl in enumerate(income_lv_list):
        try:
            if income_lvl == '20% or under':
                row_output[output_columns[index + 1]] = \
                    trans_data[f"{transgender_label}-{housing_type[0]}-{AMHI[1]}-{CHN_status[1]}"].item() / \
                    trans_data[f"{transgender_label}-{housing_type[0]}-{AMHI[0]}-{CHN_status[1]}"].item()
            else:
                row_output[output_columns[index + 1]] = \
                    trans_data[f"{transgender_label}-{housing_type[0]}-{AMHI[index + 1]}-{CHN_status[1]}"].item() / \
                    trans_data[f"{transgender_label}-{housing_type[0]}-{AMHI[0]}-{CHN_status[1]}"].item()
        except ZeroDivisionError:
            row_output[output_columns[index + 1]] = None
    return pd.Series(row_output)


partners[output_columns] = partners.apply(add_columns, axis=1)

sql = 'DROP TABLE IF EXISTS partners;'
result = engine.execute(sql)


class Partners(Base):
    __tablename__ = "partners"

    # define your primary key
    pk = Column(Integer, primary_key=True, comment='primary key')

    # columns except pk
    Geography = Column(String)
    for i in partners.columns[2:]:
        vars()[f'{i}'] = Column(Float)


Partners.__table__.create(bind=engine, checkfirst=True)

for i in range(0, len(partners)):
    conn.execute(insert(Partners), [partners.loc[i, :].to_dict()])
conn.close()
