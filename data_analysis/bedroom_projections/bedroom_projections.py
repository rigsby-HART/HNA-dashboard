import re
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

# Specify the file path of the CSV file
csv_file = 'data_analysis/bedroom_projections/2021_Unit_Mix_Consolidated.csv'  # Replace with the actual file path
households_by_income_and_size = pd.read_csv("data_analysis/bedroom_projections/households_by_income_and_size_2021.csv",
                                            encoding='latin-1')
engine = create_engine(f'sqlite:///data_analysis//hart2021.db')

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

prediction_data = pd.merge(prediction_data, households_by_income_and_size, on="Geography", how="left")

# Create engine
# engine = create_engine(f'sqlite:///sources//previous_years//hart2021.db')
mapped_geo_code = pd.read_sql_table('geocodes_integrated', engine.connect())
partners = pd.read_sql_table('partners', engine.connect())
predictions = pd.read_sql_table('csd_hh_projections', engine.connect())
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


predictions = pd.merge(predictions, geo_codes, on="Geo_Code", how="left")
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

current_year = 2021
prediction_year = current_year + 10

income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']
# One for percent of the total population, then one for each income
output_columns = [f"{prediction_year} Projected bedroom need {bed} bed {income}" for bed in beds for income in
                  income_lv_list] + \
                 [f"{prediction_year} Projected bedroom need delta {bed} bed {income}" for bed in beds for income in
                  income_lv_list]
income_map = {
    # 2021 data
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
    # 2016 data
    'Households with income 20% or under of area median household income (AMHI)': "20% or under of area median household income (AMHI)",
    'Households with income 21% to 50% of AMHI': "21% to 50% of AMHI",
    'Households with income 51% to 80% of AMHI': "51% to 80% of AMHI",
    'Households with income 81% to 120% of AMHI': "81% to 120% of AMHI",
    'Households with income 121% or more of AMHI': "121% or over of AMHI"
}

hh_pp_map = {
    # For 2021 data
    '1 person HH': "1pp HH",
    '2 persons HH': "2pp HH",
    '3 persons HH': "3pp HH",
    '4 persons HH': "4pp HH",
    '5 or more persons HH': "5pp HH",
    # For 2016 data
    '1 person': "1pp HH",
    '2 persons': "2pp HH",
    '3 persons': "3pp HH",
    '4 persons': "4pp HH",
    '5 or more persons household': "5pp HH",
}


def get_percentage(column: pd.Series):
    _sum = column.sum()
    if _sum == 0:
        return column
    return column / _sum


# Applies the methodology outlined by the HART page.
# Basically first calculate the percentage split by housing type, then assume that the percentage of current HHs
# extend to the future hhs as well.  As we already do a linear prediction on the population from 2016->2026, we have
# future population data.  Then multiply that value in.
np.seterr(all='raise')

def add_columns(row):
    # Region name
    geo = row["Geography"]
    # Get the data from Census CSV, if we don't have the data, drop the row
    projection_row = predictions[predictions["Geography"] == geo].head(1).squeeze()
    if projection_row.empty or np.isnan(projection_row.iat[0]):
        return pd.Series(dict([(val, 0) for val in output_columns]))
    # Generate the output row that we append into our current SQL table
    output = dict([(val, 0) for val in output_columns])
    # Temporary Storage for the HH type x HH size matrix
    df_prediction = pd.DataFrame(columns=hh_size)
    # Our 2021 bedroom count x income matrix but flattened
    bedrooms_2021 = dict(
        [(val, 0) for val in
         [f"{current_year} bedroom need {bed} bed {income}" for bed in beds for income in income_lv_list]])

    # Fill HH type x HH size matrix
    for i, income in enumerate(AMHI):
        for size in hh_size:
            for type in hh_type:
                df_prediction.at[type, size] = row[
                    f"{size}-{type}-{income}-{CHN_status[0]}"]
                # We're only interested in the total here, since we're trying to calculate

        # Percent of each hh size @ that income level

        df_prediction = df_prediction.apply(get_percentage)

        # Currently we are predicting using the 2031 projections by HH size & income level
        for hh in df_prediction.columns:
            df_prediction[hh] = projection_row[
                                    f"{prediction_year} Projected {hh_pp_map[hh]} with income {income_map[income]}"] * \
                                df_prediction[hh]

        # Iterate through housing type x hh size matrix at each income level to generate bedroom count x income matrix
        for y in range(len(df_prediction.index)):  # Index is Housing Type
            for x in range(len(df_prediction.columns)):  # Columns are HH size
                bed = bedroom_map(df_prediction.index[y], int(df_prediction.columns[x][0]))
                if bed < 1 or bed > 5:
                    continue
                    # This just means that the entry is empty anyways.  The census does a cross product of all
                    # household types and person counts.  This leads to impossible combinations (1 person hh with child)
                short_income = income_lv_list[i]
                if not (df_prediction.iat[y, x] == 0 or np.isnan(df_prediction.iat[y, x]) or np.isinf(df_prediction.iat[y, x])):
                    output[f"{prediction_year} Projected bedroom need {bed} bed {short_income}"] += df_prediction.iat[
                        y, x]
                # We don't have 2021 bedroom count, so I calculate it here, then do 2031 - the value we get
                bedrooms_2021[f"{current_year} bedroom need {bed} bed {short_income}"] += row[
                    f"{df_prediction.columns[x]}-{df_prediction.index[y]}-{income}-{CHN_status[0]}"]
    projection_AMHI = ["20% or under",
                       "21% to 50% of AMHI",
                       "51% to 80% of AMHI",
                       "81% to 120% of AMHI",
                       "121% or over of AMHI"]
    for bed in beds:
        for index, short_income in enumerate(income_lv_list):
            output[f"{prediction_year} Projected bedroom need delta {bed} bed {short_income}"] = \
                output[f"{prediction_year} Projected bedroom need {bed} bed {short_income}"] - \
                bedrooms_2021[f"{current_year} bedroom need {bed} bed {short_income}"]
    # scale output to match delta from household size projection
    for i, short_income in enumerate(income_lv_list):
        calculated_delta = sum(
            [output[f"{prediction_year} Projected bedroom need delta {bed} bed {short_income}"] for bed in beds])
        row = projection_row[projection_row.index.str.contains(projection_AMHI[i]) &
                             projection_row.index.str.contains("Delta") &
                             projection_row.index.str.contains("pp")]
        row = row.replace([np.inf, -np.inf, np.nan], np.nan).dropna()  # 2016 data has infs for some reason??????
        projected_delta = row.sum()
        if calculated_delta == 0:
            ratio = 0
        else:
            ratio = projected_delta / calculated_delta

        if np.isnan(ratio) or np.isinf(ratio):
            print("broke")
        for bed in beds:
            output[f"{prediction_year} Projected bedroom need delta {bed} bed {short_income}"] *= ratio
    output = pd.Series(output)
    return output


# If they already are in the database, replace them
if all(column in predictions.columns for column in output_columns):
    predictions = predictions.drop(output_columns, axis=1)
geo_label = prediction_data.columns[0]

bedroom_predictions = prediction_data.apply(add_columns, axis=1)
bedroom_predictions.insert(0, geo_label, prediction_data[geo_label])
# prediction_data[output_columns] = prediction_data.apply(add_columns, axis=1)
predictions = pd.merge(predictions, bedroom_predictions, on="Geography", how="left")
predictions = predictions.drop(["Region_Code", "Province_Code", "Geography", "Region", "Province"], axis=1)
sql = 'DROP TABLE IF EXISTS csd_hh_projections;'
result = engine.execute(sql)
predictions.to_sql("csd_hh_projections", engine, index=False)
