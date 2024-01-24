# This file is used to remove any discrepancies within 2016 and 2021 files.
import pandas as pd


# Gets the first four rows of the dataframe, and returns each row as a unique list
def strip_column_names(df: pd.DataFrame):
    minority_status = [x for x in df.iloc[0, 1:].unique()]
    housing_type = [x for x in df.iloc[1, 1:].unique()]

    AMHI = [x for x in df.iloc[2, 1:].unique()]
    CHN_status = [x for x in df.iloc[3, 1:].unique()]

    return minority_status, housing_type, AMHI, CHN_status


# Lists the differences between the two dataframes
def list_differences(df_2016, df_2021):
    info_2016 = strip_column_names(df_2016)
    info_2021 = strip_column_names(df_2021)
    for i in range(len(info_2021)):
        col_0 = set(info_2016[i])
        col_1 = set(info_2021[i])

        # for col_0, col_1 in zip(info_2016[i], info_2021[i]):
        print("in 2016 but not 2021")
        print(list(col_0 - col_1))
        print("in 2021 but not 2016")
        print(list(col_1 - col_0))


map_2016_to_2021 = {
    "  5 or more persons household": "  5 or more persons HH",
    "  4 persons": "  4 persons HH",
    "  3 persons": "  3 persons HH",
    "  2 persons": "  2 persons HH",
    "  1 person": "  1 person HH",
    "Total - Private households by tenure including presence of mortgage payments and subsidized housing":
        "Total - Private households by tenure",
    "  Renter": "  Renter households  ",
    "  Owner": "  Owner households ",
    "Total - Household size": "Total - Private households by household size",
    "  Households examined for core housing need": "  Households examined for core housing need status",
    "    Households in core housing need": "    Households in core housing need status",
    "Total - Private households by household income proportion to AMHI_1":
        "Total - Private households by Household income as a proportion to Area Median Household Income (AMHI)_1",
    "  Households with income 20% or under of area median household income (AMHI)":
        "  Households with household income 20% or under of area median household income (AMHI)",
    '  Households with income 21% to 50% of AMHI': '  Households with household income 21% to 50% of AMHI',
    '  Households with income 51% to 80% of AMHI': '  Households with household income 51% to 80% of AMHI',
    '  Households with income 81% to 120% of AMHI': '  Households with household income 81% to 120% of AMHI',
    '  Households with income 121% or more of AMHI': '  Households with household income 121% and over of AMHI'

}
csv_2016 = 'data_analysis/renter_owner/2016_HNA_Consolidated.csv'
csv_2021 = 'data_analysis/renter_owner/2021_Consolidated_trans added.csv'

df_2016 = pd.read_csv(csv_2016, header=None, encoding='latin-1', dtype=str)
df_2021 = pd.read_csv(csv_2021, header=None, encoding='latin-1', dtype=str)
for key in map_2016_to_2021.keys():
    df_2016 = df_2016.replace(key, map_2016_to_2021[key])

df_2016.to_csv('data_analysis/renter_owner/2016_HNA_Consolidated_processed.csv', index=False, header=False)
# Read the CSV file into a DataFrame
