# Importing Libraries

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import math as math
import warnings
from dash import dcc, dash_table, html, Input, Output, ctx, callback
from dash.dash_table.Format import Format, Scheme, Group
from plotly.subplots import make_subplots
from sqlalchemy import create_engine

engine = create_engine('sqlite:///sources//hart.db')
warnings.filterwarnings("ignore")

# Importing income data

df_income = pd.read_sql_table('income', engine.connect())

# Importing partners data

df_partners = pd.read_sql_table('partners', engine.connect())

# Importing Geo Code Information

mapped_geo_code = pd.read_sql_table('geocodes_integrated', engine.connect())

# Configuration for plot icons

config = {'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']}

# Preprocessing - Preparing main dataset and categories being used for plots

income_category = df_income.drop(['Geography'], axis=1)
income_category = income_category.rename(columns = {'Formatted Name': 'Geography'})

joined_df = income_category.merge(df_partners, how = 'left', on = 'Geography')


x_base =['Very Low Income',
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

hh_p_num_list = [1,2,3,4,'5 or more']

amhi_range = ['20% or under of AMHI', '21% to 50% of AMHI', '51% to 80% of AMHI', '81% to 120% of AMHI', '121% and more of AMHI']

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

joined_df_filtered = joined_df.query('Geography == "Fraser Valley (CD, BC)"')

x_list = []

i = 0
for b, c in zip(x_base, x_columns):
    if i < 4:
        x = b + " ($" + str(joined_df_filtered[c].tolist()[0]) + ")"
        x_list.append(x)
    else:
        x = b + " (>$" + str(joined_df_filtered[c].tolist()[0]) + ")"
        x_list.append(x)
    i += 1

columns = ['Percent HH with income 20% or under of AMHI in core housing need',
            'Percent HH with income 21% to 50% of AMHI in core housing need',
            'Percent HH with income 51% to 80% of AMHI in core housing need',
            'Percent HH with income 81% to 120% of AMHI in core housing need',
            'Percent HH with income 121% or more of AMHI in core housing need'
            ]

plot_df = pd.DataFrame({'Income_Category': x_list, 'Percent HH': joined_df_filtered[columns].T.iloc[:,0].tolist()})

fig = px.line(x = ['Not Available'], y = ['Not Available'])

table = joined_df_filtered[['Rent 20% of AMHI', 'Rent 50% of AMHI']]
table2 = joined_df_filtered[['Rent 20% of AMHI', 'Rent 50% of AMHI']]



# Setting layout for dashboard


layout = html.Div(children = [

        # Fetching Area/Comparison Area/Clicked area scale info in local storage

        dcc.Store(id='area-scale-store', storage_type='local'),
        dcc.Store(id='main-area', storage_type='local'),
        dcc.Store(id='comparison-area', storage_type='local'),

        # Main Layout

        html.Div(
        children = [

        # Income Categories and Affordable Shelter Costs, 2016

            html.Div([
                # Title
                html.H3(children = html.Strong('Income Categories and Affordable Shelter Costs, 2016'), id = 'visualization3'),
                # Description
                html.Div([
                    html.H6('This table shows the range of household incomes and affordable shelter costs for each income category, in 2015 dollar values, as well what percentage of the total number of households falls within each category.')
                ], className = 'muni-reg-text-lgeo'),

            # Table

                html.Div([
                    dash_table.DataTable(
                        id='datatable-interactivity',
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
                        merge_duplicate_headers=True,
                        export_format = "xlsx",
                        style_cell = {'font-family': 'Bahnschrift'},
                        style_header = {'text-align': 'middle', 'fontWeight': 'bold'}
                    ),
                    html.Div(id='datatable-interactivity-container')
                ], className = 'pg2-table-lgeo'

                ),

            ], className = 'pg2-table-plot-box-lgeo'),


        # Percentage of Households in Core Housing Need, by Income Category, 2016


            html.Div([
                # Title
                html.H3(children = html.Strong('Percentage of Households in Core Housing Need, by Income Category, 2016'), id = 'visualization'),
                # Description
                html.Div([
                    html.H6('Income categories are determined by their relationship with each geography’s Area Median Household Income (AMHI). This table shows the range of household incomes and affordable shelter costs for each income category, in 2015 dollar values, as well what percentage of the total number of households falls within each category.')
                ], className = 'muni-reg-text-lgeo'),

            # Graph

                html.Div(children = [ 

                    dcc.Graph(
                        id='graph',
                        figure=fig,
                        config = config,
                    )
                ],
                    className = 'pg2-plot-lgeo'

                ),

            ], className = 'pg2-table-plot-box-lgeo'),


        # Percentage of Households in Core Housing Need, by Income Category and HH Size, 2016

            html.Div([
                # Title
                html.H3(children = html.Strong('Percentage of Households in Core Housing Need, by Income Category and HH Size, 2016'), id = 'visualization2'),
                # Description
                html.Div([
                    html.H6('This chart looks at those households in Core Housing Need and shows their relative distribution by household size (i.e. the number of individuals in a given houshold) for each household income category. When there is no bar for an income category, it means that either there are no households in Core Housing Need within an income category, or that there are too few households to report.')
                ], className = 'muni-reg-text-lgeo'),


                # Graph

                html.Div(children = [ 

                    dcc.Graph(
                        id='graph2',
                        figure=fig,
                        config = config,
                    )
                ],
                    className = 'pg2-plot-lgeo'
                ),

            ], className = 'pg2-table-plot-box-lgeo'),


        # 2016 Affordable Housing Deficit

            html.Div([
                # Title
                html.H3(children = html.Strong('2016 Affordable Housing Deficit'), id = 'visualization4'),
                # Description
                html.Div([
                    html.H6('This table shows the total number of households in Core Housing Need by household size and income category, which may be considered as the existing deficit of housing options in the community.')
                ], className = 'muni-reg-text-lgeo'),


                # Table
                
                html.Div(children = [ 

                    html.Div([
                        dash_table.DataTable(
                            id='datatable2-interactivity',
                            columns=[
                                {"name": i, "id": i, "deletable": False, "selectable": False} for i in table2.columns
                            ],
                            data=table2.to_dict('records'),
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
                            merge_duplicate_headers=True,
                            style_cell = {'font-family': 'Bahnschrift'},
                            style_header = {'text-align': 'middle', 'fontWeight': 'bold'},
                            export_format = "xlsx"
                        ),
                        html.Div(id='datatable2-interactivity-container')
                    ], className = 'pg2-table-lgeo'
                    ),
                ]
                ),
            ], className = 'pg2-table-plot-box-lgeo'),


        # Percentage of Households in Core Housing Need by Priority Population, 2016

            html.Div([
                # Title
                html.H3(children = html.Strong('Percentage of Households in Core Housing Need by Priority Population, 2016'), id = 'visualization5'),
                # Description
                html.Div([
                    html.H6('This chart compares the rates of Core Housing Need across populations that are at high risk of experiencing housing need. The "Community (all HH)" bar represents the rate of Core Housing Need for all households in the selected community to act as a point of reference. The population with the greatest rate of Core Housing Need is highlighted in dark blue. When there is no bar for a priority population, it means that either there are no households in Core Housing Need within that priority population, or that there are too few households to report.')
                ], className = 'muni-reg-text-lgeo'),

                # Graphs

                html.Div(children = [ 

                    dcc.Graph(
                        id='graph5',
                        figure=fig,
                        config = config,
                    )
                ],
                        className = 'pg2-plot-lgeo'
                ),
            ], className = 'pg2-table-plot-box-lgeo'),

        # Percentage of Households in Core Housing Need by Priority Population and Income Category, 2016

            html.Div([
                # Title
                html.H3(children = html.Strong('Percentage of Households in Core Housing Need by Priority Population and Income Category, 2016'), id = 'visualization6'),
                # Description
                html.Div([
                    html.H6('This chart looks at those households in Core Housing Need for each priority population and shows their relative distribution by household income category. When there is no bar for a priority population, it means that either there are no households in Core Housing Need within that priority population, or that there are too few households to report.')
                ], className = 'muni-reg-text-lgeo'),

                # Graphs

                html.Div(children = [ 

                    dcc.Graph(
                        id='graph6',
                        figure=fig,
                        config = config,
                    )

                ],
                        className = 'pg2-plot-lgeo'
                ),

            ], className = 'pg2-table-plot-box-lgeo'),


        # Raw data download button

            html.Div([
                html.Button("Download This Community", id="ov7-download-csv"),
                dcc.Download(id="ov7-download-text")
                ],
                className = 'region-button-lgeo'
            ),
        
        # LGEO

            html.Div([
                    'This dashboard was created in collaboration with ',  html.A('Licker Geospatial', href = 'https://www.lgeo.co/)', target="_blank"),' using Plotly.'
                ], className = 'lgeo-credit-text'),


        ], className = 'dashboard-pg2-lgeo'
    ), 
], className = 'background-pg2-lgeo'
)


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


# Plot/table generators and callbacks

# Income Categories and Affordable Shelter Costs, 2016

# Table generator
def table_amhi_shelter_cost(geo, IsComparison):

    joined_df_filtered = joined_df.query('Geography == '+ f'"{geo}"')

    portion_of_total_hh = []
    for x in x_base:
        portion_of_total_hh.append(round(joined_df_filtered[f'Percent of Total HH that are in {x}'].tolist()[0] * 100, 2))

    amhi_list = []
    for a in amhi_range:
        amhi_list.append(joined_df_filtered[a].tolist()[0])

    shelter_range = ['20% or under of AMHI.1', '21% to 50% of AMHI.1', '51% to 80% of AMHI.1', '81% to 120% of AMHI.1', '121% and more of AMHI.1']
    shelter_list = []
    for s in shelter_range:
        shelter_list.append(joined_df_filtered[s].tolist()[0])

    if IsComparison != True:
        table = pd.DataFrame({'Income Category': income_ct, '% of Total HHs': portion_of_total_hh , 'Annual HH Income': amhi_list, 'Affordable Shelter Cost (2015 CAD$)': shelter_list})
        table['% of Total HHs'] = table['% of Total HHs'].astype(str) + '%'
    else:
        table = pd.DataFrame({'Income Category': income_ct, '% of Total HHs ': portion_of_total_hh , 'Annual HH Income ': amhi_list, 'Affordable Shelter Cost ': shelter_list})
        table['% of Total HHs '] = table['% of Total HHs '].astype(str) + '%'

    return table


# Callback logic for the table update

@callback(
    Output('datatable-interactivity', 'columns'),
    Output('datatable-interactivity', 'data'),
    Output('datatable-interactivity', 'style_data_conditional'),
    Output('datatable-interactivity', 'style_cell_conditional'),
    Output('datatable-interactivity', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('datatable-interactivity', 'selected_columns'),
    Input('area-scale-store', 'data'),
)
def update_table1(geo, geo_c, selected_columns, scale):

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
        else:
            geo = geo

        # Generating table
        table = table_amhi_shelter_cost(geo, IsComparison = False)
    
        # Generating callback output to update table
        col_list = []

        for i in table.columns:
            col_list.append({"name": [geo, i], "id": i})

        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'backgroundColor': columns_color_fill[1]
            } for c in table.columns[1:]
        ] + [
            {
                'if': {'column_id': table.columns[0]},
                'backgroundColor': columns_color_fill[0]
            }
        ]

        return col_list, table.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional

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

        # Main Table

        # Generating main table
        table = table_amhi_shelter_cost(geo, IsComparison = False)
 


        # Comparison Table

        if geo_c == None:
            geo_c = geo

        # Generating comparison table
        table_c = table_amhi_shelter_cost(geo_c, IsComparison = True)

        # Merging main and comparison table
        table_j = table.merge(table_c, how = 'left', on = 'Income Category')

        # Generating Callback output

        col_list = []

        for i in table.columns:
            if i == 'Income Category':
                col_list.append({"name": ["Area", i], "id": i})
            else:
                col_list.append({"name": [geo, i], "id": i})

        for i in table_c.columns[1:]:
            col_list.append({"name": [geo_c, i], "id": i})

        style_cell_conditional=[
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
        ]

        return col_list, table_j.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional




# Percentage of Households in Core Housing Need, by Income Category, 2016


# Plot dataframe generator
def plot_df_core_housing_need_by_income(geo, IsComparison):

    joined_df_filtered = joined_df.query('Geography == '+ f'"{geo}"')

    x_list = []

    i = 0
    for b, c in zip(x_base, x_columns):
        value = joined_df_filtered[c].tolist()[0]
        if i < 4:
            if IsComparison != True:
                x = b + '<br>' + " ($" + f'{value:,}' + ")"
            else:
                x = " ($" + f'{value:,}' + ") "
            x_list.append(x)
        else:
            if IsComparison != True:
                x = b + '<br>' + " (>$" + f'{value:,}' + ")"
            else:
                x = " (>$" + f'{value:,}' + ") "
            x_list.append(x)
        i += 1

    plot_df = pd.DataFrame({'Income_Category': x_list, 'Percent HH': joined_df_filtered[columns].T.iloc[:,0].tolist()})

    return plot_df

# Callback logic for the plot update
@callback(
    Output('graph', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('datatable-interactivity', 'selected_columns'),
)
def update_geo_figure(geo, geo_c, scale, refresh):

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

        # Generating dataframe for plot
        plot_df = plot_df_core_housing_need_by_income(geo, IsComparison = False)

        # Generating plot
        fig = go.Figure()
        for i, c in zip(plot_df['Income_Category'], colors):
            plot_df_frag = plot_df.loc[plot_df['Income_Category'] == i, :]
            fig.add_trace(go.Bar(
                                y = plot_df_frag['Income_Category'],
                                x = plot_df_frag['Percent HH'],
                                name = i,
                                marker_color = c,
                                orientation = 'h', 
                                hovertemplate= '%{y} - ' + '%{x: .2%}<extra></extra>'
                        ))

        # Plot layout settings
        fig.update_layout(
                        width = 900,
                        showlegend = False, 
                        legend=dict(font = dict(size = 9)), 
                        yaxis=dict(autorange="reversed"), 
                        modebar_color = modebar_color, 
                        modebar_activecolor = modebar_activecolor, 
                        plot_bgcolor='#F8F9F9', 
                        title = f'Percentage of Households in Core Housing Need, by Income Category, 2016<br>{geo}', 
                        legend_title = "Income",          
                        )
        fig.update_xaxes(
                        fixedrange = True, 
                        range = [0, 1], 
                        tickformat =  ',.0%', 
                        title = '% of HH', 
                        tickfont = dict(size = 10)
                        )      
        fig.update_yaxes(
            tickfont = dict(size = 10), 
            fixedrange = True, 
            title = 'Income Categories<br>(Max. affordable shelter costs)'
                        )

        return fig

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

        # Subplot setting for the comparison mode
        fig = make_subplots(rows=1, cols=2, subplot_titles=(f"{geo}", f"{geo_c}"), shared_xaxes=True)

        # Main Plot

        # Generating dataframe for main plot
        plot_df = plot_df_core_housing_need_by_income(geo, IsComparison = False)

        # Generating main plot
        n = 0
        for i, c, b in zip(plot_df['Income_Category'], colors, x_base):
            plot_df_frag = plot_df.loc[plot_df['Income_Category'] == i, :]
            fig.add_trace(go.Bar(
                y = plot_df_frag['Income_Category'],
                x = plot_df_frag['Percent HH'],
                name = b.replace(" Income", ""),
                marker_color = c,
                orientation = 'h', 
                hovertemplate= '%{y} - ' + '%{x: .2%}<extra></extra>',
                legendgroup = f'{n}'
            ), row = 1, col = 1)
            n += 1

        fig.update_yaxes(title = 'Income Categories<br>(Max. affordable shelter costs)', row = 1, col = 1)

        # Comparison plot

        # Generating dataframe for comparison plot
        plot_df_c = plot_df_core_housing_need_by_income(geo_c, IsComparison = True)

        # Generating comparison plot
        n = 0
        for i, c, b in zip(plot_df_c['Income_Category'], colors, x_base):
            plot_df_frag_c = plot_df_c.loc[plot_df_c['Income_Category'] == i, :]
            fig.add_trace(go.Bar(
                                y = plot_df_frag_c['Income_Category'],
                                x = plot_df_frag_c['Percent HH'],
                                name = b.replace(" Income", ""),
                                marker_color = c,
                                orientation = 'h', 
                                hovertemplate= '%{y} - ' + '%{x: .2%}<extra></extra>',
                                legendgroup = f'{n}',
                                showlegend = False,
                                ), row = 1, col = 2)
            n += 1

        # Plot layout settings
        fig.update_layout(
                        title = 'Percentage of Households in Core Housing Need, by Income Category, 2016',
                        showlegend = False, 
                        width = 900,
                        legend=dict(font = dict(size = 8)), 
                        modebar_color = modebar_color, 
                        modebar_activecolor = modebar_activecolor, 
                        plot_bgcolor='#F8F9F9', 
                        legend_title = "Income"
                        )
        fig.update_yaxes(
                        fixedrange = True, 
                        autorange = "reversed", 
                        title_font = dict(size = 10), 
                        tickfont = dict(size = 10)
                        )
        fig.update_xaxes(
                        fixedrange = True, 
                        range = [0, 1], 
                        tickformat =  ',.0%', 
                        title = '% of HH', 
                        title_font = dict(size = 10), 
                        tickfont = dict(size = 10)
                        )

        return fig



# Percentage of Households in Core Housing Need, by Income Category and HH Size, 2016

# Plot dataframe generator
def plot_df_core_housing_need_by_amhi(geo, IsComparison):
    
    joined_df_filtered = joined_df.query('Geography == '+ f'"{geo}"')

    x_list = []

    i = 0
    for b, c in zip(x_base, x_columns):
        value = joined_df_filtered[c].tolist()[0]
        if i < 4:
            if IsComparison != True:
                x = b + '<br>' + " ($" + f'{value:,}' + ")"
            else:
                x = " ($" + f'{value:,}' + ") "
            x_list.append(x)
        else:
            if IsComparison != True:
                x = b + '<br>' + " (>$" + f'{value:,}' + ")"
            else:
                x = " (>$" + f'{value:,}' + ") "
            x_list.append(x)
        i += 1

    income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']

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
    Input('area-scale-store', 'data'),
    Input('datatable-interactivity', 'selected_columns'),
)
def update_geo_figure2(geo, geo_c, scale, refresh):

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

        # Generating dataframe for plot
        plot_df = plot_df_core_housing_need_by_amhi(geo, False)

        # Generating plot
        fig2 = go.Figure()

        for h, c in zip(plot_df['HH_Size'].unique(), hh_colors):
            plot_df_frag = plot_df.loc[plot_df['HH_Size'] == h, :]
            fig2.add_trace(go.Bar(
                                y = plot_df_frag['Income_Category'],
                                x = plot_df_frag['Percent'],
                                name = h,
                                marker_color = c,
                                orientation = 'h', 
                                hovertemplate= '%{y}, ' + f'HH Size: {h} - ' + '%{x: .2%}<extra></extra>',
                            ))

        # Plot layout settings    
        fig2.update_layout(
                        legend_traceorder = 'normal', 
                        width = 900,
                        legend=dict(font = dict(size = 9)), 
                        modebar_color = modebar_color, 
                        modebar_activecolor = modebar_activecolor, 
                        yaxis=dict(autorange="reversed"), 
                        barmode='stack', 
                        plot_bgcolor='#F8F9F9', 
                        title = f'Percentage of Households in Core Housing Need, by Income Category and HH Size, 2016<br>{geo}', 
                        legend_title = "Household Size"
                        )
        fig2.update_yaxes(
                        tickfont = dict(size = 10), 
                        fixedrange = True, 
                        title = 'Income Categories<br>(Max. affordable shelter costs)'
                        )
        fig2.update_xaxes(
                        fixedrange = True, 
                        tickformat =  ',.0%', 
                        title = '% of HH', 
                        tickfont = dict(size = 10)
                        )

        return fig2


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

        # Subplot setting for the comparison mode
        fig2 = make_subplots(rows=1, cols=2, subplot_titles=(f"{geo}", f"{geo_c}"), shared_xaxes=True)

        # Main Plot

        # Generating dataframe for main plot
        plot_df = plot_df_core_housing_need_by_amhi(geo, False)

        # Generating main plot
        n = 0
        for h, c in zip(plot_df['HH_Size'].unique(), hh_colors):
            plot_df_frag = plot_df.loc[plot_df['HH_Size'] == h, :]
            fig2.add_trace(go.Bar(
                y = plot_df_frag['Income_Category'],
                x = plot_df_frag['Percent'],
                name = h,
                marker_color = c,
                orientation = 'h', 
                hovertemplate= '%{y}, ' + f'HH Size: {h} - ' + '%{x: .2%}<extra></extra>',
                legendgroup = f'{n}'
            ), row = 1, col = 1)
            n += 1
        
        fig2.update_yaxes(title = 'Income Categories<br>(Max. affordable shelter costs)', row = 1, col = 1)


        # Comparison plot

        # Generating dataframe for comparison plot
        plot_df_c = plot_df_core_housing_need_by_amhi(geo_c, True)

        # Generating comparison plot
        n = 0
        for h, c in zip(plot_df_c['HH_Size'].unique(), hh_colors):
            plot_df_frag_c = plot_df_c.loc[plot_df_c['HH_Size'] == h, :]
            fig2.add_trace(go.Bar(
                                    y = plot_df_frag_c['Income_Category'],
                                    x = plot_df_frag_c['Percent'],
                                    name = h,
                                    marker_color = c,
                                    orientation = 'h', 
                                    hovertemplate= '%{y}, ' + f'HH Size: {h} - ' + '%{x: .2%}<extra></extra>',
                                    legendgroup = f'{n}',
                                    showlegend = False,
                                ), row = 1, col = 2)
            n += 1

        # Plot layout settings
        fig2.update_layout(
                            font = dict(size = 10), 
                            title = 'Percentage of Households in Core Housing Need, by Income Category and HH Size, 2016',
                            legend_traceorder = 'normal', 
                            modebar_color = modebar_color,
                            modebar_activecolor = modebar_activecolor, 
                            barmode='stack', 
                            plot_bgcolor='#F8F9F9', 
                            legend_title = "Household Size", 
                            legend = dict(font = dict(size = 8))
                            )
        fig2.update_yaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 10), 
                            fixedrange = True, 
                            autorange = "reversed"
                            )
        fig2.update_xaxes(
                            title_font = dict(size = 10), 
                            fixedrange = True, 
                            tickformat =  ',.0%', 
                            title = '% of HH', 
                            tickfont = dict(size = 10)
                            )

        return fig2



# 2016 Affordable Housing Deficit

# Table generator
def table_core_affordable_housing_deficit(geo, IsComparison):

    joined_df_filtered = joined_df.query('Geography == '+ f'"{geo}"')

    table2 = pd.DataFrame({'Income Category': income_ct})

    h_hold_value = []
    hh_p_num_list = [1,2,3,4,'5 or more']
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
                column = f'Total - Private households by presence of at least one or of the combined activity limitations (Q11a, Q11b, Q11c or Q11f or combined)-{h2}-Households with income {i} of area median household income (AMHI)-Households in core housing need'
                h_hold_value.append(joined_df_filtered[column].tolist()[0])

            else:
                column = f'Total - Private households by presence of at least one or of the combined activity limitations (Q11a, Q11b, Q11c or Q11f or combined)-{h2}-Households with income {i} of AMHI-Households in core housing need'
                h_hold_value.append(joined_df_filtered[column].tolist()[0])
                
        if IsComparison != True:
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

    table2['Income Category'] = [
                                'Very low Income',
                                'Low Income',
                                'Moderate Income',
                                'Median Income',
                                'High Income'
                                ]
    
    table2['Total'] = table2.sum(axis = 1)
    row_total_csd = table2.sum(axis=0)
    row_total_csd[0] = 'Total'
    table2.loc[len(table2['Income Category']), :] = row_total_csd
    
    if IsComparison == True:
        table2 = table2.rename(columns = {'Total': 'Total '})

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
    Input('datatable2-interactivity', 'selected_columns'),
    Input('area-scale-store', 'data'),
)
def update_table2(geo, geo_c, selected_columns, scale):

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

        # Generating table
        table2 = table_core_affordable_housing_deficit(geo, False)
        table2 = table2[['Income Category', '1 Person HH', '2 Person HH',
                        '3 Person HH', '4 Person HH', '5+ Person HH', 'Total']]

        # Generating callback output to update table
        col_list = []

        style_cell_conditional=[
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

        return col_list, table2.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional


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

        # Main Table

        # Generating main table

        table2 = table_core_affordable_housing_deficit(geo, False)
        table2 = table2[['Income Category', '1 Person HH', '2 Person HH',
                        '3 Person HH', '4 Person HH', '5+ Person HH', 'Total']]


        # Comparison Table

        if geo == None:
            geo = default_value

        # Generating comparison table

        table2_c = table_core_affordable_housing_deficit(geo_c, True)
        table2_c = table2_c[['Income Category', '1 Person HH ', '2 Person HH ',
                        '3 Person HH ', '4 Person HH ', '5+ Person HH ', 'Total ']]

        # Merging main and comparison table

        table2_j = table2.merge(table2_c, how = 'left', on = 'Income Category')

        # Generating Callback output

        col_list = []

        for i in table2.columns:
            if i == 'Income Category':
                col_list.append({"name": ["Area", i], "id": i})
            else:
                col_list.append({"name": [geo, i], 
                                    "id": i, 
                                    "type": 'numeric', 
                                    "format": Format(
                                                    group=Group.yes,
                                                    scheme=Scheme.fixed,
                                                    precision=0
                                                    )})

        for i in table2_c.columns[1:]:
            if i == 'Income Category':
                col_list.append({"name": ["Income Category", i], "id": i})
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
            } for c in table2.columns[1:]
        ] + [
            {
                'if': {'column_id': c},
                'font_size': comparison_font_size,
                'minWidth': '70px',
                'backgroundColor': columns_color_fill[2]
            } for c in table2_c.columns[1:]
        ] + [
            {
                'if': {'column_id': table2.columns[0]},
                'font_size': comparison_font_size,
                'backgroundColor': columns_color_fill[0]
            }
        ]

        return col_list, table2_j.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional



# Percentage of Households in Core Housing Need by Priority Population, 2016

# Preparing global variables for the table

hh_category_dict = {
            'Percent Single Mother led HH in core housing need' : 'Single mother-led HH', 
            'Percent Women-led HH in core housing need' : 'Women-led HH', 
            'Percent Indigenous HH in core housing need' : 'Indigenous HH', 
            'Percent Visible minority HH in core housing need' : 'Visible minority HH', 
            'Percent Black-led HH in core housing need' : 'Black-led HH', 
            'Percent New migrant-led HH in core housing need' : 'New migrant-led HH', 
            'Percent Refugee claimant-led HH in core housing need' : 'Refugee claimant-led HH', 
            'Percent HH head under 25 in core housing need' : 'HH head under 25', 
            'Percent HH head over 65 in core housing need' : 'HH head over 65', 
            'Percent HH head over 85 in core housing need' : 'HH head over 85', 
            'Percent HH with physical act. limit. in core housing need' : 'HH with physical activity limitation', 
            'Percent HH with cognitive, mental, or addictions activity limitation in core housing need' : 'HH with cognitive, mental,<br>or addictions activity limitation', 
            'Percent HH in core housing need' : 'Community (all HH)'
        }

hh_columns = hh_category_dict.keys()
hh_categories = list(hh_category_dict.values())

# Plot dataframe generator

def plot_df_core_housing_need_by_priority_population(geo):

    joined_df_filtered = joined_df.query('Geography == '+ f'"{geo}"')

    percent_hh = [joined_df_filtered[c].tolist()[0] for c in hh_columns]

    plot_df = pd.DataFrame({'HH_Category': hh_categories, 'Percent_HH': percent_hh})
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
    Input('area-scale-store', 'data'),
    Input('datatable-interactivity', 'selected_columns'),
)
def update_geo_figure5(geo, geo_c, scale, refresh):

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

        # Generating dataframe for plot and color lists

        plot_df = plot_df_core_housing_need_by_priority_population(geo)
        color_dict = color_dict_core_housing_need_by_priority_population(plot_df)

        # Generating plot

        fig5 = go.Figure()
        for i in hh_categories:
            plot_df_frag = plot_df.loc[plot_df['HH_Category'] == i, :]
            fig5.add_trace(go.Bar(
                                y = plot_df_frag['HH_Category'],
                                x = plot_df_frag['Percent_HH'],
                                name = i,
                                marker_color = color_dict[i],
                                orientation = 'h', 
                                hovertemplate= '%{y} - ' + '%{x: .2%}<extra></extra>',                
                                ))
            
        # Plot layout settings
        fig5.update_layout(
                            yaxis=dict(autorange="reversed"), 
                            width = 900,
                            modebar_color = modebar_color, 
                            modebar_activecolor = modebar_activecolor, 
                            showlegend = False, 
                            plot_bgcolor='#F8F9F9', 
                            title = f'Percentage of Households in Core Housing Need by Priority Population, 2016<br>{geo}', 
                            legend_title = "HH Category"
                            )
        fig5.update_xaxes(
                            title_font = dict(size = 10), 
                            fixedrange = True, 
                            tickformat =  ',.0%', 
                            range=[0, math.ceil(plot_df['Percent_HH'].max()*10)/10], 
                            title = '% of Priority Population HH'
                            )
        fig5.update_yaxes(
                            fixedrange = True, 
                            tickfont = dict(size = 8)
                            )

        return fig5

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

        # Subplot setting for the comparison mode 
        fig5 = make_subplots(rows=1, cols=2, subplot_titles=(f"{geo}", f"{geo_c}"), shared_yaxes=True, shared_xaxes=True)

        # Main Plot

        # Generating dataframe for main plot and color list

        plot_df = plot_df_core_housing_need_by_priority_population(geo)
        color_dict = color_dict_core_housing_need_by_priority_population(plot_df)

        # Generating main plot

        for i in hh_categories:
            plot_df_frag = plot_df.loc[plot_df['HH_Category'] == i, :]
            fig5.add_trace(go.Bar(
                                y = plot_df_frag['HH_Category'],
                                x = plot_df_frag['Percent_HH'],
                                name = i,
                                marker_color = color_dict[i],
                                orientation = 'h', 
                                hovertemplate= '%{y} - ' + '%{x: .2%}<extra></extra>',
                                ),row = 1, col = 1)

        # Comparison Plot

        # Generating dataframe for comparison plot and color list

        plot_df_c = plot_df_core_housing_need_by_priority_population(geo_c)
        color_dict = color_dict_core_housing_need_by_priority_population(plot_df_c)

        # Generating comparison plot

        for i in hh_categories:
            plot_df_frag_c = plot_df_c.loc[plot_df_c['HH_Category'] == i, :]
            fig5.add_trace(go.Bar(
                                y = plot_df_frag_c['HH_Category'],
                                x = plot_df_frag_c['Percent_HH'],
                                name = i,
                                marker_color = color_dict[i],
                                orientation = 'h', 
                                hovertemplate= '%{y} - ' + '%{x: .2%}<extra></extra>',
                                ),row = 1, col = 2)

        # Plot layout settings

        fig5.update_layout(
                            title = 'Percentage of Households in Core Housing Need by Priority Population, 2016',
                            width = 900,
                            legend = dict(font = dict(size = 8)),
                            yaxis=dict(autorange="reversed"), 
                            modebar_color = modebar_color, 
                            modebar_activecolor = modebar_activecolor, 
                            showlegend = False, 
                            plot_bgcolor='#F8F9F9', 
                            legend_title = "HH Category"
                            )
        fig5.update_xaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 8), 
                            tickformat =  ',.0%', 
                            fixedrange = True, 
                            range=[0, math.ceil(max(plot_df['Percent_HH'].max(), plot_df_c['Percent_HH'].max())*10)/10], 
                            title = '% of Priority Population HH'
                            )
        fig5.update_yaxes(
                            fixedrange = True, 
                            tickfont = dict(size = 8)
                            )

        return fig5



# Percentage of Households in Core Housing Need by Priority Population and Income Category, 2016

# Preparing global variables for the table

hh_category_dict2 = {
                    'Percent of Single Mother led HH in core housing need' : 'Single mother-led HH', 
                    'Percent of Women-led HH in core housing need' : 'Women-led HH', 
                    'Percent of Indigenous HH in core housing need' : 'Indigenous HH', 
                    'Percent of Visible minority HH in core housing need' : 'Visible minority HH', 
                    'Percent of Black-led HH in core housing need' : 'Black-led HH', 
                    'Percent of New migrant-led HH in core housing need' : 'New migrant-led HH', 
                    'Percent of Refugee claimant-led HH in core housing need' : 'Refugee claimant-led HH', 
                    'Percent of HH head under 25 in core housing need' : 'HH head under 25', 
                    'Percent of HH head over 65 in core housing need' : 'HH head over 65', 
                    'Percent of HH head over 85 in core housing need' : 'HH head over 85', 
                    'Percent of HH with physical act. limit. in core housing need' : 'HH with physical activity limitation', 
                    'Percent of HH with with cognitive, mental, or addictions activity limitation in core housing need' : 'HH with cognitive, mental,<br>or addictions activity limitation',
                    }

hh_category_dict3 = {
                    'Percent of Single Mother led HH core housing' : 'Single mother-led HH', 
                    'Percent of Women-led HH core housing' : 'Women-led HH', 
                    'Percent of Indigenous HH in core housing' : 'Indigenous HH', 
                    'Percent of Visible minority HH core housing' : 'Visible minority HH', 
                    'Percent of Black-led HH core housing' : 'Black-led HH', 
                    'Percent of New migrant-led HH core housing' : 'New migrant-led HH', 
                    'Percent of Refugee claimant-led HH core housing' : 'Refugee claimant-led HH', 
                    'Percent of HH head under 25 core housing' : 'HH head under 25', 
                    'Percent of HH head over 65 core housing' : 'HH head over 65', 
                    'Percent of HH head over 85 core housing' : 'HH head over 85', 
                    'Percent of HH with physical act. limit. in core housing' : 'HH with physical activity limitation', 
                    'Percent of HH with cognitive, mental, or addictions activity limitation in core housing' : 'HH with cognitive, mental,<br>or addictions activity limitation', 
                    }

hh_category_dict4 = {
                    'Percent of Single Mother led HH in core housing' : 'Single mother-led HH', 
                    'Percent of Women-led HH in core housing' : 'Women-led HH', 
                    'Percent of Indigenous HH in core housing' : 'Indigenous HH', 
                    'Percent of Visible minority HH in core housing' : 'Visible minority HH', 
                    'Percent of Black-led HH in core housing' : 'Black-led HH', 
                    'Percent of New migrant-led HH in core housing' : 'New migrant-led HH', 
                    'Percent of Refugee claimant-led HH in core housing' : 'Refugee claimant-led HH', 
                    'Percent of HH head under 25 in core housing' : 'HH head under 25', 
                    'Percent of HH head over 65 in core housing' : 'HH head over 65', 
                    'Percent of HH head over 85 in core housing' : 'HH head over 85', 
                    'Percent of HH with physical act. limit. in core housing' : 'HH with physical activity limitation', 
                    'Percent of HH with cognitive, mental, or addictions activity limitation in core housing' : 'HH with cognitive, mental,<br>or addictions activity limitation',
                    }

columns2 = hh_category_dict2.keys()
columns3 = hh_category_dict3.keys()
columns4 = hh_category_dict4.keys()

income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']

# Plot dataframe generator

def plot_df_core_housing_need_by_priority_population_income(geo):
    
    joined_df_filtered = joined_df.query('Geography == '+ f'"{geo}"')

    income_col = []
    percent_col = []
    hh_cat_col = []

    for c, c2, c3 in zip(columns2, columns3, columns4):
        for i in income_lv_list:
            if i == '20% or under':
                p_hh = joined_df_filtered[f'{c} with income {i} of the AMHI'].tolist()[0]
                hh_cat_col.append(hh_category_dict2[c])
            elif i == '21% to 50%':
                p_hh = joined_df_filtered[f'{c2} with income {i} of AMHI'].tolist()[0]
                hh_cat_col.append(hh_category_dict3[c2])
            else:
                p_hh = joined_df_filtered[f'{c3} with income {i} of AMHI'].tolist()[0]
                hh_cat_col.append(hh_category_dict4[c3])

            income_col.append(i)
            percent_col.append(p_hh)

    plot_df = pd.DataFrame({'Income_Category': income_col, 'HH_Category': hh_cat_col, 'Percent': percent_col})
    
    return plot_df

# Callback logic for the plot update

@callback(
    Output('graph6', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('datatable-interactivity', 'selected_columns'),
)
def update_geo_figure6(geo, geo_c, scale, refresh):

    # Overried income category values
    income_category_override = ['Very Low', 'Low', 'Moderate', 'Median', 'High']

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

        # Generating dataframe for plot
        plot_df = plot_df_core_housing_need_by_priority_population_income(geo)

        # Generating plot
        fig6 = go.Figure()

        for i, c, o in zip(plot_df['Income_Category'].unique(), colors, income_category_override):
            plot_df_frag = plot_df.loc[plot_df['Income_Category'] == i, :]
            fig6.add_trace(go.Bar(
                                    y = plot_df_frag['HH_Category'],
                                    x = plot_df_frag['Percent'],
                                    name = o,
                                    marker_color = c,
                                    orientation = 'h', 
                                    hovertemplate= '%{y}, ' + f'{o} Income - ' + '%{x: .2%}<extra></extra>',
                                ))
            
        # Plot layout settings
        fig6.update_layout(
                            width = 900,
                            legend_traceorder="normal", 
                            font = dict(size = 10), 
                            legend = dict(font = dict(size = 9)), 
                            modebar_color = modebar_color, 
                            modebar_activecolor = modebar_activecolor, 
                            yaxis=dict(autorange="reversed"), 
                            barmode='stack', 
                            plot_bgcolor='#F8F9F9', 
                            title = f'Percentage of Households in Core Housing Need by Priority Population and Income Category, 2016<br>{geo}', 
                            legend_title = "Income Category"
                            )
        fig6.update_xaxes(
                            title_font = dict(size = 10), 
                            fixedrange = True, 
                            tickformat =  ',.0%', 
                            title = '% of HH'
                            )
        fig6.update_yaxes(
                            fixedrange = True, 
                            tickfont = dict(size = 8)
                            )

        return fig6

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

        # Subplot setting for the comparison mode
        fig6 = make_subplots(rows=1, cols=2, subplot_titles=(f"{geo}", f"{geo_c}"), shared_yaxes=True, shared_xaxes=True)

        # Main Plot

        # Generating dataframe for main plot
        plot_df = plot_df_core_housing_need_by_priority_population_income(geo)

        # Generating main plot

        n = 0
        for i, c, o in zip(plot_df['Income_Category'].unique(), colors, income_category_override):
            plot_df_frag = plot_df.loc[plot_df['Income_Category'] == i, :]
            fig6.add_trace(go.Bar(
                                    y = plot_df_frag['HH_Category'],
                                    x = plot_df_frag['Percent'],
                                    name = o,
                                    marker_color = c,
                                    orientation = 'h', 
                                    hovertemplate= '%{y}, ' + f'{o} Income - ' + '%{x: .2%}<extra></extra>',
                                    legendgroup= f'{n}'
                                ), row = 1, col = 1)
            n += 1
            
        # Comparison plot

        # Generating dataframe for comparison plot
        plot_df_c = plot_df_core_housing_need_by_priority_population_income(geo_c)

        # Generating comparison plot

        n = 0
        for i, c, o in zip(plot_df['Income_Category'].unique(), colors, income_category_override):
            plot_df_frag_c = plot_df_c.loc[plot_df_c['Income_Category'] == i, :]
            fig6.add_trace(go.Bar(
                                    y = plot_df_frag_c['HH_Category'],
                                    x = plot_df_frag_c['Percent'],
                                    name = o,
                                    marker_color = c,
                                    orientation = 'h', 
                                    hovertemplate= '%{y}, ' + f'{o} Income - ' + '%{x: .2%}<extra></extra>',
                                    legendgroup = f'{n}',
                                    showlegend = False
                                ), row = 1, col = 2)
            n += 1
        
        # Plot layout settings

        fig6.update_layout(
                            title = 'Percentage of Households in Core Housing Need by Priority Population and Income Category, 2016',
                            width = 900,
                            font = dict(size = 10), 
                            legend = dict(font = dict(size = 8)), 
                            legend_traceorder="normal", 
                            modebar_color = modebar_color, 
                            modebar_activecolor = modebar_activecolor, 
                            yaxis=dict(autorange="reversed"), 
                            barmode='stack', 
                            plot_bgcolor='#F8F9F9', 
                            legend_title = "Income Category"
                            )
        fig6.update_xaxes(
                            title_font = dict(size = 10), 
                            tickfont = dict(size = 8), 
                            fixedrange = True, 
                            tickformat =  ',.0%', 
                            title = '% of HH'
                            )
        fig6.update_yaxes(
                            fixedrange = True, 
                            tickfont = dict(size = 8)
                            )

        return fig6



# Creating raw csv data file when user clicks Download Raw Data button

@callback(
    Output("ov7-download-text", "data"),
    Input("ov7-download-csv", "n_clicks"),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    prevent_initial_call=True,
)
def func_ov7(n_clicks, geo, geo_c):

    if geo == None:
        geo = default_value

    if "ov7-download-csv" == ctx.triggered_id:

        joined_df_geo = joined_df.query("Geography == " + f"'{geo}'")
        joined_df_geo_c = joined_df.query("Geography == " + f"'{geo_c}'")
        joined_df_download = pd.concat([joined_df_geo, joined_df_geo_c])
        joined_df_download = joined_df_download.drop(columns = ['pk_x', 'pk_y'])

        return dcc.send_data_frame(joined_df_download.to_csv, "result.csv")