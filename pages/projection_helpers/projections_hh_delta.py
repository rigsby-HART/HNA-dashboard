import numpy as np
import pandas as pd
import plotly.graph_objects as go

from dash import Output, callback, Input, State
from dash.dash_table.Format import Format, Group, Scheme
from plotly.subplots import make_subplots

from app_file import cache
from helpers.create_engine import default_year, mapped_geo_code, updated_csd_year
from helpers.localization import localization
from helpers.style_helper import colors, modebar_color, modebar_activecolor, columns_color_fill, style_data_conditional, \
    style_header_conditional, comparison_font_size, bar_colors
from helpers.table_helper import get_language, area_scale_primary_only, error_region_table_population, \
    area_scale_comparison, default_value

# 2031 Projected Household Gain/Loss (2021 to 2031)

# Presetting global variables for table/plot

income_col_list = ['20% or under of area median household income (AMHI)',
                   '21% to 50% of AMHI',
                   '51% to 80% of AMHI',
                   '81% to 120% of AMHI',
                   '121% or over of AMHI']

pp_list = ['1pp', '2pp', '3pp', '4pp', '5pp']


# Plot DF/Table Generator

def projections_future_deltas(geo, IsComparison, language, year: int = default_year):
    geo_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Geo_Code'].tolist()[0]
    updated_csd_filtered = updated_csd_year[year].query('Geo_Code ==' + f"{geo_code_clicked}")
    # This predicts 10 years into the future.  I will hardcode the assumption of year + 10
    prediction_year = year + 10

    income_l = []
    pp_l = []
    result_csd_l = []

    for i in income_col_list:
        for p in pp_list:
            col_format = f'{prediction_year} Population Delta {p} HH with income {i}'
            income_l.append(i)
            pp_l.append(p)
            result_csd_l.append(updated_csd_filtered[col_format].tolist()[0])

    # income_l = ['Very Low Income'] * 5 + ['Low Income'] * 5 + ['Moderate Income'] * 5 + ['Median Income'] * 5 + [
    #     'High Income'] * 5
    income_l = (
            [localization[language]["Very Low Income"]] * 5 +
            [localization[language]["Low Income"]] * 5 +
            [localization[language]["Moderate Income"]] * 5 +
            [localization[language]["Median Income"]] * 5 +
            [localization[language]["High Income"]] * 5)
    # hh_l = ['1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']
    row_labels = ["1 Person", "2 Person", "3 Person", "4 Person", "5+ Person"]
    hh_l = [localization[language][label] for label in row_labels]

    table3 = pd.DataFrame({'Income Category': income_l, 'HH Category': hh_l * 5, 'value': np.round(result_csd_l, 0)})
    table3 = table3.fillna(0)
    table3 = table3.replace([np.inf, -np.inf], 0)

    table3_csd = table3.pivot_table(values='value', index=['Income Category'], columns=['HH Category'], sort=False)
    table3_csd = table3_csd.reset_index()

    table3_csd_plot = table3

    row_total_csd = table3_csd.sum(axis=0)
    row_total_csd[0] = 'Total'
    table3_csd.loc[5, :] = row_total_csd

    if IsComparison != True:
        table3_csd.columns = ['HH Income Category', '1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']
        table3_csd['Total'] = table3_csd.sum(axis=1)

    else:
        table3_csd.columns = ['HH Income Category', '1 Person ', '2 Person ', '3 Person ', '4 Person ', '5+ Person ']
        table3_csd['Total '] = table3_csd.sum(axis=1)

    return table3_csd, table3_csd_plot


# Callback logic for the table/plot update


@callback(
    Output('datatable7-interactivity', 'columns'),
    Output('datatable7-interactivity', 'data'),
    Output('datatable7-interactivity', 'style_data_conditional'),
    Output('datatable7-interactivity', 'style_cell_conditional'),
    Output('datatable7-interactivity', 'style_header_conditional'),
    Output('graph11', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('datatable7-interactivity', 'selected_columns'),
    State('url', 'search'),
    cache_args_to_ignore=[3]
)
@cache.memoize()
def update_geo_figure8(geo, geo_c, scale, selected_columns, lang_query):
    language = get_language(lang_query)
    # Single area mode

    if (geo == geo_c or geo_c == None or (geo == None and geo_c != None)):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        geo = area_scale_primary_only(geo, scale)

        # Generating plot dataframe/table
        if error_region_table_population(geo, default_year, language):
            return error_region_table_population(geo, default_year, language)
        table1, table1_csd_plot = projections_future_deltas(geo, False, language)

        # Generating plot
        fig_csd = go.Figure()
        for i, c in zip(table1_csd_plot['HH Category'].unique(), colors):
            plot_df_frag = table1_csd_plot.loc[table1_csd_plot['HH Category'] == i, :]
            fig_csd.add_trace(go.Bar(
                x=plot_df_frag['Income Category'],
                y=plot_df_frag['value'],
                name=i,
                marker_color=c,
                # orientation = 'h',
                hovertemplate='%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ))

        # Plot layout settings
        fig_csd.update_layout(
            yaxis_tickformat=',',
            legend_traceorder="normal",
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            barmode='relative',
            plot_bgcolor='#F8F9F9',
            title=f'{default_year + 10} {localization[language]["Projected Household Gain/Loss"]} '
                  f'({default_year} {localization[language]["to"]} {default_year + 10})<br>{geo}',
            legend=dict(font=dict(size=9)),
            legend_title=localization[language]["HH Size"]
        )
        fig_csd.update_xaxes(
            title_font=dict(size=10),
            tickfont=dict(size=9),
            fixedrange=True,
            title=localization[language]["Income Category"]
        )
        fig_csd.update_yaxes(
            title_font=dict(size=10),
            tickfont=dict(size=9),
            fixedrange=True
        )

        # Generating Table Callback output

        col_list = []

        style_cell_conditional = [
                                     {
                                         'if': {'column_id': c},
                                         'minWidth': '100px',
                                         'backgroundColor': columns_color_fill[1]
                                     } for c in table1.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': table1.columns[0]},
                                         'backgroundColor': columns_color_fill[0]
                                     }
                                 ]

        for i in table1.columns:
            col_list.append({"name": [geo, i],
                             "id": i,
                             "type": 'numeric',
                             "format": Format(
                                 group=Group.yes,
                                 scheme=Scheme.fixed,
                                 precision=0
                             )})

        return col_list, table1.to_dict(
            'record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_csd

    # Comparison mode

    else:
        # Area Scaling up/down when user clicks area scale button on page 1
        geo, geo_c = area_scale_comparison(geo, geo_c, scale)
        original_year, compared_year = default_year, default_year

        # Main Plot/Table

        # Generating main plot df/table
        if error_region_table_population(geo, default_year, language):
            return error_region_table_population(geo, default_year, language)
        table1, table1_csd_plot = (
            projections_future_deltas(geo, False, language)
        )

        # Generating main plot

        fig_csd = make_subplots(rows=1, cols=2, subplot_titles=(geo, geo_c), shared_yaxes=True,
                                shared_xaxes=True)

        for i, c in zip(table1_csd_plot['HH Category'].unique(), colors):
            plot_df_frag = table1_csd_plot.loc[table1_csd_plot['HH Category'] == i, :]
            fig_csd.add_trace(go.Bar(
                x=plot_df_frag['Income Category'],
                y=plot_df_frag['value'],
                name=i,
                marker_color=c,
                hovertemplate='%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ), row=1, col=1)

        # Comparison Plot/Table

        # Generating comparison plot df/table
        if error_region_table_population(geo_c, default_year, language):
            return error_region_table_population(geo_c, default_year, language)
        table1_c, table1_csd_plot_c = (
            projections_future_deltas(geo_c, True, language)
        )

        # Generating comparison plot

        for i, c in zip(table1_csd_plot_c['HH Category'].unique(), colors):
            plot_df_frag = table1_csd_plot_c.loc[table1_csd_plot_c['HH Category'] == i, :]
            fig_csd.add_trace(go.Bar(
                x=plot_df_frag['Income Category'],
                y=plot_df_frag['value'],
                name=i,
                marker_color=c,
                showlegend=False,
                hovertemplate='%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ), row=1, col=2)

        # Plot layout settings

        fig_csd.update_layout(
            yaxis_tickformat=',',
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            barmode='relative',
            plot_bgcolor='#F8F9F9',
            title=f'{default_year + 10} {localization[language]["Projected Household Gain/Loss"]} '
                  f'({default_year} {localization[language]["to"]} {default_year + 10})',
            legend=dict(font=dict(size=9)),
            legend_title=localization[language]["HH Size"]
        )
        fig_csd.update_yaxes(
            range=[min(table1_csd_plot.groupby('Income Category')['value'].sum().min(),
                       table1_csd_plot_c.groupby('Income Category')['value'].sum().min()) * 1.1,
                   max(table1_csd_plot.groupby('Income Category')['value'].sum().max(),
                       table1_csd_plot_c.groupby('Income Category')['value'].sum().max()) * 1.1],
            title_font=dict(size=10),
            tickfont=dict(size=9),
            fixedrange=True
        )
        fig_csd.update_xaxes(
            title_font=dict(size=10),
            tickfont=dict(size=9),
            fixedrange=True,
            title=localization[language]["Income Category"]
        )

        # Merging main and comparison table

        table1_j = table1.merge(table1_c, how='left', on='HH Income Category')

        # Generating Table Callback output

        col_list = []

        for i in table1.columns:
            if i == 'HH Income Category':
                col_list.append({"name": ["Areas", i], "id": i})
            else: # Projected Household Gain/Loss Table Name
                col_list.append({"name": [geo, i],
                                 "id": i,
                                 "type": 'numeric',
                                 "format": Format(
                                     group=Group.yes,
                                     scheme=Scheme.fixed,
                                     precision=0
                                 )})

        for i in table1_c.columns[1:]:
            if i == 'HH Income Category':
                col_list.append({"name": ["Areas", i], "id": i})
            else: # Projected Household Gain/Loss Table Name
                col_list.append({"name": [geo_c, i],
                                 "id": i,
                                 "type": 'numeric',
                                 "format": Format(
                                     group=Group.yes,
                                     scheme=Scheme.fixed,
                                     precision=0
                                 )})

        style_cell_conditional = [
                                     {
                                         'if': {'column_id': c},
                                         'font_size': comparison_font_size,
                                         'minWidth': '70px',
                                         'backgroundColor': columns_color_fill[1]
                                     } for c in table1.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': c},
                                         'font_size': comparison_font_size,
                                         'minWidth': '70px',
                                         'backgroundColor': columns_color_fill[2]
                                     } for c in table1_c.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': table1.columns[0]},
                                         'font_size': comparison_font_size,
                                         'backgroundColor': columns_color_fill[0]
                                     }
                                 ]

        return col_list, table1_j.to_dict(
            'record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_csd