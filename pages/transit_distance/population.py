import pandas as pd

from app_file import cache
from helpers.create_engine import transit_distance


@cache.memoize()
def get_quintile_info(geo_code, is_second=False) -> pd.DataFrame:
    # Change these numbers to adjust quantile ranges
    quintiles = pd.Series([0, 0.005419, 0.013614, 0.026050, 0.052920, 1])

    # Provided by stats canada
    # quintiles = pd.Series([0, 0.003, 0.007, 0.013, 0.028, 1])

    if geo_code == 1:
        df_data = transit_distance
    else:
        df_data = transit_distance[transit_distance['CSDUID'].astype(str).str.startswith(str(geo_code))]
    # Calculate the population for each quintile and the total population
    df_output = pd.DataFrame(
        columns=["0 to 20%", "20 to 40%", "40 to 60%", "60 to 80%", "80 to 100%", "No Transit Available", "Total"],
        index=["Quintile Range", "Population"]
    )
    for i in range(1, 6):
        df_output.at["Population", df_output.columns[i - 1]] \
            = df_data[(df_data["prox_idx_transit"] < quintiles.iat[i])
                      & (df_data["prox_idx_transit"] > quintiles.iat[i - 1])]["DBPOP"].sum()

    quintile_values = (quintiles.iloc[:-1].reset_index(drop=True).astype(str) + " - " + quintiles.iloc[1:].reset_index(
        drop=True).astype(str))
    quintile_values.at["No Transit Available"] = ""
    quintile_values.at["Total"] = "0 - 1.0"
    df_output.at["Population", "No Transit Available"] = df_data[df_data["prox_idx_transit"].isna()]["DBPOP"].sum()
    quintile_values.index = df_output.columns
    df_output.loc["Quintile Range"] = quintile_values
    df_output.at["Population", "Total"] = df_output.loc["Population", :"No Transit Available"].sum()

    # Craig wants it the other direction, no agreedge from me
    df_output = df_output.T
    df_output = df_output.reset_index(names="Quintile Percentages")

    if is_second:
        df_output = df_output.rename(
            columns={"Population": "Population "}
        )
    return df_output
