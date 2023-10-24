from dash import html, dash_table, dcc
import plotly.express as px
import pandas as pd

from helpers.create_engine import default_year
from helpers.table_helper import storage_variables

# Setting a default plot and table which renders before the dashboard is fully loaded

fig = px.line(x=['Not Available in CD/Regional level. Please select CSD/Municipal level'],
              y=['Not Available in CD/Regional level. Please select CSD/Municipal level'])

table = pd.DataFrame({'Not Available in CD/Regional level. Please select CSD/Municipal level': [0]})
# Configuration for plot icons

config = {'displayModeBar': True, 'displaylogo': False,
          'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale',
                                     'resetScale']}


def layout(year=default_year):
    return html.Div(children=
                    # Fetching Area/Comparison Area/Clicked area scale info in local storage
                    storage_variables()
                    + [

                        # Main Layout

                        html.Div(
                            children=[

                                html.Div([

                                    # 2031 Household Projections by Income Category

                                    html.Div([
                                        # Title
                                        html.H3(children=html.Strong('2031 Household Projections by Income Category'),
                                                className='subtitle-lgeo'),

                                        # Table Description
                                        html.Div([
                                            html.H6(
                                                'The following table shows the total number of households in 2021, for each household income category, as well as the projected gain (positive) or loss (negative) of households over the period between 2021 and 2031 by applying the percentage change from 2006-2021, to 2021 households.')
                                        ], className='muni-reg-text-lgeo'),

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
                                                'The following graph illustrates the above table, displaying the total number of households in 2021, for each income category, with the projected gain of households between 2021 and 2031 stacked on top, and the projected loss of household stacked underneath.')
                                        ], className='muni-reg-text-lgeo'),

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

                                        html.H3(children=html.Strong('2031 Household Projections by Household Size'),
                                                className='subtitle-lgeo'),

                                        # Table Description

                                        html.Div([
                                            html.H6(
                                                'The following table shows the total number of households in 2021, for each household size category, as well as the projected gain (positive) or loss (negative) of households over the period between 2021 and 2031 by applying the percentage change from 2006-2021, to 2021 households.')
                                        ], className='muni-reg-text-lgeo'),

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
                                                'The following graph illustrates the above table, displaying the total number of households in 2021, for each size of household, with the projected gain of households between 2021 and 2031 stacked on top, and the projected loss of household stacked underneath.')
                                        ], className='muni-reg-text-lgeo'),

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
                                            '2031 Projected Households by Household Size and Income Category'),
                                            className='subtitle-lgeo'),

                                        # Table Description

                                        html.Div([
                                            html.H6(
                                                'The following table shows the projected total number of households in 2031 by household size and income category.')
                                        ], className='muni-reg-text-lgeo'),

                                        # Table

                                        html.Div([
                                            dash_table.DataTable(
                                                id='datatable-h-interactivity',
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

                                        html.Div(id='datatable-h-interactivity-container'),

                                        # Graph Description

                                        html.Div([
                                            html.H6(
                                                'The following graph illustrates the above table, displaying the projected total number of households in 2031 by household size and income category. Each bar is broken out by the projected number of households within each income category.')
                                        ], className='muni-reg-text-lgeo'),

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
                                            children=html.Strong('2031 Projected Household Gain/Loss (2021 to 2031)'),
                                            className='table-title'),

                                        # Table Description

                                        html.Div([
                                            html.H6(
                                                'The following table shows the projected gain or loss of households by household size and income. These values represent projections for the period between 2021 and 2031.')
                                        ], className='muni-reg-text-lgeo'),

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
                                                'The following graph illustrates the above table, displaying the projected gain or loss of households between 2021 and 2031 for each size of household. Each bar is broken out by the projected number of households within each income category. Projected loss of households are stacked underneath.')
                                        ], className='muni-reg-text-lgeo'),

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

                                    # Municipal vs Regional Growth Rates

                                    html.Div([

                                        # Title
                                        html.H3(children=html.Strong('Municipal vs Regional Growth Rates'),
                                                className='subtitle-lgeo'),

                                        # Description
                                        html.H6([
                                            'Comparing a local community’s growth rates to the growth rate of the region allows for insight into if the community is matching regional patterns of change. There are numerous potential causes for discrepencies, which are further discussed in ',
                                            html.A('the project methods.',
                                                   href='https://hart.ubc.ca/wp-content/uploads/2023/06/HNA-Methodology-06-09-2023.pdf',
                                                   target="_blank")])
                                    ], className='muni-reg-text-lgeo'),

                                    # 2031 Projected Municipal vs Regional Household Growth Rates by Income Category

                                    html.Div([
                                        # Title

                                        html.H3(children=html.Strong(
                                            '2031 Projected Municipal vs Regional Household Growth Rates by Income Category'),
                                            className='subtitle-lgeo'),

                                        # Table Description

                                        html.Div([
                                            html.H6(
                                                'The following table illustrates the projected household growth rates between 2021 and 2031 in the community and surrounding region for each income category.')
                                        ], className='muni-reg-text-lgeo'),

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
                                                'The following graph illustrates the above table, displaying the projected household growth rates between 2021 and 2031 in the community and surrounding region for each income category.')
                                        ], className='muni-reg-text-lgeo'),

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
                                                'The following table illustrates the projected household growth rates between 2021 and 2031 in the community and surrounding region for each household size.')
                                        ], className='muni-reg-text-lgeo'),

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
                                                'The following graph illustrates the above table, displaying the projected household growth rates between 2021 and 2031 in the community and surrounding region for each income category.')
                                        ], className='muni-reg-text-lgeo'),

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

                                ]),

                            ], className='dashboard-pg3-lgeo'
                        ),
                    ], className='background-pg3-lgeo'
                    )
