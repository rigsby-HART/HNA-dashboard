import pandas as pd

from helpers.create_engine import transit_distance


def get_quintile_info(geo_code) -> pd.DataFrame:
    quintiles = pd.Series([0, 0.005419, 0.013614, 0.026050, 0.052920, 1])

    if geo_code == 1:
        df_data = transit_distance
    else:
        df_data = transit_distance[transit_distance['CSDUID'].astype(str).str.startswith(str(geo_code))]
    # Calculate the population for each quintile and the total population
    df_output = pd.DataFrame(
        columns=["0 to 20%", "20 to 40%", "40 to 60%", "60 to 80%", "80 to 100%", "Total"],
        index=["Quintile Range", "Population"]
    )
    for i in range(1, 6):
        df_output.at["Population", df_output.columns[i-1]] \
            = df_data[(quintiles.iat[i] > df_data["prox_idx_transit"])
                      & (df_data["prox_idx_transit"] > quintiles.iat[i - 1])]["DBPOP"].sum()
    df_output.at["Population", "Total"] = df_output.loc["Population", :"80% to 100%"].sum()

    quintile_values = (quintiles.iloc[:-1].reset_index(drop=True).astype(str) + " - " + quintiles.iloc[1:].reset_index(drop=True).astype(str))
    quintile_values.at["Total"] = "0 - 1.0"
    quintile_values.index = df_output.columns
    df_output.loc["Quintile Range"] = quintile_values

    df_output = df_output.reset_index(names="")
    return df_output
