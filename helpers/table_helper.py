import math
import re

import pandas as pd
import plotly.express as px
from dash import dcc

from helpers.create_engine import mapped_geo_code, partner_table, updated_csd_year, income_indigenous_year, \
    default_year, mapped_geo_code_year
from helpers.localization import localization
from helpers.style_helper import style_header_conditional


# Used when people click different region scales, eg Census subdivision vs Region/Territory
def area_scale_primary_only(geo, scale):
    if "to-geography-1" == scale:
        geo = geo
    elif "to-region-1" == scale:
        geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Region'].tolist()[0]
    elif "to-province-1" == scale:
        geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Province'].tolist()[0]
    if geo is None:
        geo = "Canada"
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
    if geo is None:
        geo = "Canada"
    if geo_c is None:
        geo_c = "Canada"
    return geo, geo_c


def storage_variables():
    return [
        dcc.Store(id='area-scale-store', storage_type='local'),
        dcc.Store(id='main-area', storage_type='local'),
        dcc.Store(id='comparison-area', storage_type='local'),
        dcc.Store(id='year-comparison', storage_type='local'),
    ]


def error_region_table(geo: str, year: int, language: str):
    try:
        geo, row = query_table(geo, year, partner_table)
    except:
        no_data = localization[language]["No Data for {geo}, in the {year} dataset"].format(geo=geo, year=year)
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional
    row_exists, _ = row.shape
    if row_exists == 0:  # Most likely because the 2016 vs 2021 datasets differ
        no_data = localization[language]["No Data for {geo}, in the {year} dataset"].format(geo=geo, year=year)
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional
    elif row["20% of AMHI"].item() is None or row['Median income of household ($)'].item() is None:
        # No data for the selected region
        no_data = localization[language]["No Data for {geo}, please try CD/Provincial level"].format(geo=geo)
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional
    return None


def error_region_table_population(geo: str, year: int, language: str, no_cd=False):
    geo_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Geo_Code'].tolist()[0]
    updated_csd_filtered = updated_csd_year[year].query('Geo_Code ==' + f"{geo_code_clicked}")
    hh_size = updated_csd_filtered[
        ('Total - Private households by household type including census family structure -   Households with income '
         '20% or under of area median household income (AMHI) - Total - Household size')].empty
    if hh_size:
        # No data for the selected region
        if no_cd:
            fig = px.line(x=[localization[language]["No Data for {geo}, please try another CSD"].format(geo=geo)],
                          y=[''])
            no_data = localization[language]["No Data for {geo}, please try another CSD"].format(geo=geo)
        else:
            fig = px.line(
                x=[localization[language]["No Data for {geo}, please try CD/Provincial level"].format(geo=geo)],
                y=[''])
            no_data = localization[language]["No Data for {geo}, please try CD/Provincial level"].format(geo=geo)
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional, fig
    return False


def error_indigenous_table(geo: str, year: int, language="en"):
    try:
        geo, joined_df_filtered = query_table(geo, year, income_indigenous_year)
    except:
        no_data = localization[language]["No Data for {geo}, in the {year} dataset"].format(geo=geo, year=year)
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional

    query = joined_df_filtered[(f'Aboriginal household status-Total - Private households by tenure including presence '
                                f'of mortgage payments and subsidized housing-Households with income 21% to 50% of '
                                f'AMHI-Households examined for core housing need')]
    if query.empty or query.item() is None or math.isnan(query.item()):
        no_data = f"No Data for {geo}, please try CD/Provincial level"
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional


def error_region_figure(geo: str, year: int, language: str):
    try:
        geo, row = query_table(geo, year, partner_table)
    except:
        fig = px.line(x=[localization[language]["No Data for {geo}, in the {year} dataset"].format(geo=geo, year=year)],
                      y=[''])
        return fig
    row_exists, _ = row.shape
    if row_exists == 0:  # Most likely because the 2016 vs 2021 datasets differ
        fig = px.line(x=[localization[language]["No Data for {geo}, in the {year} dataset"].format(geo=geo, year=year)],
                      y=[''])
        return fig
    elif row["20% of AMHI"].item() is None:
        fig = px.line(x=[localization[language]["No Data for {geo}, please try CD/Provincial level"].format(geo=geo)],
                      y=[''])
        return fig


def error_indigenous_figure(geo: str, year: int, language: str):
    try:
        geo, joined_df_filtered = query_table(geo, year, income_indigenous_year)
    except:
        fig = px.line(x=[localization[language]["No Data for {geo}, in the {year} dataset"].format(geo=geo, year=year)],
                      y=[''])
        return fig
    query = joined_df_filtered[(f'Aboriginal household status-Total - Private households by tenure including presence '
                                f'of mortgage payments and subsidized housing-Households with income 21% to 50% of '
                                f'AMHI-Households examined for core housing need')]
    if query.empty or query.item() is None or math.isnan(query.item()):
        fig = px.line(x=[localization[language]["No Data for {geo}, please try CD/Provincial level"].format(geo=geo)],
                      y=[''])
        return fig


# Every year has varying names, so this converts between them
def query_table(geo: str, year: int, df_list, source_year=default_year):
    if year == 2021:
        return geo, df_list[year].query('Geography == ' + f'"{geo}"')
    if year == 2016:
        # Takes the name from 2021 (or whatever source year is), converts to geo code, then converts to year
        geo_code = mapped_geo_code_year[source_year].query('Geography == ' + f'"{geo}"')["Geo_Code"].item()
        geo_name = mapped_geo_code_year[year].query(f'Geo_Code == {geo_code}')["Geography"].item()
        return geo_name, df_list[year].query('Geography == ' + f'"{geo_name}"')


def query_table_owner(geo: str, year: int, df_list, source_year=default_year, owner=True):
    if year == 2021:
        return geo, df_list[year].query('Geography == ' + f'"{geo}"')
    if year == 2016:
        # Takes the name from 2021 (or whatever source year is), converts to geo code, then converts to year
        geo_code = mapped_geo_code_year[source_year].query('Geography == ' + f'"{geo}"')["Geo_Code"].item()
        geo_name = mapped_geo_code_year[year].query(f'Geo_Code == {geo_code}')["Geography"].item()
        return geo_name, df_list[year].query('Geography == ' + f'"{geo_name}"')


def change_download_title(geo: str, geo_c: str, year_comparison: str, scale: str, title: str):
    # When no area is selected
    if geo == None and geo_c != None:
        geo = geo_c
    elif geo == None and geo_c == None:
        geo = "Canada"

    # Area Scaling up/down when user clicks area scale button on page 1
    geo = area_scale_primary_only(geo, scale)
    if geo_c:
        geo = geo + "vs" + geo_c
    config = {
        'displayModeBar': True, 'displaylogo': False,
        'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale',
                                   'resetScale'],
        "toImageButtonOptions": {
            "filename": 'la mao'
        }
    }

    year = default_year
    if year_comparison:
        original_year, compared_year = year_comparison.split("-")
        year = f"{compared_year} vs {original_year}"

    return {**config, 'toImageButtonOptions': {'filename': f'{geo}_{title}_{year}'}}


def get_language(lang_query: str):
    match = re.search(r'\blang=(.+)', lang_query)
    output = match.group(1) if match else "en"
    if output not in localization.keys():
        return "en"
    return output


default_value = 'Canada'
