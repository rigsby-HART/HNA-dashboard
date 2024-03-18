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
config = {
    'displayModeBar': True, 'displaylogo': False,
    'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale',
                               'resetScale'],
    "toImageButtonOptions": {
        "filename": 'custom_image'
    }
}


# TODO: Make the table actually select by year


@cache.memoize()
def layout(year: int = default_year):
    return html.Div(children=
                    # Fetching Area/Comparison Area/Clicked area scale info in local storage
                    storage_variables()
                    + [
                        # Main Layout

                        html.Div(
                            children=[

                                # Income Categories and Affordable Shelter Costs

                                html.Div([
                                    # Title
                                    html.H3(
                                        children=html.Strong(f'Income Categories and Affordable Shelter Costs, {year}'),
                                        id='income-categories-title-pg2'),
                                    # Description
                                    html.Div([
                                        dcc.Markdown(
                                            strings['income-categories-page2'],
                                            link_target="_blank"
                                        )
                                    ], className='muni-reg-text-lgeo', ),

                                    # Table

                                    html.Div([
                                        dash_table.DataTable(
                                            id='income-category-affordability-table',
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
                                    ], className='pg2-table-lgeo'

                                    ),

                                ], className='pg2-table-plot-box-lgeo'),

                                # Percentage of Households in Core Housing Need, by Income Category

                                html.Div([
                                    # Title
                                    html.H3(children=html.Strong(
                                        f'Percentage of Households in Core Housing Need, by Income Category, {year}'),
                                        id='percent-HH-CHN-title-pg2'),
                                    # Description
                                    html.Div([
                                        dcc.Markdown(
                                            strings['percentage-CHN-by-income-table-page2'],
                                            link_target="_blank"
                                        )], className='muni-reg-text-lgeo'),

                                    # Graph

                                    html.Div(children=[

                                        dcc.Graph(
                                            id='graph',
                                            figure=fig,
                                            config=config,
                                        )
                                    ],
                                        className='pg2-plot-lgeo'

                                    ),

                                ], className='pg2-table-plot-box-lgeo'),

                                # Percentage of Households in Core Housing Need, by Income Category and HH Size,

                                html.Div([
                                    # Title
                                    html.H3(children=html.Strong(
                                        f'Percentage of Households in Core Housing Need, by Income Category and HH Size, {year}'),
                                        id='percent-IC-HH-CHN-title-pg2'),
                                    # Description
                                    html.Div([
                                        dcc.Markdown(
                                            strings['percentage-CHN-by-income-graph-page2'],
                                            link_target="_blank"
                                        )
                                    ], id='percent-IC-HH-CHN-description-pg2',
                                        className='muni-reg-text-lgeo'),

                                    # Graph

                                    html.Div(children=[

                                        dcc.Graph(
                                            id='graph2',
                                            figure=fig,
                                            config=config,
                                        )
                                    ],
                                        className='pg2-plot-lgeo'
                                    ),

                                ], className='pg2-table-plot-box-lgeo'),

                                # Affordable Housing Deficit

                                html.Div([
                                    # Title
                                    html.H3(children=html.Strong(f'{year} Affordable Housing Deficit'),
                                            id='housing-deficit-pg2'),
                                    # Description
                                    html.Div([
                                        dcc.Markdown(
                                            strings["housing-deficit-page2"],
                                            link_target="_blank"
                                        )
                                    ], className='muni-reg-text-lgeo'),

                                    # Table

                                    html.Div(children=[

                                        html.Div([
                                            dash_table.DataTable(
                                                id='datatable2-interactivity',
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
                                        ], className='pg2-table-lgeo'
                                        ),
                                    ]
                                    ),  # Description
                                    html.Div([
                                        dcc.Markdown(
                                            strings["housing-deficit-bedrooms-page2"],
                                            link_target="_blank"
                                        )
                                    ], className='muni-reg-text-lgeo'),

                                    # Table

                                    html.Div(children=[

                                        html.Div([
                                            dash_table.DataTable(
                                                id='housing-deficit-bedroom-table',
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
                                            html.Div(id='housing-deficit-bedroom-table-container')
                                        ], className='pg2-table-lgeo'
                                        ),
                                    ]
                                    ),
                                ], className='pg2-table-plot-box-lgeo'),

                                # Percentage of Households in Core Housing Need by Priority Population

                                html.Div([
                                    # Title
                                    html.H3(
                                        children=html.Strong(
                                            f'Percentage of Households in Core Housing Need by Priority Population, {year}'),
                                        id='pct-pp-hh-chn-pg2'),
                                    # Description
                                    html.Div([
                                        dcc.Markdown(
                                            strings["percentage-CHN-by-priority-population-page2"],
                                            link_target="_blank"
                                        )
                                    ],
                                        id='percent-CHN-PP-description-pg2',
                                        className='muni-reg-text-lgeo'
                                    ),

                                    # Graphs

                                    html.Div(children=[

                                        dcc.Graph(
                                            id='graph5',
                                            figure=fig,
                                            config=config,
                                        )
                                    ],
                                        className='pg2-plot-lgeo'
                                    ),
                                ], className='pg2-table-plot-box-lgeo'),

                                # Percentage of Households in Core Housing Need by Priority Population and Income Category

                                html.Div([
                                    # Title
                                    html.H3(children=html.Strong(
                                        f'Percentage of Households in Core Housing Need by Priority Population and Income Category, {year}'),
                                        id='pct-pp-ic-chn-pg2'),
                                    # Description
                                    html.Div([
                                        dcc.Markdown(
                                            strings["percentage-CHN-by-pp-income-page2"],
                                            link_target="_blank"
                                        )
                                    ],
                                        id='percent-CHN-PP-IC-description-pg2',
                                        className='muni-reg-text-lgeo'
                                    ),

                                    # Graphs

                                    html.Div(children=[

                                        dcc.Graph(
                                            id='graph6',
                                            figure=fig,
                                            config=config,
                                        )

                                    ],
                                        className='pg2-plot-lgeo'
                                    ),

                                ], className='pg2-table-plot-box-lgeo'),

                                # Raw data download button

                                html.Div([
                                    html.Button("Download This Community", id="ov7-download-csv"),
                                    dcc.Download(id="ov7-download-text")
                                ],
                                    className='region-button-lgeo'
                                ),

                                # LGEO

                                html.Div([
                                    'This dashboard was created in collaboration with ',
                                    html.A('Licker Geospatial', href='https://www.lgeo.co/', target="_blank"),
                                    ' using Plotly.'
                                ], className='lgeo-credit-text'),

                                # Whitespace

                                html.Div(
                                    style={"height": "70px"},
                                )

                            ], className='dashboard-pg2-lgeo'
                        ),
                    ], className='background-pg2-lgeo'
                    )
