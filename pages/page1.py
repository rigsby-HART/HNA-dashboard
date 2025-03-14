# Importing Libraries

import dash
import pandas as pd
import numpy as np
import warnings
import json
import geopandas as gpd
import plotly.graph_objects as go
from dash import dcc, html, Input, Output, ctx, callback, State, clientside_callback

from app_file import cache
# Importing Geo Code Information
from helpers.create_engine import engine_current, mapped_geo_code, df_province_list, df_region_list
from helpers.table_helper import storage_variables

warnings.filterwarnings("ignore")

gdf_p_code_added = gpd.read_file('./sources/mapdata_simplified/province.shp')
gdf_p_code_added = gdf_p_code_added.set_index('Geo_Code')

# Importing subregions which don't have data

not_avail = pd.read_sql_table('not_available_csd', engine_current.connect())
not_avail['CSDUID'] = not_avail['CSDUID'].astype(str)

# Configuration for plot icons

config = {'displayModeBar': True, 'displaylogo': False,
          'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'autoScale', 'resetScale', 'resetViewMapbox']}

# Colors for map

map_colors_province = ['#1a3758', '#78cb80', '#74d3f9', '#a480bb', '#80c2c0', '#7480dd', '#ffe6d6', '#e98098',
                       '#b6657c', '#490076', '#008481', '#622637']
map_colors_wo_black = ['#7480dd', '#1a3758', '#7480dd', '#b6657c', '#622637', '#80c2c0', '#78cb80', '#ffe6d6',
                       '#e98098', '#a480bb', '#490076', '#008481', '#74d3f9']
map_colors_w_black = ['#000000', '#1a3758', '#7480dd', '#b6657c', '#622637', '#80c2c0', '#78cb80', '#ffe6d6', '#e98098',
                      '#a480bb', '#490076', '#008481', '#74d3f9']

# Map color opacity

opacity_value = 0.2

# Default location in the map

default_value = 'Canada'

# Plot icon colors

modebar_color = '#099DD7'
modebar_activecolor = '#044762'

# Setting orders of areas in dropdown

order = mapped_geo_code.copy()
order['Geo_Code'] = order['Geo_Code'].astype(str)
order = order.sort_values(by=['Province_Code', 'Region_Code', 'Geo_Code'])

# Setting a default map which renders before the dashboard is fully loaded

gdf_p_code_added["rand"] = np.random.randint(1, 100, len(gdf_p_code_added))

fig_m = go.Figure()

fig_m.add_trace(go.Choroplethmapbox(geojson=json.loads(gdf_p_code_added.geometry.to_json()),
                                    locations=gdf_p_code_added.index,
                                    z=gdf_p_code_added.rand,
                                    showscale=False,
                                    hovertext=gdf_p_code_added.NAME,
                                    marker=dict(opacity=opacity_value),
                                    marker_line_width=.5))

fig_m.update_layout(mapbox_style="carto-positron",
                    mapbox_center={"lat": gdf_p_code_added.geometry.centroid.y.mean() + 10,
                                   "lon": gdf_p_code_added.geometry.centroid.x.mean()},
                    height=500,
                    width=1000,
                    mapbox_zoom=1.4,
                    autosize=True)

# Setting layout for dashboard

dash.register_page(__name__)

layout = html.Div(children=
                  # Fetching Area/Comparison Area/Clicked area scale info in local storage
                  storage_variables()
                  + [

                      # Main Layout

                      html.Div(
                          children=[

                              # Select Area Dropdowns
                              html.Div(
                                  children=[

                                      # Main Area Dropdown
                                      html.Div(
                                          id='primary-geo-dropdown-parent',
                                          children=[
                                              html.Strong('Select Census Geography'),
                                              dcc.Dropdown(order['Geography'].unique(), default_value,
                                                           id='primary-geo-dropdown'),
                                          ],
                                          className='dropdown-lgeo'
                                      ),

                                      # Comparison Area Dropdown
                                      html.Div(
                                          id='comparison-geo-dropdown-parent',
                                          children=[
                                              html.Strong('Select Comparison Census Geography (Optional)'),
                                              dcc.Dropdown(order['Geography'].unique(), id='comparison-geo-dropdown'),
                                          ],
                                          className='dropdown-lgeo',
                                          style={
                                              "visibility": "visible"
                                          }
                                      ),
                                  ],
                                  className='dropdown-box-lgeo'
                              ),

                              # Area Scale Buttons
                              html.Div(children=[

                                  html.Div(children=[
                                      html.Button('View Census Subdivision (CSD)',
                                                  title='A provincially-legislated area at the municipal scale, or areas treated as municipal equivalents for statistical purposes (e.g. reserves, settlements and unorganized territories). Municipal status is defined by laws in effect in each province and territory in Canada.',
                                                  id='to-geography-1', n_clicks=0, className='region-button-lgeo'),
                                  ], className='region-button-box-lgeo'
                                  ),
                                  html.Div(children=[
                                      html.Button('View Census Division (CD)',
                                                  title='A provincially legislated area like counties, regional districts or equivalent areas. Census divisions are intermediate geographic areas between the province/territory level and the municipality (census subdivision).',
                                                  id='to-region-1', n_clicks=0, className='region-button-lgeo'),
                                  ], className='region-button-box-lgeo'
                                  ),
                                  html.Div(children=[
                                      html.Button('View Province / Territory',
                                                  title="'Province' and 'territory' refer to the major political units of Canada. Canada is divided into 10 provinces and 3 territories.",
                                                  id='to-province-1', n_clicks=0, className='region-button-lgeo'),
                                  ], className='region-button-box-lgeo'
                                  ),
                                  html.Div(children=[
                                      html.Button('Compare 2016 vs 2021',
                                                  title="Toggle a comparison between 2016 and 2021",
                                                  id='year-comparison-button', n_clicks=0,
                                                  className='region-button-lgeo'),
                                  ], className='region-button-box-lgeo'
                                  )

                              ],
                                  className='scale-button-box-lgeo'
                              ),

                              # Area Map picker

                              html.Div(children=[
                                  html.Div(
                                      dcc.Graph(
                                          id='canada_map',
                                          figure=fig_m,
                                          config=config,
                                      ),
                                      className='map-lgeo'

                                  ),

                                  # Map Reset Button
                                  html.Div(children=[
                                      html.Button('Reset Map', id='reset-map', n_clicks=0),
                                  ], className='reset-button-lgeo'
                                  ),

                              ], className='map-area-box-lgeo'
                              ),

                          ], className='dashboard-pg1-lgeo'
                      ),
                  ], className='background-lgeo'
                  )


# Callback for storing selected areas and area scale level


@callback(
    Output('main-area', 'data'),
    Output('comparison-area', 'data'),
    Output('area-scale-store', 'data'),
    Input('primary-geo-dropdown', 'value'),
    Input('comparison-geo-dropdown', 'value'),
    Input('comparison-geo-dropdown-parent', 'n_clicks'),
    Input('to-geography-1', 'n_clicks'),
    Input('to-region-1', 'n_clicks'),
    Input('to-province-1', 'n_clicks'),
    cache_args_to_ignore=[2, 3, 4, 5]
)
@cache.memoize()
def store_geo(geo, geo_c, *args):
    id_name = str(ctx.triggered_id)
    return geo, geo_c, id_name


# Area Selection Map

# Province Map generator
def province_map(value, random_color):
    clicked_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == value, :]['Province_Code'].tolist()[0]

    gdf_p_code_added['Geo_Code'] = gdf_p_code_added.index

    if random_color == True:
        gdf_p_code_added["rand"] = [round(i / (len(gdf_p_code_added) - 1) * 100) for i in
                                    range(0, len(gdf_p_code_added))]
        map_colors = map_colors_wo_black
    else:
        gdf_p_code_added["rand"] = gdf_p_code_added['Geo_Code'].apply(lambda x: 0 if x == int(clicked_code) else 100)
        map_colors = ['#37BB31', '#74D3F9']

    fig_m = go.Figure()

    fig_m.add_trace(go.Choroplethmapbox(geojson=json.loads(gdf_p_code_added.geometry.to_json()),
                                        locations=gdf_p_code_added.index,
                                        z=gdf_p_code_added.rand,
                                        showscale=False,
                                        colorscale=map_colors,
                                        text=gdf_p_code_added.NAME,
                                        hovertemplate='%{text} - %{location}<extra></extra>',
                                        marker=dict(opacity=opacity_value),
                                        marker_line_width=.5))
    fig_m.update_layout(mapbox_style="carto-positron",
                        mapbox_center={"lat": gdf_p_code_added['lat'].mean() + 10,
                                       "lon": gdf_p_code_added['lon'].mean()},
                        mapbox_zoom=2.0,
                        margin=dict(b=0, t=10, l=0, r=10),
                        modebar_color=modebar_color, modebar_activecolor=modebar_activecolor,
                        autosize=True)

    return fig_m


# Region Map generator
def region_map(value, random_color, clicked_code):
    if clicked_code == 'N':

        clicked_province_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == value, :]['Province_Code'].tolist()[
            0]
        clicked_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == value, :]['Region_Code'].tolist()[0]

        gdf_r_filtered = gpd.read_file(f'./sources/mapdata_simplified/region_data/{clicked_province_code}.shp',
                                       encoding='UTF-8')

    else:

        gdf_r_filtered = gpd.read_file(f'./sources/mapdata_simplified/region_data/{clicked_code}.shp', encoding='UTF-8')

    if random_color == True:
        gdf_r_filtered["rand"] = [i for i in range(0, len(gdf_r_filtered))]
        map_colors = map_colors_wo_black

    else:
        gdf_r_filtered["rand"] = gdf_r_filtered['CDUID'].apply(lambda x: 0 if x == clicked_code else 100)
        map_colors = ['#37BB31', '#74D3F9']

    gdf_r_filtered = gdf_r_filtered.set_index('CDUID')

    fig_mr = go.Figure()

    fig_mr.add_trace(go.Choroplethmapbox(geojson=json.loads(gdf_r_filtered.geometry.to_json()),
                                         locations=gdf_r_filtered.index,
                                         z=gdf_r_filtered.rand,
                                         showscale=False,
                                         colorscale=map_colors,
                                         text=gdf_r_filtered.CDNAME,
                                         hovertemplate='%{text} - %{location}<extra></extra>',
                                         marker=dict(opacity=opacity_value),
                                         marker_line_width=.5))

    fig_mr.update_layout(mapbox_style="carto-positron",
                         mapbox_center={"lat": gdf_r_filtered['lat'].mean(), "lon": gdf_r_filtered['lon'].mean()},
                         mapbox_zoom=3.0,
                         margin=dict(b=0, t=10, l=0, r=10),
                         modebar_color=modebar_color, modebar_activecolor=modebar_activecolor,
                         autosize=True)

    return fig_mr


# Subregion Map generator
def subregion_map(value, random_color, clicked_code):
    if clicked_code == 'N':
        clicked_region_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == value, :]['Region_Code'].tolist()[0]
        clicked_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == value, :]['Geo_Code'].tolist()[0]
        clicked_code = str(clicked_code)

        gdf_sr_filtered = gpd.read_file(f'./sources/mapdata_simplified/subregion_data/{clicked_region_code}.shp')

    else:
        clicked_code_region = clicked_code[:4]
        gdf_sr_filtered = gpd.read_file(f'./sources/mapdata_simplified/subregion_data/{clicked_code_region}.shp')

    if random_color == True:
        gdf_sr_filtered["rand"] = gdf_sr_filtered['CSDUID'].apply(
            lambda x: 0 if x in not_avail['CSDUID'].tolist() else np.random.randint(30, 100))

        if 0 in gdf_sr_filtered["rand"].tolist():
            colorlist = map_colors_w_black
        else:
            colorlist = map_colors_wo_black

    else:
        gdf_sr_filtered["rand"] = gdf_sr_filtered['CSDUID'].apply(
            lambda x: 0 if x in not_avail['CSDUID'].tolist() else (50 if x == clicked_code else 100))

        if 0 in gdf_sr_filtered["rand"].tolist():
            colorlist = ['#000000', '#37BB31', '#74D3F9']
        else:
            colorlist = ['#37BB31', '#74D3F9']

    gdf_sr_filtered = gdf_sr_filtered.set_index('CSDUID')

    fig_msr = go.Figure()

    fig_msr.add_trace(go.Choroplethmapbox(geojson=json.loads(gdf_sr_filtered.geometry.to_json()),
                                          locations=gdf_sr_filtered.index,
                                          z=gdf_sr_filtered.rand,
                                          showscale=False,
                                          text=gdf_sr_filtered.CSDNAME,
                                          hovertemplate='%{text} - %{location}<extra></extra>',
                                          colorscale=colorlist,
                                          marker=dict(opacity=opacity_value),
                                          marker_line_width=.5))

    max_bound = max(abs((gdf_sr_filtered['lat'].max() - gdf_sr_filtered['lat'].min())),
                    abs((gdf_sr_filtered['lon'].max() - gdf_sr_filtered['lon'].min()))) * 111

    zoom = 11.5 - np.log(max_bound)

    if len(gdf_sr_filtered) == 1:
        zoom = 9

    fig_msr.update_layout(mapbox_style="carto-positron",
                          mapbox_center={"lat": gdf_sr_filtered['lat'].mean(), "lon": gdf_sr_filtered['lon'].mean()},
                          mapbox_zoom=zoom,
                          margin=dict(b=0, t=10, l=0, r=10),
                          modebar_color=modebar_color, modebar_activecolor=modebar_activecolor,
                          autosize=True)
    return fig_msr


# Callback logic for the map picker


@callback(
    Output('canada_map', 'figure'),
    Output('primary-geo-dropdown', 'value'),
    Output('comparison-geo-dropdown', 'value'),
    [Input('canada_map', 'clickData')],
    Input('primary-geo-dropdown', 'value'),
    Input('comparison-geo-dropdown', 'value'),
    Input('reset-map', 'n_clicks'),
    Input('to-geography-1', 'n_clicks'),
    Input('to-region-1', 'n_clicks'),
    Input('to-province-1', 'n_clicks'),
)
@cache.memoize()
# 
def update_map(clickData, select_region, comparison_region, *args):
    # If no area is selected, then map will show Canada Map
    if select_region is None:
        select_region = default_value
    # Make the logic below zoom to the correct level even during comparison

    # User clicked on comparison dropdown
    if ctx.triggered_id == "comparison-geo-dropdown" or ctx.triggered_id == "comparison-geo-dropdown-parent":
        if comparison_region is None:
            return dash.no_update, select_region, None
        region_in_focus = comparison_region
        clicked_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == comparison_region, :]['Geo_Code'].tolist()[0]
    else:
        region_in_focus = select_region
        clicked_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == select_region, :]['Geo_Code'].tolist()[0]
    clicked_code = str(clicked_code)

    selectedDropDown = (ctx.triggered_id == 'primary-geo-dropdown' or ctx.triggered_id == 'comparison-geo-dropdown')

    # When Canada is selected in the textbox

    if len(clicked_code) == 1 and selectedDropDown:
        fig_m = province_map(default_value, True)

        return fig_m, select_region, comparison_region

    # When users click 'View Province' button or select a province on dropbox menu

    if (len(clicked_code) == 2 and selectedDropDown) or "to-province-1" == ctx.triggered_id:
        fig_m = province_map(region_in_focus, False)

        return fig_m, select_region, comparison_region

    # When users click 'View Census Division' button or select a Census Division on dropbox menu

    if (len(clicked_code) == 4 and selectedDropDown) or "to-region-1" == ctx.triggered_id:

        # When users click 'View Census Division' button after selecting Province on dropbox menu
        # Canada is the current focus
        if len(clicked_code) == 1:
            fig_m = province_map(default_value, True)

            return fig_m, select_region, comparison_region
        # -> Show map for Province
        if len(clicked_code) == 2:
            fig_m = province_map(region_in_focus, False)

            return fig_m, select_region, comparison_region

        # When users select Census Division on dropbox menu
        # or When users click 'View Census Division' button after selecting Census Division on dropbox menu
        # -> Show map for Census Division

        fig_mr = region_map(region_in_focus, False, 'N')

        return fig_mr, select_region, comparison_region

    # When users click 'View Census SubDivision' button or select a Census SubDivision on dropbox menu

    if (len(clicked_code) > 4 and selectedDropDown) or "to-geography-1" == ctx.triggered_id:

        # When users click 'View Census SubDivision' button after selecting Census Division on dropbox menu
        # -> Show map for Census Division

        if len(clicked_code) == 4:

            fig_mr = region_map(region_in_focus, False, 'N')

            return fig_mr, select_region, comparison_region

        # When users click 'View Census SubDivision' button after selecting Province on dropbox menu
        # -> Show map for Province

        elif len(clicked_code) == 2:

            fig_m = province_map(region_in_focus, False)

            return fig_m, select_region, comparison_region

        # When users select Census SubDivision on dropbox menu 
        # or when users click 'View Census SubDivision' button after selecting Census SubDivision on dropbox menu
        # -> Show map for Census SubDivision

        elif len(clicked_code) == 7:

            fig_msr = subregion_map(region_in_focus, False, 'N')

            return fig_msr, select_region, comparison_region

    # When Reset-Map button is clicked

    if "reset-map" == ctx.triggered_id:
        fig_m = province_map(select_region, True)

        return fig_m, default_value, None

    # When users clicked province on the map

    if type(clickData) == dict:

        clicked_code = str(clickData['points'][0]['location'])

        if len(clicked_code) == 2:

            fig_mr = region_map(select_region, True, clicked_code)

            region_name = df_province_list.query("Geo_Code == " + f"{clicked_code}")['Geography'].tolist()[0]

            return fig_mr, region_name, comparison_region

        # When users clicked region on the regional map after clicking province 
        # -> show subregion map

        elif len(clicked_code) == 4:

            fig_msr = subregion_map(select_region, True, clicked_code)

            region_name = df_region_list.query("Geo_Code == " + f"{clicked_code}")['Geography'].tolist()[0]

            return fig_msr, region_name, comparison_region

        # When users clicked subregion on the regional map after clicking province 
        # -> remains subregion map and send subregion code to area selection dropdown

        elif len(clicked_code) > 4:

            fig_msr = subregion_map(select_region, False, clicked_code)

            subregion_name = mapped_geo_code.query("Geo_Code == " + f"{clicked_code}")['Geography'].tolist()[0]

            return fig_msr, subregion_name, comparison_region

    # default map (show provinces) before clicking anything on the map

    fig_m = province_map(select_region, True)

    return fig_m, select_region, comparison_region


# Add custom CSS to change the color of the disabled input
clientside_callback(
    """
    function updateDisabledColor(isDisabled) {
        if (isDisabled) {
            // Change the color of the disabled input
            return { backgroundColor: 'lightgray', color: 'darkgray' };
        } else {
            // Reset styles when the input is not disabled
            return { backgroundColor: 'white', color: 'black' };
        }
    }
    """,
    Output('comparison-geo-dropdown', 'style'),
    [Input('comparison-geo-dropdown', 'disabled')]
)


@callback(
    Output('year-comparison', 'data'),
    Output("comparison-geo-dropdown", "disabled"),
    Output("year-comparison-button", "style"),
    State('year-comparison', 'data'),
    Input("year-comparison-button", "n_clicks"),
    Input('reset-map', 'n_clicks'),
    cache_args_to_ignore=[1, 2]
)
@cache.memoize()
def toggle_year_comparison(year_comparison, *args):
    if ctx.triggered_id == "year-comparison-button":
        if year_comparison is not None:
            year_comparison = None
            return year_comparison, False, {}
        else:
            year_comparison = "2021-2016"
            return year_comparison, True, {
                "color": "#FFFFFF",
                "background-color": "#3EB549"
            }
    # return dash.no_update, dash.no_update
    return None, False, {}
