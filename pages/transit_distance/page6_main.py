from dash import html, dash_table, dcc
from plotly import express as px

from app_file import cache
from helpers.create_engine import partner_table, default_year, mapped_geo_code, transit_distance
from helpers.paragraph_files import strings
from helpers.table_helper import storage_variables
from pages.transit_distance.population import get_quintile_info

# Generate tables needed for default page
geo = 5915
table = get_quintile_info(geo)
fig = px.line(x=['Not Available'], y=['Not Available'])
config = {'displayModeBar': True, 'displaylogo': False,
          'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale',
                                     'resetScale']}


@cache.memoize()
def layout(year: int = default_year):
    return html.Div(
        children=
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
                            children=html.Strong(f'Public Transit Distance'),
                            id='title-page6'),
                        # Description
                        html.Div([
                            dcc.Markdown(
                                strings["table-description-page6"],
                                link_target="_blank"
                            )
                        ], className='muni-reg-text-lgeo'),
                        # Transportation Distance
                        html.Div([
                            # dcc.Input(
                            #     type='text',
                            #     value='0.1',
                            #     debounce=0.5,
                            #     id="transportation-min-page6",
                            # ),
                            # Table

                            html.Div([
                                dash_table.DataTable(
                                    id='datatable-transit-page6',
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
                            ]),
                        ]),
                        # Whitespace

                        html.Div(
                            style={"height": "70px"},
                        ),
                        # Raw data download button

                        html.Div([
                            html.Button("Download This Community", id="ov7-download-csv-pg6"),
                            dcc.Download(id="ov7-download-text-pg6")
                        ],
                            className='region-button-lgeo'
                        ),
                        html.P(id='placeholder-pg6'),

                        # Hee hee it's only me jack this time

                        # Whitespace

                        html.Div(
                            style={"height": "70px"},
                        )

                    ],
                        className='dashboard-pg2-lgeo'
                    ),
                ], className='background-pg5-lgeo'
            )
        ]
    )
