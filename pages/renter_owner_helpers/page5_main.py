from dash import html, dash_table, dcc
from plotly import express as px

from app_file import cache
from helpers.create_engine import partner_table, default_year
from helpers.paragraph_files import strings
from helpers.table_helper import storage_variables

# Generate tables needed for default page
joined_df_filtered = partner_table[default_year].query('Geography == "Fraser Valley (CD, BC)"')
table = joined_df_filtered[['Rent 20% of AMHI', 'Rent 50% of AMHI']]
table2 = joined_df_filtered[['Rent 20% of AMHI', 'Rent 50% of AMHI']]
fig = px.line(x=['Not Available'], y=['Not Available'])
config = {'displayModeBar': True, 'displaylogo': False,
          'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale',
                                     'resetScale']}


@cache.memoize()
def layout(year: int = default_year):
    return html.Div(children=
                    # Fetching Area/Comparison Area/Clicked area scale info in local storage
                    storage_variables()
                    + [
                        # Main Layout

                        html.Div(
                            children=[

                                # Income Categories and Affordable Shelter Costs Renters vs Owners

                                html.Div([
                                    # Title
                                    html.H3(
                                        children=html.Strong(f'Income Categories and Affordable Shelter Costs, {year}'),
                                        id='income-categories-title-page5'),
                                    # Description
                                    html.Div([
                                        dcc.Markdown(
                                            strings["income-categories-page5"] ,
                                            link_target="_blank"
                                        )
                                    ], className='muni-reg-text-lgeo'),

                                    # Table

                                    html.Div([
                                        dash_table.DataTable(
                                            id='income-category-affordability-table-pg5',
                                            columns=[
                                                {"name": i, 'id': i, "deletable": False, "selectable": False} for i in
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
                                            # style_table={
                                            #               'padding':'20px',
                                            #
                                            #               },
                                            style_data={'whiteSpace': 'normal', 'overflow': 'hidden',
                                                        'textOverflow': 'ellipsis'},
                                            style_cell={'font-family': 'Bahnschrift',
                                                        'height': 'auto',
                                                        'whiteSpace': 'normal',
                                                        'overflow': 'hidden',
                                                        'textOverflow': 'ellipsis'
                                                        },
                                            style_header={'textAlign': 'right', 'fontWeight': 'bold'}
                                        ),
                                        html.Div(id='income-category-affordability-table-container')
                                    ], className='pg5-table-lgeo'

                                    ),

                                ], className='pg5-table-plot-box-lgeo'),

                                # Percentage of Households in Core Housing Need, by Income Category

                                html.Div([
                                    # Title
                                    html.H3(children=html.Strong(
                                        f'Percentage of Households in Core Housing Need, by Income Category, {year}'),
                                        id='percent-HH-CHN-title-page5'),
                                    # Description
                                    html.Div([
                                        dcc.Markdown(
                                            strings["percentage-CHN-by-income-graph-page5"],
                                            link_target="_blank"
                                        )
                                    ], className='muni-reg-text-lgeo'),

                                    # Graph

                                    html.Div(children=[

                                        dcc.Graph(
                                            id='graph-pg5',
                                            figure=fig,
                                            config=config,
                                        )
                                    ],
                                        className='pg5-plot-lgeo'

                                    ),

                                ], className='pg5-table-plot-box-lgeo'),

                                # Percentage of Households in Core Housing Need, by Income Category and HH Size,

                                html.Div([
                                    # Title
                                    html.H3(children=html.Strong(
                                        f'Percentage of Households in Core Housing Need, by Income Category and Housing Type, {year}'),
                                        id='percent-IC-HH-CHN-title-page5'),
                                    # Description
                                    html.Div([
                                        dcc.Markdown(
                                            strings["percentage-CHN-by-IC-HH-size-page5"] ,
                                            link_target="_blank"
                                        )
                                    ], className='muni-reg-text-lgeo'),

                                    # Graph

                                    html.Div(children=[

                                        dcc.Graph(
                                            id='graph2-pg5',
                                            figure=fig,
                                            config=config,
                                        )
                                    ],
                                        className='pg5-plot-lgeo'
                                    ),

                                ], className='pg5-table-plot-box-lgeo'),

                                # Affordable Housing Deficit

                                html.Div([
                                    # Title
                                    html.H3(children=html.Strong(f'{year} Affordable Housing Deficit'),
                                            id='housing-deficit-page5'),
                                    # Description
                                    html.Div([
                                        dcc.Markdown(
                                            strings["housing-deficit-page5"],
                                            link_target="_blank"
                                        )
                                    ], className='muni-reg-text-lgeo'),

                                    # Table

                                    html.Div(children=[

                                        html.Div([
                                            dash_table.DataTable(
                                                id='datatable2-interactivity-pg5',
                                                columns=[
                                                    {"name": i, "id": i, "deletable": False, "selectable": False} for i
                                                    in
                                                    table2.columns
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
                                                page_current=0,
                                                page_size=25,
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
                                            html.Div(id='datatable2-interactivity-container')
                                        ], className='pg5-table-lgeo'
                                        ),
                                    ]
                                    ),
                                ], className='pg5-table-plot-box-lgeo'),

                                # Raw data download button

                                html.Div([
                                        html.Button("Download This Community", id="ov7-download-csv-pg5"),
                                        dcc.Download(id="ov7-download-text-pg5")
                                    ],
                                    className='region-button-lgeo'
                                ),

                                # Hee hee it's only me jack this time

                                # Whitespace

                                html.Div(
                                    style={"height": "70px"},
                                )

                            ], className='dashboard-pg2-lgeo'
                        ),
                    ], className='background-pg5-lgeo'
                    )
