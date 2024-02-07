from dash import html, dash_table, dcc
import plotly.express as px
import pandas as pd

from app_file import cache
from helpers.create_engine import default_year
from helpers.table_helper import storage_variables
import dash_bootstrap_components as dbc

# Setting a default plot and table which renders before the dashboard is fully loaded

fig = px.line(x=['Not Available in CD/Regional level. Please select CSD/Municipal level'],
              y=['Not Available in CD/Regional level. Please select CSD/Municipal level'])

table = pd.DataFrame({'Not Available in CD/Regional level. Please select CSD/Municipal level': [0]})
# Configuration for plot icons

config = {'displayModeBar': True, 'displaylogo': False,
          'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale',
                                     'resetScale']}


@cache.memoize()
def layout(year=default_year):
    prediction_year = year + 10
    year_minus_15 = year - 15
    return html.Div(children=
                    # Fetching Area/Comparison Area/Clicked area scale info in local storage
                    storage_variables()
                    + [

                        # Main Layout

                        html.Div(
                            children=[
                                # Warning popup
                                dbc.Modal(
                                    [
                                        dbc.ModalHeader(children=[
                                            dcc.Markdown(
                                                "### Projection Disclaimer"
                                            )
                                        ]),
                                        dbc.ModalBody(children=[
                                            dcc.Markdown(
                                                "###### Projections are done assuming \"Business as Usual\", and thus do not take account for any policy changes that could affect populations.  Predictions are made using the [HNA methodology](https://hart.ubc.ca/hna-methodology/)",
                                                link_target="_blank",
                                            )
                                        ]),
                                    ],
                                    id="projection-modal",
                                    is_open=True,
                                    size="lg"
                                ),

                                html.Div([

                                    # 2031 Household Projections by Income Category

                                    html.Div([
                                        # Title
                                        html.H3(children=html.Strong(
                                            f'{prediction_year} Household Projections by Income Category'),
                                            className='subtitle-lgeo',
                                            id="HH-IC-page3"),

                                        # Table Description
                                        html.Div([
                                            html.H6(
                                                'The following table shows the total number of households in 2021, '
                                                'for each household income category, as well as the projected gain ('
                                                'positive) or loss (negative) of households over the period between '
                                                '2021 and 2031 by using a line of best fit from 2006-2021, '
                                                'projecting forward to estimate the number of 2031 households. Please '
                                                'note this is not a projection of housing need, but a projection of '
                                                'total households in each category.')
                                        ], className='muni-reg-text-lgeo',
                                            id="HH-IC-description-page3"
                                        ),

                                        # Table

                                        html.Div(children=[

                                            dash_table.DataTable(
                                                id='datatable5-interactivity',
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
                                                style_cell={'font-family': 'Bahnschrift'},
                                                merge_duplicate_headers=True,
                                                export_format="xlsx",
                                                style_header={'text-align': 'middle', 'fontWeight': 'bold'}
                                            ),
                                        ], className='pg3-table-lgeo'
                                        ),

                                        html.Div(id='datatable5-interactivity-container'),

                                        # Graph Description
                                        html.Div([
                                            html.H6(
                                                'The following graph illustrates the above table, displaying the '
                                                'total number of households in 2021, for each income category, '
                                                'with the projected gain of households between 2021 and 2031 stacked '
                                                'on top, and the projected loss of households stacked underneath.')
                                            ],
                                            className='muni-reg-text-lgeo',
                                            id="HH-IC-graph-description-page3"
                                        ),

                                        # Graph

                                        html.Div(children=[

                                            dcc.Graph(
                                                id='graph9',
                                                figure=fig,
                                                config=config,
                                            ),

                                        ], className='pg3-plot-lgeo'
                                        ),

                                    ], className='pg3-table-plot-box-lgeo'),

                                    # 2031 Household Projections by Household Size

                                    html.Div([
                                        # Title

                                        html.H3(children=html.Strong(
                                            f'{prediction_year} Household Projections by Household Size'),
                                            className='subtitle-lgeo',
                                            id="HH-size-page3"),

                                        # Table Description

                                        html.Div([
                                            html.H6(
                                                'The following table shows the total number of households in 2021, '
                                                'for each household size category, as well as the projected gain ('
                                                'positive) or loss (negative) of households over the period between '
                                                '2021 and 2031 by using a line of best fit from 2006-2021, '
                                                'projecting forward to estimate the number of 2031 households')
                                            ],
                                            id="HH-size-description-page3",
                                            className='muni-reg-text-lgeo'),

                                        # Table

                                        html.Div([
                                            dash_table.DataTable(
                                                id='datatable6-interactivity',
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
                                                style_cell={'font-family': 'Bahnschrift'},
                                                merge_duplicate_headers=True,
                                                export_format="xlsx",
                                                style_header={'text-align': 'middle', 'fontWeight': 'bold'}
                                            ),
                                        ], className='pg3-table-lgeo'
                                        ),

                                        html.Div(id='datatable6-interactivity-container'),

                                        # Graph Description

                                        html.Div([
                                            html.H6(
                                                'The following graph illustrates the above table, displaying the '
                                                'total number of households in 2021, for each size of household, '
                                                'with the projected gain of households between 2021 and 2031 stacked '
                                                'on top, and the projected loss of households stacked underneath.')
                                            ],
                                            id="HH-size-graph-description-page3",
                                            className='muni-reg-text-lgeo'),

                                        # Graph

                                        html.Div(children=[
                                            dcc.Graph(
                                                id='graph10',
                                                figure=fig,
                                                config=config,
                                            ),
                                        ], className='pg3-plot-lgeo'
                                        ),
                                    ], className='pg3-table-plot-box-lgeo'),

                                    # 2031 Projected Households by Household Size and Income Category

                                    html.Div([
                                        # Title

                                        html.H3(children=html.Strong(
                                            f'{prediction_year} Projected Households by Household Size and Income Category'),
                                            className='subtitle-lgeo',
                                            id="HH-size-IC-page3"),

                                        # Table Description

                                        html.Div([
                                            html.H6(
                                                'The following table shows the projected total number of households '
                                                'in 2031 by household size and income category.')
                                        ],
                                            id="HH-size-IC-description-page3",
                                            className='muni-reg-text-lgeo'),

                                        # Table

                                        html.Div([
                                            dash_table.DataTable(
                                                id='projected-hh-by-hh-size-income',
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
                                                style_cell={'font-family': 'Bahnschrift'},
                                                merge_duplicate_headers=True,
                                                export_format="xlsx",
                                                style_header={'text-align': 'middle', 'fontWeight': 'bold'}
                                            ),
                                        ], className='pg3-table-lgeo'
                                        ),

                                        html.Div(id='projected-hh-by-hh-size-income-container'),

                                        # Graph Description

                                        html.Div([
                                            html.H6(
                                                'The following graph illustrates the above table, displaying the '
                                                'projected total number of households in 2031 by household size and '
                                                'income category. Each bar is broken out by the projected total '
                                                'number of households within each income category.'
                                            )
                                        ],
                                            id="HH-size-IC-graph-description-page3",
                                            className='muni-reg-text-lgeo'
                                        ),

                                        # Graph

                                        html.Div(children=[

                                            dcc.Graph(
                                                id='graph-h',
                                                figure=fig,
                                                config=config,
                                            )

                                        ], className='pg3-plot-lgeo'
                                        ),
                                    ], className='pg3-table-plot-box-lgeo'),

                                    # 2031 Projected Household Gain/Loss (2021 to 2031)

                                    html.Div([

                                        # Title

                                        html.H3(
                                            children=html.Strong(
                                                f'{prediction_year} Projected Household Gain/Loss ({year} to {prediction_year})'),
                                            id="HH-gain-page3",
                                            className='table-title'),

                                        # Table Description

                                        html.Div([
                                            html.H6(
                                                'The following table shows the projected gain or loss of households '
                                                'by household size and income. These values represent projections of '
                                                'total households for the period between 2021 and 2031.')
                                            ],
                                            id="HH-gain-description-page3",
                                            className='muni-reg-text-lgeo'
                                        ),

                                        # Table

                                        html.Div([
                                            dash_table.DataTable(
                                                id='datatable7-interactivity',
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
                                                style_cell={'font-family': 'Bahnschrift'},
                                                merge_duplicate_headers=True,
                                                export_format="xlsx",
                                                style_header={'text-align': 'middle', 'fontWeight': 'bold'}
                                            ),
                                        ], className='pg3-table-lgeo'
                                        ),

                                        html.Div(id='datatable7-interactivity-container'),

                                        # Graph Description

                                        html.Div([
                                            html.H6(
                                                'The following graph illustrates the above table, displaying the '
                                                'projected gain or loss of households between 2021 and 2031 for each '
                                                'size of household. Each bar is broken out by the projected number of '
                                                'households within each income category. Projected loss of households '
                                                'are stacked underneath.')
                                            ],
                                            id="HH-gain-graph-description-page3",
                                            className='muni-reg-text-lgeo'),

                                        # Graph

                                        html.Div(children=[

                                            dcc.Graph(
                                                id='graph11',
                                                figure=fig,
                                                config=config,
                                            )
                                        ], className='pg3-plot-lgeo'
                                        ),
                                    ], className='pg3-table-plot-box-lgeo'),

                                    # 2031 Bedroom Projections by Income Category

                                    html.Div([
                                        # Title
                                        html.H3(children=html.Strong(
                                            f'{prediction_year} Projected Households by Bedroom Count and Income Category'),
                                            className='subtitle-lgeo',
                                            id="bedroom-title-page3"),

                                        # Table Description
                                        html.Div([
                                            html.H6(
                                                f'The following table shows the projected total number of households in'
                                                f' {prediction_year} by bedroom count and income category.')
                                        ], className='muni-reg-text-lgeo',
                                            id="bedroom-description-page3"
                                        ),

                                        # Table

                                        html.Div(children=[

                                            dash_table.DataTable(
                                                id='bedroom-projection-table',
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
                                                style_cell={'font-family': 'Bahnschrift'},
                                                merge_duplicate_headers=True,
                                                export_format="xlsx",
                                                style_header={'text-align': 'middle', 'fontWeight': 'bold'}
                                            ),
                                        ], className='pg3-table-lgeo'
                                        ),

                                        # Graph Description

                                        html.Div([
                                            html.H6(
                                                f'The following graph illustrates the above table, displaying the '
                                                f'projected total number of households in {prediction_year} by '
                                                f'household size and bedroom count. Each bar is broken out by the '
                                                f'projected number of households within each income category.'
                                            )
                                        ],
                                            id="HH-gain-graph-description-page3",
                                            className='muni-reg-text-lgeo'),

                                        # Graph

                                        html.Div(children=[

                                            dcc.Graph(
                                                id='bedroom-projection-graph',
                                                figure=fig,
                                                config=config,
                                            )
                                        ]),

                                    ], className='pg3-table-plot-box-lgeo'),
                                    # 2031 Bedroom Projections Delta by Income Category

                                    html.Div([
                                        # Title
                                        html.H3(children=html.Strong(
                                            f'{prediction_year} Projected Household Gain/Loss'),
                                            className='subtitle-lgeo',
                                            id="bedroom-delta-title-page3"),

                                        # Table Description
                                        html.Div([
                                            html.H6(
                                                f'The following table shows the projected gain or loss of households '
                                                f'by bedroom count and income. These values represent projections '
                                                f'for the period between {year} and {prediction_year}.')
                                        ], className='muni-reg-text-lgeo',
                                            id="bedroom-delta-description-page3"
                                        ),

                                        # Table

                                        html.Div(children=[

                                            dash_table.DataTable(
                                                id='bedroom-projection-delta-table',
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
                                                style_cell={'font-family': 'Bahnschrift'},
                                                merge_duplicate_headers=True,
                                                export_format="xlsx",
                                                style_header={'text-align': 'middle', 'fontWeight': 'bold'}
                                            ),
                                        ], className='pg3-table-lgeo'
                                        ),

                                        # Graph Description

                                        html.Div([
                                            html.H6(
                                                f'The following graph illustrates the above table, displaying the '
                                                f'projected gain or loss of households between {year} and '
                                                f'{prediction_year} for each size of household. Each bar is broken '
                                                f'out by the projected number of households within each income '
                                                f'category. Projected loss of households are stacked underneath.')
                                        ],
                                            id="HH-gain-graph-description-page3",
                                            className='muni-reg-text-lgeo'),

                                        # Graph

                                        html.Div(children=[

                                            dcc.Graph(
                                                id='bedroom-projection-delta-graph',
                                                figure=fig,
                                                config=config,
                                            )
                                        ], className='pg3-plot-lgeo'
                                        ),

                                    ], className='pg3-table-plot-box-lgeo'),
                                    # Municipal vs Regional Growth Rates

                                    html.Div([

                                        # Title
                                        html.H3(children=html.Strong('Municipal vs Regional Growth Rates'),
                                                className='subtitle-lgeo'),

                                        # Description
                                        html.H6([
                                            'Comparing a local community’s growth rates to the growth rate of the '
                                            'region allows for insight into if the community is matching regional '
                                            'patterns of change. There are numerous potential causes for '
                                            'discrepancies, which are further discussed in ',
                                            html.A('the project methods.',
                                                   href='https://hart.ubc.ca/hna-methodology/',
                                                   target="_blank")])
                                    ], className='muni-reg-text-lgeo'),

                                    # 2031 Projected Municipal vs Regional Household Growth Rates by Income Category

                                    html.Div([
                                        # Title

                                        html.H3(children=html.Strong(
                                            f'{prediction_year} Projected Municipal vs Regional Household Growth Rates by Income Category'),
                                            id="growth-IC-page3",
                                            className='subtitle-lgeo'),

                                        # Table Description

                                        html.Div([
                                            html.H6(
                                                'The following table illustrates the projected total household growth '
                                                'rates between 2021 and 2031 in the community and surrounding region '
                                                'for each income category.')
                                            ],
                                            id="growth-IC-description-page3",
                                            className='muni-reg-text-lgeo'),

                                        # Table

                                        html.Div([

                                            dash_table.DataTable(
                                                id='datatable8-interactivity',
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
                                                style_cell={'font-family': 'Bahnschrift'},
                                                merge_duplicate_headers=True,
                                                export_format="xlsx",
                                                style_header={'text-align': 'middle', 'fontWeight': 'bold'}
                                            ),
                                        ], className='pg3-table-lgeo'
                                        ),

                                        html.Div(id='datatable8-interactivity-container'),

                                        # Graph Description

                                        html.Div([
                                            html.H6(
                                                'The following graph illustrates the above table, displaying the '
                                                'projected household growth rates between 2021 and 2031 in the '
                                                'community and surrounding region for each income category')
                                            ],
                                            id="growth-IC-description2-page3",
                                            className='muni-reg-text-lgeo'),

                                        # Graph

                                        html.Div(children=[
                                            dcc.Graph(
                                                id='graph12',
                                                figure=fig,
                                                config=config,
                                            )
                                        ],
                                            className='pg3-plot-lgeo'
                                        ),

                                    ], className='pg3-table-plot-box-lgeo'),

                                    # Municipal vs Regional Growth Rates by Household Size

                                    html.Div([
                                        # Title

                                        html.H3(
                                            children=html.Strong(
                                                'Municipal vs Regional Growth Rates by Household Size'),
                                            className='subtitle-lgeo'),

                                        # Table Description

                                        html.Div([
                                            html.H6(
                                                f'The following table illustrates the projected household growth '
                                                f'rates between {year} and {prediction_year} in the community and '
                                                f'surrounding region for each household size.')
                                        ],
                                            id="growth-IC-description3-page3",
                                            className='muni-reg-text-lgeo'
                                        ),

                                        # Table

                                        html.Div([
                                            dash_table.DataTable(
                                                id='datatable9-interactivity',
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
                                                style_cell={'font-family': 'Bahnschrift'},
                                                merge_duplicate_headers=True,
                                                export_format="xlsx",
                                                style_header={'text-align': 'middle', 'fontWeight': 'bold'}
                                            ),

                                        ], className='pg3-table-lgeo'
                                        ),

                                        html.Div(id='datatable9-interactivity-container'),

                                        # Graph Description

                                        html.Div([
                                            html.H6(
                                                f'The following graph illustrates the above table, displaying the '
                                                f'projected household growth rates between {year} and '
                                                f'{prediction_year} in the community and surrounding region for each '
                                                f'income category.')
                                        ],
                                            id="growth-IC-description4-page3",
                                            className='muni-reg-text-lgeo'),

                                        # Graph

                                        html.Div(children=[

                                            dcc.Graph(
                                                id='graph13',
                                                figure=fig,
                                                config=config,
                                            )
                                        ],
                                            className='pg3-plot-lgeo'
                                        ),
                                    ], className='pg3-table-plot-box-lgeo'),

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

                                ]),

                            ], className='dashboard-pg3-lgeo'
                        ),
                    ], className='background-pg3-lgeo'
                    )
