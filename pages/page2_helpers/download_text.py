from dash import Output, callback, Input, State

from helpers.table_helper import change_download_title


@callback(
    Output('graph', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p2_0(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Percentage of Households in Core Housing Need, by Income Category")
@callback(
    Output('graph2', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p2_1(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Percentage of Households in Core Housing Need, by Income Category and HH Size")
@callback(
    Output('graph5', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p2_2(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Percentage of Households in Core Housing Need, by Priority Population")
@callback(
    Output('graph6', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p2_3(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Percentage of Households in Core Housing Need, by Priority Population and Income Category")