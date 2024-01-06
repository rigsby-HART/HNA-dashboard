# Importing Libraries

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import warnings
from dash import dcc, html, Input, Output, ctx, callback, State, register_page
from dash.dash_table.Format import Format, Scheme, Group
from plotly.subplots import make_subplots

from app_file import cache
from helpers.create_engine import income_indigenous_year, default_year, default_value
from helpers.style_helper import style_data_conditional, style_header_conditional
from helpers.table_helper import area_scale_comparison, area_scale_primary_only, error_indigenous_table, error_indigenous_figure, query_table, get_language
from helpers.localization import localization

from pages.page4_helpers.page4_main import layout

register_page(__name__)

# Setting layout for dashboard

layout = layout(default_year)


# Plot/table generators and callbacks
# Import helpers
import pages.page4_helpers.income_categories                     # noqa
import pages.page4_helpers.percentage_CHN_by_income_and_HH_size              # noqa
import pages.page4_helpers.housing_deficit             # noqa


# Download This Community


@callback(
    Output("ov7-download-text_ind", "data"),
    Input("ov7-download-csv_ind", "n_clicks"),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    State('year-comparison', 'data'),
    prevent_initial_call=True,
    cache_args_to_ignore=[0,2]
)
@cache.memoize()
def func_ov7(n_clicks, geo, geo_c, year_comparison):
    if geo == None:
        geo = default_value

    if "ov7-download-csv_ind" == ctx.triggered_id:
        if year_comparison:
            original_year, compared_year = year_comparison.split("-")
            _, joined_df_geo = query_table(geo, int(original_year), income_indigenous_year)
            _, joined_df_geo_c = query_table(geo, int(compared_year), income_indigenous_year)
            joined_df_download = pd.concat([joined_df_geo, joined_df_geo_c])
            joined_df_download = joined_df_download.drop(columns=['pk_x', 'pk_y'])

            return dcc.send_data_frame(joined_df_download.to_csv, "result.csv")
        else:
            _, joined_df_geo = query_table(geo, default_year, income_indigenous_year)
            _, joined_df_geo_c = query_table(geo, default_year, income_indigenous_year)
            joined_df_download_ind = pd.concat([joined_df_geo, joined_df_geo_c])
            joined_df_download_ind = joined_df_download_ind.drop(columns=['pk_x', 'pk_y'])

            return dcc.send_data_frame(joined_df_download_ind.to_csv, "result.csv")



@callback(
    Output("Income-Category-Indigenous-Title-page4", "children"),
    Output("CHN-IC-page4", "children"),
    Output("CHN-IC-HH-page4", "children"),
    Output("Deficit-page4", "children"),
    State('main-area', 'data'),
    State('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    State('area-scale-store', 'data'),
    Input('datatable-interactivity_ind', 'selected_columns'),
    State('url', 'search'),
    cache_args_to_ignore=[0, 1, 3, 4]
)
@cache.memoize()
def change_title_labels(geo, geo_c, year_comparison, scale, refresh, lang_query):
    language = get_language(lang_query)
    # change based off of url
    year = default_year
    if year_comparison:
        original_year, compared_year = year_comparison.split("-")

        return (
            html.Strong(f'Income Categories and Affordable Shelter Costs, {compared_year} vs {year}'),
            html.Strong(
                f'Percentage of Indigenous Households in Core Housing Need, by Income Category, {compared_year} vs {year}'),
            html.Strong(
                f'Percentage of Indigenous Households in Core Housing Need, by Income Category and HH Size, {compared_year} vs {year}'),
            html.Strong(f'{compared_year} vs {year} Affordable Housing Deficit for Indigenous Households'),
        )
    prediction_year = default_year + 10
    return (
        html.Strong(f'Income Categories and Affordable Shelter Costs, {year}'),
        html.Strong(f'Percentage of Indigenous Households in Core Housing Need, by Income Category, {year}'),
        html.Strong(
            f'Percentage of Indigenous Households in Core Housing Need, by Income Category and HH Size, {year}'),
        html.Strong(f'{year} Affordable Housing Deficit for Indigenous Households'),
    )
