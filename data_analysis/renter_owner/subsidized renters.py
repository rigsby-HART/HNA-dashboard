import pandas as pd
import numpy as np
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# This file takes in the associated.csv and hart20xx.db
# The purpose is to add in subsidized vs unsubsidized renter data into the owners table in the database
# Both files should be placed in the same directory as this file


# Specify the file path of the CSV file
csv_file = 'data_analysis/renter_owner/subsidized_renters_2021.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file, header=None, encoding='latin-1', dtype=str)

subsidization = [x.strip() for x in df.iloc[0, 1:].unique()]  # [Subsidized housing, Not subsidized housing]
AMHI = [x.strip() for x in df.iloc[1, 1:].unique()]
CHN_status = [x.strip() for x in df.iloc[2, 1:].unique()]

numbers = df.iloc[3:, 1:].replace("x", "0").fillna(0).astype(int)  # Census censors data with 'x'

groups = len(CHN_status) * len(AMHI) * len(subsidization)
subsidized_renters = numbers.iloc[:, :]

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
subsidized_renters.insert(0, "Geography", df.iloc[3:, 0])
subsidized_renters = subsidized_renters.reset_index(drop=True)

# Create engine
engine = create_engine(f'sqlite:///data_analysis//renter_owner///hart2021.db')
mapped_geo_code = pd.read_sql_table('geocodes_integrated', engine.connect())
ownership = pd.read_sql_table('ownership', engine.connect())
conn = engine.connect()


def convert_to_name(original_name):
    pattern = r"\(\d+\)"
    code = re.findall(pattern, original_name)[0]
    code = code[1:-1]  # strip brackets
    try:
        geo: pd.Series = mapped_geo_code[mapped_geo_code["Geo_Code"] == int(code)]["Geography"]
        if geo.empty:
            return np.nan
    except:
        return np.nan
    return geo.item()


subsidized_renters.iat[0, 0] = "Canada"
subsidized_renters.iloc[1:, 0] = subsidized_renters.iloc[1:, 0].apply(convert_to_name)
condition = subsidized_renters.iloc[:, 0].notna()
subsidized_renters = subsidized_renters[condition]
subsidized_renters = subsidized_renters.reset_index(drop=True)

# Calculate the percentages of households in each income category

income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']
income_labels = ['Very Low Income', 'Low Income', 'Moderate Income', 'Median Income', 'High Income']
# One for percent of the total population, then one for each income
label = '{household} Percent HH with income {range} of AMHI in core housing need'
subsidized = subsidization[0]
unsubsidized = subsidization[1]
output_columns = [label.format(household=subsidized, range=income) for income in income_lv_list] + \
                 [label.format(household=unsubsidized, range=income) for income in income_lv_list] + \
                 [f'Per HH with income {income} of AMHI in core housing need that are {subsidized} HH' for income in
                  income_lv_list] + \
                 [f'Per HH with income {income} of AMHI in core housing need that are {unsubsidized} HH' for income in
                  income_lv_list] + \
                 [f'{subsidized}-{income}-{type}' for income in AMHI for type in CHN_status] + \
                 [f'{unsubsidized}-{income}-{type}' for income in AMHI for type in CHN_status] + \
                 [f'Percent of {subsidized} HH that are in {income}' for income in income_labels] + \
                 [f'Percent of {unsubsidized} HH that are in {income}' for income in income_labels]


def add_columns(row):
    geo = row["Geography"]
    row_output = {}
    label = '{household} Percent HH with income {range} of AMHI in core housing need'
    examined_for_chn = CHN_status[1]
    in_chn = CHN_status[2]
    for index, income_lvl in enumerate(income_lv_list):
        index += 1  # Because our income level doesn't have a total as the first index, unlike our AMHI list
        try:
            row_output[label.format(household=subsidized, range=income_lvl)] = \
                row[f"{subsidized}-{AMHI[index]}-{in_chn}"] / \
                row[f"{subsidized}-{AMHI[index]}-{examined_for_chn}"]
        except ZeroDivisionError:
            row_output[label.format(household=subsidized, range=income_lvl)] = None
        try:
            row_output[label.format(household=unsubsidized, range=income_lvl)] = \
                row[f"{unsubsidized}-{AMHI[index]}-{in_chn}"] / \
                row[f"{unsubsidized}-{AMHI[index]}-{examined_for_chn}"]
        except ZeroDivisionError:
            row_output[label.format(household=unsubsidized, range=income_lvl)] = None
        # Info for Percentage of Households in Core Housing Need, by Income Category and HH Size
        try:
            row_output[f'Per HH with income {income_lvl} of AMHI in core housing need that are {subsidized} HH'] = \
                row[f"{subsidized}-{AMHI[index]}-{in_chn}"] / \
                (row[f"{subsidized}-{AMHI[index]}-{in_chn}"] +
                 row[f"{unsubsidized}-{AMHI[index]}-{in_chn}"])
        except ZeroDivisionError:
            row_output[f'Per HH with income {income_lvl} of AMHI in core housing need that are {subsidized} HH'] = 0
        try:
            row_output[f'Per HH with income {income_lvl} of AMHI in core housing need that are {unsubsidized} HH'] = \
                row[f"{unsubsidized}-{AMHI[index]}-{in_chn}"] / \
                (row[f"{subsidized}-{AMHI[index]}-{in_chn}"] +
                 row[f"{unsubsidized}-{AMHI[index]}-{in_chn}"])
        except ZeroDivisionError:
            row_output[f'Per HH with income {income_lvl} of AMHI in core housing need that are {unsubsidized} HH'] = 0
    # Info for affordable Housing Deficit
    for index, income_lvl in enumerate(AMHI):
        for status in CHN_status:
            row_output[f'{unsubsidized}-{AMHI[index]}-{status}'] = row[f"{unsubsidized}-{AMHI[index]}-{status}"]
            row_output[f'{subsidized}-{AMHI[index]}-{status}'] = row[f"{subsidized}-{AMHI[index]}-{status}"]
    # Info for Income Categories and Affordable Shelter Costs table
    for index, label in enumerate(income_labels):
        try:
            row_output[f'Percent of {subsidized} HH that are in {label}'] = \
                row[f"{subsidized}-{AMHI[index + 1]}-{examined_for_chn}"] / \
                row[f"{subsidized}-{AMHI[0]}-{examined_for_chn}"]
            row_output[f'Percent of {unsubsidized} HH that are in {label}'] = \
                row[f"{unsubsidized}-{AMHI[index + 1]}-{examined_for_chn}"] / \
                row[f"{unsubsidized}-{AMHI[0]}-{examined_for_chn}"]
        except ZeroDivisionError:
            # print(f"division by zero on {geo}")
            True

    return pd.Series(row_output)


output_columns.sort()
# ownership = subsidized_renters["Geography"].to_frame(name="Geography")
new_columns = subsidized_renters.apply(add_columns, axis=1)
new_columns = pd.concat([subsidized_renters["Geography"], new_columns], axis=1)
ownership = pd.merge(ownership, new_columns, on="Geography")
# ownership.drop("index", inplace=True, axis=1)
sql = 'DROP TABLE IF EXISTS ownership;'
result = engine.execute(sql)
ownership.to_sql("ownership", engine, index=False)