# Percentage of Indigenous Households in Core Housing Need, by Income Category and HH Size, 2021 (plot)
# and 2021 Affordable Housing Deficit for Indigenous Households (table)
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Output, Input, State, callback
from dash.dash_table.Format import Format, Group, Scheme
from plotly.subplots import make_subplots

from app_file import cache
from helpers.create_engine import default_year, default_value, income_indigenous_year
from helpers.localization import localization
from helpers.style_helper import modebar_color, modebar_activecolor, hh_colors, columns_color_fill, \
    style_data_conditional, style_header_conditional, comparison_font_size
from helpers.table_helper import query_table, get_language, area_scale_primary_only, area_scale_comparison, \
    error_indigenous_table, error_indigenous_figure


x_columns = ['Rent 20% of AMHI',
             'Rent 50% of AMHI',
             'Rent 80% of AMHI',
             'Rent 120% of AMHI',
             'Rent 120% of AMHI'
             ]


x_base = ['Very Low Income',
          'Low Income',
          'Moderate Income',
          'Median Income',
          'High Income',
          ]




# plot df, table generator
def plot_df_core_housing_need_by_amhi(geo, IsComparison, language, year: int = default_year):
    geo, joined_df_filtered = query_table(geo, year, income_indigenous_year)

    x_list = []
    x_list_plot = []

    i = 0
    for b, c in zip(x_base, x_columns):
        value = joined_df_filtered[c].tolist()[0]
        if i < 4:
            if IsComparison != True:
                x = b + " ($" + str(int(float(joined_df_filtered[c].tolist()[0]))) + ")"
                x_plot = " ($" + str(int(float(joined_df_filtered[c].tolist()[0]))) + ")"
            else:
                x = b + " ($" + str(int(float(joined_df_filtered[c].tolist()[0]))) + ") "
                x_plot = " ($" + str(int(float(joined_df_filtered[c].tolist()[0]))) + ") "
            x_list.append(x)
            x_list_plot.append(x_plot)
        else:
            if IsComparison != True:
                x = b + " (>$" + str(int(float(joined_df_filtered[c].tolist()[0]))) + ")"
                x_plot = " (>$" + str(int(float(joined_df_filtered[c].tolist()[0]))) + ")"
            else:
                x = b + " (>$" + str(int(float(joined_df_filtered[c].tolist()[0]))) + ") "
                x_plot = " (>$" + str(int(float(joined_df_filtered[c].tolist()[0]))) + ") "
            x_list.append(x)
            x_list_plot.append(x_plot)
        i += 1

    x_list = [sub.replace('$$', '$') for sub in x_list]
    x_list = [sub.replace('.0', '') for sub in x_list]

    x_list_plot = [sub.replace('$$', '$') for sub in x_list_plot]
    x_list_plot = [sub.replace('.0', '') for sub in x_list_plot]

    income_lv_list = [
        '20% or under of area median household income (AMHI)',
        '21% to 50% of AMHI',
        '51% to 80% of AMHI',
        '81% to 120% of AMHI',
        '121% or more of AMHI'
    ]

    h_hold_value = []
    hh_p_num_list_full = []
    hh_column_name = ['1 person', '2 persons', '3 persons', '4 persons', '5 or more persons household']
    # hh_p_num_list = ['1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']
    row_labels = ["1 Person", "2 Person", "3 Person", "4 Person", "5+ Person"]
    hh_p_num_list = [localization[language][label] for label in row_labels]
    for h, hc in zip(hh_p_num_list, hh_column_name):
        for i in income_lv_list:
            column = f'Aboriginal household status-{hc}-Households with income {i}-Households in core housing need'
            h_hold_value.append(joined_df_filtered[column].tolist()[0])
            hh_p_num_list_full.append(h)

    plot_df = pd.DataFrame({'HH_Size': hh_p_num_list_full, 'Income_Category': x_base * 5, 'Percent': h_hold_value})
    plot_df['Percent'] = np.round(plot_df['Percent'], 2)
    percent = plot_df.groupby('Income_Category')['Percent'].sum().reset_index()
    percent = percent.rename(columns={'Percent': 'Sum'})
    plot_df_final = plot_df.merge(percent, how='left', on='Income_Category')
    plot_df_final['Income_Category'] = x_list_plot * 5
    plot_df_final['Percent'] = plot_df_final['Percent'] / plot_df_final['Sum']
    plot_df_final['Percent'] = plot_df_final['Percent'].fillna(0)
    plot_df_final = plot_df_final.drop(columns=['Sum'])

    # comp_table = plot_df.copy()
    # pdb.set_trace()
    # comp_table = comp_table.rename(columns = {'Income': 'Geography'})

    table = pd.DataFrame({'Income_Category': x_base, 'Income Category (Max. affordable shelter cost)': x_list}) \
        .merge(plot_df.pivot_table(values='Percent', index='Income_Category', columns='HH_Size').reset_index(),
               how='left', on='Income_Category')

    row_total = table.sum(axis=0)
    row_total[0] = 'Total'
    table.loc[5, :] = row_total

    # plot_table = table.drop('Income Category (Max. affordable shelter cost)', axis=1)

    if IsComparison != True:
        # plot_table.columns = ['Income Category', '1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']
        # plot_table['Total'] = plot_table.sum(axis=1)

        table.columns = ['Income Category', 'Income Category (Max. affordable shelter cost)', '1 Person', '2 Person',
                         '3 Person', '4 Person', '5+ Person']
        table['Total'] = table.sum(axis=1)
        table.loc[5, 'Income Category (Max. affordable shelter cost)'] = 'Total'

    else:
        # plot_table.columns = ['Income Category', '1 Person ', '2 Person ', '3 Person ', '4 Person ', '5+ Person ']
        # plot_table['Total '] = plot_table.sum(axis=1)

        table.columns = ['Income Category', 'Income Category (Max. affordable shelter cost) ', '1 Person ', '2 Person ',
                         '3 Person ', '4 Person ', '5+ Person ']
        table['Total '] = table.sum(axis=1)
        table.loc[5, 'Income Category (Max. affordable shelter cost) '] = 'Total'
        # pdb.set_trace()

    return plot_df_final, table



@callback(
    Output('graph2_ind', 'figure'),
    Output('datatable2-interactivity_ind', 'columns'),
    Output('datatable2-interactivity_ind', 'data'),
    Output('datatable2-interactivity_ind', 'style_data_conditional'),
    Output('datatable2-interactivity_ind', 'style_cell_conditional'),
    Output('datatable2-interactivity_ind', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    Input('datatable-interactivity_ind', 'selected_columns'),
    State('url', 'search'),
    cache_args_to_ignore=[4]
)
@cache.memoize()
def update_geo_figure34(geo, geo_c, year_comparison, scale, refresh, lang_query):
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
        if error_indigenous_table(geo, default_year):
            return ([error_indigenous_figure(geo, default_year, language)] + list(
                error_indigenous_table(geo, default_year)))
        plot_df, table2 = plot_df_core_housing_need_by_amhi(geo, False, language)
        table2 = table2.drop('Income Category', axis=1)
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
                hovertemplate='%{y}, ' + f'{localization[language]["HH Size"]}: {h} - ' + '%{x: .2%}<extra></extra>',
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
            title=f'{localization[language]["Percentage of Indigenous Households in Core Housing Need, by Income and HH Size"]}, {default_year}<br>{geo}',
            legend_title=localization[language]["HH Size"]
        )
        fig2.update_yaxes(
            tickfont=dict(size=10),
            fixedrange=True,
            title=f'{localization[language]["Income Category"]}<br>{localization[language]["(Max. affordable shelter costs)"]}'
        )
        fig2.update_xaxes(
            fixedrange=True,
            tickformat=',.0%',
            title=localization[language]["% of Indigenous HH"],
            tickfont=dict(size=10)
        )

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
            col_list.append({"name": [geo + " (Indigenous HH)", i],
                             "id": i,
                             "type": 'numeric',
                             "format": Format(
                                 group=Group.yes,
                                 scheme=Scheme.fixed,
                                 precision=0
                             )})

        return fig2, col_list, table2.to_dict(
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

        # Subplot setting for the comparison mode
        fig2 = make_subplots(rows=1, cols=2, subplot_titles=(
            f"{geo} {compared_year}" if year_comparison else geo,
            f"{geo} {original_year}" if year_comparison else geo_c), shared_xaxes=True)

        # Main Plot

        # Generating dataframe for main plot
        if year_comparison:
            if error_indigenous_table(geo, int(compared_year)):
                return [error_indigenous_figure(geo, int(compared_year), language)] + \
                    list(error_indigenous_table(geo, int(compared_year)))
        else:
            if error_indigenous_table(geo, default_year):
                return [error_indigenous_figure(geo, default_year, language)] + list(
                    error_indigenous_table(geo, default_year))
        plot_df, table2 = (
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

        fig2.update_yaxes(title=f'{localization[language]["Income Category"]}<br>'
                                f'{localization[language]["(Max. affordable shelter costs)"]}', row=1, col=1)

        # Comparison plot

        # Generating dataframe for comparison plot
        if year_comparison:
            if error_indigenous_table(geo, default_year):
                return [error_indigenous_figure(geo, default_year, language)] + list(
                    error_indigenous_table(geo, default_year))
        else:
            if error_indigenous_table(geo_c, default_year):
                return [error_indigenous_figure(geo_c, default_year, language)] + list(
                    error_indigenous_table(geo_c, default_year))
        plot_df_c, table2_c = (
            plot_df_core_housing_need_by_amhi(geo, True, language, int(original_year)) if year_comparison else
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
            title=f'{localization[language]["Percentage of Indigenous Households in Core Housing Need, by Income and HH Size"]}, {default_year}',
            legend_traceorder='normal',
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            barmode='stack',
            plot_bgcolor='#F8F9F9',
            legend_title=localization[language]["HH Size"],
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
            title=localization[language]["% of Indigenous HH"],
            tickfont=dict(size=10)
        )

        # Merging main and comparison table

        table2_j = table2.merge(table2_c, how='left', on='Income Category')
        new_table2_j = table2_j.iloc[:, 1:]
        # pdb.set_trace()
        # Generating Callback output

        col_list = []

        for i in table2.columns[1:]:
            if i == 'Income Category (Max. affordable shelter cost)':
                col_list.append({"name": ["Area (Indigenous HH)", i], "id": i})
            else:
                col_list.append({"name": [f"{geo} {compared_year}" if year_comparison else geo, i],
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
                col_list.append({"name": [f"{geo} {original_year}" if year_comparison else geo_c, i],
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

        return fig2, col_list, new_table2_j.to_dict(
            'record'), style_data_conditional, style_cell_conditional, style_header_conditional