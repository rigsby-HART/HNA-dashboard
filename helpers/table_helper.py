import pandas as pd
import plotly.express as px

from dash import dcc
from helpers.create_engine import mapped_geo_code, income_partners_year, updated_csd_year
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
    row = income_partners_year[year].query('Geography == ' + f'"{geo}"')
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


def errorRegionTablePopulation(geo:str, year:int):
    geo_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Geo_Code'].tolist()[0]
    updated_csd_filtered = updated_csd_year[year].query('Geo_Code ==' + f"{geo_code_clicked}")
    hh_size = updated_csd_filtered['Total - Private households by household type including census family structure -   Households with income 20% or under of area median household income (AMHI) - Total - Household size'].empty
    if hh_size:
        fig = px.line(x=[f"No Data for {geo}, please try CD/Provincial level"],
                      y=[''])
        # No data for the selected region
        no_data = f"No Data for {geo}, please try CD/Provincial level"
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional, fig
    return False
def errorRegionFigure(geo: str, year: int):
    row = income_partners_year[year].query('Geography == ' + f'"{geo}"')
    row_exists, _ = row.shape
    if row_exists == 0:  # Most likely because the 2016 vs 2021 datasets differ
        fig = px.line(x=[f"No Data for {geo} in the {year} dataset"],
                      y=[''])
        return fig
    elif row["20% of AMHI"].item() is None:
        fig = px.line(x=[f"No Data for {geo}, please try CD/Provincial level"],
                      y=[''])
        return fig
    return None