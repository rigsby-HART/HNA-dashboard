import re
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# Specify the file path of the CSV file
csv_file = 'data_analysis/2021_Unit_Mix_Consolidated.csv'  # Replace with the actual file path

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file, header=None, encoding='latin-1', dtype=str)

CHN_status = [x.strip() for x in df.iloc[0, 1:].unique()]
hh_type = [x.strip() for x in df.iloc[1, 1:].unique()]

AMHI = [x.strip() for x in df.iloc[2, 1:].unique()]
hh_size = [x.strip() for x in df.iloc[3, 1:].unique()]

numbers = df.iloc[4:, 1:].replace("x", "0").fillna(0).astype(int)

# Total households/Transgender households are the last two types
groups = len(CHN_status) * len(hh_type) * len(AMHI) * len(hh_size)
bedroom_predictions = numbers

# Create the names of the columns
columnName = pd.Series([""] * (groups))
index = 0

for status in CHN_status:
    for housing in hh_type:
        for income in AMHI:
            for size in hh_size:
                columnName[index] = f"{size}-{housing}-{income}-{status}"
                index += 1
columnName = columnName.rename({x: (x + 1) for x in range(groups)})
bedroom_predictions = bedroom_predictions.rename(columns=columnName.to_dict())
bedroom_predictions.insert(0, "Geography", df.iloc[4:, 0])
bedroom_predictions = bedroom_predictions.reset_index(drop=True)

# Create engine
# engine = create_engine(f'sqlite:///sources//previous_years//hart2021.db')
engine = create_engine(f'sqlite:///data_analysis//hart2021.db')
mapped_geo_code = pd.read_sql_table('geocodes_integrated', engine.connect())
partners = pd.read_sql_table('partners', engine.connect())
predictions_2031 = pd.read_sql_table('csd_hh_projections', engine.connect())
geo_codes = pd.read_sql_table('geocodes_integrated', engine.connect())
conn = engine.connect()


def geo_code_to_name(geo_code):
    val = geo_codes["Geo_Code"] == geo_code
    return geo_codes[val]["Geography"]


def convert_to_name(original_name):
    pattern = r"\(\d+\)"
    code = re.findall(pattern, original_name)[0]
    code = code[1:-1]  # strip brackets
    try:
        geo = mapped_geo_code[mapped_geo_code["Geo_Code"] == int(code)]["Geography"].item()
    except:
        return np.nan
    return geo


predictions_2031.iloc[:, 0] = predictions_2031.iloc[:, 0].apply(geo_code_to_name)
bedroom_predictions.iat[0, 0] = "Canada"
bedroom_predictions.iloc[1:, 0] = bedroom_predictions.iloc[1:, 0].apply(convert_to_name)
condition = bedroom_predictions.iloc[:, 0].notna()
bedroom_predictions = bedroom_predictions[condition]
bedroom_predictions = bedroom_predictions.reset_index(drop=True)


def bedroom_map(type, hh_size):
    if type == "Without children":
        return 1
    elif type == "With children":
        return hh_size - 1
    elif type == 'One-census-family household without additional persons: one-parent family':
        return hh_size
    elif type == 'One-census-family households with additional persons':
        return hh_size - 1
    elif type == 'One-census-family household with additional persons: one-parent family':
        return hh_size
    elif type == 'Multiple-census-family household':
        return hh_size - 2
    else:
        return hh_size


beds = [1, 2, 3, 4, 5]
income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']
# One for percent of the total population, then one for each income
output_columns = [f"2031 Projected bedroom need {type} bed {income}" for bed in beds for income in income_lv_list]
income_map = {
    'Households with household income 20% or under of area median household income (AMHI)': "20% or under of area median household income (AMHI)",
    'Households with household income 21% to 50% of AMHI': "21% to 50% of AMHI",
    'Households with household income 51% to 80% of AMHI': "51% to 80% of AMHI",
    'Households with household income 81% to 120% of AMHI': "81% to 120% of AMHI",
    'Households with household income 121% and over of AMHI': "121% or over of AMHI"
}
hh_pp_map = {
    '1 person HH': "1pp HH",
    '2 person HH': "2pp HH",
    '3 person HH': "3pp HH",
    '4 person HH': "4pp HH",
    '5 or more persons HH': "5pp HH",
}


def add_columns(row):
    geo = row["Geography"]
    projection_row = predictions_2031[predictions_2031["Geography"] == geo]
    if projection_row.empty:
        return pd.Series(dict([(None, val) for val in output_columns]))
    for income in AMHI:
        _df = pd.DataFrame(columns=hh_size)
        for size in hh_size:
            for type in hh_type:
                _df.at[type, size] = row[f"{size}-{type}-{income}-{'Households in core housing need status'}"]
        # Percent of each hh size @ that income level
        _df = _df.apply((lambda x: x / x.sum()))
        for hh in _df.columns:
            _df[hh] = projection_row[f"2031 Projected {income_map[income]} with income {hh_pp_map[hh]}"] * _df[hh]
        income


bedroom_predictions.apply(add_columns, axis=1)