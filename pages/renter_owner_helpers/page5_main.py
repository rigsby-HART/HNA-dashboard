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
                                        html.H6(
                                            'The following table shows the range of household incomes and affordable '
                                            'shelter costs for each income category, in 2020 dollar values, '
                                            'as well compares owner and renter households for what percentage of the '
                                            'total number of households falls within each category.')
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

                                # Income Categories and Affordable Shelter Costs Subsidized Renters vs Unsubsidized

                                html.Div([
                                    # Title
                                    html.H3(
                                        children=html.Strong(f'Income Categories and Affordable Shelter Costs for Subsidized and Unsubsidized Renters, {year}'),
                                        id='income-category-subsidized-title-page5'),
                                    # Description
                                    html.Div([
                                        html.H6(
                                            'The following table shows the range of household incomes and affordable '
                                            'shelter costs for each income category, in 2020 dollar values, '
                                            'as well compares subsidized and unsubsidized renters for what percentage '
                                            'of the total number of households falls within each category.')
                                    ], className='muni-reg-text-lgeo'),

                                    # Table

                                    html.Div([
                                        dash_table.DataTable(
                                            id='income-category-subsidized-table-pg5',
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
                                        html.H6(
                                            'Income categories are determined by their relationship with each geography’s Area Median Household Income (AMHI). This table shows the range of household incomes and affordable shelter costs for each income category, in 2020 dollar values, as well what percentage of the total number of households falls within each category.')
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
                                        html.H6(
                                            'The following chart looks at those households in Core Housing Need and shows their relative distribution by housing type for each household income category. When there is no bar for an income category, it means that either there are no households in Core Housing Need within an income category, or that there are too few households to report.')
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
                                        html.H6(
                                            'The following table shows the total number of households in Core Housing Need by household size and income category, which may be considered as the existing deficit of housing options in the community.')
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

                            ], className='dashboard-pg2-lgeo'
                        ),
                    ], className='background-pg2-lgeo'
                    )