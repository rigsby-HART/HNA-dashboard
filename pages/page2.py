# Importing Libraries
import warnings

import pandas as pd
from dash import dcc, Input, Output, ctx, callback, State, html, clientside_callback
from dash import register_page

from app_file import cache
from helpers.create_engine import partner_table, default_year, default_value
from helpers.paragraph_files import strings
from helpers.table_helper import query_table, area_scale_primary_only, change_download_title
from pages.page2_helpers.page2_main import layout

register_page(__name__)
warnings.filterwarnings("ignore")

# Setting layout for dashboard

layout = layout(default_year)

# Import helpers
import pages.page2_helpers.income_categories  # noqa
import pages.page2_helpers.percentage_CHN_by_income  # noqa
import pages.page2_helpers.percentage_CHN_by_income_and_HH_size  # noqa
import pages.page2_helpers.housing_deficit  # noqa
import pages.page2_helpers.housing_deficit_bedrooms  # noqa
import pages.page2_helpers.percentage_CHN_by_pp_income  # noqa
import pages.page2_helpers.percentage_CHN_by_priority_population  # noqa
# import pages.page2_helpers.download_text  # noqa



@callback(
    Output('graph', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input("main-area", "modified_timestamp"),
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
    Input("main-area", "modified_timestamp"),
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
    Input("main-area", "modified_timestamp"),
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
    Input("main-area", "modified_timestamp"),
)
def change_download_names_p2_3(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    return change_download_title(geo, geo_c, year_comparison, scale,
                       "Percentage of Households in Core Housing Need, by Priority Population and Income Category")




@callback(
    Output("income-categories-title-pg2", "children"),
    Output("percent-HH-CHN-title-pg2", "children"),
    Output("percent-IC-HH-CHN-title-pg2", "children"),
    Output("housing-deficit-pg2", "children"),
    Output("pct-pp-hh-chn-pg2", "children"),
    Output("pct-pp-ic-chn-pg2", "children"),
    Input('year-comparison', 'data'),
    Input("year-comparison", "modified_timestamp"),
    cache_args_to_ignore=[-1]
)
@cache.memoize()
def change_title_labels(year_comparison, refresh):
    # change based off of url
    if year_comparison:
        original_year, compared_year = year_comparison.split("-")
        return (
            html.Strong(f'Income Categories and Affordable Shelter Costs, {compared_year} vs {original_year}'),
            html.Strong(
                f'Percentage of Households in Core Housing Need, by Income Category, {compared_year} vs {original_year}'),
            html.Strong(
                f'Percentage of Households in Core Housing Need, by Income Category and HH Size, {compared_year} vs {original_year}'),
            html.Strong(f'{compared_year} vs {original_year} Affordable Housing Deficit'),
            html.Strong(
                f'Percentage of Households in Core Housing Need by Priority Population, {compared_year} vs {original_year}'),
            html.Strong(
                f'Percentage of Households in Core Housing Need by Priority Population and Income Category, {compared_year} vs {original_year}')
        )
    return (
        html.Strong(f'Income Categories and Affordable Shelter Costs, {default_year}'),
        html.Strong(f'Percentage of Households in Core Housing Need, by Income Category, {default_year}'),
        html.Strong(f'Percentage of Households in Core Housing Need, by Income Category and HH Size, {default_year}'),
        html.Strong(f'{default_year} Affordable Housing Deficit'),
        html.Strong(f'Percentage of Households in Core Housing Need by Priority Population, {default_year}'),
        html.Strong(
            f'Percentage of Households in Core Housing Need by Priority Population and Income Category, {default_year}')
    )


@callback(
    Output("percent-CHN-PP-description-pg2", "children"),
    Output("percent-CHN-PP-IC-description-pg2", "children"),
    Input('year-comparison', 'data'),
    Input("year-comparison", "modified_timestamp"),
    cache_args_to_ignore=[-1]
)
@cache.memoize()
def change_descriptions(year_comparison, refresh):
    # change based off of url
    if year_comparison:
        return (
            dcc.Markdown(
                strings['percentage-CHN-by-priority-population-page2'] +
                'Census Canada didn\'t collect data on transgender or non-binary households in 2016'
                , link_target="_blank"
            ),
            dcc.Markdown(
                strings['percentage-CHN-by-pp-income-page2'] +
                'Census Canada didn\'t collect data on transgender or non-binary households in 2016'
                , link_target="_blank"
            ),
        )
    return (
        dcc.Markdown(
            strings['percentage-CHN-by-priority-population-page2']
            , link_target="_blank"
        ),
        dcc.Markdown(
            strings['percentage-CHN-by-pp-income-page2']
            , link_target="_blank"
        ),
    )


clientside_callback(
    """
    async function (input) {
        if (input > 0) {
            console.log("Downloading page")
            html2canvas(document.body, { allowTaint: true , scrollX:0, scrollY: 0  }).then(function(canvas) {
                saveAs(canvas.toDataURL(), 'CoreHousingNeed.png');
            });
        }

        return "";
    }
    """,
    Output("placeholder-pg2", "children"),
    Input("ov7-download-csv", "n_clicks"),
)
@callback(
    Output("ov7-download-text", "data"),
    Input("ov7-download-csv", "n_clicks"),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    State('year-comparison', 'data'),
    cache_args_to_ignore=[0]
)
@cache.memoize()
def func_ov7(n_clicks, geo, geo_c, year_comparison):
    if geo == None:
        geo = default_value

    if "ov7-download-csv" == ctx.triggered_id:
        if year_comparison:
            original_year, compared_year = year_comparison.split("-")
            _, joined_df_geo = query_table(geo, int(original_year), partner_table)
            _, joined_df_geo_c = query_table(geo, int(compared_year), partner_table)
            joined_df_download = pd.concat([joined_df_geo, joined_df_geo_c])
            joined_df_download = joined_df_download.drop(columns=['pk_x', 'pk_y'])
            return dcc.send_data_frame(joined_df_download.to_csv, "result.csv")
        else:
            _, joined_df_geo = query_table(geo, default_year, partner_table)
            _, joined_df_geo_c = query_table(geo_c, default_year, partner_table)
            joined_df_download = pd.concat([joined_df_geo, joined_df_geo_c])
            joined_df_download = joined_df_download.drop(columns=['pk_x', 'pk_y'])

            return dcc.send_data_frame(joined_df_download.to_csv, "result.csv")
