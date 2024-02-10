# Importing Libraries
from dash import register_page
from helpers.create_engine import default_year
from pages.projection_helpers.page3_main import layout

register_page(__name__)
# Default selected area
default_value = 'Canada'

# Setting layout for dashboard
layout = layout(default_year)

# Import all callbacks for table updates and generation
# Callbacks are used w/o us calling them explicitly
# noqa pervents pycharm from marking these as unused
import pages.projection_helpers.municipal_vs_regional_hh # noqa
import pages.projection_helpers.municipal_vs_regional_income # noqa
import pages.projection_helpers.projections_hh_delta # noqa
import pages.projection_helpers.projections_by_hh_size_and_IC # noqa
# import pages.projection_helpers.bedroom_projections # noqa
# import pages.projection_helpers.bedroom_projections_delta # noqa
import pages.projection_helpers.projections_by_household_size # noqa
import pages.projection_helpers.projections_by_income_category # noqa


# 
# @callback(
#     Output("HH-IC-page3", "children"),
#     Output("HH-size-page3", "children"),
#     Output("HH-size-IC-page3", "children"),
#     Output("HH-gain-page3", "children"),
#     Output("growth-IC-page3", "children"),
#     Input('year-comparison', 'data'),
#     Input('datatable9-interactivity', 'selected_columns'),
#     State('url', 'search'),
# )
# def change_title_labels(year_comparison, _, lang_query):
#     language = get_language(lang_query)
#     # change based off of url
#     year = default_year
#     if year_comparison:
#         original_year, compared_year = year_comparison.split("-")
#         prediction_year = int(original_year) + 10
#         compared_prediction = int(compared_year) + 10
#
#         return (
#             html.Strong(f'{compared_prediction} vs {prediction_year} Household Projections by Income Category'),
#             html.Strong(f'{compared_prediction} vs {prediction_year} Household Projections by Household Size'),
#             html.Strong(f'{compared_prediction} vs {prediction_year} Projected Households by Household Size and Income Category'),
#             html.Strong(f'{compared_prediction} vs {prediction_year} Projected Household Gain/Loss ({compared_year} to {compared_prediction} vs {year} to {prediction_year})'),
#             html.Strong(f'{compared_prediction} vs {prediction_year} Projected Municipal vs Regional Household Growth Rates by Income Category')
#         )
#     prediction_year = default_year + 10
#     return (
#         html.Strong(f'{prediction_year} Household Projections by Income Category'),
#         html.Strong(f'{prediction_year} Household Projections by Household Size'),
#         html.Strong(f'{prediction_year} Projected Households by Household Size and Income Category'),
#         html.Strong(f'{prediction_year} Projected Household Gain/Loss ({year} to {prediction_year})'),
#         html.Strong(f'{prediction_year} Projected Municipal vs Regional Household Growth Rates by Income Category')
#     )
#
# 
# @callback(
#     Output("HH-IC-description-page3", "children"),
#     Output("HH-IC-graph-description-page3", "children"),
#     Output("HH-size-description-page3", "children"),
#     Output("HH-size-graph-description-page3", "children"),
#     Output("HH-size-IC-description-page3", "children"),
#     Output("HH-size-IC-graph-description-page3", "children"),
#     Output("HH-gain-description-page3", "children"),
#     Output("HH-gain-graph-description-page3", "children"),
#     Input('year-comparison', 'data'),
#     Input('datatable9-interactivity', 'selected_columns'),
#     State('url', 'search'),
# )
# def change_description_labels(year_comparison, _, lang_query):
#     language = get_language(lang_query)
#     # change based off of url
#     if year_comparison:
#         original_year, compared_year = year_comparison.split("-")
#         prediction_year = int(original_year) + 10
#         compared_prediction = int(compared_year) + 10
#         return (
#             html.H6(
#                 f'The following table shows the total number of households in {compared_year} and {original_year}, '
#                 f'for each household income category, as well as the projected gain ('
#                 f'positive) or loss (negative) of households between {compared_year}, '
#                 f'{original_year} and 10 years in the future by applying the percentage change from '
#                 f'2006 census data, to current households.'),
#             html.H6(
#                 f'The following graph illustrates the above table, displaying the '
#                 f'total number of households in {compared_year} and {original_year}, for each income category, '
#                 f'with the projected gain of households between these years and '
#                 f'{compared_prediction} and {prediction_year} stacked on top, and the projected loss of '
#                 f'household stacked underneath.'),
#             html.H6(
#                 f'The following table shows the total number of households in {compared_year} and {original_year}, '
#                 f'for each household size category, as well as the projected gain ('
#                 f'positive) or loss (negative) of households over the period between {compared_year}, '
#                 f'{original_year} and 10 years in the future by applying the percentage change from '
#                 f'2006 census data, to current households.'),
#             html.H6(
#                 f'The following graph illustrates the above table, displaying the '
#                 f'total number of households in {compared_year} and {original_year}, for each size of household, '
#                 f'with the projected gain of households between {compared_year} and {original_year} '
#                 f'and in ten years stacked on top, and the projected loss of '
#                 f'household stacked underneath.'),
#             html.H6(
#                 f'The following table shows the projected total number of households in '
#                 f'{compared_prediction} and {prediction_year} by household size and income category.'),
#             html.H6(
#                 f'The following graph illustrates the above table, displaying the '
#                 f'projected total number of households in {compared_prediction} and {prediction_year} by '
#                 f'household size and income category. Each bar is broken out by the '
#                 f'projected number of households within each income category.'),
#             html.H6(
#                 f'The following table shows the projected gain or loss of households '
#                 f'by household size and income. These values represent projections '
#                 f'for the period between {compared_year} and {original_year} and 10 years in the future.'),
#             html.H6(
#                 f'The following graph illustrates the above table, displaying the '
#                 f'projected gain or loss of households between {compared_year} and {original_year} and '
#                 f'in ten years for each size of household. Each bar is broken '
#                 f'out by the projected number of households within each income '
#                 f'category. Projected loss of households are stacked underneath.'),
#         )
#
#     prediction_year = int(default_year) + 10
#     compared_prediction = int(default_year) + 10
#     year = default_year
#     year_minus_15 = year-15
#     return (
#         html.H6(
#             f'The following table shows the total number of households in {year}, '
#             f'for each household income category, as well as the projected gain ('
#             f'positive) or loss (negative) of households over the period between '
#             f'{year} and {prediction_year} by applying the percentage change from '
#             f'{year_minus_15}-{year}, to {year} households.'),
#         html.H6(
#             f'The following graph illustrates the above table, displaying the '
#             f'total number of households in {year}, for each income category, '
#             f'with the projected gain of households between {year} and '
#             f'{prediction_year} stacked on top, and the projected loss of '
#             f'household stacked underneath.'),
#         html.H6(
#             f'The following table shows the total number of households in {year}, '
#             f'for each household size category, as well as the projected gain ('
#             f'positive) or loss (negative) of households over the period between '
#             f'{year} and {prediction_year} by applying the percentage change from '
#             f'{year_minus_15}-{year}, to {year} households.'),
#         html.H6(
#             f'The following graph illustrates the above table, displaying the '
#             f'total number of households in {year}, for each size of household, '
#             f'with the projected gain of households between {year} and '
#             f'{prediction_year} stacked on top, and the projected loss of '
#             f'household stacked underneath.'),
#         html.H6(
#             f'The following table shows the projected total number of households in '
#             f'{prediction_year} by household size and income category.'),
#         html.H6(
#             f'The following graph illustrates the above table, displaying the '
#             f'projected total number of households in {prediction_year} by '
#             f'household size and income category. Each bar is broken out by the '
#             f'projected number of households within each income category.'),
#         html.H6(
#             f'The following table shows the projected gain or loss of households '
#             f'by household size and income. These values represent projections '
#             f'for the period between {year} and {prediction_year}.'),
#         html.H6(
#             f'The following graph illustrates the above table, displaying the '
#             f'projected gain or loss of households between {year} and '
#             f'{prediction_year} for each size of household. Each bar is broken '
#             f'out by the projected number of households within each income '
#             f'category. Projected loss of households are stacked underneath.'),
#     )
#
# # Split into two for easier debugging and reading
# 
# @callback(
#     Output("growth-IC-description-page3", "children"),
#     Output("growth-IC-description2-page3", "children"),
#     Output("growth-IC-description3-page3", "children"),
#     Output("growth-IC-description4-page3", "children"),
#     Input('year-comparison', 'data'),
#     Input('datatable9-interactivity', 'selected_columns'),
#     State('url', 'search'),
# )
# def change_description_labels_2(year_comparison, _, lang_query):
#     language = get_language(lang_query)
#     # change based off of url
#     if year_comparison:
#         original_year, compared_year = year_comparison.split("-")
#         prediction_year = int(original_year) + 10
#         compared_prediction = int(compared_year) + 10
#         return (
#             html.H6(
#                 f'The following table illustrates the projected household growth '
#                 f'rates between {compared_year}, {original_year} and in ten years in the community and '
#                 f'{compared_prediction}, {prediction_year} in the surrounding region for each income category.'),
#             html.H6(
#                 f'The following graph illustrates the above table, displaying the '
#                 f'projected household growth rates between {compared_year}, {original_year} and in '
#                 f'{compared_prediction}, {prediction_year} in the community and in the community and surrounding region'
#                 f' for each income category.'),
#             html.H6(
#                 f'The following table illustrates the projected household growth '
#                 f'rates between {compared_year}, {original_year} and in {compared_prediction}, '
#                 f'{prediction_year} in the community and surrounding region for each household size.'),
#             html.H6(
#                 f'The following graph illustrates the above table, displaying the '
#                 f'projected household growth rates {compared_year}, {original_year} and in {compared_prediction}, '
#                 f'{prediction_year} in the community and surrounding region for each income category.')
#         )
#
#     prediction_year = int(default_year) + 10
#     compared_prediction = int(default_year) + 10
#     year = default_year
#     year_minus_15 = year-15
#     return (
#         html.H6(
#             f'The following table illustrates the projected household growth '
#             f'rates between {year} and {prediction_year} in the community and '
#             f'surrounding region for each income category.'),
#         html.H6(
#             f'The following graph illustrates the above table, displaying the '
#             f'projected household growth rates between {year} and '
#             f'{prediction_year} in the community and surrounding region for each '
#             f'income category.'),
#         html.H6(
#             f'The following table illustrates the projected household growth '
#             f'rates between {year} and {prediction_year} in the community and '
#             f'surrounding region for each household size.'),
#         html.H6(
#             f'The following graph illustrates the above table, displaying the '
#             f'projected household growth rates between {year} and '
#             f'{prediction_year} in the community and surrounding region for each '
#             f'income category.')
#     )