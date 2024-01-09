# Income Categories and Affordable Shelter Costs, 2021
import pandas as pd
from dash import Output, Input, State, callback

from app_file import cache
from helpers.create_engine import default_year, default_value, income_indigenous_year
from helpers.style_helper import style_data_conditional, style_header_conditional, columns_color_fill, \
    comparison_font_size2
from helpers.table_helper import query_table, get_language, area_scale_primary_only, area_scale_comparison, \
    error_indigenous_table

x_base_echn = [
    '20% or under of area median household income (AMHI)-Households examined for core housing need',
    '21% to 50% of AMHI-Households examined for core housing need',
    '51% to 80% of AMHI-Households examined for core housing need',
    '81% to 120% of AMHI-Households examined for core housing need',
    '121% or more of AMHI-Households examined for core housing need'
]
amhi_range = ['20% or under of AMHI', '21% to 50% of AMHI', '51% to 80% of AMHI', '81% to 120% of AMHI',
              '121% and more of AMHI']
x_base = ['Very Low Income',
          'Low Income',
          'Moderate Income',
          'Median Income',
          'High Income',
          ]
income_ct = [x + f" ({a})" for x, a in zip(x_base, amhi_range)]

# Table generator

def table_amhi_shelter_cost_ind(geo, IsComparison, language, year: int = default_year):
    # joined_df_filtered = income_indigenous_year[year].query('Geography == ' + f'"{geo}"')
    geo, joined_df_filtered = query_table(geo, year, income_indigenous_year)
    portion_of_total_hh = []

    for x in x_base_echn:
        portion_of_total_hh.append(joined_df_filtered[
                                       f'Aboriginal household status-Total - Private households by tenure including presence of mortgage payments and subsidized housing-Households with income {x}'].tolist()[
                                       0])

    sum_portion_of_total_hh = sum(portion_of_total_hh)

    if sum_portion_of_total_hh > 0:
        portion_of_total_hh = [round(p * (1 / sum_portion_of_total_hh * 100), 2) for p in portion_of_total_hh]
    else:
        portion_of_total_hh = [0 for p in portion_of_total_hh]

    amhi_list = []
    for a in amhi_range:
        amhi_list.append(joined_df_filtered[a].tolist()[0])

    shelter_range = ['20% or under of AMHI.1', '21% to 50% of AMHI.1', '51% to 80% of AMHI.1', '81% to 120% of AMHI.1',
                     '121% and more of AMHI.1']
    shelter_list = []
    for s in shelter_range:
        shelter_list.append(joined_df_filtered[s].tolist()[0])

    joined_df_geo_index = joined_df_filtered.set_index('Geography')
    # pdb.set_trace()
    median_income = '${:0,.0f}'.format(float(joined_df_geo_index.at[geo, 'Median income of household ($)']))
    # print(median_income)
    median_rent = '${:0,.0f}'.format(float(joined_df_geo_index.at[geo, 'Rent AMHI']))

    if IsComparison != True:
        table = pd.DataFrame({'Income Category': income_ct, '% of Total Indigenous HHs': portion_of_total_hh,
                              'Annual HH Income': amhi_list, 'Affordable Shelter Cost (2020 CAD$)': shelter_list})
        table['% of Total Indigenous HHs'] = table['% of Total Indigenous HHs'].astype(str) + '%'
    else:
        table = pd.DataFrame({'Income Category': income_ct, '% of Total Indigenous HHs ': portion_of_total_hh,
                              'Annual HH Income ': amhi_list, 'Affordable Shelter Cost (2020 CAD$) ': shelter_list})
        table['% of Total Indigenous HHs '] = table['% of Total Indigenous HHs '].astype(str) + '%'

    return table, median_income, median_rent


# Callback logic for the table update


@callback(
    Output('datatable-interactivity_ind', 'columns'),
    Output('datatable-interactivity_ind', 'data'),
    Output('datatable-interactivity_ind', 'style_data_conditional'),
    Output('datatable-interactivity_ind', 'style_cell_conditional'),
    Output('datatable-interactivity_ind', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('datatable-interactivity_ind', 'selected_columns'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    cache_args_to_ignore=[3]
)
@cache.memoize()
def update_table1(geo, geo_c, year_comparison, selected_columns, scale, lang_query):
    language = get_language(lang_query)
    # Single area mode
    if not year_comparison and (geo == geo_c or geo_c == None or (geo == None and geo_c != None)):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        geo = area_scale_primary_only(geo, scale)

        # Generating table
        if error_indigenous_table(geo, default_year, ):
            return error_indigenous_table(geo, default_year)
        table, median_income, median_rent = table_amhi_shelter_cost_ind(geo, False, language)

        # Generating callback output to update table
        col_list = []
        median_row = ['Area Median Household Income', "", median_income, median_rent]

        # for i in table.columns:
        #     col_list.append({"name": [geo + " (Indigenous HH)", i], "id": i})
        for i, j in zip(list(table.columns), median_row):
            col_list.append({"name": [geo + " (Indigenous HH)", i, j], "id": i})

        style_cell_conditional = [
                                     {
                                         'if': {'column_id': c},
                                         'backgroundColor': columns_color_fill[1]
                                     } for c in table.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': table.columns[0]},
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
                                         'maxWidth': "120px",
                                         'width': '35%'

                                     }
                                 ]

        return col_list, table.to_dict(
            'record'), style_data_conditional, style_cell_conditional, style_header_conditional

    # Comparison mode
    else:
        # Area Scaling up/down when user clicks area scale button on page 1
        if year_comparison:
            original_year, compared_year = year_comparison.split("-")
            geo = area_scale_primary_only(geo, scale)
        # Area Scaling up/down when user clicks area scale button on page 1
        else:
            geo, geo_c = area_scale_comparison(geo, geo_c, scale)
            original_year, compared_year = default_year, default_year

        # Main Table
        if year_comparison:
            if error_indigenous_table(geo, int(compared_year)):
                return error_indigenous_table(geo, int(compared_year))
        else:
            if error_indigenous_table(geo, default_year):
                return error_indigenous_table(geo, default_year)
        # Generating main table
        table, median_income, median_rent = (
            table_amhi_shelter_cost_ind(geo, False, language, int(compared_year)) if year_comparison else
            table_amhi_shelter_cost_ind(geo, False, language)
        )

        # Comparison Table

        if geo_c == None:
            geo_c = geo
        if year_comparison:
            if error_indigenous_table(geo, default_year):
                return error_indigenous_table(geo, default_year)
        else:
            if error_indigenous_table(geo_c, default_year):
                return error_indigenous_table(geo_c, default_year)
        # Generating comparison table
        table_c, median_income_c, median_rent_c = (
            table_amhi_shelter_cost_ind(geo, True, language, int(original_year)) if year_comparison else
            table_amhi_shelter_cost_ind(geo_c, True, language)
        )

        # Merging main and comparison table
        table_j = table.merge(table_c, how='left', on='Income Category')

        # Generating Callback output

        col_list = []
        median_row = ['Area Median Household Income', "", median_income, median_rent]
        median_row_c = ["", median_income_c, median_rent_c]

        for i, j in zip(list(table.columns), median_row):
            if i == 'Income Category':
                col_list.append({"name": ["Area (Indigenous HH)", i, j], "id": i})
            else:
                col_list.append({"name": [f"{geo} {compared_year}" if year_comparison else geo, i, j], "id": i})

        for i, j in zip(list(table_c.columns[1:]), median_row_c):
            col_list.append({"name": [f"{geo} {original_year}" if year_comparison else geo_c, i, j], "id": i})

        # for i in table.columns:
        #     if i == 'Income Category':
        #         col_list.append({"name": ["Area (Indigenous HH)", i], "id": i})
        #     else:
        #         col_list.append({"name": [geo, i], "id": i})
        #
        # for i in table_c.columns[1:]:
        #     col_list.append({"name": [geo_c, i], "id": i})

        style_cell_conditional = [
                                     {
                                         'if': {'column_id': c},
                                         'font_size': comparison_font_size2,
                                         'backgroundColor': columns_color_fill[1]
                                     } for c in table.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': c},
                                         'font_size': comparison_font_size2,
                                         'backgroundColor': columns_color_fill[2]
                                     } for c in table_c.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': table.columns[0]},
                                         'font_size': comparison_font_size2,
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
                                         'maxWidth': "120px",
                                         'width': '28%'

                                     }
                                 ]

        return col_list, table_j.to_dict(
            'record'), style_data_conditional, style_cell_conditional, style_header_conditional