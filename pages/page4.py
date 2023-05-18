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

# Importing indigenous data

df_ind = pd.read_sql_table('indigenous', engine.connect())

# Importing income data

df_income = pd.read_sql_table('income', engine.connect())

# Preprocessing - Preparing main dataset and categories being used for plots

income_category = df_income.drop(['Geography'], axis=1)
income_category = income_category.rename(columns = {'Formatted Name': 'Geography'})
joined_df = income_category.merge(df_ind, how = 'left', on = 'Geography')

# Importing Geo Code Information

mapped_geo_code = pd.read_sql_table('geocodes_integrated', engine.connect())

# Configuration for plot icons

config = {'displayModeBar': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale']}

# Color Lists

colors = ['#D7F3FD', '#88D9FA', '#39C0F7', '#099DD7', '#044762']
hh_colors = ['#D8EBD4', '#93CD8A', '#3DB54A', '#297A32', '#143D19']
hh_type_color = ['#002145', '#3EB549', '#39C0F7']
columns_color_fill = ['#F3F4F5', '#EBF9FE', '#F0FAF1']
modebar_color = '#099DD7'
modebar_activecolor = '#044762'

# Font size for tables when they are displayed on the comparison mode
comparison_font_size = '0.7em'
comparison_font_size2 = '0.65em'

# Default selected area
default_value = 'Canada'

# Setting global variables can be re-used

x_base =['Very Low Income',
            'Low Income',
            'Moderate Income',
            'Median Income',
            'High Income',
            ]

x_base_echn = [
    '20% or under of area median household income (AMHI)-Households examined for core housing need',
    '21% to 50% of AMHI-Households examined for core housing need',
    '51% to 80% of AMHI-Households examined for core housing need',
    '81% to 120% of AMHI-Households examined for core housing need',
    '121% or more of AMHI-Households examined for core housing need'       
         ]

x_base_chn = [
    '20% or under of area median household income (AMHI)-Households in core housing need',
    '21% to 50% of AMHI-Households in core housing need',
    '51% to 80% of AMHI-Households in core housing need',
    '81% to 120% of AMHI-Households in core housing need',
    '121% or more of AMHI-Households in core housing need'       
         ]

x_columns = ['Rent 20% of AMHI',
             'Rent 50% of AMHI',
             'Rent 80% of AMHI',
             'Rent 120% of AMHI',
             'Rent 120% of AMHI'
            ]

amhi_range = ['20% or under of AMHI', '21% to 50% of AMHI', '51% to 80% of AMHI', '81% to 120% of AMHI', '121% and more of AMHI']

income_ct = [x + f" ({a})" for x, a in zip(x_base, amhi_range)]

# Setting a default plot and table which renders before the dashboard is fully loaded

fig = px.line(x = ['Loading'], y = ['Loading'])

table = pd.DataFrame({'Loading':[0]})


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
                    html.H6('This table shows the range of Indigenous household incomes and affordable shelter costs for each income category, in 2015 dollar values, as well what percentage of the total number of Indigenous households that fall within each category.')
                ], className = 'muni-reg-text-lgeo'),

            # Table

                html.Div([
                    dash_table.DataTable(
                        id='datatable-interactivity_ind',
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
                    html.Div(id='datatable-interactivity-container_ind')
                ], className = 'pg4-table-lgeo'

                ),

            ], className = 'pg4-table-plot-box-lgeo'),


        # Percentage of Households in Core Housing Need, by Income Category, 2016


            html.Div([
                # Title
                html.H3(children = html.Strong('Percentage of Indigenous Households in Core Housing Need, by Income Category, 2016'), id = 'visualization'),
                # Description
                html.Div([
                    html.H6('Income categories are determined by their relationship with each geography’s Area Median Household Income (AMHI). This table shows the range of Indigenous household incomes and affordable shelter costs for each income category, in 2015 dollar values, as well what percentage of the total number of Indigenous households falls within each category.')
                ], className = 'muni-reg-text-lgeo'),

            # Graph

                html.Div(children = [ 

                    dcc.Graph(
                        id='graph_ind',
                        figure=fig,
                        config = config,
                    )
                ],
                    className = 'pg4-plot-lgeo'

                ),

            ], className = 'pg4-table-plot-box-lgeo'),


        # Percentage of Households in Core Housing Need, by Income Category and HH Size, 2016

            html.Div([
                # Title
                html.H3(children = html.Strong('Percentage of Indigenous Households in Core Housing Need, by Income Category and HH Size, 2016'), id = 'visualization2'),
                # Description
                html.Div([
                    html.H6('This chart looks at those Indigenous households in Core Housing Need and shows their relative distribution by household size (i.e. the number of individuals in a given household) for each household income category. Where there are no reported households in Core Housing Need, there are too few households to report while protecting privacy.')
                ], className = 'muni-reg-text-lgeo'),


                # Graph

                html.Div(children = [ 

                    dcc.Graph(
                        id='graph2_ind',
                        figure=fig,
                        config = config,
                    )
                ],
                    className = 'pg4-plot-lgeo'
                ),

            ], className = 'pg4-table-plot-box-lgeo'),


        # 2016 Affordable Housing Deficit

            html.Div([
                # Title
                html.H3(children = html.Strong('2016 Affordable Housing Deficit for Indigenous Households'), id = 'visualization4'),
                # Description
                html.Div([
                    html.H6('This table shows the total number of Indigenous households in Core Housing Need by household size and income category, which may be considered as the existing deficit of housing options in the community. Where there are zero households to report, it means there are too few to report while protecting privacy.')
                ], className = 'muni-reg-text-lgeo'),


                # Table
                
                html.Div(children = [ 

                    html.Div([
                        dash_table.DataTable(
                            id='datatable2-interactivity_ind',
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
                            style_cell = {'font-family': 'Bahnschrift'},
                            style_header = {'text-align': 'middle', 'fontWeight': 'bold'},
                            export_format = "xlsx"
                        ),
                        html.Div(id='datatable2-interactivity-container_ind')
                    ], className = 'pg4-table-lgeo'
                    ),
                ]
                ),
            ], className = 'pg4-table-plot-box-lgeo'),


        # Raw data download button

            html.Div([
                html.Button("Download This Community", id="ov7-download-csv_ind"),
                dcc.Download(id="ov7-download-text_ind")
                ],
                className = 'region-button-lgeo'
            ),
        
        # LGEO

            html.Div([
                    'This dashboard was created in collaboration with ',  html.A('Licker Geospatial', href = 'https://www.lgeo.co/)', target="_blank"),' using Plotly.'
                ], className = 'lgeo-credit-text'),


        ], className = 'dashboard-pg4-lgeo'
    ), 
], className = 'background-pg4-lgeo'
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

def table_amhi_shelter_cost_ind(geo, IsComparison):

    joined_df_filtered = joined_df.query('Geography == '+ f'"{geo}"')

    portion_of_total_hh = []

    for x in x_base_echn:
        portion_of_total_hh.append(joined_df_filtered[f'Aboriginal household status-Total - Private households by tenure including presence of mortgage payments and subsidized housing-Households with income {x}'].tolist()[0])
    
    sum_portion_of_total_hh = sum(portion_of_total_hh)

    if sum_portion_of_total_hh > 0:
        portion_of_total_hh = [round(p * (1/sum_portion_of_total_hh * 100),2) for p in portion_of_total_hh]
    else:
        portion_of_total_hh = [0 for p in portion_of_total_hh]
    
    amhi_list = []
    for a in amhi_range:
        amhi_list.append(joined_df_filtered[a].tolist()[0])

    shelter_range = ['20% or under of AMHI.1', '21% to 50% of AMHI.1', '51% to 80% of AMHI.1', '81% to 120% of AMHI.1', '121% and more of AMHI.1']
    shelter_list = []
    for s in shelter_range:
        shelter_list.append(joined_df_filtered[s].tolist()[0])

    if IsComparison != True:
        table = pd.DataFrame({'Income Category': income_ct, '% of Total Indigenous HHs': portion_of_total_hh , 'Annual HH Income': amhi_list, 'Affordable Shelter Cost (2015 CAD$)': shelter_list})
        table['% of Total Indigenous HHs'] = table['% of Total Indigenous HHs'].astype(str) + '%'
    else:
        table = pd.DataFrame({'Income Category': income_ct, '% of Total Indigenous HHs ': portion_of_total_hh , 'Annual HH Income ': amhi_list, 'Affordable Shelter Cost ': shelter_list})
        table['% of Total Indigenous HHs '] = table['% of Total Indigenous HHs '].astype(str) + '%'

    return table



# Callback logic for the table update

@callback(
    Output('datatable-interactivity_ind', 'columns'),
    Output('datatable-interactivity_ind', 'data'),
    Output('datatable-interactivity_ind', 'style_data_conditional'),
    Output('datatable-interactivity_ind', 'style_cell_conditional'),
    Output('datatable-interactivity_ind', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('datatable-interactivity_ind', 'selected_columns'),
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
        table = table_amhi_shelter_cost_ind(geo, IsComparison = False)
    
        # Generating callback output to update table
        col_list = []

        for i in table.columns:
            col_list.append({"name": [geo + " (Indigenous HH)", i], "id": i})

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
        table = table_amhi_shelter_cost_ind(geo, IsComparison = False)
 


        # Comparison Table

        if geo_c == None:
            geo_c = geo

        # Generating comparison table
        table_c = table_amhi_shelter_cost_ind(geo_c, IsComparison = True)

        # Merging main and comparison table
        table_j = table.merge(table_c, how = 'left', on = 'Income Category')

        # Generating Callback output

        col_list = []

        for i in table.columns:
            if i == 'Income Category':
                col_list.append({"name": ["Area (Indigenous HH)", i], "id": i})
            else:
                col_list.append({"name": [geo, i], "id": i})

        for i in table_c.columns[1:]:
            col_list.append({"name": [geo_c, i], "id": i})

        style_cell_conditional=[
            {
                'if': {'column_id': c},
                'font_size': comparison_font_size2,
                'backgroundColor': columns_color_fill[1]
            } for c in table.columns[1:]
        ] + [
            {
                'if': {'column_id': c},
                'font_size': comparison_font_size2,
                'backgroundColor': columns_color_fill[2]
            } for c in table_c.columns[1:]
        ] + [
            {
                'if': {'column_id': table.columns[0]},
                'font_size': comparison_font_size2,
                'backgroundColor': columns_color_fill[0]
            }
        ]

        return col_list, table_j.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional


# Percentage of Indigenous Households in Core Housing Need, by Income Category, 2016

column_format = 'Aboriginal household status-Total - Private households by tenure including presence of mortgage payments and subsidized housing-Households with income '
echn_columns = [column_format + e for e in x_base_echn]
chn_columns = [column_format + c for c in x_base_chn]

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

    plot_df = pd.DataFrame({
            'Income_Category': x_list, 
            'ECHN': joined_df_filtered[echn_columns].T.iloc[:,0].tolist(),
            'CHN': joined_df_filtered[chn_columns].T.iloc[:,0].tolist()
        })

    plot_df['Percent HH'] = np.round(plot_df['CHN'] / plot_df['ECHN'], 2)
    plot_df = plot_df.replace([np.inf, -np.inf], 0)
    plot_df = plot_df.fillna(0)
    plot_df = plot_df.drop(columns = ['ECHN', 'CHN'])
    
    return plot_df


# Callback logic for the plot update
@callback(
    Output('graph_ind', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('area-scale-store', 'data'),
    Input('datatable-interactivity_ind', 'selected_columns'),
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
                        title = f'Percentage of Indigenous Households in Core Housing Need, by Income Category, 2016<br>{geo}', 
                        legend_title = "Income",          
                        )
        fig.update_xaxes(
                        fixedrange = True, 
                        range = [0, 1], 
                        tickformat =  ',.0%', 
                        title = '% of Indigenous HH', 
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
                        title = 'Percentage of Indigenous Households in Core Housing Need, by Income Category, 2016',
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
                        title = '% of Indigenous HH', 
                        title_font = dict(size = 10), 
                        tickfont = dict(size = 10)
                        )

        return fig
    

# Percentage of Indigenous Households in Core Housing Need, by Income Category and HH Size, 2016 (plot)
# and 2016 Affordable Housing Deficit for Indigenous Households (table)

# plot df, table generator
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
    hh_p_num_list = ['1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']
    for h, hc in zip(hh_p_num_list, hh_column_name):
        for i in income_lv_list:
            column = f'Aboriginal household status-{hc}-Households with income {i}-Households in core housing need'
            h_hold_value.append(joined_df_filtered[column].tolist()[0])
            hh_p_num_list_full.append(h)

    plot_df = pd.DataFrame({'HH_Size': hh_p_num_list_full, 'Income_Category': x_base * 5, 'Percent': h_hold_value})
    plot_df['Percent'] = np.round(plot_df['Percent'], 2)
    percent = plot_df.groupby('Income_Category')['Percent'].sum().reset_index()
    percent = percent.rename(columns = {'Percent':'Sum'})
    plot_df_final = plot_df.merge(percent, how = 'left', on = 'Income_Category')
    plot_df_final['Income_Category'] = x_list * 5
    plot_df_final['Percent'] = plot_df_final['Percent'] / plot_df_final['Sum']
    plot_df_final['Percent'] = plot_df_final['Percent'].fillna(0)
    plot_df_final = plot_df_final.drop(columns = ['Sum'])
    
    table = pd.DataFrame({'Income_Category': x_base})\
            .merge(plot_df.pivot_table(values = 'Percent', index = 'Income_Category', columns = 'HH_Size').reset_index(), \
                  how = 'left', on = 'Income_Category')

    row_total = table.sum(axis=0)
    row_total[0] = 'Total'
    table.loc[5, :] = row_total

    if IsComparison != True:
        table.columns = ['Income Category', '1 Person', '2 Person', '3 Person', '4 Person', '5+ Person']
        table['Total'] = table.sum(axis=1)

    else:
        table.columns = ['Income Category', '1 Person ', '2 Person ', '3 Person ', '4 Person ', '5+ Person ']
        table['Total '] = table.sum(axis=1)
    
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
    Input('area-scale-store', 'data'),
    Input('datatable-interactivity_ind', 'selected_columns'),
)
def update_geo_figure34(geo, geo_c, scale, refresh):

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
        plot_df, table2 = plot_df_core_housing_need_by_amhi(geo, False)

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
                        title = f'Percentage of Indigenous Households in Core Housing Need, by Income and HH Size, 2016<br>{geo}', 
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
                        title = '% of Indigenous HH', 
                        tickfont = dict(size = 10)
                        )


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
            col_list.append({"name": [geo + " (Indigenous HH)", i],
                                    "id": i, 
                                    "type": 'numeric', 
                                    "format": Format(
                                                    group=Group.yes,
                                                    scheme=Scheme.fixed,
                                                    precision=0
                                                    )})

        return fig2, col_list, table2.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional


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
        plot_df, table2 = plot_df_core_housing_need_by_amhi(geo, False)

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
        plot_df_c, table2_c = plot_df_core_housing_need_by_amhi(geo_c, True)

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
                            title = 'Percentage of Indigenous Households in Core Housing Need, by Income Category and HH Size, 2016',
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
                            title = '% of Indigenous HH', 
                            tickfont = dict(size = 10)
                            )


        # Merging main and comparison table

        table2_j = table2.merge(table2_c, how = 'left', on = 'Income Category')

        # Generating Callback output

        col_list = []

        for i in table2.columns:
            if i == 'Income Category':
                col_list.append({"name": ["Area (Indigenous HH)", i], "id": i})
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

        return fig2, col_list, table2_j.to_dict('record'), style_data_conditional, style_cell_conditional, style_header_conditional

# Download This Community

@callback(
    Output("ov7-download-text_ind", "data"),
    Input("ov7-download-csv_ind", "n_clicks"),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    prevent_initial_call=True,
)
def func_ov7(n_clicks, geo, geo_c):

    if geo == None:
        geo = default_value

    if "ov7-download-csv_ind" == ctx.triggered_id:

        joined_df_geo = joined_df.query("Geography == " + f"'{geo}'")
        joined_df_geo_c = joined_df.query("Geography == " + f"'{geo_c}'")
        joined_df_download_ind = pd.concat([joined_df_geo, joined_df_geo_c])
        joined_df_download_ind = joined_df_download_ind.drop(columns = ['pk_x', 'pk_y'])

        return dcc.send_data_frame(joined_df_download_ind.to_csv, "result.csv")