from dash import html, dash_table, dcc
from plotly import express as px

from app_file import cache
from helpers.create_engine import income_partners_year, default_year
from helpers.table_helper import storage_variables

# Generate tables needed for default page
joined_df_filtered = income_partners_year[default_year].query('Geography == "Fraser Valley (CD, BC)"')
table = joined_df_filtered[['Rent 20% of AMHI', 'Rent 50% of AMHI']]
table2 = joined_df_filtered[['Rent 20% of AMHI', 'Rent 50% of AMHI']]
fig = px.line(x=['Not Available'], y=['Not Available'])
config = {'displayModeBar': True, 'displaylogo': False,
          'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale',
                                     'resetScale']}


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
                                            '''
                                            ###### Income categories are determined by their relationship with each geography’s [Area Median Household Income (AMHI)](https://hart.ubc.ca/housing-glossary/#amhi). The following table shows the range of household incomes and affordable shelter costs that make up each income category, in 2020 dollar values, as well what percentage of the total number of households that fall within each category.
                                            ''',
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
                                            '''
                                            ###### The following chart shows percentage of households in each income category that are in [Core Housing Need (CHN)](https://hart.ubc.ca/housing-glossary/#chn). When there is no bar for an income category, it means that either there are no households in Core Housing Need within an income category, or that there are [too few households to report](https://hart.ubc.ca/housing-glossary/#data-suppression). 
                                            ''',
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
                                            '###### The following chart looks at those households in [Core Housing Need](https://hart.ubc.ca/housing-glossary/#chn) and shows their relative distribution by household size (i.e. the number of rooms in a home) for each household income category. When there is no bar for an income category, it means that either there are no households in Core Housing Need within an income category, or that there are [too few households to report](https://hart.ubc.ca/housing-glossary/#data-suppression).',
                                            link_target="_blank"
                                        )
                                    ],  id='percent-IC-HH-CHN-description-pg2',
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
                                            '###### The following table shows the total number of households in [Core '
                                            'Housing Need](https://hart.ubc.ca/housing-glossary/#chn) by household '
                                            'size and income category, which may be'
                                            'considered as the existing deficit of housing options in the community.',
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
                                            '###### The following chart compares the rates of [Core Housing Need](https://hart.ubc.ca/housing-glossary/#chn) across '
                                            'populations that are at high risk of experiencing housing need. The '
                                            '"Community (all HH)" bar represents the rate of Core Housing Need for '
                                            'all households in the selected community to act as a point of reference. '
                                            'The population with the greatest rate of Core Housing Need is '
                                            'highlighted in dark blue. When there is no bar for a priority '
                                            'population, it means that either there are no households in Core Housing '
                                            'Need within that priority population, or that there are [too few '
                                            'households to report](https://hart.ubc.ca/housing-glossary/#data-suppression).',
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
                                                '###### The following chart looks at those households in Core Housing '
                                                'Need for each priority population and shows their relative '
                                                'distribution by household income category. When there is no bar for '
                                                'a priority population, it means that either there are no households '
                                                'in [Core Housing Need](https://hart.ubc.ca/housing-glossary/#chn) within that priority population, or that there '
                                                'are [too few households to report](https://hart.ubc.ca/housing-glossary/#data-suppression).',
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

                            ], className='dashboard-pg2-lgeo'
                        ),
                    ], className='background-pg2-lgeo'
                    )
