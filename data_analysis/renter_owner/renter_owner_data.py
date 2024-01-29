import pandas as pd
import numpy as np
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# This file takes in the associated.csv and hart20xx.db
# The purpose is to add in renter vs owner data and create the owners table in the database
# Both files should be placed in the same directory as this file


# Specify the file path of the CSV file
csv_file = 'data_analysis/renter_owner/2016_HNA_Consolidated_processed.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file, header=None, encoding='latin-1', dtype=str)

minority_status = [x.strip() for x in df.iloc[0, 1:].unique()]
housing_type = [x.strip() for x in df.iloc[1, 1:].unique()]

AMHI = [x.strip() for x in df.iloc[2, 1:].unique()]
CHN_status = [x.strip() for x in df.iloc[3, 1:].unique()]

numbers = df.iloc[4:, 1:].replace("x", "0").fillna(0).astype(int)

groups = len(CHN_status) * len(AMHI) * len(housing_type)
renter_vs_owner_data = numbers.iloc[:, 1:groups + 1]

# Create the names of the columns
columnName = pd.Series([""] * (groups))
index = 0

for housing in housing_type:
    for income in AMHI:
        for status in CHN_status:
            columnName[index] = f"{housing}-{income}-{status}"
            index += 1
columnName = columnName.rename({x: (x + 1) for x in range(groups * 2)})
renter_vs_owner_data = renter_vs_owner_data.rename(columns=columnName.to_dict())
renter_vs_owner_data.insert(0, "Geography", df.iloc[4:, 0])
renter_vs_owner_data = renter_vs_owner_data.reset_index(drop=True)

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


renter_vs_owner_data.iat[0, 0] = "Canada"
renter_vs_owner_data.iloc[1:, 0] = renter_vs_owner_data.iloc[1:, 0].apply(convert_to_name)
condition = renter_vs_owner_data.iloc[:, 0].notna()
renter_vs_owner_data = renter_vs_owner_data[condition]
renter_vs_owner_data = renter_vs_owner_data.reset_index(drop=True)

# 'Percent Non-Binary HH in core housing need'
# Calculate percent of the non-binary ppl in CHN by income category

# Percent of trans HH in CHN

income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']
income_labels = ['Very Low Income', 'Low Income', 'Moderate Income', 'Median Income', 'High Income']
# One for percent of the total population, then one for each income
label = '{household} Percent HH with income {range} of AMHI in core housing need'
total = housing_type[0]
owner = housing_type[1]
renter = housing_type[2]
output_columns = [label.format(household=owner, range=income) for income in income_lv_list] + \
                 [label.format(household=renter, range=income) for income in income_lv_list] + \
                 [f'Per HH with income {income} of AMHI in core housing need that are renter HH' for income in
                  income_lv_list] + \
                 [f'Per HH with income {income} of AMHI in core housing need that are owner HH' for income in
                  income_lv_list] + \
                 [f'{owner}-{income}-{type}' for income in AMHI for type in CHN_status] + \
                 [f'{renter}-{income}-{type}' for income in AMHI for type in CHN_status] + \
                 [f'Percent of {owner} HH that are in {income}' for income in income_labels] + \
                 [f'Percent of {renter} HH that are in {income}' for income in income_labels]


def add_columns(row):
    # Match row to transgender row
    geo = row["Geography"]
    rent_row = renter_vs_owner_data[renter_vs_owner_data["Geography"] == geo]
    # Sometimes it exists in Partners, but not in the other transgender data
    if rent_row.empty:
        row_output = {x: None for x in output_columns}
        return pd.Series(row_output)
    # Naming scheme produces repeated names, so the query for geo returns two series
    rent_row = rent_row.iloc[0] if isinstance(rent_row, pd.DataFrame) else rent_row

    row_output = {}
    label = '{household} Percent HH with income {range} of AMHI in core housing need'
    for index, income_lvl in enumerate(income_lv_list):
        index += 1  # Because our income level doesn't have a total as the first index, unlike our AMHI list
        try:
            row_output[label.format(household=owner, range=income_lvl)] = \
                rent_row[f"{owner}-{AMHI[index]}-{CHN_status[1]}"].item() / \
                rent_row[f"{owner}-{AMHI[index]}-{CHN_status[0]}"].item()
        except ZeroDivisionError:
            row_output[output_columns[index]] = None
        try:
            row_output[label.format(household=renter, range=income_lvl)] = \
                rent_row[f"{renter}-{AMHI[index]}-{CHN_status[1]}"].item() / \
                rent_row[f"{renter}-{AMHI[index]}-{CHN_status[0]}"].item()
        except ZeroDivisionError:
            row_output[output_columns[index + len(income_lv_list)]] = None
        # Info for Percentage of Households in Core Housing Need, by Income Category and HH Size
        try:
            row_output[f'Per HH with income {income_lvl} of AMHI in core housing need that are owner HH'] = \
                rent_row[f"{owner}-{AMHI[index]}-{CHN_status[1]}"].item() / \
                rent_row[f"{total}-{AMHI[index]}-{CHN_status[1]}"].item()
        except ZeroDivisionError:
            row_output[f'Per HH with income {income_lvl} of AMHI in core housing need that are owner HH'] = None
        try:
            row_output[f'Per HH with income {income_lvl} of AMHI in core housing need that are renter HH'] = \
                rent_row[f"{renter}-{AMHI[index]}-{CHN_status[1]}"].item() / \
                rent_row[f"{total}-{AMHI[index]}-{CHN_status[1]}"].item()
        except ZeroDivisionError:
            row_output[f'Per HH with income {income_lvl} of AMHI in core housing need that are renter HH'] = None
    # Info for affordable Housing Deficit
    for index, income_lvl in enumerate(AMHI):
        for status in CHN_status:
            row_output[f'{renter}-{AMHI[index]}-{status}'] = rent_row[f"{renter}-{AMHI[index]}-{status}"].item()
            row_output[f'{owner}-{AMHI[index]}-{status}'] = rent_row[f"{owner}-{AMHI[index]}-{status}"].item()
    # Info for Income Categories and Affordable Shelter Costs table
    for index, label in enumerate(income_labels):
        try:
            row_output[f'Percent of {owner} HH that are in {label}'] = \
                rent_row[f"{owner}-{AMHI[index + 1]}-{CHN_status[0]}"].item() / \
                rent_row[f"{owner}-{AMHI[0]}-{CHN_status[0]}"].item()
            row_output[f'Percent of {renter} HH that are in {label}'] = \
                rent_row[f"{renter}-{AMHI[index + 1]}-{CHN_status[0]}"].item() / \
                rent_row[f"{renter}-{AMHI[0]}-{CHN_status[0]}"].item()
        except ZeroDivisionError:
            # print(f"division by zero on {geo}")
            True

    return pd.Series(row_output)


output_columns.sort()
ownership = partners["Geography"].to_frame(name="Geography")
ownership[output_columns] = partners.apply(add_columns, axis=1)
# partners = pd.concat([partners, partners.apply(add_columns, axis=1)])
sql = 'DROP TABLE IF EXISTS ownership;'
result = engine.execute(sql)
ownership.to_sql("ownership", engine, index=False)
# class Ownership(Base):
#     __tablename__ = "ownership"
#
#     # define your primary key
#     pk = Column(Integer, primary_key=True, comment='primary key')
#
#     # columns except pk
#     Geography = Column(String)
#     for i in ownership.columns[1:]:
#         vars()[f'{i}'] = Column(Float)
#
#
# Ownership.__table__.create(bind=engine, checkfirst=True)
#
# for i in range(0, len(ownership)):
#     conn.execute(insert(Ownership), [ownership.loc[i, :].to_dict()])
conn.close()
