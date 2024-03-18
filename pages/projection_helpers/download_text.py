from dash import Output, callback, Input, State

from helpers.table_helper import change_download_title


@callback(
    Output('graph9', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('projected-hh-by-hh-size-income', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p3_0(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Projected Household Gain/Loss by Income")
@callback(
    Output('graph10', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('projected-hh-by-hh-size-income', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p3_1(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Projected Household Gain/Loss by Household Size")
@callback(
    Output('graph-h', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('projected-hh-by-hh-size-income', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p3_2(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Projected Household Gain/Loss by Household Size and Income")
@callback(
    Output('graph11', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('projected-hh-by-hh-size-income', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p3_3(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Projected Household Gain/Loss by Household Size and Income Delta")
@callback(
    Output('graph12', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('projected-hh-by-hh-size-income', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p3_4(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Projected Municipal Household Growth Rates by Income Category")
@callback(
    Output('graph13', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('projected-hh-by-hh-size-income', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
def change_download_names_p3_5(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Projected Community and Regional Household Growth Rates")