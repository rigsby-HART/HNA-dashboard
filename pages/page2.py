# Importing Libraries
import copy
import pandas as pd
import plotly.graph_objects as go
import math as math
import warnings
from dash import register_page
from dash import dcc, Input, Output, ctx, callback, State, html
from dash.dash_table.Format import Format, Scheme, Group
from plotly.subplots import make_subplots

from app_file import cache
from helpers.style_helper import style_header_conditional, style_data_conditional
from helpers.create_engine import income_partners_year, default_year
from helpers.table_helper import area_scale_comparison, area_scale_primary_only, error_region_table, \
    error_region_figure, \
    query_table, get_language
from pages.page2_helpers.page2_main import layout
from helpers.localization import localization
register_page(__name__)
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
    Output('income-category-affordability-table', 'columns'),
    Output('income-category-affordability-table', 'data'),
    Output('income-category-affordability-table', 'style_data_conditional'),
    Output('income-category-affordability-table', 'style_cell_conditional'),
    Output('income-category-affordability-table', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
@cache.memoize()
def update_table1(geo, geo_c, year_comparison: str, scale, lang_query, refresh):
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
    row_labels = ["Very Low Income", "Low Income", "Moderate Income", "Median Income", "High Income"]
    base = [localization[language][label] for label in row_labels]
    for income_category, income_query_string in zip(base, x_columns):
        value = str(joined_df_filtered[income_query_string].tolist()[0])
        # print(i, b,c, value, type(value))
        if i < 4:
            if is_second is False:
                x = localization[language]["{b}<br> (${value})"].format(b=income_category, value=value)
                # print(x)
            else:
                x = localization[language][" (${value}) "].format(b=income_category, value=value)
            x_list.append(x)
        else:
            if is_second is False:
                x = localization[language]["{b}<br> (>${value})"].format(b=income_category, value=value)
            else:
                x = localization[language][" (>${value}) "].format(b=income_category, value=value)
            x_list.append(x)
        i += 1

    x_list = [sub.replace('$$', '$') for sub in x_list]
    x_list = [sub.replace('.0', '') for sub in x_list]
    plot_df = pd.DataFrame({"Income_Category": x_list, 'Percent HH': joined_df_filtered[columns].T.iloc[:, 0].tolist()})

    return plot_df


# Callback logic for the plot update

@callback(
    Output('graph', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
@cache.memoize()
def update_geo_figure(geo: str, geo_c: str, year_comparison: str, scale, lang_query, refresh):
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
            title=localization[language]['Percentage of Households in Core Housing Need, by Income Category,'] + f" {default_year}<br>{geo}",
            legend_title=localization[language]["Income"],
        )
        fig.update_xaxes(
            fixedrange=True,
            range=[0, 1],
            tickformat=',.0%',
            title=localization[language]["% of HH"],
            tickfont=dict(size=10)
        )
        fig.update_yaxes(
            tickfont=dict(size=10),
            fixedrange=True,
            title=localization[language]["Income Category"] + '<br>' + localization[language]["(Max. affordable shelter costs)"]
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

        fig.update_yaxes(title=localization[language]["Income Category"] +
                               '<br>' + localization[language]["(Max. affordable shelter costs)"], row=1, col=1)

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
            title=localization[language]['Percentage of Households in Core Housing Need, by Income Category,'] + f" {geo}" +
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
            title=localization[language]["% of HH"],
            title_font=dict(size=10),
            tickfont=dict(size=10)
        )

        return fig


# Percentage of Households in Core Housing Need, by Income Category and HH Size, 2021

# Plot dataframe generator
def plot_df_core_housing_need_by_amhi(geo: str, IsComparison: bool, language: str, year: int = default_year):
    geo, joined_df_filtered = query_table(geo, year, income_partners_year)

    x_list = []

    i = 0
    row_labels = ["Very Low Income", "Low Income", "Moderate Income", "Median Income", "High Income"]
    base = [localization[language][label] for label in row_labels]
    for b, c in zip(base, x_columns):
        value = str(joined_df_filtered[c].tolist()[0])
        if i < 4:
            if IsComparison is False:
                x = localization[language]["{b}<br> (${value})"].format(b=b, value=value)
            else:
                x = localization[language][" (${value}) "].format(b=b, value=value)
            x_list.append(x)
        else:
            if IsComparison is False:
                x = localization[language]["{b}<br> (>${value})"].format(b=b, value=value)
            else:
                x = localization[language][" (>${value}) "].format(b=b, value=value)
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
    Output('graph2', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
@cache.memoize()
def update_geo_figure2(geo, geo_c, year_comparison: str, scale, lang_query, refresh):
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
            title=localization[language]['Percentage of Households in Core Housing Need, by Income Category and HH Size,'] + f' {default_year}<br>{geo}',
            legend_title="Household Size"
        )
        fig2.update_yaxes(
            tickfont=dict(size=10),
            fixedrange=True,
            title=localization[language]["Income Category"] + '<br>' + localization[language]["(Max. affordable shelter costs)"]
        )
        fig2.update_xaxes(
            fixedrange=True,
            tickformat=',.0%',
            title=localization[language]["% of HH"],
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

        fig2.update_yaxes(title=localization[language]["Income Category"] +
                                '<br>' + localization[language]["(Max. affordable shelter costs)"], row=1, col=1)

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
            title=localization[language]['Percentage of Households in Core Housing Need, by Income Category and HH Size,'] + f" {geo}" +
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
            title=localization[language]["% of HH"],
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


# Percentage of Households in Core Housing Need by Priority Population, 2021

# Preparing global variables for the table

hh_category_dict = {
    'Percent Single Mother led HH in core housing need': 'Single mother-led HH',
    'Percent Women-led HH in core housing need': 'Women-led HH',
    'Percent Indigenous HH in core housing need': 'Indigenous HH',
    'Percent Visible minority HH in core housing need': 'Visible minority HH',
    'Percent Black-led HH in core housing need': 'Black-led HH',
    'Percent New migrant-led HH in core housing need': 'New migrant-led HH',
    'Percent Refugee claimant-led HH in core housing need': 'Refugee claimant-led HH',
    'Percent HH head under 25 in core housing need': 'HH head under 25',
    'Percent HH head over 65 in core housing need': 'HH head over 65',
    'Percent HH head over 85 in core housing need': 'HH head over 85',
    'Percent HH with physical act. limit. in core housing need': 'HH with physical activity limitation',
    'Percent HH with cognitive, mental, or addictions activity limitation in core housing need': 'HH with cognitive, mental,<br>or addictions activity limitation',
    'Percent of Transgender HH in core housing': 'Transgender or Non-binary HH',
    'Percent HH in core housing need': 'Community (all HH)'
}

hh_columns = hh_category_dict.keys()
hh_categories = list(hh_category_dict.values())


# Plot dataframe generator

def plot_df_core_housing_need_by_priority_population(geo, language: str, year: int = default_year):
    geo, joined_df_filtered = query_table(geo, year, income_partners_year)
    if year == 2016:
        columns = list(hh_columns)
        columns.remove('Percent of Transgender HH in core housing')
        percent_hh = [joined_df_filtered[c].tolist()[0] for c in columns]

        categories = [localization[language][category] for category in hh_categories]
        categories.remove(localization[language]["Transgender or Non-binary HH"])
        plot_df = pd.DataFrame({'HH_Category': categories, 'Percent_HH': percent_hh})
    else:
        percent_hh = [joined_df_filtered[c].tolist()[0] for c in hh_columns]
        categories = [localization[language][category] for category in hh_categories]
        plot_df = pd.DataFrame({'HH_Category': categories, 'Percent_HH': percent_hh})
        plot_df['Percent_HH'] = plot_df['Percent_HH'].fillna(0)

    return plot_df


# Plot bar color generator

def color_dict_core_housing_need_by_priority_population(plot_df):
    color_dict = {}

    for h in plot_df['HH_Category'].unique():

        if plot_df['Percent_HH'].max() == 0:
            color_dict[h] = hh_type_color[2]
        else:
            if h == plot_df.loc[plot_df['Percent_HH'] == plot_df['Percent_HH'].max(), 'HH_Category'].tolist()[0]:
                color_dict[h] = hh_type_color[0]
            elif h == 'Community (all HH)':
                color_dict[h] = hh_type_color[1]
            else:
                color_dict[h] = hh_type_color[2]

    return color_dict


# Callback logic for the plot update


@callback(
    Output('graph5', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
@cache.memoize()
def update_geo_figure5(geo, geo_c, year_comparison: str, scale, lang_query, refresh):
    language = get_language(lang_query)

    if (geo == geo_c or geo_c == None or (geo == None and geo_c != None)) and not year_comparison:

        # When no area is selected

        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1

        geo = area_scale_primary_only(geo, scale)

        # Generating dataframe for plot and color lists
        if error_region_figure(geo, default_year, language):
            return error_region_figure(geo, default_year, language)
        plot_df = plot_df_core_housing_need_by_priority_population(geo, language)
        color_dict = color_dict_core_housing_need_by_priority_population(plot_df)

        # Generating plot

        fig5 = go.Figure()
        for i in [localization[language][category] for category in hh_categories]:
            plot_df_frag = plot_df.loc[plot_df['HH_Category'] == i, :]
            fig5.add_trace(go.Bar(
                y=plot_df_frag['HH_Category'],
                x=plot_df_frag['Percent_HH'],
                name=i,
                marker_color=color_dict[i],
                orientation='h',
                hovertemplate='%{y} - ' + '%{x: .2%}<extra></extra>',
            ))

        # Plot layout settings
        fig5.update_layout(
            yaxis=dict(autorange="reversed"),
            width=900,
            height=500,
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            showlegend=False,
            plot_bgcolor='#F8F9F9',
            title=localization[language]['Percentage of Households in Core Housing Need by Priority Population, '] + f' {default_year}<br>{geo}',
            legend_title="HH Category"
        )
        fig5.update_xaxes(
            title_font=dict(size=10),
            fixedrange=True,
            tickformat=',.0%',
            range=[0, math.ceil(plot_df['Percent_HH'].max() * 10) / 10],
            title=localization[language]["% of Priority Population HH"]
        )
        fig5.update_yaxes(
            fixedrange=True,
            tickfont=dict(size=10)
        )

        return fig5

    # Comparison mode

    else:
        if year_comparison:
            original_year, compared_year = year_comparison.split("-")
            geo = area_scale_primary_only(geo, scale)
        # Area Scaling up/down when user clicks area scale button on page 1
        else:
            geo, geo_c = area_scale_comparison(geo, geo_c, scale)
            original_year, compared_year = default_year, default_year

        # Subplot setting for the comparison mode 
        fig5 = make_subplots(rows=1, cols=2, subplot_titles=(f"{geo + ' ' + compared_year if year_comparison else geo}",
                                                             f"{geo + ' ' + original_year if year_comparison else geo_c}"),
                             shared_yaxes=True, shared_xaxes=True)

        # Main Plot

        # Generating dataframe for main plot and color list

        if year_comparison:
            if error_region_figure(geo, int(compared_year), language):
                return error_region_figure(geo, int(compared_year), language)
        else:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        plot_df = plot_df_core_housing_need_by_priority_population(geo, language,
                                                                   int(compared_year) if year_comparison else
                                                                   default_year)
        color_dict = color_dict_core_housing_need_by_priority_population(plot_df)

        # Generating main plot

        for i in plot_df["HH_Category"]:
            plot_df_frag = plot_df.loc[plot_df['HH_Category'] == i, :]
            fig5.add_trace(go.Bar(
                y=plot_df_frag['HH_Category'],
                x=plot_df_frag['Percent_HH'],
                name=i,
                marker_color=color_dict[i],
                orientation='h',
                hovertemplate='%{y} - ' + '%{x: .2%}<extra></extra>',
            ), row=1, col=1)

        # Comparison Plot

        # Generating dataframe for comparison plot and color list

        if year_comparison:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        else:
            if error_region_figure(geo_c, default_year, language):
                return error_region_figure(geo_c, default_year, language)
        plot_df_c = (
            plot_df_core_housing_need_by_priority_population(geo, language, int(original_year)) if year_comparison else
            plot_df_core_housing_need_by_priority_population(geo_c, language)
        )
        color_dict = color_dict_core_housing_need_by_priority_population(plot_df_c)

        # Generating comparison plot

        for i in [localization[language][category] for category in hh_categories]:
            plot_df_frag_c = plot_df_c.loc[plot_df_c['HH_Category'] == i, :]
            fig5.add_trace(go.Bar(
                y=plot_df_frag_c['HH_Category'],
                x=plot_df_frag_c['Percent_HH'],
                name=i,
                marker_color=color_dict[i],
                orientation='h',
                hovertemplate='%{y} - ' + '%{x: .2%}<extra></extra>',
            ), row=1, col=2)

        # Plot layout settings

        fig5.update_layout(
            title=localization[language]['Percentage of Households in Core Housing Need by Priority Population, '] + f'<br>{geo}',
            width=900,
            height=500,
            legend=dict(font=dict(size=8)),
            yaxis=dict(autorange="reversed"),
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            showlegend=False,
            plot_bgcolor='#F8F9F9',
            legend_title="HH Category"
        )
        fig5.update_xaxes(
            title_font=dict(size=10),
            tickfont=dict(size=8),
            tickformat=',.0%',
            fixedrange=True,
            range=[0, math.ceil(max(plot_df['Percent_HH'].max(), plot_df_c['Percent_HH'].max()) * 10) / 10],
            title=localization[language]["% of Priority Population HH"]
        )
        fig5.update_yaxes(
            fixedrange=True,
            tickfont=dict(size=10)
        )

        return fig5


# Percentage of Households in Core Housing Need by Priority Population and Income Category, 2021

# Preparing global variables for the table

hh_category_dict2 = {
    'Percent of Single Mother led HH in core housing need': 'Single mother-led HH',
    'Percent of Women-led HH in core housing need': 'Women-led HH',
    'Percent of Indigenous HH in core housing need': 'Indigenous HH',
    'Percent of Visible minority HH in core housing need': 'Visible minority HH',
    'Percent of Black-led HH in core housing need': 'Black-led HH',
    'Percent of New migrant-led HH in core housing need': 'New migrant-led HH',
    'Percent of Refugee claimant-led HH in core housing need': 'Refugee claimant-led HH',
    'Percent of HH head under 25 in core housing need': 'HH head under 25',
    'Percent of HH head over 65 in core housing need': 'HH head over 65',
    'Percent of HH head over 85 in core housing need': 'HH head over 85',
    'Percent of HH with physical act. limit. in core housing need': 'HH with physical activity limitation',
    'Percent of HH with with cognitive, mental, or addictions activity limitation in core housing need': 'HH with cognitive, mental,<br>or addictions activity limitation',
}

hh_category_dict3 = {
    'Percent of Single Mother led HH core housing': 'Single mother-led HH',
    'Percent of Women-led HH core housing': 'Women-led HH',
    'Percent of Indigenous HH in core housing': 'Indigenous HH',
    'Percent of Visible minority HH core housing': 'Visible minority HH',
    'Percent of Black-led HH core housing': 'Black-led HH',
    'Percent of New migrant-led HH core housing': 'New migrant-led HH',
    'Percent of Refugee claimant-led HH core housing': 'Refugee claimant-led HH',
    'Percent of HH head under 25 core housing': 'HH head under 25',
    'Percent of HH head over 65 core housing': 'HH head over 65',
    'Percent of HH head over 85 core housing': 'HH head over 85',
    'Percent of HH with physical act. limit. in core housing': 'HH with physical activity limitation',
    'Percent of HH with cognitive, mental, or addictions activity limitation in core housing': 'HH with cognitive, mental,<br>or addictions activity limitation',
}

hh_category_dict4 = {
    'Percent of Single Mother led HH in core housing': 'Single mother-led HH',
    'Percent of Women-led HH in core housing': 'Women-led HH',
    'Percent of Indigenous HH in core housing': 'Indigenous HH',
    'Percent of Visible minority HH in core housing': 'Visible minority HH',
    'Percent of Black-led HH in core housing': 'Black-led HH',
    'Percent of New migrant-led HH in core housing': 'New migrant-led HH',
    'Percent of Refugee claimant-led HH in core housing': 'Refugee claimant-led HH',
    'Percent of HH head under 25 in core housing': 'HH head under 25',
    'Percent of HH head over 65 in core housing': 'HH head over 65',
    'Percent of HH head over 85 in core housing': 'HH head over 85',
    'Percent of HH with physical act. limit. in core housing': 'HH with physical activity limitation',
    'Percent of HH with cognitive, mental, or addictions activity limitation in core housing': 'HH with cognitive, mental,<br>or addictions activity limitation',
}

columns2 = hh_category_dict2.keys()
columns3 = hh_category_dict3.keys()
columns4 = hh_category_dict4.keys()

income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']


# Plot dataframe generator

def plot_df_core_housing_need_by_priority_population_income(geo: str, language: str, year=default_year):
    geo, joined_df_filtered = query_table(geo, year, income_partners_year)

    income_col = []
    percent_col = []
    hh_cat_col = []

    col2 = columns2
    col3 = columns3
    col4 = columns4

    dict2 = hh_category_dict2
    dict3 = hh_category_dict3
    dict4 = hh_category_dict4
    if year != 2016:
        dict2 = copy.deepcopy(dict2)
        dict3 = copy.deepcopy(dict3)
        dict4 = copy.deepcopy(dict4)
        dict2['Percent of Transgender HH in core housing'] = 'Transgender or Non-binary HH'
        dict3['Percent of Transgender HH in core housing'] = 'Transgender or Non-binary HH'
        dict4['Percent of Transgender HH in core housing'] = 'Transgender or Non-binary HH'
        col2 = dict2.keys()
        col3 = dict3.keys()
        col4 = dict4.keys()
    dict2 = {key: localization[language][value] for key, value in zip(dict2.keys(), dict2.values())}
    dict3 = {key: localization[language][value] for key, value in zip(dict3.keys(), dict3.values())}
    dict4 = {key: localization[language][value] for key, value in zip(dict4.keys(), dict4.values())}
    row_labels = ["Very Low Income", "Low Income", "Moderate Income", "Median Income", "High Income"]
    base = [localization[language][label] for label in row_labels]
    for c, c2, c3 in zip(col2, col3, col4):
        for index, i in enumerate(income_lv_list):
            if i == '20% or under':
                p_hh = joined_df_filtered[f'{c} with income {i} of the AMHI'].tolist()[0]
                hh_cat_col.append(dict2[c])
            elif i == '21% to 50%':
                p_hh = joined_df_filtered[f'{c2} with income {i} of AMHI'].tolist()[0]
                hh_cat_col.append(dict3[c2])
            else:
                p_hh = joined_df_filtered[f'{c3} with income {i} of AMHI'].tolist()[0]
                hh_cat_col.append(dict4[c3])

            income_col.append(base[index])
            percent_col.append(p_hh)

    plot_df = pd.DataFrame({'Income_Category': income_col, 'HH_Category': hh_cat_col, 'Percent': percent_col})

    return plot_df


# Callback logic for the plot update


@callback(
    Output('graph6', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
@cache.memoize()
def update_geo_figure6(geo, geo_c, year_comparison, scale, lang_query, refresh):
    # Overried income category values
    income_category_override = ['Very Low', 'Low', 'Moderate', 'Median', 'High']

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
        plot_df = plot_df_core_housing_need_by_priority_population_income(geo, language)

        # Generating plot
        fig6 = go.Figure()

        for i, c, o in zip(plot_df['Income_Category'].unique(), colors, income_category_override):
            plot_df_frag = plot_df.loc[plot_df['Income_Category'] == i, :]
            fig6.add_trace(go.Bar(
                y=plot_df_frag['HH_Category'],
                x=plot_df_frag['Percent'],
                name=o,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y}, ' + f'{o} Income - ' + '%{x: .2%}<extra></extra>',
            ))

        # Plot layout settings
        fig6.update_layout(
            width=900,
            height=500,
            legend_traceorder="normal",
            font=dict(size=10),
            legend=dict(font=dict(size=9)),
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            yaxis=dict(autorange="reversed"),
            barmode='stack',
            plot_bgcolor='#F8F9F9',
            title=localization[language]["Percentage of Households in Core Housing Need by Priority Population and Income Category,"] + f' {default_year}<br>{geo}',
            legend_title=localization[language]["Income Category"]
        )
        fig6.update_xaxes(
            title_font=dict(size=10),
            fixedrange=True,
            tickformat=',.0%',
            title=localization[language]["% of HH"]
        )
        fig6.update_yaxes(
            fixedrange=True,
            tickfont=dict(size=10)
        )

        return fig6

    # Comparison mode
    else:
        if year_comparison:
            original_year, compared_year = year_comparison.split("-")
            geo = area_scale_primary_only(geo, scale)
        # Area Scaling up/down when user clicks area scale button on page 1
        else:
            geo, geo_c = area_scale_comparison(geo, geo_c, scale)
            original_year, compared_year = default_year, default_year

        # Subplot setting for the comparison mode
        fig6 = make_subplots(rows=1, cols=2,
                             subplot_titles=(f"{geo + ' ' + compared_year if year_comparison else geo}",
                                             f"{geo + ' ' + original_year if year_comparison else geo_c}"),
                             shared_yaxes=True, shared_xaxes=True)

        # Main Plot
        if year_comparison:
            if error_region_figure(geo, int(compared_year), language):
                return error_region_figure(geo, int(compared_year), language)
        else:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        # Generating dataframe for main plot
        plot_df = (
            plot_df_core_housing_need_by_priority_population_income(geo, language,
                                                                    int(compared_year) if year_comparison else
                                                                    int(original_year))
        )

        # Generating main plot

        n = 0
        for i, c, o in zip(plot_df['Income_Category'].unique(), colors, income_category_override):
            plot_df_frag = plot_df.loc[plot_df['Income_Category'] == i, :]
            fig6.add_trace(go.Bar(
                y=plot_df_frag['HH_Category'],
                x=plot_df_frag['Percent'],
                name=i,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y}, ' + f'{i} Income - ' + '%{x: .2%}<extra></extra>',
                legendgroup=f'{n}'
            ), row=1, col=1)
            n += 1

        # Comparison plot

        # Generating dataframe for comparison plot
        if year_comparison:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        else:
            if error_region_figure(geo_c, default_year, language):
                return error_region_figure(geo_c, default_year, language)
        plot_df_c = (
            plot_df_core_housing_need_by_priority_population_income(geo, language, int(original_year))
            if year_comparison
            else plot_df_core_housing_need_by_priority_population_income(geo_c, language)
        )

        # Generating comparison plot

        n = 0
        for i, c, o in zip(plot_df['Income_Category'].unique(), colors, income_category_override):
            plot_df_frag_c = plot_df_c.loc[plot_df_c['Income_Category'] == i, :]
            fig6.add_trace(go.Bar(
                y=plot_df_frag_c['HH_Category'],
                x=plot_df_frag_c['Percent'],
                name=i,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y}, ' + f'{i} Income - ' + '%{x: .2%}<extra></extra>',
                legendgroup=f'{n}',
                showlegend=False
            ), row=1, col=2)
            n += 1

        # Plot layout settings

        fig6.update_layout(
            title=localization[language]["Percentage of Households in Core Housing Need by Priority Population and Income Category,"],
            width=900,
            height=500,
            font=dict(size=10),
            legend=dict(font=dict(size=8)),
            legend_traceorder="normal",
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            yaxis=dict(autorange="reversed"),
            barmode='stack',
            plot_bgcolor='#F8F9F9',
            legend_title=localization[language]["Income Category"]
        )
        fig6.update_xaxes(
            title_font=dict(size=10),
            tickfont=dict(size=8),
            fixedrange=True,
            tickformat=',.0%',
            title=localization[language]["% of HH"]
        )
        fig6.update_yaxes(
            fixedrange=True,
            tickfont=dict(size=10)
        )

        return fig6


@callback(
    Output("income-categories-title-pg2", "children"),
    Output("percent-HH-CHN-title-pg2", "children"),
    Output("percent-IC-HH-CHN-title-pg2", "children"),
    Output("housing-deficit-pg2", "children"),
    Output("pct-pp-hh-chn-pg2", "children"),
    Output("pct-pp-ic-chn-pg2", "children"),
    Input('year-comparison', 'data'),
    Input('income-category-affordability-table', 'selected_columns'),
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
