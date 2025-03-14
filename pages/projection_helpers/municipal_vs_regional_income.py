import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from dash import Output, callback, Input, State
from dash.dash_table.Format import Format, Group, Scheme
from plotly.subplots import make_subplots

from app_file import cache
from helpers.create_engine import default_year, mapped_geo_code, updated_csd_year, updated_cd_year
from helpers.localization import localization
from helpers.style_helper import colors, modebar_color, modebar_activecolor, columns_color_fill, style_data_conditional, \
    style_header_conditional, comparison_font_size, bar_colors, comparison_font_size2
from helpers.table_helper import get_language, area_scale_primary_only, error_region_table_population, \
    area_scale_comparison, default_value

# 2031 Projected Municipal vs Regional Household Growth Rates by Income Category

# Presetting global variables for table/plot

# Plot DF/Table Generator

m_r_colors = ['#002145', '#39c0f7']


def projections_future_pop_income(geo, IsComparison, language, year: int = default_year):
    geo_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Geo_Code'].tolist()[0]
    geo_region_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Region_Code'].tolist()[0]
    # This predicts 10 years into the future.  I will hardcode the assumption of year + 10
    prediction_year = year + 10
    updated_csd_filtered = updated_csd_year[year].query('Geo_Code ==' + f"{geo_code_clicked}")
    updated_cd_filtered = updated_cd_year[year].query('Geo_Code ==' + f"{geo_region_code_clicked}")

    income_categories_g11 = [
        'income 20% or under of area median household income (AMHI)',
        'income 21% to 50% of AMHI',
        'income 51% to 80% of AMHI',
        'income 81% to 120% of AMHI',
        'income 121% or over of AMHI'
    ]

    pop_original = []
    gr_csd = []
    gr_cd = []
    tr_cd = []
    delta = []

    # i_l = [
    #     'Very low Income',
    #     'Low Income',
    #     'Moderate Income',
    #     'Median Income',
    #     'High Income'
    # ]
    row_labels = ["Very Low Income", "Low Income", "Moderate Income", "Median Income", "High Income"]
    i_l = [localization[language][label] for label in row_labels]
    for i in income_categories_g11:
        p = updated_csd_filtered[
            f'Total - Private households by household type including census family structure -   Households with {i} - Total - Household size'].tolist()[
            0]
        g = updated_csd_filtered[f'{prediction_year} Population Growth Rate with {i}'].tolist()[0]
        g_cd = updated_cd_filtered[f'{prediction_year} Population Growth Rate with {i}'].tolist()[0]
        t_cd = updated_cd_filtered[f'{prediction_year} Population Trend with {i}'].tolist()[0]
        d = updated_csd_filtered[f'{prediction_year} Population Delta with {i}'].tolist()[0]
        pop_original.append(p)
        gr_csd.append(g)
        gr_cd.append(g_cd)
        tr_cd.append(t_cd)
        delta.append(d)
    table = pd.DataFrame(
        {'Income Category': i_l, 'current pop.': pop_original, 'Muni. Growth (%)': gr_csd, 'Regional Growth (%)': gr_cd,
         'Delta(Muni. GR)': np.round(delta, 0)})

    table = table.replace([np.inf, -np.inf], 0)
    table = table.fillna(0)

    table['Delta(Regional GR)'] = np.round(table['current pop.'] * table['Regional Growth (%)'], 0)
    table[f'{prediction_year} Pop.(Muni.)'] = np.round(table['current pop.'] + (table['current pop.'] * table['Muni. Growth (%)']), 0)
    table[f'{prediction_year} Pop.(Regional)'] = tr_cd

    table_for_plot = table[['Income Category', 'Muni. Growth (%)', 'Regional Growth (%)']]
    table_for_plot.columns = ['Income Category', localization[language]["Municipal"], localization[language]["Regional"]]
    plot_df = table_for_plot.melt(id_vars='Income Category', value_vars=[localization[language]["Municipal"], localization[language]["Regional"]])
    plot_df.columns = ['Income Category', 'Category', 'value']

    table = table.drop(columns=['Delta(Muni. GR)', 'Delta(Regional GR)'])
    table['Muni. Growth (%)'] = np.round(table['Muni. Growth (%)'] * 100, 1).astype(str) + '%'
    table['Regional Growth (%)'] = np.round(table['Regional Growth (%)'] * 100, 1).astype(str) + '%'

    if IsComparison:
        table.columns = ['HH Income Category', f'{year} HHs ', 'Muni. Growth Rate (%) ',
                         'Regional Growth Rate (%) ', f'{prediction_year} HHs (Muni. Rate) ', f'{prediction_year} HHs (Region. Rate) ']
    else:
        table.columns = ['HH Income Category', f'{year} HHs', 'Muni. Growth Rate (%)',
                         'Regional Growth Rate (%)', f'{prediction_year} HHs (Muni. Rate)', f'{prediction_year} HHs (Region. Rate)']

    return table, plot_df


# Callback logic for the table/plot update


@callback(
    Output('datatable8-interactivity', 'columns'),
    Output('datatable8-interactivity', 'data'),
    Output('datatable8-interactivity', 'style_data_conditional'),
    Output('datatable8-interactivity', 'style_cell_conditional'),
    Output('datatable8-interactivity', 'style_header_conditional'),
    Output('graph12', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('datatable8-interactivity', 'selected_columns'),
    State('url', 'search'),
)
@cache.memoize()
def update_geo_figure8(geo, geo_c, scale, selected_columns, lang_query):
    language = get_language(lang_query)
    # If selected area is None
    # -> Set default area (Canada)

    if geo == None:
        geo = default_value

    # If selected area is not CSD
    # -> print 'Not Available in CD/Regional level. Please select CSD/Municipal level'
    if geo_c is None:
        geo = area_scale_primary_only(geo, scale)
    else:
        geo, geo_c = area_scale_comparison(geo, geo_c, scale)
    # This should apply to comparison region too
    clicked_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Geo_Code'].tolist()[0]
    if geo_c is not None:
        clicked_code_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c, :]['Geo_Code'].tolist()[0]
    else:
        clicked_code_c = clicked_code
    if len(str(clicked_code)) < 7 or len(str(clicked_code_c)) < 7:

        table3_csd = pd.DataFrame({localization[language]["Not Available in CD/Regional level. Please select CSD/Municipal level"]: [0]})

        col_list_csd = []

        for i in table3_csd.columns:
            col_list_csd.append({"name": [i],
                                 "id": i, })

        style_cell_conditional_csd = [
                                         {
                                             'if': {'column_id': c},
                                             'backgroundColor': columns_color_fill[1]
                                         } for c in table3_csd.columns[1:]
                                     ] + [
                                         {
                                             'if': {'column_id': table3_csd.columns[0]},
                                             'backgroundColor': columns_color_fill[0],
                                             'width': '130px'
                                         }
                                     ]

        fig_csd = px.line(x=[localization[language]["Not Available in CD/Regional level. Please select CSD/Municipal level"]],
                          y=[localization[language]["Not Available in CD/Regional level. Please select CSD/Municipal level"]])

        return col_list_csd, \
            table3_csd.to_dict('record'), \
            [{
                'if': {'column_id': i},
                'background_color': '#D2F3FF'
            } for i in selected_columns], \
            style_cell_conditional_csd, style_header_conditional, fig_csd

    # Single area mode

    if len(str(clicked_code)) >= 7 and geo_c != None:

        clicked_code_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c, :]['Geo_Code'].tolist()[0]

        if len(str(clicked_code_c)) < 7:
            geo_c = None

    if (geo == geo_c or geo_c == None or (geo == None and geo_c != None)):

        # When no area is selected

        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1

        geo = area_scale_primary_only(geo, scale)

        # Generating plot dataframe/table
        if error_region_table_population(geo, default_year, language, no_cd=True):
            return error_region_table_population(geo, default_year, language, no_cd=True)
        table1, plot_df = projections_future_pop_income(geo, True, language)

        # Generating plot
        fig_pgr = go.Figure()

        for s, c in zip(plot_df['Category'].unique(), m_r_colors):
            plot_df_frag = plot_df.loc[plot_df['Category'] == s, :]

            fig_pgr.add_trace(go.Bar(
                x=plot_df_frag['Income Category'],
                y=plot_df_frag['value'],
                name=s,
                marker_color=c,
                hovertemplate='%{x}, ' + f'{s} - ' + '%{y}<extra></extra>'
            ))

        # Plot layout settings

        fig_pgr.update_layout(
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            plot_bgcolor='#F8F9F9',
            title=f'{default_year+10} {localization[language]["Projected Municipal vs Regional Household Growth Rates by Income Category"]}<br>{geo}',
            legend=dict(font=dict(size=9)),
            legend_title=localization[language]["Category"]
        )
        fig_pgr.update_xaxes(
            title_font=dict(size=10),
            tickfont=dict(size=9),
            fixedrange=True,
            title=localization[language]["Income Category"]
        )
        fig_pgr.update_yaxes(
            title_font=dict(size=10),
            tickfont=dict(size=9),
            fixedrange=True,
            title=localization[language]["Growth Rate (%)"],
            tickformat=',.0%',
            range=[min(0, plot_df['value'].min()), math.ceil(plot_df['value'].max() * 10) / 10]
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
            'record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_pgr

    # Comparison mode

    else:
        # Area Scaling up/down when user clicks area scale button on page 1
        geo, geo_c = area_scale_comparison(geo, geo_c, scale)
        original_year, compared_year = default_year, default_year

        # Main Plot/Table

        # Generating main plot df/table
        if error_region_table_population(geo, default_year, language, no_cd=True):
            return error_region_table_population(geo, default_year, language, no_cd=True)
        table1, plot_df = (
            projections_future_pop_income(geo, False, language)
        )

        # Generating main plot

        fig_pgr = make_subplots(rows=1, cols=2, subplot_titles=(geo, geo_c),
                                shared_yaxes=True,
                                shared_xaxes=True)

        for s, c in zip(plot_df['Category'].unique(), m_r_colors):
            plot_df_frag = plot_df.loc[plot_df['Category'] == s, :]

            fig_pgr.add_trace(go.Bar(
                x=plot_df_frag['Income Category'],
                y=plot_df_frag['value'],
                name=s,
                marker_color=c,
                hovertemplate='%{x}, ' + f'{s} - ' + '%{y}<extra></extra>'

            ), row=1, col=1)

        # Comparison Plot/Table

        # Generating comparison plot df/table
        if error_region_table_population(geo_c, default_year, language, True):
            return error_region_table_population(geo_c, default_year, language, True)
        table1_c, plot_df_c = (
            projections_future_pop_income(geo_c, True, language)
        )

        # Generating comparison plot

        for s, c in zip(plot_df_c['Category'].unique(), m_r_colors):
            plot_df_frag = plot_df_c.loc[plot_df_c['Category'] == s, :]
            # plot_df_frag['Income Category'] = ['Very Low', 'Low', 'Moderate', 'Median', 'High']

            fig_pgr.add_trace(go.Bar(
                x=plot_df_frag['Income Category'],
                y=plot_df_frag['value'],
                name=s,
                marker_color=c,
                hovertemplate='%{x}, ' + f'{s} - ' + '%{y:.0%}<extra></extra>',
                showlegend=False
            ), row=1, col=2)

        # Plot layout settings

        range_ref = plot_df.groupby(['Income Category', 'Category'])['value'].sum()
        range_ref_c = plot_df_c.groupby(['Income Category', 'Category'])['value'].sum()

        fig_pgr.update_layout(
            legend=dict(font=dict(size=9)),
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            plot_bgcolor='#F8F9F9',
            title=f'{int(original_year)+10} {localization[language]["Projected Municipal vs Regional Household Growth Rates by Income Category"]}',
            legend_title=localization[language]["Category"]
        )
        fig_pgr.update_yaxes(
            title_font=dict(size=10),
            tickfont=dict(size=9),
            tickformat=',.0%',
            fixedrange=True,
            range=[min(0, min(range_ref.min(), range_ref_c.min())),
                   math.ceil(max(range_ref.max(), range_ref_c.max()) * 10) / 10]
        )
        fig_pgr.update_yaxes(title=localization[language]["Growth Rate (%)"], row=1, col=1)
        fig_pgr.update_xaxes(
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
            else:
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
            else:
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
                                         'font_size': comparison_font_size2,
                                         'minWidth': '70px',
                                         'backgroundColor': columns_color_fill[1]
                                     } for c in table1.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': c},
                                         'font_size': comparison_font_size2,
                                         'minWidth': '70px',
                                         'backgroundColor': columns_color_fill[2]
                                     } for c in table1_c.columns[1:]
                                 ] + [
                                     {
                                         'if': {'column_id': table1.columns[0]},
                                         'font_size': comparison_font_size2,
                                         'backgroundColor': columns_color_fill[0]
                                     }
                                 ]

        return col_list, table1_j.to_dict(
            'record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_pgr