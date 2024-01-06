import pandas as pd
from dash import Output, Input, State, callback
from dash.dash_table.Format import Format, Group, Scheme

from app_file import cache
from helpers.create_engine import default_year, default_value, income_partners_year
from helpers.style_helper import style_data_conditional, style_header_conditional, columns_color_fill, \
    comparison_font_size
from helpers.table_helper import query_table, get_language, area_scale_primary_only, error_region_table, \
    area_scale_comparison

# Base is what we actually label the groups as, columns is what the column the data lays in is called in the hart.db
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

hh_p_num_list = [1, 2, 3, 4, '5 or more']

amhi_range = ['20% or under of AMHI', '21% to 50% of AMHI', '51% to 80% of AMHI', '81% to 120% of AMHI',
              '121% and more of AMHI']

income_ct = [x + f" ({a})" for x, a in zip(x_base, amhi_range)]

columns = ['Percent HH with income 20% or under of AMHI in core housing need',
           'Percent HH with income 21% to 50% of AMHI in core housing need',
           'Percent HH with income 51% to 80% of AMHI in core housing need',
           'Percent HH with income 81% to 120% of AMHI in core housing need',
           'Percent HH with income 121% or more of AMHI in core housing need'
           ]


# 2021 Affordable Housing Deficit

# Table generator
def table_core_affordable_housing_deficit(geo, is_second, year: int = default_year):
    geo, joined_df_filtered = query_table(geo, year, income_partners_year)

    table2 = pd.DataFrame({'Income Category': income_ct})

    hh_p_num_list = [1, 2, 3, 4, '5 or more']
    income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']

    for h in hh_p_num_list:
        h_hold_value = []
        if h == 1:
            h2 = '1 person'
        elif h == '5 or more':
            h2 = '5 or more persons household'
        else:
            h2 = f'{str(h)} persons'
        for i in income_lv_list:
            if i == '20% or under':
                column = (f'Total - Private households by presence of at least one or of the combined activity '
                          f'limitations (Q11a, Q11b, Q11c or Q11f or combined)-{h2}-Households with income {i} of '
                          f'area median household income (AMHI)-Households in core housing need')
                h_hold_value.append(joined_df_filtered[column].tolist()[0])

            else:
                column = (f'Total - Private households by presence of at least one or of the combined activity '
                          f'limitations (Q11a, Q11b, Q11c or Q11f or combined)-{h2}-Households with income {i} of '
                          f'AMHI-Households in core housing need')
                h_hold_value.append(joined_df_filtered[column].tolist()[0])

        if is_second is False:
            if h == 1:
                table2[f'{h} Person HH'] = h_hold_value
            elif h == '5 or more':
                table2[f'5+ Person HH'] = h_hold_value
            else:
                table2[f'{h} Person HH'] = h_hold_value

        else:
            if h == 1:
                table2[f'{h} Person HH '] = h_hold_value
            elif h == '5 or more':
                table2[f'5+ Person HH '] = h_hold_value
            else:
                table2[f'{h} Person HH '] = h_hold_value

    x_list = []

    i = 0
    for b, c in zip(x_base, x_columns):
        if i < 4:
            x = b + " ($" + str(int(float(joined_df_filtered[c].tolist()[0]))) + ")"
            x_list.append(x)
        else:
            x = b + " (>$" + str(int(float(joined_df_filtered[c].tolist()[0]))) + ")"
            x_list.append(x)
        i += 1

    table2['Income Category (Max. affordable shelter cost)'] = x_list
    table2['Income Category'] = [
        'Very low Income',
        'Low Income',
        'Moderate Income',
        'Median Income',
        'High Income'
    ]

    table2['Total'] = table2.sum(axis=1)
    row_total_csd = table2.sum(axis=0)
    row_total_csd[0] = 'Total'
    table2.loc[len(table2['Income Category']), :] = row_total_csd
    table2.loc[5, 'Income Category (Max. affordable shelter cost)'] = 'Total'
    # pdb.set_trace()
    if is_second is True:
        table2 = table2.rename(columns={'Total': 'Total ', 'Income Category (Max. affordable shelter cost)':
            'Income Category (Max. affordable shelter cost) '})

    return table2


# Callback logic for the table update


@callback(
    Output('datatable2-interactivity', 'columns'),
    Output('datatable2-interactivity', 'data'),
    Output('datatable2-interactivity', 'style_data_conditional'),
    Output('datatable2-interactivity', 'style_cell_conditional'),
    Output('datatable2-interactivity', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
@cache.memoize()
def update_table2(geo, geo_c, year_comparison: str, scale, lang_query, refresh):
    # Single area mode
    language = get_language(lang_query)
    if not year_comparison and (geo == geo_c or geo_c == None or (geo == None and geo_c != None)):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        geo = area_scale_primary_only(geo, scale)

        # Generating table
        try:
            table2 = table_core_affordable_housing_deficit(geo, False)
        except:
            # No data for the selected region
            no_data = f"No Data for {geo}, please try CD/Provincial level"
            table = pd.DataFrame({no_data: [""]})
            return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional

        table2 = table2[['Income Category (Max. affordable shelter cost)', '1 Person HH', '2 Person HH',
                         '3 Person HH', '4 Person HH', '5+ Person HH', 'Total']]

        # Generating callback output to update table
        col_list = []

        style_cell_conditional = [
                                     {
                                         'if': {'column_id': c},
                                         'backgroundColor': columns_color_fill[1],
                                         'minWidth': '100px',
                                     } for c in table2.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': table2.columns[0]},
                                         'backgroundColor': columns_color_fill[0],

                                     }
                                 ] + [
                                     {
                                         'if': {'column_id': 'Income Category (Max. affordable shelter cost)'},
                                         'maxWidth': "120px",

                                     }
                                 ]

        for i in table2.columns:
            col_list.append({"name": [geo, i],
                             "id": i,
                             "type": 'numeric',
                             "format": Format(
                                 group=Group.yes,
                                 scheme=Scheme.fixed,
                                 precision=0
                             )})

        return col_list, table2.to_dict(
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
        table2 = (
            table_core_affordable_housing_deficit(geo, False, int(compared_year)) if year_comparison else
            table_core_affordable_housing_deficit(geo, False)
        )

        table2 = table2[['Income Category', 'Income Category (Max. affordable shelter cost)',
                         '1 Person HH', '2 Person HH', '3 Person HH',
                         '4 Person HH', '5+ Person HH', 'Total']]

        # Generating comparison table
        if year_comparison:
            if error_region_table(geo, default_year, language):
                return error_region_table(geo, default_year, language)
        else:
            if error_region_table(geo_c, default_year, language):
                return error_region_table(geo_c, default_year, language)
        table2_c = (
            table_core_affordable_housing_deficit(geo, True) if year_comparison else
            table_core_affordable_housing_deficit(geo_c, True)
        )

        table2_c = table2_c[['Income Category', 'Income Category (Max. affordable shelter cost) ',
                             '1 Person HH ', '2 Person HH ', '3 Person HH ',
                             '4 Person HH ', '5+ Person HH ', 'Total ']]

        # Merging main and comparison table

        table2_j = table2.merge(table2_c, how='left', on='Income Category')
        new_table2_j = table2_j.iloc[:, 1:]
        # pdb.set_trace()
        # Generating Callback output

        col_list = []

        for i in table2.columns[1:]:
            if i == 'Income Category (Max. affordable shelter cost)':
                col_list.append({"name": ["Area", i], "id": i})
            else:
                col_list.append({"name": [geo + " " + compared_year if year_comparison else geo, i],
                                 "id": i,
                                 "type": 'numeric',
                                 "format": Format(
                                     group=Group.yes,
                                     scheme=Scheme.fixed,
                                     precision=0
                                 )})

        for i in table2_c.columns[1:]:
            if i == 'Income Category (Max. affordable shelter cost) ':
                col_list.append({"name": ["", i], "id": i})
            else:
                col_list.append({"name": [geo + " " + original_year if year_comparison else geo_c, i],
                                 "id": i,
                                 "type": 'numeric',
                                 "format": Format(
                                     group=Group.yes,
                                     scheme=Scheme.fixed,
                                     precision=0
                                 )})
        # pdb.set_trace()
        style_cell_conditional = [
                                     {
                                         'if': {'column_id': c},
                                         'font_size': comparison_font_size,
                                         'minWidth': '75px',
                                         'backgroundColor': columns_color_fill[1]
                                     } for c in table2.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': c},
                                         'font_size': comparison_font_size,
                                         'minWidth': '75px',
                                         'backgroundColor': columns_color_fill[2]
                                     } for c in table2_c.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': table2.columns[0]},
                                         'font_size': comparison_font_size,
                                         'backgroundColor': columns_color_fill[0]
                                     }
                                 ] + [
                                     {
                                         'if': {'column_id': 'Income Category (Max. affordable shelter cost)'},
                                         'maxWidth': "120px",

                                     }
                                 ] + [
                                     {
                                         'if': {'column_id': 'Income Category (Max. affordable shelter cost) '},
                                         'maxWidth': "120px",

                                     }
                                 ]
        # pdb.set_trace()
        return col_list, new_table2_j.to_dict(
            'record'), style_data_conditional, style_cell_conditional, style_header_conditional
