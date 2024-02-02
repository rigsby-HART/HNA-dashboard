import re
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# Specify the file path of the CSV file
csv_file = 'data_analysis/bedroom_projections/2021_Unit_Mix_Consolidated_canada.csv'  # Replace with the actual file path

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file, header=None, encoding='latin-1', dtype=str)

CHN_status = [x.strip() for x in df.iloc[0, 1:].unique()]
hh_type = [x.strip() for x in df.iloc[1, 1:].unique()]
AMHI = [x.strip() for x in df.iloc[2, 1:].unique()]
hh_size = [x.strip() for x in df.iloc[3, 1:].unique()]

numbers = df.iloc[4:, 1:].replace("x", "0").fillna(0).astype(int)

groups = len(CHN_status) * len(hh_type) * len(AMHI) * len(hh_size)
prediction_data = numbers

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
prediction_data = prediction_data.rename(columns=columnName.to_dict())
prediction_data.insert(0, "Geography", df.iloc[4:, 0])
prediction_data = prediction_data.reset_index(drop=True)

# Import the households by income and size
households_by_income_and_size = pd.read_csv("data_analysis/bedroom_projections/households_by_income_and_size.csv",
                                            encoding='latin-1')
prediction_data = pd.merge(prediction_data, households_by_income_and_size, on="Geography", how="left")

# Create engine
engine = create_engine(f'sqlite:///data_analysis//hart2016.db')
mapped_geo_code = pd.read_sql_table('geocodes_integrated', engine.connect())
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


# predictions_2031 = pd.merge(predictions_2031, geo_codes, on="Geo_Code", how="left")
prediction_data.iat[0, 0] = "Canada"
prediction_data.iloc[1:, 0] = prediction_data.iloc[1:, 0].apply(convert_to_name)
condition = prediction_data.iloc[:, 0].notna()
prediction_data = prediction_data[condition]
prediction_data = prediction_data.reset_index(drop=True)


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
output_columns = [f"bedroom need {bed} bed {income}" for bed in beds for income in income_lv_list]
income_map = {
    'Households with  income 20% or under of area median household income (AMHI)': "20% or under of area median household income (AMHI)",
    'Households with income 21% to 50% of AMHI': "21% to 50% of AMHI",
    'Households with income 51%  to 80% of AMHI': "51% to 80% of AMHI",
    'Households with income 81% to 120% of AMHI': "81% to 120% of AMHI",
    'Households with income 121% or over of AMHI': "121% or over of AMHI",
    'Households with household income 20% or under of area median household income (AMHI)': "20% or under of area median household income (AMHI)",
    'Households with household income 21% to 50% of AMHI': "21% to 50% of AMHI",
    'Households with household income 51% to 80% of AMHI': "51% to 80% of AMHI",
    'Households with household income 81% to 120% of AMHI': "81% to 120% of AMHI",
    'Households with household income 121% and over of AMHI': "121% or over of AMHI",
}
hh_pp_map = {
    '1 person HH': "1pp HH",
    '2 persons HH': "2pp HH",
    '3 persons HH': "3pp HH",
    '4 persons HH': "4pp HH",
    '5 or more persons HH': "5pp HH",
}


def get_percentage(column: pd.Series):
    _sum = column.sum()
    if _sum == 0:
        return column
    return column / _sum


# Calculate the number of missing bedrooms using the HNA methodology listed on the website
def add_columns(row):
    # Generate the output row that we append into our current SQL table
    output = dict([(val, 0) for val in output_columns])
    # Temporary Storage for the HH type x HH size matrix
    hh_type_size_matrix = pd.DataFrame(columns=hh_size)
    # Our current bedroom count x income matrix but flattened

    # Fill HH type x HH size matrix
    for i, income in enumerate(AMHI):
        for size in hh_size:
            for type in hh_type:
                hh_type_size_matrix.at[type, size] = row[
                    f"{size}-{type}-{income}-{CHN_status[1]}"]
                # We're only interested in the total here, since we're trying to calculate

        # Iterate through housing type x hh size matrix at each income level to generate bedroom count x income matrix
        for y in range(len(hh_type_size_matrix.index)):  # Index is Housing Type
            for x in range(len(hh_type_size_matrix.columns)):  # Columns are HH size
                bed = bedroom_map(hh_type_size_matrix.index[y], int(hh_type_size_matrix.columns[x][0]))
                if bed < 1 or bed > 5:
                    continue
                    # This just means that the entry is empty anyways.  The census does a cross product of all
                    # household types and person counts.  This leads to impossible combinations (1 person hh with child)
                short_income = income_lv_list[i]
                if not (hh_type_size_matrix.iat[y, x] == 0 or np.isnan(hh_type_size_matrix.iat[y, x])):
                    output[f"bedroom need {bed} bed {short_income}"] += hh_type_size_matrix.iat[y, x]

    output = pd.Series(output)
    return output


# If they already are in the database, replace them
geo_label = prediction_data.columns[0]

bedroom_predictions = prediction_data.apply(add_columns, axis=1)
bedroom_predictions.insert(0, geo_label, prediction_data[geo_label])
# prediction_data[output_columns] = prediction_data.apply(add_columns, axis=1)
# predictions_2031 = pd.merge(predictions_2031, bedroom_predictions, on="Geography", how="left")
# predictions_2031 = predictions_2031.drop(["Region_Code", "Province_Code", "Geography", "Region", "Province"], axis=1)
sql = 'DROP TABLE IF EXISTS bedrooms_2016;'
result = engine.execute(sql)
bedroom_predictions.to_sql("bedrooms_2016", engine, index=False)
