from dash import Output, callback, Input, State, ctx

from app_file import cache
from helpers.create_engine import default_year
from helpers.table_helper import area_scale_primary_only, change_download_title
from pages.page3 import default_value


@callback(
    Output('graph-pg5', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table-pg5', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p5_0(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Percentage of Households in Core Housing Need, by Income Category")


@callback(
    Output('graph2-pg5', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table-pg5', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p5_1(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Percentage of Households in Core Housing Need, by Income Category and Housing Type")


@callback(
    Output('percent-HH-CHN-subsidized-graph-pg5', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table-pg5', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p5_2(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Percentage of Households in Core Housing Need for Subsidized vs Unsubsidized Renters, by Income Category")


@callback(
    Output('CHN-by-IC-HH-subsidized-graph-pg5', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table-pg5', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p5_3(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Percentage of Households in Core Housing Need for Subsidized vs Unsubsidized Renters, by Income Category and Housing Type")
