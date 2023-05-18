# Importing Libraries

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import math as math
import warnings
from dash.dash_table.Format import Format, Scheme, Group
from plotly.subplots import make_subplots
from dash import dcc, dash_table, html, Input, Output, ctx, callback
from sqlalchemy import create_engine

warnings.filterwarnings("ignore")
engine = create_engine('sqlite:///sources//hart.db')

# Importing Geo Code Information

mapped_geo_code = pd.read_sql_table('geocodes_integrated', engine.connect())
df_geo_list = pd.read_sql_table('geocodes', engine.connect())
df_region_list = pd.read_sql_table('regioncodes', engine.connect())
df_region_list.columns = df_geo_list.columns
df_province_list = pd.read_sql_table('provincecodes', engine.connect())
df_province_list.columns = df_geo_list.columns

# Importing Projection Data

updated_csd = pd.read_sql_table('csd_hh_projections', engine.connect()) # CSD level projections
updated_cd = pd.read_sql_table('cd_hh_projections', engine.connect()) # CD level projections

# Configuration for plot icons

config = {'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']}

# Color lists

colors = ['#D7F3FD', '#88D9FA', '#39C0F7', '#099DD7', '#044762']
hh_colors = ['#D8EBD4', '#93CD8A', '#3DB54A', '#297A32', '#143D19']
hh_type_color = ['#3949CE', '#3EB549', '#39C0F7']
columns_color_fill = ['#F3F4F5', '#EBF9FE', '#F0FAF1']
modebar_color = '#099DD7'
modebar_activecolor = '#044762'

# Font size for tables when they are displayed on the comparison mode

comparison_font_size = '0.7em'
comparison_font_size2 = '0.6em'

# Default selected area

default_value = 'Canada'

# Setting a default plot and table which renders before the dashboard is fully loaded

fig = px.line(x = ['Not Available in CD/Regional level. Please select CSD/Municipal level'], y = ['Not Available in CD/Regional level. Please select CSD/Municipal level'])

table = pd.DataFrame({'Not Available in CD/Regional level. Please select CSD/Municipal level':[0]})


# Setting layout for dashboard

layout = html.Div(children = [

        # Fetching Area/Comparison Area/Clicked area scale info in local storage

        dcc.Store(id='area-scale-store', storage_type='local'),
        dcc.Store(id='main-area', storage_type='local'),
        dcc.Store(id='comparison-area', storage_type='local'),

        # Main Layout

        html.Div(
        children = [    

            html.Div([

                # 2026 Household Projections by Income Category 

                html.Div([
                    # Title
                    html.H3(children = html.Strong('2026 Household Projections by Income Category'), className = 'subtitle-lgeo'),
                    # Table Description
                    html.Div([
                        html.H6('This table shows the total number of households in 2016, for each household income category, as well as the projected gain (positive) or loss (negative) of households over the 10-year period between 2016 and 2026 by applying the percentage change from 2006-2016, to 2016 households.')
                    ], className = 'muni-reg-text-lgeo'),

                    # Table

                    html.Div(children = [ 

                        dash_table.DataTable(
                            id='datatable5-interactivity',
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": False} for i in table.columns
                            ],
                            data=table.to_dict('records'),
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 10,
                            style_cell = {'font-family': 'Bahnschrift'},
                            merge_duplicate_headers=True,
                            export_format="xlsx",
                            style_header = {'text-align': 'middle', 'fontWeight': 'bold'}
                        ),
                    ], className = 'pg3-table-lgeo'
                    ),

                    html.Div(id='datatable5-interactivity-container'),

                    # Graph Description
                    html.Div([
                        html.H6('This graph illustrates the above table, displaying the total number of households in 2016, for each income category, with the projected gain of households between 2016 and 2026 stacked on top, and the projected loss of household stacked underneath.')
                    ], className = 'muni-reg-text-lgeo'),

                    # Graph

                    html.Div(children = [ 

                        dcc.Graph(
                            id='graph9',
                            figure=fig,
                            config = config,
                        ),

                    ], className = 'pg3-plot-lgeo'
                    ),

                ], className = 'pg3-table-plot-box-lgeo'),


                # 2026 Household Projections by Household Size

                html.Div([
                    # Title

                    html.H3(children = html.Strong('2026 Household Projections by Household Size'), className = 'subtitle-lgeo'),
                    # Table Description

                    html.Div([
                        html.H6('This table shows the total number of households in 2016, for each household size category, as well as the projected gain (positive) or loss (negative) of households over the 10-year period between 2016 and 2026 by applying the percentage change from 2006-2016, to 2016 households.')
                    ], className = 'muni-reg-text-lgeo'),

                    # Table

                    html.Div([
                        dash_table.DataTable(
                            id='datatable6-interactivity',
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": False} for i in table.columns
                            ],
                            data=table.to_dict('records'),
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 10,
                            style_cell = {'font-family': 'Bahnschrift'},
                            merge_duplicate_headers=True,
                            export_format="xlsx",
                            style_header = {'text-align': 'middle', 'fontWeight': 'bold'}
                        ),
                    ], className = 'pg3-table-lgeo'
                    ),

                    html.Div(id='datatable6-interactivity-container'),

                    # Graph Description

                    html.Div([
                        html.H6('This graph illustrates the above table, displaying the total number of households in 2016, for each size of household, with the projected gain of households between 2016 and 2026 stacked on top, and the projected loss of household stacked underneath.')
                    ], className = 'muni-reg-text-lgeo'),

                    # Graph

                    html.Div(children = [ 
                        dcc.Graph(
                            id='graph10',
                            figure=fig,
                            config = config,
                        ),                            
                    ], className = 'pg3-plot-lgeo'
                    ),
                ], className = 'pg3-table-plot-box-lgeo'),


                # 2026 Projected Households by Household Size and Income Category

                html.Div([
                    # Title

                    html.H3(children = html.Strong('2026 Projected Households by Household Size and Income Category'), className = 'subtitle-lgeo'),

                    # Table Description

                    html.Div([
                        html.H6('This table shows the projected total number of households in 2026 by household size and income category.')
                    ], className = 'muni-reg-text-lgeo'),
                    
                    # Table

                    html.Div([
                        dash_table.DataTable(
                            id='datatable-h-interactivity',
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": False} for i in table.columns
                            ],
                            data=table.to_dict('records'),
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 10,
                            style_cell = {'font-family': 'Bahnschrift'},
                            merge_duplicate_headers=True,
                            export_format="xlsx",
                            style_header = {'text-align': 'middle', 'fontWeight': 'bold'}
                        ),
                    ], className = 'pg3-table-lgeo'
                    ),

                    html.Div(id='datatable-h-interactivity-container'),

                    # Graph Description

                    html.Div([
                        html.H6('This graph illustrates the above table, displaying the projected total number of households in 2026 by household size and income category. Each bar is broken out by the projected number of households within each income category.')
                    ], className = 'muni-reg-text-lgeo'),

                    # Graph

                    html.Div(children = [ 

                        dcc.Graph(
                            id='graph-h',
                            figure=fig,
                            config = config,
                        )

                    ], className = 'pg3-plot-lgeo'
                    ),
                ], className = 'pg3-table-plot-box-lgeo'),

                # 2026 Projected Household Gain/Loss (2016 to 2026)

                html.Div([
    
                    # Title

                    html.H3(children = html.Strong('2026 Projected Household Gain/Loss (2016 to 2026)'), className = 'table-title'),

                    # Table Description

                    html.Div([
                        html.H6('This table shows the projected gain or loss of households by household size and income. These values represent projections for the period between 2016 and 2026.')
                    ], className = 'muni-reg-text-lgeo'),

                    # Table

                    html.Div([
                        dash_table.DataTable(
                            id='datatable7-interactivity',
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": False} for i in table.columns
                            ],
                            data=table.to_dict('records'),
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 10,
                            style_cell = {'font-family': 'Bahnschrift'},
                            merge_duplicate_headers=True,
                            export_format="xlsx",
                            style_header = {'text-align': 'middle', 'fontWeight': 'bold'}
                        ),
                    ], className = 'pg3-table-lgeo'
                    ),

                    html.Div(id='datatable7-interactivity-container'),

                    # Graph Description

                    html.Div([
                        html.H6('This graph illustrates the above table, displaying the projected gain or loss of households between 2016 and 2026 for each size of household. Each bar is broken out by the projected number of households within each income category. Projected loss of households are stacked underneath.')
                    ], className = 'muni-reg-text-lgeo'),

                    # Graph

                    html.Div(children = [ 

                        dcc.Graph(
                            id='graph11',
                            figure=fig,
                            config = config,
                        )
                    ], className = 'pg3-plot-lgeo'
                    ),
                ], className = 'pg3-table-plot-box-lgeo'),

                # Municipal vs Regional Growth Rates

                html.Div([
    
                    # Title
                    html.H3(children = html.Strong('Municipal vs Regional Growth Rates'), className = 'subtitle-lgeo'),

                    # Description
                    html.H6(['Comparing a local community’s growth rates to the growth rate of the region allows for insight into if the community is matching regional patterns of change. There are numerous potential causes for discrepencies, which are further discussed in ', html.A('the project methods.', href = 'https://hart.ubc.ca/wp-content/uploads/2023/03/HNA-Methodology.pdf', target="_blank")])
                ], className = 'muni-reg-text-lgeo'),


                # 2026 Projected Municipal vs Regional Household Growth Rates by Income Category

                html.Div([
                    # Title

                    html.H3(children = html.Strong('2026 Projected Municipal vs Regional Household Growth Rates by Income Category'), className = 'subtitle-lgeo'),

                    # Table Description

                    html.Div([
                        html.H6('The following table illustrates the projected household growth rates between 2016 and 2026 in the community and surrounding region for each income category.')
                    ], className = 'muni-reg-text-lgeo'),

                    # Table

                    html.Div([

                        dash_table.DataTable(
                            id='datatable8-interactivity',
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": False} for i in table.columns
                            ],
                            data=table.to_dict('records'),
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 10,
                            style_cell = {'font-family': 'Bahnschrift'},
                            merge_duplicate_headers=True,
                            export_format="xlsx",
                            style_header = {'text-align': 'middle', 'fontWeight': 'bold'}
                        ),
                    ], className = 'pg3-table-lgeo'
                    ),

                    html.Div(id='datatable8-interactivity-container'),

                    # Graph Description

                    html.Div([
                        html.H6('This graph illustrates the above table, displaying the projected household growth rates between 2016 and 2026 in the community and surrounding region for each income category.')
                    ], className = 'muni-reg-text-lgeo'),

                    # Graph

                    html.Div(children = [ 
                        dcc.Graph(
                            id='graph12',
                            figure=fig,
                            config = config,
                        )
                    ],
                    className = 'pg3-plot-lgeo'
                    ),
                ], className = 'pg3-table-plot-box-lgeo'),

                # Municipal vs Regional Growth Rates by Household Size

                html.Div([
                    # Title

                    html.H3(children = html.Strong('Municipal vs Regional Growth Rates by Household Size'), className = 'subtitle-lgeo'),

                    # Table Description

                    html.Div([
                        html.H6('The following table illustrates the projected household growth rates between 2016 and 2026 in the community and surrounding region for each household size.')
                    ], className = 'muni-reg-text-lgeo'),

                    # Table

                    html.Div([
                        dash_table.DataTable(
                            id='datatable9-interactivity',
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": False} for i in table.columns
                            ],
                            data=table.to_dict('records'),
                            editable=True,
                            sort_action="native",
                            sort_mode="multi",
                            column_selectable=False,
                            row_selectable=False,
                            row_deletable=False,
                            selected_columns=[],
                            selected_rows=[],
                            page_action="native",
                            page_current= 0,
                            page_size= 10,
                            style_cell = {'font-family': 'Bahnschrift'},
                            merge_duplicate_headers=True,
                            export_format="xlsx",
                            style_header = {'text-align': 'middle', 'fontWeight': 'bold'}
                        ),

                    ], className = 'pg3-table-lgeo'
                    ),

                    html.Div(id='datatable9-interactivity-container'),

                    # Graph Description

                    html.Div([
                        html.H6('This graph illustrates the above table, displaying the projected household growth rates between 2016 and 2026 in the community and surrounding region for each income category.')
                    ], className = 'muni-reg-text-lgeo'),

                    # Graph

                    html.Div(children = [ 

                        dcc.Graph(
                            id='graph13',
                            figure=fig,
                            config = config,
                            )
                    ],
                    className = 'pg3-plot-lgeo'
                    ),
                ], className = 'pg3-table-plot-box-lgeo'),

            # LGEO

            html.Div([
                    'This dashboard was created in collaboration with ',  html.A('Licker Geospatial', href = 'https://www.lgeo.co/)', target="_blank"),' using Plotly.'
                ], className = 'lgeo-credit-text'),


        ]),

        ], className = 'dashboard-pg3-lgeo'
    ), 
], className = 'background-pg3-lgeo'
)




# Plot/table generators and callbacks

# Preset row colors for tables

style_data_conditional=[
    {
        'if': {'row_index': 0},
        'backgroundColor': '#b0e6fc',
        'color': '#000000'
    },
    {
        'if': {'row_index': 1},
        'backgroundColor': '#74d3f9',
        'color': '#000000'
    },
    {
        'if': {'row_index': 2},
        'backgroundColor': '#b0e6fc',
        'color': '#000000'
    },
    {
        'if': {'row_index': 3},
        'backgroundColor': '#74d3f9',
        'color': '#000000'
    },
    {
        'if': {'row_index': 4},
        'backgroundColor': '#b0e6fc',
        'color': '#000000'
    },
    {
        'if': {'row_index': 5},
        'backgroundColor': '#39c0f7',
        'color': '#000000'
    },
]

style_header_conditional=[
    {
        'if': {'header_index': 0},
        'backgroundColor': '#002145',
        'color': '#FFFFFF'
    },
    {
        'if': {'header_index': 1},
        'backgroundColor': '#39C0F7',
        'color': '#000000'
    },
]

width_num = 1000


# 2026 Household Projections by Income Category


# Plot DF/Table Generator

def plot1_new_projection(geo, IsComparison):

    geo_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Geo_Code'].tolist()[0]
    updated_csd_filtered = updated_csd.query('Geo_Code ==' +  f"{geo_code_clicked}")

    updated_csd_filtered_2016_plot1 = updated_csd_filtered[[
        'Total - Private households by household type including census family structure -   Households with income 20% or under of area median household income (AMHI) - Total - Household size', 
        'Total - Private households by household type including census family structure -   Households with income 21% to 50% of AMHI - Total - Household size',
        'Total - Private households by household type including census family structure -   Households with income 51% to 80% of AMHI - Total - Household size',
        'Total - Private households by household type including census family structure -   Households with income 81% to 120% of AMHI - Total - Household size',
        'Total - Private households by household type including census family structure -   Households with income 121% or over of AMHI - Total - Household size'
        ]].T.reset_index().drop(columns = ['index'])

    updated_csd_filtered_2026_plot1 = updated_csd_filtered[[
        '2026 Population Delta with income 20% or under of area median household income (AMHI)',
        '2026 Population Delta with income 21% to 50% of AMHI',
        '2026 Population Delta with income 51% to 80% of AMHI',
        '2026 Population Delta with income 81% to 120% of AMHI',
        '2026 Population Delta with income 121% or over of AMHI'
        ]].T.reset_index().drop(columns = ['index'])

    income_category = ['Very Low Income', 'Low Income', 'Moderate Income', 'Median Income', 'High Income']


    table1 = pd.DataFrame({'Income Category': income_category, 
                            'Category': (['2016 Pop'] * len(income_category)),
                            'Pop': updated_csd_filtered_2016_plot1.iloc[:,0]})
    table1 = table1.replace([np.inf, -np.inf], 0)
    table1 = table1.fillna(0)
    table1_2016 = table1.copy()

    table1['2026 Delta'] = np.round(updated_csd_filtered_2026_plot1.iloc[:,0],0)
    table1 = table1.drop(columns = ['Category'])

    plot_df = pd.concat([table1_2016,
                        pd.DataFrame({'Income Category': income_category,
                            'Category': (['2026 Delta'] * len(income_category)),
                            'Pop': np.round(updated_csd_filtered_2026_plot1.iloc[:,0],0)})])
    
    table1['Total'] = table1.sum(axis = 1)
    row_total_csd = table1.sum(axis=0)
    row_total_csd[0] = 'Total'
    table1.loc[len(table1['Income Category']), :] = row_total_csd

    if IsComparison != True:
        table1.columns = ['HH Income Category', '2016 HHs', 'Projected Gain/Loss of HHs by 2026', 'Total']
    else:
        table1.columns = ['HH Income Category', '2016 HHs ', 'Projected Gain/Loss of HHs by 2026 ', 'Total ']
    
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
)
def update_geo_figure6(geo, geo_c, scale, selected_columns):

    # Single area mode

    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Province'].tolist()[0]

        # Generating plot dataframe/table
        plot_df, table1 = plot1_new_projection(geo, False)

        # Generating plot
        fig_new_proj_1 = go.Figure()

        for i, c in zip(plot_df['Category'].unique(), colors[3:]):
            plot_df_frag = plot_df.loc[plot_df['Category'] == i, :]
            fig_new_proj_1.add_trace(go.Bar(
                x = plot_df_frag['Income Category'],
                y = plot_df_frag['Pop'],
                name = i,
                marker_color = c,
                # orientation = 'h', 
                hovertemplate= '%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ))

        # Plot layout settings
        fig_new_proj_1.update_layout(
                                    yaxis_tickformat = ',',
                                    legend_traceorder="normal", 
                                    modebar_color = modebar_color, 
                                    modebar_activecolor = modebar_activecolor, 
                                    barmode='relative', 
                                    plot_bgcolor='#F8F9F9', 
                                    title = f'2026 Household Projections by Income Category<br>{geo}', 
                                    legend = dict(font = dict(size = 9)), 
                                    legend_title = "2016 households<br>and 2016-2026 change<br>"
                                    )
        fig_new_proj_1.update_xaxes(
                                    title_font = dict(size = 10), 
                                    tickfont = dict(size = 9), 
                                    fixedrange = True, 
                                    title = 'Income Category'
                                    )
        fig_new_proj_1.update_yaxes(
                                    title_font = dict(size = 10), 
                                    tickfont = dict(size = 9), 
                                    fixedrange = True, 
                                    title = 'Number of Households'
                                    )


        # Generating Table Callback output
        col_list = []

        style_cell_conditional=[
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

        return col_list, table1.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_new_proj_1


    # Comparison mode

    else:

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
            geo_c = geo_c
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Region'].tolist()[0]
            geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c,:]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Province'].tolist()[0]
            geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c,:]['Province'].tolist()[0]

        # Main Plot/Table

        # Generating main plot df/table

        plot_df, table1 = plot1_new_projection(geo, False)

        # Generating main plot

        fig_new_proj_1 = make_subplots(rows=1, cols=2, subplot_titles=(f"{geo}", f"{geo_c}"), shared_yaxes=True, shared_xaxes=True)

        for i, c in zip(plot_df['Category'].unique(), colors[3:]):
            plot_df_frag = plot_df.loc[plot_df['Category'] == i, :]
            fig_new_proj_1.add_trace(go.Bar(
                x = plot_df_frag['Income Category'],
                y = plot_df_frag['Pop'],
                name = i,
                marker_color = c,
                hovertemplate= '%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ),row = 1, col = 1)


        # Comparison Plot/Table

        # Generating comparison plot df/table

        plot_df_c, table1_c = plot1_new_projection(geo_c, True)

        # Generating comparison plot

        for i, c in zip(plot_df_c['Category'].unique(), colors[3:]):
            plot_df_frag = plot_df_c.loc[plot_df['Category'] == i, :]
            fig_new_proj_1.add_trace(go.Bar(
                x = plot_df_frag['Income Category'],
                y = plot_df_frag['Pop'],
                name = i,
                marker_color = c,
                showlegend = False, 
                hovertemplate= '%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ),row = 1, col = 2)

        # Plot layout settings

        fig_new_proj_1.update_layout(
                                    yaxis_tickformat = ',',
                                    modebar_color = modebar_color, 
                                    modebar_activecolor = modebar_activecolor, 
                                    barmode='relative', 
                                    plot_bgcolor='#F8F9F9', 
                                    title = f'2026 Household Projections by Income Category', 
                                    legend = dict(font = dict(size = 9)), 
                                    legend_title = "2016 households<br>and 2016-2026 change<br>")
        fig_new_proj_1.update_yaxes(
                                    range=[min(plot_df['Pop'].min(), plot_df_c['Pop'].min()) * 1.1, max(plot_df.groupby('Income Category')['Pop'].sum().max(), plot_df_c.groupby('Income Category')['Pop'].sum().max()) * 1.1],
                                    title_font = dict(size = 10), 
                                    tickfont = dict(size = 9), 
                                    fixedrange = True                                    
                                    )
        fig_new_proj_1.update_xaxes(
                                    title_font = dict(size = 10), 
                                    tickfont = dict(size = 9), 
                                    fixedrange = True, 
                                    title = 'Income Category'
                                    )
        fig_new_proj_1.update_yaxes(title = 'Number of Households', row = 1, col = 1)

        # Merging main and comparison table

        table1_j = table1.merge(table1_c, how = 'left', on = 'HH Income Category')

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

        style_cell_conditional=[
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

        return col_list, table1_j.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_new_proj_1




# 2026 Household Projections by Household Size

# Plot DF/Table Generator

def plot2_new_projection(geo, IsComparison):

    geo_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Geo_Code'].tolist()[0]
    updated_csd_filtered = updated_csd.query('Geo_Code ==' +  f"{geo_code_clicked}")

    updated_csd_filtered_2016_plot2 = updated_csd_filtered[[
'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   1pp',
'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   2pp',
'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   3pp',
'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   4pp',
'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   5pp'
        ]].T.reset_index().drop(columns = ['index'])

    updated_csd_filtered_2026_plot2 = updated_csd_filtered[[
    '2026 Population Delta 1pp HH',
    '2026 Population Delta 2pp HH',
    '2026 Population Delta 3pp HH',
    '2026 Population Delta 4pp HH',
    '2026 Population Delta 5pp HH'
        ]].T.reset_index().drop(columns = ['index'])

    hh_category = ['1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']


    table2 = pd.DataFrame({'HH Category': hh_category, 
                            'Category': (['2016 Pop'] * len(hh_category)),
                            'Pop': updated_csd_filtered_2016_plot2.iloc[:,0]})
    
    table2 = table2.replace([np.inf, -np.inf], 0)
    table2 = table2.fillna(0)

    table2_2016 = table2.copy()

    table2['2026 Delta'] = np.round(updated_csd_filtered_2026_plot2.iloc[:,0],0)
    table2 = table2.drop(columns = ['Category'])

    table2['Total'] = table2.sum(axis = 1)
    row_total_csd = table2.sum(axis=0)
    row_total_csd[0] = 'Total'
    table2.loc[len(table2['HH Category']), :] = row_total_csd

    if IsComparison != True:
        table2.columns = ['HH Size', '2016 HHs', 'Projected Gain/Loss of HHs by 2026', 'Total']
    else:
        table2.columns = ['HH Size', '2016 HHs ', 'Projected Gain/Loss of HHs by 2026 ', 'Total ']

    plot_df = pd.concat([table2_2016,
                        pd.DataFrame({'HH Category': hh_category,
                            'Category': (['2026 Delta'] * len(hh_category)),
                            'Pop': np.round(updated_csd_filtered_2026_plot2.iloc[:,0],0)})])
    
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
)
def update_geo_figure7(geo, geo_c, scale, selected_columns):

    # Single area mode

    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Province'].tolist()[0]

        # Generating plot dataframe/table
        plot_df, table1 = plot2_new_projection(geo, False)

        # Generating plot
        fig_new_proj_1 = go.Figure()

        for i, c in zip(plot_df['Category'].unique(), colors[3:]):
            plot_df_frag = plot_df.loc[plot_df['Category'] == i, :]
            fig_new_proj_1.add_trace(go.Bar(
                                            x = plot_df_frag['HH Category'],
                                            y = plot_df_frag['Pop'],
                                            name = i,
                                            marker_color = c,
                                            hovertemplate= '%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
                                        ))

        # Plot layout settings
        fig_new_proj_1.update_layout(
                                    yaxis_tickformat = ',',
                                    legend_traceorder="normal", 
                                    modebar_color = modebar_color, 
                                    modebar_activecolor = modebar_activecolor, 
                                    barmode='relative', 
                                    plot_bgcolor='#F8F9F9', 
                                    title = f'2026 Household Projections by Household Size<br>{geo}', 
                                    legend = dict(font = dict(size = 9)), 
                                    legend_title = "2016 households<br>and 2016-2026 change<br>"
                                    )
        
        fig_new_proj_1.update_xaxes(
                                    title_font = dict(size = 10), 
                                    tickfont = dict(size = 9), 
                                    fixedrange = True, 
                                    title = 'Household Size'
                                    )
        fig_new_proj_1.update_yaxes(
                                    title_font = dict(size = 10), 
                                    tickfont = dict(size = 9), 
                                    fixedrange = True, 
                                    title = 'Number of Households'
                                    )


        # Generating Table Callback output

        col_list = []

        style_cell_conditional=[
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

        return col_list, table1.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_new_proj_1

    # Comparison mode

    else:

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
            geo_c = geo_c
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Region'].tolist()[0]
            geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c,:]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Province'].tolist()[0]
            geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c,:]['Province'].tolist()[0]

        # Main Plot/Table

        # Generating main plot df/table

        plot_df, table1 = plot2_new_projection(geo, False)

        # Generating main plot

        fig_new_proj_1 = make_subplots(rows=1, cols=2, subplot_titles=(f"{geo}", f"{geo_c}"), shared_yaxes=True, shared_xaxes=True)

        for i, c in zip(plot_df['Category'].unique(), colors[3:]):
            plot_df_frag = plot_df.loc[plot_df['Category'] == i, :]
            fig_new_proj_1.add_trace(go.Bar(
                x = plot_df_frag['HH Category'],
                y = plot_df_frag['Pop'],
                name = i,
                marker_color = c,
                hovertemplate= '%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ),row = 1, col = 1)

        # Comparison Plot/Table

        # Generating comparison plot df/table

        plot_df_c, table1_c = plot2_new_projection(geo_c, True)

        # Generating comparison plot

        for i, c in zip(plot_df_c['Category'].unique(), colors[3:]):
            plot_df_frag = plot_df_c.loc[plot_df['Category'] == i, :]
            fig_new_proj_1.add_trace(go.Bar(
                x = plot_df_frag['HH Category'],
                y = plot_df_frag['Pop'],
                name = i,
                marker_color = c,
                showlegend = False,
                hovertemplate= '%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ),row = 1, col = 2)

        # Plot layout settings

        fig_new_proj_1.update_layout(
                                    yaxis_tickformat = ',',
                                    modebar_color = modebar_color, 
                                    modebar_activecolor = modebar_activecolor, 
                                    barmode='relative', 
                                    plot_bgcolor='#F8F9F9', 
                                    title = f'2026 Household Projections by Household Size', 
                                    legend = dict(font = dict(size = 9)), 
                                    legend_title = "2016 households<br>and 2016-2026 change<br>"
                                    )
        fig_new_proj_1.update_yaxes(
                                    range=[min(plot_df['Pop'].min(), plot_df_c['Pop'].min()) * 1.1, max(plot_df.groupby('HH Category')['Pop'].sum().max(), plot_df_c.groupby('HH Category')['Pop'].sum().max()) * 1.1],
                                    title_font = dict(size = 10), 
                                    tickfont = dict(size = 9), 
                                    fixedrange = True
                                    )
        fig_new_proj_1.update_xaxes(
                                    title_font = dict(size = 10), 
                                    tickfont = dict(size = 9), 
                                    fixedrange = True, 
                                    title = 'Household Size'
                                    )
        fig_new_proj_1.update_yaxes(title = 'Number of Households', row = 1, col = 1)

        # Merging main and comparison table

        table1_j = table1.merge(table1_c, how = 'left', on = 'HH Size')

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


        style_cell_conditional=[
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

        return col_list, table1_j.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_new_proj_1




# 2026 Projected Households by Household Size and Income Category

# Presetting global variables for table/plot

income_col_list = ['20% or under of area median household income (AMHI)', 
                    '21% to 50% of AMHI', 
                    '51% to 80% of AMHI', 
                    '81% to 120% of AMHI', 
                    '121% or over of AMHI']

pp_list = ['1pp', '2pp', '3pp', '4pp', '5pp']

# Plot DF/Table Generator

def projections_2026_hh_size(geo, IsComparison):
    
    geo_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Geo_Code'].tolist()[0]
    updated_csd_filtered = updated_csd.query('Geo_Code ==' +  f"{geo_code_clicked}")

    income_l = []
    pp_l = []
    result_csd_l = []


    for i in income_col_list:
        for p in pp_list:
            col_format = f'2026 Projected {p} HH with income {i}'
            income_l.append(i)
            pp_l.append(p)
            result_csd_l.append(updated_csd_filtered[col_format].tolist()[0])

    income_l = ['Very Low Income'] * 5 + ['Low Income'] * 5 + ['Moderate Income'] * 5 + ['Median Income'] * 5 + ['High Income'] * 5
    hh_l = ['1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']
    
    table3 = pd.DataFrame({'Income Category': income_l, 'HH Category': hh_l * 5, 'value': np.round(result_csd_l,0)})
    table3 = table3.fillna(0)
    table3 = table3.replace([np.inf, -np.inf], 0)

    table3_csd = table3.pivot_table(values='value', index=['Income Category'], columns=['HH Category'], sort = False)
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
    Output('datatable-h-interactivity', 'columns'),
    Output('datatable-h-interactivity', 'data'),
    Output('datatable-h-interactivity', 'style_data_conditional'),
    Output('datatable-h-interactivity', 'style_cell_conditional'),
    Output('datatable-h-interactivity', 'style_header_conditional'),
    Output('graph-h', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('datatable-h-interactivity', 'selected_columns'),
)
def update_geo_figure_h(geo, geo_c, scale, selected_columns):

    # Single area mode

    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected

        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1

        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Province'].tolist()[0]

        # Generating plot dataframe/table

        table1, table1_csd_plot = projections_2026_hh_size(geo, False)

        # Generating plot

        fig_csd = go.Figure()
        for i, c in zip(table1_csd_plot['HH Category'].unique(), colors):
            plot_df_frag = table1_csd_plot.loc[table1_csd_plot['HH Category'] == i, :]
            fig_csd.add_trace(go.Bar(
                x = plot_df_frag['Income Category'],
                y = plot_df_frag['value'],
                name = i,
                marker_color = c,
                # orientation = 'h', 
                hovertemplate= '%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ))

        # Plot layout settings
        fig_csd.update_layout(
                            yaxis_tickformat = ',',
                            legend_traceorder="normal", 
                            modebar_color = modebar_color, 
                            modebar_activecolor = modebar_activecolor, 
                            barmode='relative', 
                            plot_bgcolor='#F8F9F9', 
                            title = f'2026 Projected Households by Household Size and Income Category<br>{geo}', 
                            legend = dict(font = dict(size = 9)), 
                            legend_title = "HH Size"
                            )
        fig_csd.update_xaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9), 
                            fixedrange = True, 
                            title = 'Income Category'
                            )
        fig_csd.update_yaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9), 
                            fixedrange = True, 
                            title = 'Number of Households'
                            )

        # Generating Table Callback output

        col_list = []

        style_cell_conditional=[
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

        return col_list, table1.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_csd

    # Comparison mode

    else:

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
            geo_c = geo_c
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Region'].tolist()[0]
            geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c,:]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Province'].tolist()[0]
            geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c,:]['Province'].tolist()[0]

        # Main Plot/Table

        # Generating main plot df/table

        table1, table1_csd_plot = projections_2026_hh_size(geo, False)

        # Generating main plot

        fig_csd = make_subplots(rows=1, cols=2, subplot_titles=(f"{geo}", f"{geo_c}"), shared_yaxes=True, shared_xaxes=True)

        for i, c in zip(table1_csd_plot['HH Category'].unique(), colors):
            plot_df_frag = table1_csd_plot.loc[table1_csd_plot['HH Category'] == i, :]
            fig_csd.add_trace(go.Bar(
                x = plot_df_frag['Income Category'],
                y = plot_df_frag['value'],
                name = i,
                marker_color = c,
                hovertemplate= '%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ),row = 1, col = 1)


        # Comparison Plot/Table

        # Generating comparison plot df/table
        table1_c, table1_csd_plot_c = projections_2026_hh_size(geo_c, True)

        for i, c in zip(table1_csd_plot_c['HH Category'].unique(), colors):
            plot_df_frag = table1_csd_plot_c.loc[table1_csd_plot_c['HH Category'] == i, :]
            fig_csd.add_trace(go.Bar(
                x = plot_df_frag['Income Category'],
                y = plot_df_frag['value'],
                name = i,
                marker_color = c,
                showlegend = False,
                hovertemplate= '%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ),row = 1, col = 2)

        # Plot layout settings

        fig_csd.update_layout(
                                yaxis_tickformat = ',',
                                modebar_color = modebar_color, 
                                modebar_activecolor = modebar_activecolor, 
                                barmode='relative', 
                                plot_bgcolor='#F8F9F9', 
                                title = f'2026 Projected Households by Household Size and Income Category', 
                                legend = dict(font = dict(size = 9)), 
                                legend_title = "HH Size"
                                )
        fig_csd.update_yaxes(
                                range=[0, max(table1_csd_plot.groupby('Income Category')['value'].sum().max(), table1_csd_plot_c.groupby('Income Category')['value'].sum().max()) * 1.1],
                                title_font = dict(size = 10), 
                                tickfont = dict(size = 9), 
                                fixedrange = True
                                )
        fig_csd.update_xaxes(
                                title_font = dict(size = 10), 
                                tickfont = dict(size = 9), 
                                fixedrange = True, 
                                title = 'Income Category'
                                )
        fig_csd.update_yaxes(title = 'Number of Households', row = 1, col = 1)

        # Merging main and comparison table

        table1_j = table1.merge(table1_c, how = 'left', on = 'HH Income Category')

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

        style_cell_conditional=[
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

        return col_list, table1_j.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_csd




# 2026 Projected Household Gain/Loss (2016 to 2026)

# Presetting global variables for table/plot

income_col_list = ['20% or under of area median household income (AMHI)', 
                    '21% to 50% of AMHI', 
                    '51% to 80% of AMHI', 
                    '81% to 120% of AMHI', 
                    '121% or over of AMHI']

pp_list = ['1pp', '2pp', '3pp', '4pp', '5pp']

# Plot DF/Table Generator

def projections_2026_deltas(geo, IsComparison):
    
    geo_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Geo_Code'].tolist()[0]
    updated_csd_filtered = updated_csd.query('Geo_Code ==' +  f"{geo_code_clicked}")

    income_l = []
    pp_l = []
    result_csd_l = []

    for i in income_col_list:
        for p in pp_list:
            col_format = f'2026 Population Delta {p} HH with income {i}'
            income_l.append(i)
            pp_l.append(p)
            result_csd_l.append(updated_csd_filtered[col_format].tolist()[0])

    income_l = ['Very Low Income'] * 5 + ['Low Income'] * 5 + ['Moderate Income'] * 5 + ['Median Income'] * 5 + ['High Income'] * 5
    hh_l = ['1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']
    
    table3 = pd.DataFrame({'Income Category': income_l, 'HH Category': hh_l * 5, 'value': np.round(result_csd_l,0)})
    table3 = table3.fillna(0)
    table3 = table3.replace([np.inf, -np.inf], 0)

    table3_csd = table3.pivot_table(values='value', index=['Income Category'], columns=['HH Category'], sort = False)
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
)
def update_geo_figure8(geo, geo_c, scale, selected_columns):

    # Single area mode

    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Province'].tolist()[0]

        # Generating plot dataframe/table
        table1, table1_csd_plot = projections_2026_deltas(geo, False)

        # Generating plot
        fig_csd = go.Figure()
        for i, c in zip(table1_csd_plot['HH Category'].unique(), colors):
            plot_df_frag = table1_csd_plot.loc[table1_csd_plot['HH Category'] == i, :]
            fig_csd.add_trace(go.Bar(
                x = plot_df_frag['Income Category'],
                y = plot_df_frag['value'],
                name = i,
                marker_color = c,
                # orientation = 'h', 
                hovertemplate= '%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ))

        # Plot layout settings
        fig_csd.update_layout(
                            yaxis_tickformat = ',',
                            legend_traceorder="normal", 
                            modebar_color = modebar_color, 
                            modebar_activecolor = modebar_activecolor, 
                            barmode='relative', 
                            plot_bgcolor='#F8F9F9', 
                            title = f'2026 Projected Household Gain/Loss (2016 to 2026)<br>{geo}', 
                            legend = dict(font = dict(size = 9)), 
                            legend_title = "HH Size"
                            )
        fig_csd.update_xaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9), 
                            fixedrange = True, 
                            title = 'Income Category'
                            )
        fig_csd.update_yaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9), 
                            fixedrange = True
                            )

        # Generating Table Callback output

        col_list = []

        style_cell_conditional=[
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

        return col_list, table1.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_csd

    # Comparison mode

    else:

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
            geo_c = geo_c
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Region'].tolist()[0]
            geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c,:]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Province'].tolist()[0]
            geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c,:]['Province'].tolist()[0]

        # Main Plot/Table

        # Generating main plot df/table

        table1, table1_csd_plot = projections_2026_deltas(geo, False)

        # Generating main plot

        fig_csd = make_subplots(rows=1, cols=2, subplot_titles=(f"{geo}", f"{geo_c}"), shared_yaxes=True, shared_xaxes=True)

        for i, c in zip(table1_csd_plot['HH Category'].unique(), colors):
            plot_df_frag = table1_csd_plot.loc[table1_csd_plot['HH Category'] == i, :]
            fig_csd.add_trace(go.Bar(
                x = plot_df_frag['Income Category'],
                y = plot_df_frag['value'],
                name = i,
                marker_color = c,
                hovertemplate= '%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ),row = 1, col = 1)

        # Comparison Plot/Table

        # Generating comparison plot df/table

        table1_c, table1_csd_plot_c = projections_2026_deltas(geo_c, True)

        # Generating comparison plot

        for i, c in zip(table1_csd_plot_c['HH Category'].unique(), colors):
            plot_df_frag = table1_csd_plot_c.loc[table1_csd_plot_c['HH Category'] == i, :]
            fig_csd.add_trace(go.Bar(
                x = plot_df_frag['Income Category'],
                y = plot_df_frag['value'],
                name = i,
                marker_color = c,
                showlegend = False,
                hovertemplate= '%{x}, ' + f'{i} - ' + '%{y}<extra></extra>'
            ),row = 1, col = 2)

        # Plot layout settings
        
        fig_csd.update_layout(
                            yaxis_tickformat = ',',
                            modebar_color = modebar_color, 
                            modebar_activecolor = modebar_activecolor, 
                            barmode='relative', 
                            plot_bgcolor='#F8F9F9', 
                            title = f'2026 Projected Household Gain/Loss (2016 to 2026)', 
                            legend = dict(font = dict(size = 9)), 
                            legend_title = "HH Size"
                            )
        fig_csd.update_yaxes(
                            range=[min(table1_csd_plot.groupby('Income Category')['value'].sum().min(), table1_csd_plot_c.groupby('Income Category')['value'].sum().min()) * 1.1, max(table1_csd_plot.groupby('Income Category')['value'].sum().max(), table1_csd_plot_c.groupby('Income Category')['value'].sum().max()) * 1.1],
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9), 
                            fixedrange = True
                            )
        fig_csd.update_xaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9), 
                            fixedrange = True, 
                            title = 'Income Category'
                            )

        # Merging main and comparison table

        table1_j = table1.merge(table1_c, how = 'left', on = 'HH Income Category')

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

        style_cell_conditional=[
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

        return col_list, table1_j.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_csd


# 2026 Projected Municipal vs Regional Household Growth Rates by Income Category

# Presetting global variables for table/plot

# Plot DF/Table Generator

m_r_colors = ['#002145', '#39c0f7']

def projections_2026_pop_income(geo, IsComparison):

    geo_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Geo_Code'].tolist()[0]
    geo_region_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Region_Code'].tolist()[0]
    updated_csd_filtered = updated_csd.query('Geo_Code ==' +  f"{geo_code_clicked}")
    updated_cd_filtered = updated_cd.query('Geo_Code ==' +  f"{geo_region_code_clicked}")
    updated_csd_filtered

    income_categories_g11 = [
        'income 20% or under of area median household income (AMHI)',
        'income 21% to 50% of AMHI',
        'income 51% to 80% of AMHI',
        'income 81% to 120% of AMHI',
        'income 121% or over of AMHI'
    ]

    pop_2016 = []
    gr_csd = []
    gr_cd = []
    delta = []

    i_l = [
        'Very low Income',
        'Low Income',
        'Moderate Income',
        'Median Income',
        'High Income'
        ]

    for i in income_categories_g11:
        p = updated_csd_filtered[f'Total - Private households by household type including census family structure -   Households with {i} - Total - Household size'].tolist()[0]
        g = updated_csd_filtered[f'2026 Population Growth Rate with {i}'].tolist()[0]
        g_cd = updated_cd_filtered[f'2026 Population Growth Rate with {i}'].tolist()[0]
        d = updated_csd_filtered[f'2026 Population Delta with {i}'].tolist()[0]
        pop_2016.append(p)
        gr_csd.append(g)
        gr_cd.append(g_cd)
        delta.append(d)

    table = pd.DataFrame({'Income Category':  i_l, '2016 Pop.': pop_2016, 'Muni. Growth (%)': gr_csd, 'Regional Growth (%)': gr_cd, 'Delta(Muni. GR)': np.round(delta, 0)})

    table = table.replace([np.inf, -np.inf], 0)
    table = table.fillna(0)

    table['Delta(Regional GR)'] = np.round(table['2016 Pop.'] * table['Regional Growth (%)'], 0)
    table['2026 Pop.(Muni.)'] = np.round(table['2016 Pop.'] + (table['2016 Pop.'] * table['Muni. Growth (%)']), 0)
    table['2026 Pop.(Regional)'] = np.round(table['2016 Pop.'] + (table['2016 Pop.'] * table['Regional Growth (%)']), 0)

    table_for_plot = table[['Income Category', 'Muni. Growth (%)', 'Regional Growth (%)']]
    table_for_plot.columns = ['Income Category', 'Municipal', 'Regional']
    plot_df = table_for_plot.melt(id_vars = 'Income Category', value_vars = ['Municipal', 'Regional'])
    plot_df.columns = ['Income Category', 'Category', 'value']

    table = table.drop(columns = ['Delta(Muni. GR)', 'Delta(Regional GR)'])
    table['Muni. Growth (%)'] = np.round(table['Muni. Growth (%)']*100,1).astype(str) + '%'
    table['Regional Growth (%)'] = np.round(table['Regional Growth (%)']*100,1).astype(str) + '%'

    if IsComparison == True:

        table.columns = ['HH Income Category', '2016 HHs ', 'Muni. Growth Rate (%) ',
           'Regional Growth Rate (%) ', '2026 HHs (Muni. Rate) ', '2026 HHs (Region. Rate) ']
        
    else:
        table.columns = ['HH Income Category', '2016 HHs', 'Muni. Growth Rate (%)',
           'Regional Growth Rate (%)', '2026 HHs (Muni. Rate)', '2026 HHs (Region. Rate)']

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
)
def update_geo_figure8(geo, geo_c, scale, selected_columns):

    # If selected area is None
    # -> Set default area (Canada)

    if geo == None:
        geo = default_value

    # If selected area is not CSD
    # -> print 'Not Available in CD/Regional level. Please select CSD/Municipal level'

    clicked_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Geo_Code'].tolist()[0]

    if len(str(clicked_code)) < 7 and geo != None and geo_c == None:

        table3_csd = pd.DataFrame({'Not Available in CD/Regional level. Please select CSD/Municipal level':[0]})
        
        col_list_csd = []

        for i in table3_csd.columns:
            col_list_csd.append({"name": [i],
                                    "id": i, })


        style_cell_conditional_csd=[
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


        fig_csd = px.line(x = ['Not Available in CD/Regional level. Please select CSD/Municipal level'], y = ['Not Available in CD/Regional level. Please select CSD/Municipal level'])

        return col_list_csd, \
                table3_csd.to_dict('record'), \
                [{
                    'if': { 'column_id': i },
                    'background_color': '#D2F3FF'
                } for i in selected_columns], \
                style_cell_conditional_csd, fig_csd

    # Single area mode

    if len(str(clicked_code)) >= 7 and geo_c != None:
       
        clicked_code_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c, :]['Geo_Code'].tolist()[0]
        
        if len(str(clicked_code_c)) < 7:
            geo_c = None

    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):

        # When no area is selected    

        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1

        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Province'].tolist()[0]

        # Generating plot dataframe/table
        table1, plot_df = projections_2026_pop_income(geo, True)

        # Generating plot
        fig_pgr = go.Figure()

        for s, c in zip(plot_df['Category'].unique(), m_r_colors):

            plot_df_frag = plot_df.loc[plot_df['Category'] == s, :]

            fig_pgr.add_trace(go.Bar(
                x = plot_df_frag['Income Category'],
                y = plot_df_frag['value'],
                name = s,
                marker_color = c,
                hovertemplate= '%{x}, ' + f'{s} - ' + '%{y}<extra></extra>'
            ))

        # Plot layout settings

        fig_pgr.update_layout(
                            modebar_color = modebar_color, 
                            modebar_activecolor = modebar_activecolor, 
                            plot_bgcolor='#F8F9F9', 
                            title = f'2026 Projected Municipal vs Regional Household Growth Rates by Income Category<br>{geo}', 
                            legend = dict(font = dict(size = 9)), 
                            legend_title = "Category"
                            )
        fig_pgr.update_xaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9), 
                            fixedrange = True, 
                            title = 'Income Category'
                            )
        fig_pgr.update_yaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9), 
                            fixedrange = True, 
                            title = 'Growth Rate (%)', 
                            tickformat =  ',.0%', 
                            range=[min(0,plot_df['value'].min()), math.ceil(plot_df['value'].max()*10)/10]
                            )

        # Generating Table Callback output

        col_list = []

        style_cell_conditional=[
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

        return col_list, table1.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_pgr

    # Comparison mode

    else:

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
            geo_c = geo_c
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Region'].tolist()[0]
            geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c,:]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Province'].tolist()[0]
            geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c,:]['Province'].tolist()[0]

        # Main Plot/Table

        # Generating main plot df/table

        table1, plot_df = projections_2026_pop_income(geo, True)

        # Generating main plot

        fig_pgr = make_subplots(rows=1, cols=2, subplot_titles=(f"{geo}", f"{geo_c}"), shared_yaxes=True, shared_xaxes=True)

        for s, c in zip(plot_df['Category'].unique(), m_r_colors):
            
            plot_df_frag = plot_df.loc[plot_df['Category'] == s, :]
           
            fig_pgr.add_trace(go.Bar(
                x = plot_df_frag['Income Category'],
                y = plot_df_frag['value'],
                name = s,
                marker_color = c,
                hovertemplate= '%{x}, ' + f'{s} - ' + '%{y}<extra></extra>'

            ),row = 1, col = 1)


        # Comparison Plot/Table

        # Generating comparison plot df/table

        table1_c, plot_df_c = projections_2026_pop_income(geo_c, False)

        # Generating comparison plot

        for s, c in zip(plot_df_c['Category'].unique(), m_r_colors):
            
            plot_df_frag = plot_df_c.loc[plot_df_c['Category'] == s, :]
            # plot_df_frag['Income Category'] = ['Very Low', 'Low', 'Moderate', 'Median', 'High']
            
            fig_pgr.add_trace(go.Bar(
                x = plot_df_frag['Income Category'],
                y = plot_df_frag['value'],
                name = s,
                marker_color = c,
                hovertemplate= '%{x}, ' + f'{s} - ' + '%{y:.0%}<extra></extra>',
                showlegend = False
            ),row = 1, col = 2)

        # Plot layout settings
                
        range_ref = plot_df.groupby(['Income Category', 'Category'])['value'].sum()
        range_ref_c = plot_df_c.groupby(['Income Category', 'Category'])['value'].sum()

        fig_pgr.update_layout(
                            legend = dict(font = dict(size = 9)), 
                            modebar_color = modebar_color, 
                            modebar_activecolor = modebar_activecolor, 
                            plot_bgcolor='#F8F9F9', 
                            title = f'2026 Projected Municipal vs Regional Household Growth Rates by Income Category', 
                            legend_title = "Category"
                            )
        fig_pgr.update_yaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9), 
                            tickformat =  ',.0%', 
                            fixedrange = True, 
                            range=[min(0, min(range_ref.min(), range_ref_c.min())), math.ceil(max(range_ref.max(), range_ref_c.max())*10)/10]
                            )
        fig_pgr.update_yaxes(title = 'Growth Rate (%)', row = 1, col = 1)
        fig_pgr.update_xaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9),  
                            fixedrange = True, 
                            title = 'Income Category'
                            )

        # Merging main and comparison table

        table1_j = table1.merge(table1_c, how = 'left', on = 'HH Income Category')

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

        style_cell_conditional=[
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

        return col_list, table1_j.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_pgr



# Municipal vs Regional Growth Rates by Household Size

# Plot DF/Table Generator

def projections_2026_pop_hh(geo, IsComparison):

    geo_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Geo_Code'].tolist()[0]
    geo_region_code_clicked = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, 'Region_Code'].tolist()[0]
    updated_csd_filtered = updated_csd.query('Geo_Code ==' +  f"{geo_code_clicked}")
    updated_cd_filtered = updated_cd.query('Geo_Code ==' +  f"{geo_region_code_clicked}")
    updated_csd_filtered

    hh_category = [
        '1pp',
        '2pp',
        '3pp',
        '4pp',
        '5pp'
    ]

    pop_2016 = []
    gr_csd = []
    gr_cd = []
    delta = []

    h_l = ['1 Person', '2 People', '3 People', '4 People', '5+ People']

    for i in hh_category:
        p = updated_csd_filtered[f'Total - Private households by household type including census family structure - Total – Private households by household income proportion to AMHI_1 -   {i}'].tolist()[0]
        g = updated_csd_filtered[f'2026 Population Growth Rate {i} HH'].tolist()[0]
        g_cd = updated_cd_filtered[f'2026 Population Growth Rate {i} HH'].tolist()[0]
        d = updated_csd_filtered[f'2026 Population Delta {i} HH'].tolist()[0]
        pop_2016.append(p)
        gr_csd.append(g)
        gr_cd.append(g_cd)
        delta.append(d)

    table = pd.DataFrame({'HH Category':  h_l, '2016 Pop.': pop_2016, 'Muni. Growth (%)': gr_csd, 'Regional Growth (%)': gr_cd, 'Delta(Muni. GR)': np.round(delta, 0)})

    table = table.replace([np.inf, -np.inf], 0)
    table = table.fillna(0)

    table['Delta(Regional GR)'] = np.round(table['2016 Pop.'] * table['Regional Growth (%)'], 0)
    table['2026 Pop.(Muni.)'] = np.round(table['2016 Pop.'] + (table['2016 Pop.'] * table['Muni. Growth (%)']), 0)
    table['2026 Pop.(Regional)'] = np.round(table['2016 Pop.'] + (table['2016 Pop.'] * table['Regional Growth (%)']), 0)

    table_for_plot = table[['HH Category', 'Muni. Growth (%)', 'Regional Growth (%)']]
    table_for_plot.columns = ['HH Category', 'Municipal', 'Regional']
    plot_df = table_for_plot.melt(id_vars = 'HH Category', value_vars = ['Municipal', 'Regional'])
    plot_df.columns = ['HH Category', 'Category', 'value']

    table = table.drop(columns = ['Delta(Muni. GR)', 'Delta(Regional GR)'])
    table['Muni. Growth (%)'] = np.round(table['Muni. Growth (%)']*100,1).astype(str) + '%'
    table['Regional Growth (%)'] = np.round(table['Regional Growth (%)']*100,1).astype(str) + '%'

    if IsComparison == True:
   
        table.columns = ['HH Size', '2016 HHs ', 'Muni. Growth Rate (%) ',
           'Regional Growth Rate (%) ', '2026 HHs (Muni. Rate) ', '2026 HHs (Region. Rate) ']

    else:
        table.columns = ['HH Size', '2016 HHs', 'Muni. Growth Rate (%)',
           'Regional Growth Rate (%)', '2026 HHs (Muni. Rate)', '2026 HHs (Region. Rate)']
        
    table['HH Size'] = ['1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']

    return table, plot_df

# Callback logic for the table/plot update

@callback(
    Output('datatable9-interactivity', 'columns'),
    Output('datatable9-interactivity', 'data'),
    Output('datatable9-interactivity', 'style_data_conditional'),
    Output('datatable9-interactivity', 'style_cell_conditional'),
    Output('datatable9-interactivity', 'style_header_conditional'),
    Output('graph13', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('datatable9-interactivity', 'selected_columns'),
)
def update_geo_figure9(geo, geo_c, scale, selected_columns):

    # If selected area is None
    # -> Set default area (Canada)

    if geo == None:
        geo = default_value

    # If selected area is not CSD
    # -> print 'Not Available in CD/Regional level. Please select CSD/Municipal level'

    clicked_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]['Geo_Code'].tolist()[0]

    if len(str(clicked_code)) < 7 and geo != None and geo_c == None:

        table3_csd = pd.DataFrame({'Not Available in CD/Regional level. Please select CSD/Municipal level':[0]})
        
        col_list_csd = []

        for i in table3_csd.columns:
            col_list_csd.append({"name": [i],
                                    "id": i, })


        style_cell_conditional_csd=[
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


        fig_csd = px.line(x = ['Not Available in CD/Regional level. Please select CSD/Municipal level'], y = ['Not Available in CD/Regional level. Please select CSD/Municipal level'])

        return col_list_csd, \
                table3_csd.to_dict('record'), \
                [{
                    'if': { 'column_id': i },
                    'background_color': '#D2F3FF'
                } for i in selected_columns], \
                style_cell_conditional_csd, fig_csd

    # Single area mode

    if len(str(clicked_code)) >= 7 and geo_c != None:
       
        clicked_code_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c, :]['Geo_Code'].tolist()[0]

        if len(str(clicked_code_c)) < 7:
            geo_c = None

    if geo == geo_c or geo_c == None or (geo == None and geo_c != None):
        
        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Province'].tolist()[0]

        # Generating plot dataframe/table
        table1, plot_df = projections_2026_pop_hh(geo, True)

        # Generating plot
        fig_pgr = go.Figure()

        for s, c in zip(plot_df['Category'].unique(), m_r_colors):
            
            plot_df_frag = plot_df.loc[plot_df['Category'] == s, :]
            plot_df_frag['HH Category'] = ['1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']
            
            fig_pgr.add_trace(go.Bar(
                x = plot_df_frag['HH Category'],
                y = plot_df_frag['value'],
                name = s,
                marker_color = c,
                hovertemplate= '%{x}, ' + f'{s} - ' + '%{y}<extra></extra>'
            ))

        # Plot layout settings
        fig_pgr.update_layout(
                            modebar_color = modebar_color, 
                            modebar_activecolor = modebar_activecolor, 
                            plot_bgcolor='#F8F9F9', 
                            title = f'2026 Projected Community and Regional Household Growth Rates <br>{geo}', 
                            legend = dict(font = dict(size = 9)), 
                            legend_title = "Population"
                            )
        fig_pgr.update_xaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9), 
                            fixedrange = True, 
                            title = 'Household Size'
                            )
        fig_pgr.update_yaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9), 
                            title = 'Growth Rate (%)', 
                            fixedrange = True, 
                            tickformat =  ',.0%', 
                            range=[min(0,plot_df['value'].min()), math.ceil(plot_df['value'].max()*10)/10]
                            )

        # Generating Table Callback output

        col_list = []

        style_cell_conditional=[
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

        return col_list, table1.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_pgr

    # Comparison mode

    else:

        # Area Scaling up/down when user clicks area scale button on page 1
        if "to-geography-1" == scale:
            geo = geo
            geo_c = geo_c
        elif "to-region-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Region'].tolist()[0]
            geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c,:]['Region'].tolist()[0]
        elif "to-province-1" == scale:
            geo = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo,:]['Province'].tolist()[0]
            geo_c = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c,:]['Province'].tolist()[0]

        # Main Plot/Table

        # Generating main plot df/table

        table1, plot_df = projections_2026_pop_hh(geo, True)

        # Generating main plot

        fig_pgr = make_subplots(rows=1, cols=2, subplot_titles=(f"{geo}", f"{geo_c}"), shared_yaxes=True, shared_xaxes=True)

        for s, c in zip(plot_df['Category'].unique(), m_r_colors):
            
            plot_df_frag = plot_df.loc[plot_df['Category'] == s, :]
            plot_df_frag['HH Category'] = ['1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']
            
            fig_pgr.add_trace(go.Bar(
                x = plot_df_frag['HH Category'],
                y = plot_df_frag['value'],
                name = s,
                marker_color = c,
                hovertemplate= '%{x}, ' + f'{s} - ' + '%{y}<extra></extra>'

            ),row = 1, col = 1)


        # Comparison Plot/Table

        # Generating comparison plot df/table

        table1_c, plot_df_c = projections_2026_pop_hh(geo_c, False)

        # Generating comparison plot

        for s, c in zip(plot_df_c['Category'].unique(), m_r_colors):
            
            plot_df_frag = plot_df_c.loc[plot_df_c['Category'] == s, :]
            plot_df_frag['HH Category'] = ['1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']
            
            fig_pgr.add_trace(go.Bar(
                x = plot_df_frag['HH Category'],
                y = plot_df_frag['value'],
                name = s,
                marker_color = c,
                hovertemplate= '%{x}, ' + f'{s} - ' + '%{y:.0%}<extra></extra>',
                showlegend = False
            ),row = 1, col = 2)

        # Plot layout settings

        range_ref = plot_df.groupby(['HH Category', 'Category'])['value'].sum()
        range_ref_c = plot_df_c.groupby(['HH Category', 'Category'])['value'].sum()

        fig_pgr.update_layout(
                            legend = dict(font = dict(size = 9)), 
                            modebar_color = modebar_color, 
                            modebar_activecolor = modebar_activecolor, 
                            plot_bgcolor='#F8F9F9', 
                            title = f'2026 Projected Community and Regional Household Growth Rates ', 
                            legend_title = "Population"
                            )
        fig_pgr.update_yaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9), tickformat =  ',.0%', 
                            fixedrange = True, 
                            range=[min(0,min(range_ref.min(), range_ref_c.min())), math.ceil(max(range_ref.max(), range_ref_c.max())*10)/10]
                            )
        fig_pgr.update_yaxes(title = 'Growth Rate (%)', row = 1, col = 1)
        fig_pgr.update_xaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 9),  
                            fixedrange = True, 
                            title = 'Household Size'
                            )

        # Merging main and comparison table

        table1_j = table1.merge(table1_c, how = 'left', on = 'HH Size')

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

        style_cell_conditional=[
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

        return col_list, table1_j.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional, fig_pgr
    

