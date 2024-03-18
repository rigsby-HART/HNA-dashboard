# Importing Libraries

import pandas as pd
import warnings
from dash import dcc, Input, Output, ctx, callback, State, html, register_page

from app_file import cache
from helpers.create_engine import income_ownership_year, default_year, default_value
from helpers.table_helper import query_table, get_language, change_download_title
from pages.renter_owner_helpers.page5_main import layout

register_page(__name__)
warnings.filterwarnings("ignore")

# Import helpers
import pages.renter_owner_helpers.income_categories                     # noqa
import pages.renter_owner_helpers.percentage_CHN_by_income              # noqa
import pages.renter_owner_helpers.percentage_CHN_by_HH_type             # noqa
import pages.renter_owner_helpers.housing_deficit                       # noqa
import pages.renter_owner_helpers.subsidized_income_categories                    # noqa
import pages.renter_owner_helpers.subsidized_percentage_CHN_by_income   # noqa
import pages.renter_owner_helpers.subsidized_percentage_CHN_by_HH_type  # noqa
import pages.renter_owner_helpers.subsidized_housing_deficit            # noqa
# import pages.renter_owner_helpers.download_text            # noqa


# Setting layout for dashboard

layout = layout(default_year)

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



# Plot/table generators and callbacks

@callback(
    Output("income-categories-title-page5", "children"),
    Output("percent-HH-CHN-title-page5", "children"),
    Output("percent-IC-HH-CHN-title-page5", "children"),
    Output("housing-deficit-page5", "children"),
    State('main-area', 'data'),
    State('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    State('area-scale-store', 'data'),
    Input('income-category-affordability-table-pg5', 'selected_columns'),
    State('url', 'search'),
    cache_args_to_ignore=[0, 1, 3, 4]
)
@cache.memoize()
def change_title_labels(geo, geo_c, year_comparison, scale, refresh, lang_query):
    language = get_language(lang_query)
    # change based off of url
    if year_comparison:
        original_year, compared_year = year_comparison.split("-")
        return (
            html.Strong(f'Income Categories and Affordable Shelter Costs, {compared_year} vs {original_year}'),
            html.Strong(
                f'Percentage of Households in Core Housing Need, by Income Category, {compared_year} vs {original_year}'),
            html.Strong(
                f'Percentage of Households in Core Housing Need, by Income Category and Housing Type, {compared_year} vs {original_year}'),
            html.Strong(f'{compared_year} vs {original_year} Affordable Housing Deficit'),
        )
    return (
        html.Strong(f'Income Categories and Affordable Shelter Costs, {default_year}'),
        html.Strong(f'Percentage of Households in Core Housing Need, by Income Category, {default_year}'),
        html.Strong(f'Percentage of Households in Core Housing Need, by Income Category and Housing Type, {default_year}'),
        html.Strong(f'{default_year} Affordable Housing Deficit'),
    )


@callback(
    Output("ov7-download-text-pg5", "data"),
    Input("ov7-download-csv-pg5", "n_clicks"),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    State('year-comparison', 'data'),
)
def func_ov7(n_clicks, geo, geo_c, year_comparison):
    if geo == None:
        geo = default_value

    if "ov7-download-csv-pg5" == ctx.triggered_id:
        # if year_comparison:
        #     original_year, compared_year = year_comparison.split("-")
        #     _, joined_df_geo = query_table(geo, int(original_year), income_ownership_year)
        #     _, joined_df_geo_c = query_table(geo, int(compared_year), income_ownership_year)
        #     joined_df_download = pd.concat([joined_df_geo, joined_df_geo_c])
        #     joined_df_download = joined_df_download.drop(columns=['pk_x', 'pk_y'])
        #     return dcc.send_data_frame(joined_df_download.to_csv, "result.csv")
        # else:
        _, joined_df_geo = query_table(geo, default_year, income_ownership_year)
        _, joined_df_geo_c = query_table(geo_c, default_year, income_ownership_year)
        joined_df_download = pd.concat([joined_df_geo, joined_df_geo_c])

        return dcc.send_data_frame(joined_df_download.to_csv, "result.csv")
