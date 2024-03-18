from dash import Output, callback, Input, State

from helpers.table_helper import change_download_title


# @callback(
#     Output('graph_ind', 'config'),
#     Input('main-area', 'data'),
#     Input('comparison-area', 'data'),
#     Input('year-comparison', 'data'),
#     Input('area-scale-store', 'data'),
#     State('url', 'search'),
#     Input('datatable-interactivity_ind', 'selected_columns'),
#     cache_args_to_ignore=[-1]
# )
# def change_download_names_p4_0(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
#     return change_download_title(geo, geo_c, year_comparison, scale,
#                        "Percentage of Indigenous Households in Core Housing Need, by Income Category")
#
# @callback(
#     Output('graph2_ind', 'config'),
#     Input('main-area', 'data'),
#     Input('comparison-area', 'data'),
#     Input('year-comparison', 'data'),
#     Input('area-scale-store', 'data'),
#     State('url', 'search'),
#     Input('datatable-interactivity_ind', 'selected_columns'),
#     cache_args_to_ignore=[-1]
# )
# def change_download_names_p4_1(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
#     return change_download_title(geo, geo_c, year_comparison, scale,
#                        "Percentage of Indigenous Households in Core Housing Need, by Income Category and HH Size")