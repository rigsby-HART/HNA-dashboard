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

# 2031 Household Projections by Income Category


# Plot DF/Table Generator

def plot1_new_projection(geo, is_comparison, language, year=default_year):
    geo_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Geo_Code'].tolist()[0]
    updated_csd_filtered = updated_csd_year[year].query('Geo_Code ==' + f"{geo_code_clicked}")

    updated_csd_filtered_current_plot1 = updated_csd_filtered[[
        'Total - Private households by household type including census family structure -   Households with income 20% or under of area median household income (AMHI) - Total - Household size',
        'Total - Private households by household type including census family structure -   Households with income 21% to 50% of AMHI - Total - Household size',
        'Total - Private households by household type including census family structure -   Households with income 51% to 80% of AMHI - Total - Household size',
        'Total - Private households by household type including census family structure -   Households with income 81% to 120% of AMHI - Total - Household size',
        'Total - Private households by household type including census family structure -   Households with income 121% or over of AMHI - Total - Household size'
    ]].T.reset_index().drop(columns=['index'])
    # This predicts 10 years into the future.  I will hardcode the assumption of year + 10
    prediction_year = year + 10
    updated_csd_filtered_future_plot1 = updated_csd_filtered[[
        f'{prediction_year} Population Delta with income 20% or under of area median household income (AMHI)',
        f'{prediction_year} Population Delta with income 21% to 50% of AMHI',
        f'{prediction_year} Population Delta with income 51% to 80% of AMHI',
        f'{prediction_year} Population Delta with income 81% to 120% of AMHI',
        f'{prediction_year} Population Delta with income 121% or over of AMHI'
    ]].T.reset_index().drop(columns=['index'])

    # income_category = ['Very Low Income', 'Low Income', 'Moderate Income', 'Median Income', 'High Income']
    row_labels = ["Very Low Income", "Low Income", "Moderate Income", "Median Income", "High Income"]
    income_category = [localization[language][label] for label in row_labels]
    table1 = pd.DataFrame({'Income Category': income_category,
                           'Category': ([f'{year} pop'] * len(income_category)),
                           'Pop': updated_csd_filtered_current_plot1.iloc[:, 0]})
    table1 = table1.replace([np.inf, -np.inf], 0)
    table1 = table1.fillna(0)
    table1_2021 = table1.copy()

    table1[f'{prediction_year} Delta'] = np.round(updated_csd_filtered_future_plot1.iloc[:, 0], 0)
    table1 = table1.drop(columns=['Category'])

    plot_df = pd.concat([table1_2021,
                         pd.DataFrame({'Income Category': income_category,
                                       'Category': ([f'{prediction_year} Delta'] * len(income_category)),
                                       'Pop': np.round(updated_csd_filtered_future_plot1.iloc[:, 0], 0)})])

    table1['Total'] = table1.sum(axis=1)
    row_total_csd = table1.sum(axis=0)
    row_total_csd[0] = 'Total'
    table1.loc[len(table1['Income Category']), :] = row_total_csd

    if is_comparison is False:
        table1.columns = ['HH Income Category', f'{year} HHs', f'Projected Gain/Loss of HHs by {prediction_year}',
                          'Total']
    else:
        table1.columns = ['HH Income Category', f'{year} HHs ', f'Projected Gain/Loss of HHs by {prediction_year} ',
                          'Total ']

    return plot_df, table1


# Callback logic for the table/plot update

@callback(
    Output('datatable5-interactivity', 'columns'),
    Output('datatable5-interactivity', 'data'),
    Output('datatable5-interactivity', 'style_data_conditional'),
    Output('datatable5-interactivity', 'style_cell_conditional'),
    Output('datatable5-interactivity', 'style_header_conditional'),
    Output('graph9', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('datatable5-interactivity', 'selected_columns'),
    State('url', 'search'),
    cache_args_to_ignore=[3]
)
@cache.memoize()
def update_geo_figure6(geo, geo_c, scale, selected_columns, lang_query):
    language = get_language(lang_query)
    # Single area mode
    prediction_year = default_year+10
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
        plot_df, table1 = plot1_new_projection(geo, False, language)

        # Generating plot
        fig_new_proj_1 = go.Figure()

        for i, c in zip(plot_df['Category'].unique(), bar_colors):
            plot_df_frag = plot_df.loc[plot_df['Category'] == i, :]
            fig_new_proj_1.add_trace(go.Bar(
                x=plot_df_frag['Income Category'],
                y=plot_df_frag['Pop'],
                name=i,
                marker_color=c,
                # orientation = 'h',
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
            title=f'{default_year + 10} {localization[language]["Household Projections by Income Category"]}<br>{geo}',
            legend=dict(font=dict(size=9)),
            legend_title=localization[language]["{prediction_year} households<br>and {year}-{prediction_year} change<br>"].format(year=default_year, prediction_year=prediction_year)
        )
        fig_new_proj_1.update_xaxes(
            title_font=dict(size=10),
            tickfont=dict(size=9),
            fixedrange=True,
            title=localization[language]["Income Category"]
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
                                         'backgroundColor': columns_color_fill[0],
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
            plot1_new_projection(geo, False, language)
        )

        # Generating main plot

        fig_new_proj_1 = make_subplots(rows=1, cols=2, subplot_titles=(geo, geo_c), shared_yaxes=True,
                                       shared_xaxes=True)

        for i, c in zip(plot_df['Category'].unique(), bar_colors):
            plot_df_frag = plot_df.loc[plot_df['Category'] == i, :]
            fig_new_proj_1.add_trace(go.Bar(
                x=plot_df_frag['Income Category'],
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
            plot1_new_projection(geo_c, True, language)
        )

        # Generating comparison plot

        for i, c in zip(plot_df_c['Category'].unique(), bar_colors):
            plot_df_frag = plot_df_c.loc[plot_df_c['Category'] == i, :]
            fig_new_proj_1.add_trace(go.Bar(
                x=plot_df_frag['Income Category'],
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
            title=f'{default_year} {localization[language]["Household Projections by Income Category"]}',
            legend=dict(font=dict(size=9)),
            legend_title=localization[language]["{prediction_year} households<br>and {year}-{prediction_year} change<br>"].format(year=default_year, prediction_year=prediction_year))
        fig_new_proj_1.update_yaxes(
            range=[min(plot_df['Pop'].min(), plot_df_c['Pop'].min()) * 1.1,
                   max(plot_df.groupby('Income Category')['Pop'].sum().max(),
                       plot_df_c.groupby('Income Category')['Pop'].sum().max()) * 1.1],
            title_font=dict(size=10),
            tickfont=dict(size=9),
            fixedrange=True
        )
        fig_new_proj_1.update_xaxes(
            title_font=dict(size=10),
            tickfont=dict(size=9),
            fixedrange=True,
            title=localization[language]["Income Category"]
        )
        fig_new_proj_1.update_yaxes(title=localization[language]["Number of Households"], row=1, col=1)

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

