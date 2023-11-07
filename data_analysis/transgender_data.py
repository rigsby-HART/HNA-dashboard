import pandas as pd
import numpy as np

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Float, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy import insert

# Specify the file path of the CSV file
csv_file = 'data_analysis/2021_Consolidated_trans added.csv'  # Replace with the actual file path

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file, header=None, encoding='latin-1', dtype=str)
minority_status = [x.strip() for x in df.iloc[0, 1:].unique()]
housing_type = [x.strip() for x in df.iloc[1, 1:].unique()]
AMHI = [x.strip() for x in df.iloc[2, 1:].unique()]
CHN_status = [x.strip() for x in df.iloc[3, 1:].unique()]
# def geo_code_extractor(geography):
#     geo = geography.split()
#     # print(geo)
#     for g in geo:
#         if g[0] == '(' and g[1].isdigit():
#             g = g.replace("(", "")
#             g = g.replace(")", "")
#             break
#     return g
# # Pure data
# df.iloc[4:, 0].apply(lambda x: geo_code_extractor(x))
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
conn = engine.connect()

Base = declarative_base()

# 'Percent Non-Binary HH in core housing need'
# Calculate percent of the non-binary ppl in CHN by income category
total_label, transgender_label = minority_status[-2:]
# Percent of trans HH in CHN
CHN_transgender = transgender_households.iloc[0, :][f"{transgender_label}-{housing_type[0]}-{AMHI[0]}-{CHN_status[1]}"]
total_transgender = transgender_households.iloc[0, :][
    f"{transgender_label}-{housing_type[0]}-{AMHI[0]}-{CHN_status[0]}"]
percent_CHN = CHN_transgender / total_transgender

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
for index, (code, region) in mapped_geo_code.iloc[:, [0, 3]].iterrows():
    CHN_transgender = transgender_households[region, :][
        f"{transgender_label}-{housing_type[0]}-{AMHI[0]}-{CHN_status[1]}"]
    total_transgender = transgender_households[region, :][
        f"{transgender_label}-{housing_type[0]}-{AMHI[0]}-{CHN_status[0]}"]
    percent_CHN = CHN_transgender / total_transgender
    newrow = {}
    for i in income_lv_list:
        # newrow[output_transgender_label] =
        if i == '20% or under':
            output_df[f'{output_transgender_label} with income {i} of the AMHI']

        else:
            output_df[f'{output_transgender_label} with income {i} of AMHI']


class Transgender(Base):
    __tablename__ = "transgender"

    # define your primary key
    pk = Column(Integer, primary_key=True, comment='primary key')

    # columns except pk
    Geography = Column(String)
    for i in transgender_households.columns[1:]:
        vars()[f'{i}'] = Column(Float)


Transgender.__table__.create(bind=engine, checkfirst=True)

for i in range(0, len(transgender_households)):
    conn.execute(insert(Transgender), [transgender_households.loc[i, :].to_dict()])

conn.close()
