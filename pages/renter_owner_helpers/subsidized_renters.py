# Income Categories and Affordable Shelter Costs, 2021
import pandas as pd
from dash import Output, Input, State, callback

from app_file import cache
from helpers.create_engine import default_year, default_value, income_ownership_year
from helpers.style_helper import style_data_conditional, style_header_conditional, columns_color_fill, \
    comparison_font_size
from helpers.table_helper import query_table, get_language, area_scale_primary_only, area_scale_comparison, \
    error_region_table

x_base = ['Very Low Income',
          'Low Income',
          'Moderate Income',
          'Median Income',
          'High Income',
          ]

x_columns = ['Rent 20% of AMHI',
             'Rent 50% of AMHI',
             'Rent 80% of AMHI',
             'Rent 120% of AMHI',
             'Rent 120% of AMHI'
             ]

amhi_range = ['20% or under of AMHI', '21% to 50% of AMHI', '51% to 80% of AMHI', '81% to 120% of AMHI',
              '121% and more of AMHI']


# Setting a default plot and table which renders before the dashboard is fully loaded

income_ct = [x + f" ({a})" for x, a in zip(x_base, amhi_range)]

# Table generator
def table_amhi_shelter_cost(geo: str, is_second: bool, year: int = default_year):
    geo, joined_df_filtered = query_table(geo, year, income_ownership_year)

    portion_of_renter_hh = []
    for x in x_base:
        portion_of_renter_hh.append(
            round(joined_df_filtered[f'Percent of Renter households HH that are in {x}'].tolist()[0] * 100, 2))
    portion_of_subsidized_renter_hh = []
    for x in x_base:
        portion_of_subsidized_renter_hh.append(
            round(joined_df_filtered[f'Percent of Subsidized Renter households HH that are in {x}'].tolist()[0] * 100, 2))

    amhi_list = []
    for a in amhi_range:
        amhi_list.append(joined_df_filtered[a].tolist()[0])

    shelter_range = ['20% or under of AMHI.1', '21% to 50% of AMHI.1', '51% to 80% of AMHI.1', '81% to 120% of AMHI.1',
                     '121% and more of AMHI.1']
    shelter_list = []
    for s in shelter_range:
        shelter_list.append(joined_df_filtered[s].tolist()[0])

    joined_df_geo_index = joined_df_filtered.set_index('Geography')

    median_income = '${:0,.0f}'.format(float(joined_df_geo_index.at[geo, 'Median income of household ($)']))

    median_rent = '${:0,.0f}'.format(float(joined_df_geo_index.at[geo, 'Rent AMHI']))

    if not is_second:
        table = pd.DataFrame(
            {'Income Category': income_ct, '% of Rental HHs': portion_of_renter_hh,
             '% of Subsidized Rental HHs': portion_of_subsidized_renter_hh, 'Annual HH Income': amhi_list,
             'Affordable Shelter Cost (2020 CAD$)': shelter_list})
        table['% of Rental HHs'] = table['% of Rental HHs'].astype(str) + '%'
        table['% of Subsidized Rental HHs'] = table['% of Subsidized Rental HHs'].astype(str) + '%'
    else:
        table = pd.DataFrame(
            {'Income Category': income_ct, '% of Rental HHs ': portion_of_renter_hh,
             '% of Subsidized Rental HHs ': portion_of_subsidized_renter_hh, 'Annual HH Income ': amhi_list,
             'Affordable Shelter Cost (2020 CAD$) ': shelter_list})
        table['% of Rental HHs '] = table['% of Rental HHs '].astype(str) + '%'
        table['% of Subsidized Rental HHs '] = table['% of Subsidized Rental HHs '].astype(str) + '%'

    return table, median_income, median_rent


# Callback logic for the table update


@callback(
    Output('income-category-subsidized-table-pg5', 'columns'),
    Output('income-category-subsidized-table-pg5', 'data'),
    Output('income-category-subsidized-table-pg5', 'style_data_conditional'),
    Output('income-category-subsidized-table-pg5', 'style_cell_conditional'),
    Output('income-category-subsidized-table-pg5', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('income-category-subsidized-table-pg5', 'selected_columns'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    cache_args_to_ignore=[3]
)
@cache.memoize()
def update_table1(geo, geo_c, year_comparison: str, selected_columns, scale, lang_query):
    # Single area mode
    language = get_language(lang_query)
    if not year_comparison and (geo == geo_c or geo_c is None or (geo is None and geo_c is not None)):

        # When no area is selected
        if geo is None and geo_c is not None:
            geo = geo_c
        elif geo is None and geo_c is None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        geo = area_scale_primary_only(geo, scale)

        # Generating table
        if error_region_table(geo, default_year, language):
            return error_region_table(geo, default_year, language)
        table, median_income, median_rent = table_amhi_shelter_cost(geo, False)

        # Generating callback output to update table
        col_list = []
        #
        median_row = ['Area Median Household Income', "", "", median_income, median_rent]
        for i, j in zip(list(table.columns), median_row):
            col_list.append({"name": [geo, i, j], "id": i})

        style_cell_conditional = [
                                     {
                                         'if': {'column_id': c},
                                         'backgroundColor': columns_color_fill[1],

                                         # "maxWidth" : "100px"
                                     } for c in table.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': table.columns[0]},
                                         'backgroundColor': columns_color_fill[0],

                                     }
                                 ] + [
                                     {
                                         'if': {'column_id': 'Affordable Shelter Cost (2020 CAD$)'},
                                         'maxWidth': "120px",

                                     }
                                 ] + [
                                     {
                                         'if': {'column_id': 'Income Category'},
                                         'maxWidth': "120px",
                                         'width': '35%'

                                     }
                                 ]
        return col_list, table.to_dict(
            'records'), style_data_conditional, style_cell_conditional, style_header_conditional

    # Comparison mode
    else:
        if year_comparison:
            geo = area_scale_primary_only(geo, scale)
            original_year, compared_year = year_comparison.split("-")
        # Area Scaling up/down when user clicks area scale button on page 1
        else:
            geo, geo_c = area_scale_comparison(geo, geo_c, scale)
            original_year, compared_year = default_year, default_year

        # Main Table

        # Generating main table
        if year_comparison:
            if error_region_table(geo, int(compared_year), language):
                return error_region_table(geo, int(compared_year), language)
        else:
            if error_region_table(geo, default_year, language):
                return error_region_table(geo, default_year, language)
        table, median_income, median_rent = (
            table_amhi_shelter_cost(geo, False, int(compared_year)) if year_comparison else
            table_amhi_shelter_cost(geo, False)
        )
        # Comparison Table

        if geo_c is None:
            geo_c = geo

        # Generating comparison table
        if year_comparison:
            if error_region_table(geo, default_year, language):
                return error_region_table(geo, default_year, language)
        else:
            if error_region_table(geo_c, default_year, language):
                return error_region_table(geo_c, default_year, language)
        table_c, median_income_c, median_rent_c = (
            table_amhi_shelter_cost(geo, True) if year_comparison else
            table_amhi_shelter_cost(geo_c, True)
        )
        # Merging main and comparison table
        table_j = table.merge(table_c, how='left', on='Income Category')

        # Generating Callback output

        col_list = []

        median_row = ['Area Median Household Income', "", "", median_income, median_rent]
        median_row_c = ["", "", median_income_c, median_rent_c]

        for i, j in zip(list(table.columns), median_row):
            if i == 'Income Category':
                col_list.append({"name": ["Area", i, j], "id": i})
            else:
                col_list.append({"name": [geo + " " + compared_year if year_comparison else geo, i, j], "id": i})

        for i, j in zip(list(table_c.columns[1:]), median_row_c):
            col_list.append({"name": [geo + " " + str(original_year) if year_comparison else geo_c, i, j], "id": i})

        style_cell_conditional = [
                                     {
                                         'if': {'column_id': c},
                                         'font_size': comparison_font_size,
                                         'backgroundColor': columns_color_fill[1]
                                     } for c in table.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': c},
                                         'font_size': comparison_font_size,
                                         'backgroundColor': columns_color_fill[2]
                                     } for c in table_c.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': table.columns[0]},
                                         'font_size': comparison_font_size,
                                         'backgroundColor': columns_color_fill[0]
                                     }
                                 ] + [
                                     {
                                         'if': {'column_id': 'Affordable Shelter Cost (2020 CAD$)'},
                                         'maxWidth': "120px",

                                     }
                                 ] + [
                                     {
                                         'if': {'column_id': 'Income Category'},
                                         'maxWidth': "100px",
                                         'width': '28%'

                                     }
                                 ]

        return col_list, table_j.to_dict(
            'records'), style_data_conditional, style_cell_conditional, style_header_conditional