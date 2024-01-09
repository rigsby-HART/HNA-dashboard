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
    area_scale_comparison
from pages.page3 import default_value


# 2031 Household Projections by Household Size

# Plot DF/Table Generator

def plot2_new_projection(geo, IsComparison, language, year: int = default_year):
    geo_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Geo_Code'].tolist()[0]
    updated_csd_filtered = updated_csd_year[year].query('Geo_Code ==' + f"{geo_code_clicked}")
    # This predicts 10 years into the future.  I will hardcode the assumption of year + 10
    prediction_year = year + 10

    updated_csd_filtered_current_plot2 = updated_csd_filtered[[
        'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   1pp',
        'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   2pp',
        'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   3pp',
        'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   4pp',
        'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   5pp'
    ]].T.reset_index().drop(columns=['index'])

    updated_csd_filtered_future_plot2 = updated_csd_filtered[[
        f'{prediction_year} Population Delta 1pp HH',
        f'{prediction_year} Population Delta 2pp HH',
        f'{prediction_year} Population Delta 3pp HH',
        f'{prediction_year} Population Delta 4pp HH',
        f'{prediction_year} Population Delta 5pp HH'
    ]].T.reset_index().drop(columns=['index'])

    # hh_category = ['1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']
    row_labels = ["1 Person", "2 Person", "3 Person", "4 Person", "5+ Person"]
    hh_category = [localization[language][label] for label in row_labels]
    table2 = pd.DataFrame({'HH Category': hh_category,
                           'Category': ([f'{str(year)} pop'] * len(hh_category)),
                           'Pop': updated_csd_filtered_current_plot2.iloc[:, 0]})

    table2 = table2.replace([np.inf, -np.inf], 0)
    table2 = table2.fillna(0)

    table2_2021 = table2.copy()

    table2[f'{prediction_year} Delta'] = np.round(updated_csd_filtered_future_plot2.iloc[:, 0], 0)
    table2 = table2.drop(columns=['Category'])

    table2[f'Total {prediction_year} HHs'] = table2.sum(axis=1)
    row_total_csd = table2.sum(axis=0)
    row_total_csd[0] = 'Total'
    table2.loc[len(table2['HH Category']), :] = row_total_csd

    if IsComparison != True:
        table2.columns = ['HH Size', f'{year} HHs', f'Projected Gain/Loss of HHs by {prediction_year}',
                          f'Total {prediction_year} HHs']
    else:
        table2.columns = ['HH Size', f'{year} HHs ', f'Projected Gain/Loss of HHs by {prediction_year} ',
                          f'Total {prediction_year} HHs ']

    plot_df = pd.concat([table2_2021,
                         pd.DataFrame({'HH Category': hh_category,
                                       'Category': ([f'{prediction_year} Delta'] * len(hh_category)),
                                       'Pop': np.round(updated_csd_filtered_future_plot2.iloc[:, 0], 0)})])

    plot_df = plot_df.replace([np.inf, -np.inf], 0)

    return plot_df, table2


# Callback logic for the table/plot update


@callback(
    Output('datatable6-interactivity', 'columns'),
    Output('datatable6-interactivity', 'data'),
    Output('datatable6-interactivity', 'style_data_conditional'),
    Output('datatable6-interactivity', 'style_cell_conditional'),
    Output('datatable6-interactivity', 'style_header_conditional'),
    Output('graph10', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('datatable6-interactivity', 'selected_columns'),
    State('url', 'search'),
    cache_args_to_ignore=[3]
)
@cache.memoize()
def update_geo_figure7(geo, geo_c, scale, selected_columns, lang_query):
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
        plot_df, table1 = plot2_new_projection(geo, False, language)

        # Generating plot
        fig_new_proj_1 = go.Figure()

        for i, c in zip(plot_df['Category'].unique(), bar_colors):
            plot_df_frag = plot_df.loc[plot_df['Category'] == i, :]
            fig_new_proj_1.add_trace(go.Bar(
                x=plot_df_frag['HH Category'],
                y=plot_df_frag['Pop'],
                name=i,
                marker_color=c,
                hovertemplate='%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ))

        # Plot layout settings
        fig_new_proj_1.update_layout(
            yaxis_tickformat=',',
            legend_traceorder="normal",
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            barmode='relative',
            plot_bgcolor='#F8F9F9',
            title=f'{default_year + 10} {localization[language]["Household Projections by Household Size"]}<br>{geo}',
            legend=dict(font=dict(size=9)),
            legend_title=localization[language]["{prediction_year} households<br>and {year}-{prediction_year} change<br>"].format(year=default_year, prediction_year=default_year+10)
        )

        fig_new_proj_1.update_xaxes(
            title_font=dict(size=10),
            tickfont=dict(size=9),
            fixedrange=True,
            title=localization[language]["Household Size"]
        )
        fig_new_proj_1.update_yaxes(
            title_font=dict(size=10),
            tickfont=dict(size=9),
            fixedrange=True,
            title=localization[language]["Number of Households"]
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
            'record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_new_proj_1

    # Comparison mode

    else:
        # Area Scaling up/down when user clicks area scale button on page 1
        geo, geo_c = area_scale_comparison(geo, geo_c, scale)
        original_year, compared_year = default_year, default_year

        # Main Plot/Table

        # Generating main plot df/table
        if error_region_table_population(geo, default_year, language):
            return error_region_table_population(geo, default_year, language)
        plot_df, table1 = (
            plot2_new_projection(geo, False, language)
        )
        # Generating main plot

        fig_new_proj_1 = make_subplots(rows=1, cols=2,
                                       subplot_titles=(geo, geo_c),
                                       shared_yaxes=True,
                                       shared_xaxes=True)

        for i, c in zip(plot_df['Category'].unique(), bar_colors):
            plot_df_frag = plot_df.loc[plot_df['Category'] == i, :]
            fig_new_proj_1.add_trace(go.Bar(
                x=plot_df_frag['HH Category'],
                y=plot_df_frag['Pop'],
                name=i,
                marker_color=c,
                hovertemplate='%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ), row=1, col=1)

        # Comparison Plot/Table

        # Generating comparison plot df/table
        if error_region_table_population(geo_c, default_year, language):
            return error_region_table_population(geo_c, default_year, language)
        plot_df_c, table1_c = (
            plot2_new_projection(geo_c, True, language)
        )

        # Generating comparison plot

        for i, c in zip(plot_df_c['Category'].unique(), bar_colors):
            plot_df_frag = plot_df_c.loc[plot_df_c['Category'] == i, :]
            fig_new_proj_1.add_trace(go.Bar(
                x=plot_df_frag['HH Category'],
                y=plot_df_frag['Pop'],
                name=i,
                marker_color=c,
                showlegend=False,
                hovertemplate='%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ), row=1, col=2)

        # Plot layout settings

        fig_new_proj_1.update_layout(
            yaxis_tickformat=',',
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            barmode='relative',
            plot_bgcolor='#F8F9F9',
            title=f'{default_year+10} {localization[language]["Household Projections by Household Size"]}',
            legend=dict(font=dict(size=9)),
            legend_title=localization[language]["{prediction_year} households<br>and {year}-{prediction_year} change<br>"].format(year=default_year, prediction_year=default_year+10)
        )
        fig_new_proj_1.update_yaxes(
            range=[min(plot_df['Pop'].min(), plot_df_c['Pop'].min()) * 1.1,
                   max(plot_df.groupby('HH Category')['Pop'].sum().max(),
                       plot_df_c.groupby('HH Category')['Pop'].sum().max()) * 1.1],
            title_font=dict(size=10),
            tickfont=dict(size=9),
            fixedrange=True
        )
        fig_new_proj_1.update_xaxes(
            title_font=dict(size=10),
            tickfont=dict(size=9),
            fixedrange=True,
            title='Household Size'
        )
        fig_new_proj_1.update_yaxes(title=localization[language]["Number of Households"], row=1, col=1)

        # Merging main and comparison table

        table1_j = table1.merge(table1_c, how='left', on='HH Size')

        # Generating Table Callback output

        col_list = []

        for i in table1.columns:
            if i == 'HH Size':
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
            if i == 'HH Size':
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
            'record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_new_proj_1