import math

import pandas as pd
import plotly.express as px

from typing import List, Dict
from dash import dcc
from helpers.create_engine import mapped_geo_code, income_partners_year, updated_csd_year, income_indigenous_year, \
    default_year, df_geo_list, mapped_geo_code_year
from helpers.style_helper import style_header_conditional


# Used when people click different region scales, eg Census subdivision vs Region/Territory
def area_scale_primary_only(geo, scale):
    if "to-geography-1" == scale:
        geo = geo
    elif "to-region-1" == scale:
        geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
    elif "to-province-1" == scale:
        geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
    return geo


# Same thing but when you have comparison selected
def area_scale_comparison(geo, geo_c, scale):
    if "to-geography-1" == scale:
        geo = geo
        geo_c = geo_c
    elif "to-region-1" == scale:
        geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
        geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c, :]['Region'].tolist()[0]
    elif "to-province-1" == scale:
        geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
        geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c, :]['Province'].tolist()[0]
    return geo, geo_c


def storage_variables():
    return [
        dcc.Store(id='area-scale-store', storage_type='local'),
        dcc.Store(id='main-area', storage_type='local'),
        dcc.Store(id='comparison-area', storage_type='local'),
        dcc.Store(id='year-comparison', storage_type='local'),
    ]


def errorRegionTable(geo: str, year: int):
    try:
        geo, row = queryTable(geo, year, income_partners_year)
    except:
        no_data = f"No Data for {geo}, in the {year} dataset"
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional
    row_exists, _ = row.shape
    if row_exists == 0:  # Most likely because the 2016 vs 2021 datasets differ
        no_data = f"No Data for {geo}, in the {year} dataset"
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional
    elif row["20% of AMHI"].item() is None:
        # No data for the selected region
        no_data = f"No Data for {geo}, please try CD/Provincial level"
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional
    return None


def errorRegionTablePopulation(geo: str, year: int, no_cd=False):
    geo_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Geo_Code'].tolist()[0]
    updated_csd_filtered = updated_csd_year[year].query('Geo_Code ==' + f"{geo_code_clicked}")
    hh_size = updated_csd_filtered[
        'Total - Private households by household type including census family structure -   Households with income 20% or under of area median household income (AMHI) - Total - Household size'].empty
    if hh_size:
        # No data for the selected region
        if no_cd:
            fig = px.line(x=[f"No Data for {geo}, please try another CSD"],
                          y=[''])
            no_data = f"No Data for {geo}, please try another CSD"
        else:
            fig = px.line(x=[f"No Data for {geo}, please try CD/Provincial level"],
                          y=[''])
            no_data = f"No Data for {geo}, please try CD/Provincial level"
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional, fig
    return False


def errorIndigenousTable(geo: str, year: int):
    try:
        geo, joined_df_filtered = queryTable(geo, year, income_indigenous_year)
    except:
        no_data = f"No Data for {geo}, please try CD/Provincial level"
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional

    query = joined_df_filtered[(f'Aboriginal household status-Total - Private households by tenure including presence '
                                f'of mortgage payments and subsidized housing-Households with income 21% to 50% of '
                                f'AMHI-Households examined for core housing need')]
    if query.empty or query.item() is None or math.isnan(query.item()):
        no_data = f"No Data for {geo}, please try CD/Provincial level"
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional

def errorRegionFigure(geo: str, year: int):
    try:
        geo, row = queryTable(geo, year, income_partners_year)
    except:
        fig = px.line(x=[f"No Data for {geo} in the {year} dataset"],
                      y=[''])
        return fig
    row_exists, _ = row.shape
    if row_exists == 0:  # Most likely because the 2016 vs 2021 datasets differ
        fig = px.line(x=[f"No Data for {geo} in the {year} dataset"],
                      y=[''])
        return fig
    elif row["20% of AMHI"].item() is None:
        fig = px.line(x=[f"No Data for {geo}, please try CD/Provincial level"],
                      y=[''])
        return fig



def errorIndigenousFigure(geo: str, year: int):
    try:
        geo, joined_df_filtered = queryTable(geo, year, income_indigenous_year)
    except:
        fig = px.line(x=[f"No Data for {geo} in the {year} dataset"],
                      y=[''])
        return fig
    query = joined_df_filtered[(f'Aboriginal household status-Total - Private households by tenure including presence '
                                f'of mortgage payments and subsidized housing-Households with income 21% to 50% of '
                                f'AMHI-Households examined for core housing need')]
    if query.empty or query.item() is None or math.isnan(query.item()):
        fig = px.line(x=[f"No Data for {geo}, please try CD/Provincial level"],
                      y=[''])
        return fig

# Every year has varying names, so this converts between them
def queryTable(geo: str, year: int, df_list, source_year=default_year):
    if year == 2021:
        return geo, df_list[year].query('Geography == ' + f'"{geo}"')
    if year == 2016:
        # Takes the name from 2021 (or whatever source year is), converts to geo code, then converts to year
        geo_code = mapped_geo_code_year[source_year].query('Geography == ' + f'"{geo}"')["Geo_Code"].item()
        geo_name = mapped_geo_code_year[year].query(f'Geo_Code == {geo_code}')["Geography"].item()
        return geo_name, df_list[year].query('Geography == ' + f'"{geo_name}"')


