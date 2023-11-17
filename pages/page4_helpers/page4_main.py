from dash import html, dash_table, dcc
import plotly.express as px
import pandas as pd

from helpers.table_helper import storage_variables

# Setting a default plot and table which renders before the dashboard is fully loaded

fig = px.line(x=['Loading'], y=['Loading'])

# Configuration for plot icons

config = {'displayModeBar': True, 'displaylogo': False,
          'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale',
                                     'resetScale']}

table = pd.DataFrame({'Loading': [0]})


def layout(year):
    return html.Div(children=
                    # Fetching Area/Comparison Area/Clicked area scale info in local storage
                    storage_variables()
                    + [

                        html.Div(
                            children=[

                                # Income Categories and Affordable Shelter Costs, 2021

                                html.Div([
                                    # Title
                                    html.H3(
                                        children=html.Strong(f'Income Categories and Affordable Shelter Costs, {year}'),
                                        id='Income-Category-Indigenous-Title-page4'),
                                    # Description
                                    html.Div([
                                        html.H6(
                                            'The following table shows the range of Indigenous household incomes and '
                                            'affordable shelter costs for each income category, in 2020 dollar '
                                            'values, as well what percentage of the total number of Indigenous '
                                            'households that fall within each category. Income categories are '
                                            'determined by their relationship with each geography’s Area Median '
                                            'Household Income (AMHI). Please note that this tool only measures urban '
                                            'and non-reserve Indigenous households. On-reserve households are not '
                                            'measured in the census.'),

                                    ], className='muni-reg-text-lgeo', id='Income-Category-Indigenous-Description-page4'),

                                    # Table

                                    html.Div([
                                        dash_table.DataTable(
                                            id='datatable-interactivity_ind',
                                            columns=[
                                                {"name": i, "id": i, "deletable": False, "selectable": False} for i in
                                                table.columns
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
                                            page_current=0,
                                            page_size=10,
                                            merge_duplicate_headers=True,
                                            export_format="xlsx",
                                            style_cell={'font-family': 'Bahnschrift',
                                                        'height': 'auto',
                                                        'whiteSpace': 'normal',
                                                        'overflow': 'hidden',
                                                        'textOverflow': 'ellipsis'},
                                            style_header={'textAlign': 'right', 'fontWeight': 'bold'},
                                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                                        'textOverflow': 'ellipsis'}
                                        ),
                                        html.Div(id='datatable-interactivity-container_ind')
                                    ], className='pg4-table-lgeo'

                                    ),

                                ], className='pg4-table-plot-box-lgeo'),

                                # Percentage of Households in Core Housing Need, by Income Category, 2021

                                html.Div([
                                    # Title
                                    html.H3(children=html.Strong(
                                        f'Percentage of Indigenous Households in Core Housing Need, by Income Category, {year}'),
                                        id='CHN-IC-page4'),

                                    # Description
                                    html.Div([
                                        html.H6(
                                            'The below chart shows percentage of Indigenous households in each income '
                                            'category that are in core housing need. When there is no bar for an '
                                            'income category, it means that either there are no Indigenous households '
                                            'in Core Housing Need within an income category, or that there are too '
                                            'few to report.')
                                    ], className='muni-reg-text-lgeo', id='CHN-IC-description-page4'),

                                    # Graph

                                    html.Div(children=[

                                        dcc.Graph(
                                            id='graph_ind',
                                            figure=fig,
                                            config=config,
                                        )
                                    ],
                                        className='pg4-plot-lgeo'

                                    ),

                                ], className='pg4-table-plot-box-lgeo'),

                                # Percentage of Households in Core Housing Need, by Income Category and HH Size, 2021

                                html.Div([
                                    # Title
                                    html.H3(children=html.Strong(
                                        f'Percentage of Indigenous Households in Core Housing Need, by Income Category and HH Size, {year}'),
                                        id='CHN-IC-HH-page4'),

                                    # Description
                                    html.Div([
                                        html.H6(
                                            'The following graph looks at those Indigenous households in Core Housing '
                                            'Need and shows their relative distribution by household size (i.e. the '
                                            'number of individuals in a given household) for each household income '
                                            'category. Where there are no reported households in Core Housing Need, '
                                            'there are too few households to report while protecting privacy.')
                                    ], className='muni-reg-text-lgeo', id='CHN-IC-HH-description-page4'),

                                    # Graph

                                    html.Div(children=[

                                        dcc.Graph(
                                            id='graph2_ind',
                                            figure=fig,
                                            config=config,
                                        )
                                    ],
                                        className='pg4-plot-lgeo'
                                    ),

                                ], className='pg4-table-plot-box-lgeo'),

                                # 2021 Affordable Housing Deficit

                                html.Div([
                                    # Title
                                    html.H3(
                                        children=html.Strong(
                                            f'{year} Affordable Housing Deficit for Indigenous Households'),
                                        id='Deficit-page4'),
                                    # Description
                                    html.Div([
                                        html.H6(
                                            'The following table shows the total number of Indigenous households in '
                                            'Core Housing Need by household size and income category, which may be '
                                            'considered as the existing deficit of housing options in the community. '
                                            'Where there are zero households to report, it means there are too few to '
                                            'report while protecting privacy.')
                                    ], className='muni-reg-text-lgeo', id='Deficit-description-page4'),

                                    # Table

                                    html.Div(children=[

                                        html.Div([
                                            dash_table.DataTable(
                                                id='datatable2-interactivity_ind',
                                                columns=[
                                                    {"name": i, "id": i, "deletable": False, "selectable": False} for i
                                                    in
                                                    table.columns
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
                                                page_current=0,
                                                page_size=10,
                                                merge_duplicate_headers=True,
                                                style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                                            'textOverflow': 'ellipsis'},
                                                style_cell={'font-family': 'Bahnschrift',
                                                            'height': 'auto',
                                                            'whiteSpace': 'normal',
                                                            'overflow': 'hidden',
                                                            'textOverflow': 'ellipsis'},
                                                style_header={'text-align': 'middle', 'fontWeight': 'bold'},
                                                export_format="xlsx"
                                            ),
                                            html.Div(id='datatable2-interactivity-container_ind')
                                        ], className='pg4-table-lgeo'
                                        ),
                                    ]
                                    ),
                                ], className='pg4-table-plot-box-lgeo'),

                                # Raw data download button

                                html.Div([
                                    html.Button("Download This Community", id="ov7-download-csv_ind"),
                                    dcc.Download(id="ov7-download-text_ind")
                                ],
                                    className='region-button-lgeo'
                                ),

                                # LGEO

                                html.Div([
                                    'This dashboard was created in collaboration with ',
                                    html.A('Licker Geospatial', href='https://www.lgeo.co/', target="_blank"),
                                    ' using Plotly.'
                                ], className='lgeo-credit-text'),

                            ], className='dashboard-pg4-lgeo'
                        ),
                    ], className='background-pg4-lgeo'
                    )
