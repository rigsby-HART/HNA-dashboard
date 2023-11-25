# Importing Libraries
import copy

import pandas as pd
import plotly.graph_objects as go
import math as math
import warnings
from dash import dcc, Input, Output, ctx, callback, State, html
from dash.dash_table.Format import Format, Scheme, Group
from plotly.subplots import make_subplots
from helpers.style_helper import style_header_conditional, style_data_conditional
from helpers.create_engine import income_partners_year, default_year
from helpers.table_helper import area_scale_comparison, area_scale_primary_only, error_region_table, \
    error_region_figure, \
    query_table, get_language
from pages.page5_helpers.page5_localization import localization
from pages.page5_helpers.page5_main import layout

warnings.filterwarnings("ignore")

# Preprocessing - Preparing main dataset and categories being used for plots

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

# Color Lists

colors = ['#D7F3FD', '#88D9FA', '#39C0F7', '#099DD7', '#044762']
hh_colors = ['#D8EBD4', '#93CD8A', '#3DB54A', '#297A32', '#143D19']
hh_type_color = ['#002145', '#3EB549', '#39C0F7']
columns_color_fill = ['#F3F4F5', '#EBF9FE', '#F0FAF1']
modebar_color = '#099DD7'
modebar_activecolor = '#044762'

# Font size for tables when they are displayed on the comparison mode
comparison_font_size = '0.7em'

# Default selected area
default_value = 'Canada'

# Setting a default plot and table which renders before the dashboard is fully loaded

income_ct = [x + f" ({a})" for x, a in zip(x_base, amhi_range)]

x_list = []

columns = ['Percent HH with income 20% or under of AMHI in core housing need',
           'Percent HH with income 21% to 50% of AMHI in core housing need',
           'Percent HH with income 51% to 80% of AMHI in core housing need',
           'Percent HH with income 81% to 120% of AMHI in core housing need',
           'Percent HH with income 121% or more of AMHI in core housing need'
           ]

# Setting layout for dashboard

layout = layout(default_year)


# Plot/table generators and callbacks

# Income Categories and Affordable Shelter Costs, 2021

# Table generator
def table_amhi_shelter_cost(geo: str, is_second: bool, year: int = default_year):
    geo, joined_df_filtered = query_table(geo, year, income_partners_year)

    portion_of_total_hh = []
    for x in x_base:
        portion_of_total_hh.append(
            round(joined_df_filtered[f'Percent of Total HH that are in {x}'].tolist()[0] * 100, 2))

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
            {'Income Category': income_ct, '% of Total HHs': portion_of_total_hh, 'Annual HH Income': amhi_list,
             'Affordable Shelter Cost (2020 CAD$)': shelter_list})
        table['% of Total HHs'] = table['% of Total HHs'].astype(str) + '%'
    else:
        table = pd.DataFrame(
            {'Income Category': income_ct, '% of Total HHs ': portion_of_total_hh, 'Annual HH Income ': amhi_list,
             'Affordable Shelter Cost ': shelter_list})
        table['% of Total HHs '] = table['% of Total HHs '].astype(str) + '%'

    return table, median_income, median_rent


# Callback logic for the table update

@callback(
    Output('income-category-affordability-table-pg5', 'columns'),
    Output('income-category-affordability-table-pg5', 'data'),
    Output('income-category-affordability-table-pg5', 'style_data_conditional'),
    Output('income-category-affordability-table-pg5', 'style_cell_conditional'),
    Output('income-category-affordability-table-pg5', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('income-category-affordability-table-pg5', 'selected_columns'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
)
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
        median_row = ['Area Median Household Income', "", median_income, median_rent]
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

        median_row = ['Area Median Household Income', "", median_income, median_rent]
        median_row_c = ["", median_income_c, median_rent_c]

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


# Percentage of Households in Core Housing Need, by Income Category, 2021

# Plot dataframe generator
def plot_df_core_housing_need_by_income(geo: str, is_second: bool, language, year: int = default_year, ):
    geo, joined_df_filtered = query_table(geo, year, income_partners_year)

    x_list = []

    # Adds labels to first four groups
    i = 0
    row_labels = ["very-low-income", "low-income", "moderate-income", "median-income", "high-income"]
    base = [localization[language][label] for label in row_labels]
    for income_category, income_query_string in zip(base, x_columns):
        value = str(joined_df_filtered[income_query_string].tolist()[0])
        # print(i, b,c, value, type(value))
        if i < 4:
            if is_second is False:
                x = localization[language]["price-format-label"].format(b=income_category, value=value)
                # print(x)
            else:
                x = localization[language]["price-format-label-comp"].format(b=income_category, value=value)
            x_list.append(x)
        else:
            if is_second is False:
                x = localization[language]["price-format-label-last"].format(b=income_category, value=value)
            else:
                x = localization[language]["price-format-label-last-comp"].format(b=income_category, value=value)
            x_list.append(x)
        i += 1

    x_list = [sub.replace('$$', '$') for sub in x_list]
    x_list = [sub.replace('.0', '') for sub in x_list]
    plot_df = pd.DataFrame({"Income_Category": x_list, 'Percent HH': joined_df_filtered[columns].T.iloc[:, 0].tolist()})

    return plot_df


# Callback logic for the plot update
@callback(
    Output('graph-pg5', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    Input('income-category-affordability-table-pg5', 'selected_columns'),
    State('url', 'search')
)
def update_geo_figure(geo: str, geo_c: str, year_comparison: str, scale, refresh, lang_query):
    # Use regex to extract the value of the 'lang' parameter
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

        # Generating dataframe for plot
        if error_region_figure(geo, default_year, language):
            return error_region_figure(geo, default_year, language)
        plot_df = plot_df_core_housing_need_by_income(geo, False, language)

        # Generating plot
        fig = go.Figure()
        for i, c in zip(plot_df['Income_Category'], colors):
            plot_df_frag = plot_df.loc[plot_df['Income_Category'] == i, :]
            fig.add_trace(go.Bar(
                y=plot_df_frag['Income_Category'],
                x=plot_df_frag['Percent HH'],
                name=i,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y} - ' + '%{x: .2%}<extra></extra>'
            ))

        # Plot layout settings
        fig.update_layout(
            width=900,
            showlegend=False,
            legend=dict(font=dict(size=9)),
            yaxis=dict(autorange="reversed"),
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            plot_bgcolor='#F8F9F9',
            title=localization[language]["fig-title"] + f" {default_year}<br>{geo}",
            legend_title=localization[language]["income"],
        )
        fig.update_xaxes(
            fixedrange=True,
            range=[0, 1],
            tickformat=',.0%',
            title=localization[language]["percent-hh"],
            tickfont=dict(size=10)
        )
        fig.update_yaxes(
            tickfont=dict(size=10),
            fixedrange=True,
            title=localization[language]["income-category"] + '<br>' + localization[language]["affordable-shelter"]
        )

        return fig

    # Comparison mode
    else:
        if year_comparison:
            geo = area_scale_primary_only(geo, scale)
            original_year, compared_year = year_comparison.split("-")
        # Area Scaling up/down when user clicks area scale button on page 1
        else:
            geo, geo_c = area_scale_comparison(geo, geo_c, scale)
            original_year, compared_year = default_year, default_year

        # Subplot setting for the comparison mode
        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=(
                                f"{geo + ' ' + compared_year if year_comparison else geo}",
                                f"{geo + ' ' + str(original_year) if year_comparison else geo_c}"),
                            shared_xaxes=True)

        # Main Plot

        # Generating dataframe for main plot
        if year_comparison:
            if error_region_figure(geo, int(compared_year), language):
                return error_region_figure(geo, int(compared_year), language)
        else:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        plot_df = (
            plot_df_core_housing_need_by_income(geo, False, language, int(compared_year)) if year_comparison else
            plot_df_core_housing_need_by_income(geo, False, language)
        )

        # Generating main plot
        n = 0
        for i, c, b in zip(plot_df['Income_Category'], colors, x_base):
            plot_df_frag = plot_df.loc[plot_df['Income_Category'] == i, :]
            fig.add_trace(go.Bar(
                y=plot_df_frag['Income_Category'],
                x=plot_df_frag['Percent HH'],
                name=b.replace(" Income", ""),
                marker_color=c,
                orientation='h',
                hovertemplate='%{y} - ' + '%{x: .2%}<extra></extra>',
                legendgroup=f'{n}'
            ), row=1, col=1)
            n += 1

        fig.update_yaxes(title=localization[language]["income-category"] +
                               '<br>' + localization[language]["affordable-shelter"], row=1, col=1)

        # Comparison plot

        # Generating dataframe for comparison plot
        if year_comparison:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        else:
            if error_region_figure(geo_c, default_year, language):
                return error_region_figure(geo_c, default_year, language)
        plot_df_c = (
            plot_df_core_housing_need_by_income(geo, True, language) if year_comparison else
            plot_df_core_housing_need_by_income(geo_c, True, language)
        )

        # Generating comparison plot
        n = 0
        for i, c, b in zip(plot_df_c['Income_Category'], colors, x_base):
            plot_df_frag_c = plot_df_c.loc[plot_df_c['Income_Category'] == i, :]
            fig.add_trace(go.Bar(
                y=plot_df_frag_c['Income_Category'],
                x=plot_df_frag_c['Percent HH'],
                name=b.replace(" Income", ""),
                marker_color=c,
                orientation='h',
                hovertemplate='%{y} - ' + '%{x: .2%}<extra></extra>',
                legendgroup=f'{n}',
                showlegend=False,
            ), row=1, col=2)
            n += 1

        # Plot layout settings
        fig.update_layout(
            title=localization[language]["fig-title"] + f" {geo}" +
                  (f' {compared_year} {localization[language]["vs"]} {original_year}' if year_comparison
                   else f" {default_year}"),
            showlegend=False,
            width=900,
            legend=dict(font=dict(size=8)),
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            plot_bgcolor='#F8F9F9',
            legend_title="Income"
        )
        fig.update_yaxes(
            fixedrange=True,
            autorange="reversed",
            title_font=dict(size=10),
            tickfont=dict(size=10)
        )
        fig.update_xaxes(
            fixedrange=True,
            range=[0, 1],
            tickformat=',.0%',
            title=localization[language]["percent-hh"],
            title_font=dict(size=10),
            tickfont=dict(size=10)
        )

        return fig


# Percentage of Households in Core Housing Need, by Income Category and HH Size, 2021

# Plot dataframe generator
def plot_df_core_housing_need_by_amhi(geo: str, IsComparison: bool, language:str,  year: int = default_year):
    geo, joined_df_filtered = query_table(geo, year, income_partners_year)

    x_list = []

    i = 0
    row_labels = ["very-low-income", "low-income", "moderate-income", "median-income", "high-income"]
    base = [localization[language][label] for label in row_labels]
    for b, c in zip(base, x_columns):
        value = str(joined_df_filtered[c].tolist()[0])
        if i < 4:
            if IsComparison is False:
                x = localization[language]["price-format-label"].format(b=b, value=value)
            else:
                x = localization[language]["price-format-label-comp"].format(b=b, value=value)
            x_list.append(x)
        else:
            if IsComparison is False:
                x = localization[language]["price-format-label-last"].format(b=b, value=value)
            else:
                x = localization[language]["price-format-label-last-comp"].format(b=b, value=value)
            x_list.append(x)
        i += 1

    income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']
    x_list = [sub.replace('$$', '$') for sub in x_list]
    x_list = [sub.replace('.0', '') for sub in x_list]

    h_hold_value = []
    hh_p_num_list_full = []
    hh_column_name = ['1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']
    for h, hc in zip(hh_p_num_list, hh_column_name):
        for i in income_lv_list:
            column = f'Per HH with income {i} of AMHI in core housing need that are {h} person HH'
            h_hold_value.append(joined_df_filtered[column].tolist()[0])
            hh_p_num_list_full.append(hc)

    plot_df = pd.DataFrame({'HH_Size': hh_p_num_list_full, 'Income_Category': x_list * 5, 'Percent': h_hold_value})

    return plot_df


# Callback logic for the plot update
@callback(
    Output('graph2-pg5', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    Input('income-category-affordability-table-pg5', 'selected_columns'),
    State('url', 'search')
)
def update_geo_figure2(geo, geo_c, year_comparison: str, scale, refresh, lang_query):
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

        # Generating dataframe for plot
        if error_region_figure(geo, default_year, language):
            return error_region_figure(geo, default_year, language)
        plot_df = plot_df_core_housing_need_by_amhi(geo, False, language)

        # Generating plot
        fig2 = go.Figure()

        for h, c in zip(plot_df['HH_Size'].unique(), hh_colors):
            plot_df_frag = plot_df.loc[plot_df['HH_Size'] == h, :]
            fig2.add_trace(go.Bar(
                y=plot_df_frag['Income_Category'],
                x=plot_df_frag['Percent'],
                name=h,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y}, ' + f'HH Size: {h} - ' + '%{x: .2%}<extra></extra>',
            ))

        # Plot layout settings
        fig2.update_layout(
            legend_traceorder='normal',
            width=900,
            legend=dict(font=dict(size=9)),
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            yaxis=dict(autorange="reversed"),
            barmode='stack',
            plot_bgcolor='#F8F9F9',
            title= localization[language]["fig2-title"] + f' {default_year}<br>{geo}',
            legend_title="Household Size"
        )
        fig2.update_yaxes(
            tickfont=dict(size=10),
            fixedrange=True,
            title=localization[language]["income-category"] + '<br>' + localization[language]["affordable-shelter"]
        )
        fig2.update_xaxes(
            fixedrange=True,
            tickformat=',.0%',
            title=localization[language]["percent-hh"],
            tickfont=dict(size=10)
        )

        return fig2


    # Comparison mode
    else:
        if year_comparison:
            geo = area_scale_primary_only(geo, scale)
            original_year, compared_year = year_comparison.split("-")
        # Area Scaling up/down when user clicks area scale button on page 1
        else:
            geo, geo_c = area_scale_comparison(geo, geo_c, scale)
            original_year, compared_year = default_year, default_year

        # Subplot setting for the comparison mode
        fig2 = make_subplots(rows=1, cols=2,
                             subplot_titles=(
                                 f"{geo + ' ' + compared_year if year_comparison else geo}",
                                 f"{geo + ' ' + original_year if year_comparison else geo_c}"),
                             shared_xaxes=True)

        # Main Plot

        if year_comparison:
            if error_region_figure(geo, int(compared_year), language):
                return error_region_figure(geo, int(compared_year), language)
        else:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        # Generating dataframe for main plot
        plot_df = (
            plot_df_core_housing_need_by_amhi(geo, False, language, int(compared_year)) if year_comparison else
            plot_df_core_housing_need_by_amhi(geo, False, language)
        )

        # Generating main plot
        n = 0
        for h, c in zip(plot_df['HH_Size'].unique(), hh_colors):
            plot_df_frag = plot_df.loc[plot_df['HH_Size'] == h, :]
            fig2.add_trace(go.Bar(
                y=plot_df_frag['Income_Category'],
                x=plot_df_frag['Percent'],
                name=h,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y}, ' + f'HH Size: {h} - ' + '%{x: .2%}<extra></extra>',
                legendgroup=f'{n}'
            ), row=1, col=1)
            n += 1

        fig2.update_yaxes(title=localization[language]["income-category"] +
                               '<br>' + localization[language]["affordable-shelter"], row=1, col=1)

        # Comparison plot

        if year_comparison:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        else:
            if error_region_figure(geo_c, default_year, language):
                return error_region_figure(geo_c, default_year, language)
        # Generating dataframe for comparison plot
        plot_df_c = (
            plot_df_core_housing_need_by_amhi(geo, True, language) if year_comparison else
            plot_df_core_housing_need_by_amhi(geo_c, True, language)
        )

        # Generating comparison plot
        n = 0
        for h, c in zip(plot_df_c['HH_Size'].unique(), hh_colors):
            plot_df_frag_c = plot_df_c.loc[plot_df_c['HH_Size'] == h, :]
            fig2.add_trace(go.Bar(
                y=plot_df_frag_c['Income_Category'],
                x=plot_df_frag_c['Percent'],
                name=h,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y}, ' + f'HH Size: {h} - ' + '%{x: .2%}<extra></extra>',
                legendgroup=f'{n}',
                showlegend=False,
            ), row=1, col=2)
            n += 1

        # Plot layout settings
        fig2.update_layout(
            font=dict(size=10),
            title=localization[language]["fig2-title"] + f" {geo}" +
                  (f' {compared_year} {localization[language]["vs"]} {original_year}' if year_comparison
                   else f" {default_year}"),
            legend_traceorder='normal',
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            barmode='stack',
            plot_bgcolor='#F8F9F9',
            legend_title="Household Size",
            legend=dict(font=dict(size=8))
        )
        fig2.update_yaxes(
            title_font=dict(size=10),
            tickfont=dict(size=10),
            fixedrange=True,
            autorange="reversed"
        )
        fig2.update_xaxes(
            title_font=dict(size=10),
            fixedrange=True,
            tickformat=',.0%',
            title=localization[language]["percent-hh"],
            tickfont=dict(size=10)
        )

        return fig2


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
    Output('datatable2-interactivity-pg5', 'columns'),
    Output('datatable2-interactivity-pg5', 'data'),
    Output('datatable2-interactivity-pg5', 'style_data_conditional'),
    Output('datatable2-interactivity-pg5', 'style_cell_conditional'),
    Output('datatable2-interactivity-pg5', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('datatable2-interactivity-pg5', 'selected_columns'),
    Input('area-scale-store', 'data'),
    State('url', 'search')
)
def update_table2(geo, geo_c, year_comparison: str, selected_columns, scale, lang_query):
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
)
def change_title_labels(geo, geo_c, year_comparison, scale, refresh):
    # change based off of url
    if year_comparison:
        original_year, compared_year = year_comparison.split("-")
        return (
            html.Strong(f'Income Categories and Affordable Shelter Costs, {compared_year} vs {original_year}'),
            html.Strong(f'Percentage of Households in Core Housing Need, by Income Category, {compared_year} vs {original_year}'),
            html.Strong(f'Percentage of Households in Core Housing Need, by Income Category and HH Size, {compared_year} vs {original_year}'),
            html.Strong(f'{compared_year} vs {original_year} Affordable Housing Deficit'),
        )
    return (
        html.Strong(f'Income Categories and Affordable Shelter Costs, {default_year}'),
        html.Strong(f'Percentage of Households in Core Housing Need, by Income Category, {default_year}'),
        html.Strong(f'Percentage of Households in Core Housing Need, by Income Category and HH Size, {default_year}'),
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

    if "ov7-download-csv" == ctx.triggered_id:
        if year_comparison:
            original_year, compared_year = year_comparison.split("-")
            _, joined_df_geo = query_table(geo, int(original_year), income_partners_year)
            _, joined_df_geo_c = query_table(geo, int(compared_year), income_partners_year)
            joined_df_download = pd.concat([joined_df_geo, joined_df_geo_c])
            joined_df_download = joined_df_download.drop(columns=['pk_x', 'pk_y'])
            return dcc.send_data_frame(joined_df_download.to_csv, "result.csv")
        else:
            _, joined_df_geo = query_table(geo, default_year, income_partners_year)
            _, joined_df_geo_c = query_table(geo_c, default_year, income_partners_year)
            joined_df_download = pd.concat([joined_df_geo, joined_df_geo_c])
            joined_df_download = joined_df_download.drop(columns=['pk_x', 'pk_y'])

            return dcc.send_data_frame(joined_df_download.to_csv, "result.csv")


