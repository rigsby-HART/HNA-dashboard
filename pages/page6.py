# Importing Libraries
import dash
import pandas as pd
import warnings
from dash import dcc, Input, Output, ctx, callback, State, html, register_page, clientside_callback
from dash.dash_table.Format import Format, Group, Scheme

from app_file import cache
from helpers.create_engine import transit_distance, default_year, default_value, mapped_geo_code
from helpers.style_helper import columns_color_fill, style_data_conditional, style_header_conditional
from helpers.table_helper import query_table, area_scale_primary_only, area_scale_comparison
from pages.transit_distance.page6_main import layout
from pages.transit_distance.population import get_quintile_info

register_page(__name__)
warnings.filterwarnings("ignore")

# Import helpers

# import pages.renter_owner_helpers.download_text            # noqa


# Setting layout for dashboard

layout = layout(default_year)


@callback(
    Output('datatable-transit-page6', 'columns'),
    Output('datatable-transit-page6', 'data'),
    Output('datatable-transit-page6', 'style_data_conditional'),
    Output('datatable-transit-page6', 'style_cell_conditional'),
    Output('datatable-transit-page6', 'style_header_conditional'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    State('area-scale-store', 'data'),
    Input('area-scale-store', 'modified_timestamp'),
    State('url', 'search'),
    cache_args_to_ignore=[3]
)
@cache.memoize()
def update_transportation_table(geo, geo_c, scale, update, lang_query):
    # When no area is selected
    if geo == None and geo_c != None:
        geo = geo_c
    elif geo == None and geo_c == None:
        geo = default_value
    if not geo_c:
        # Area Scaling up/down when user clicks area scale button on page 1
        geo = area_scale_primary_only(geo, scale)
    else:
        geo, geo_c = area_scale_comparison(geo, geo_c, scale)
    try:
        geo_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]["Geo_Code"].tolist()[0]
        if geo_c:
            geo_c_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c, :]["Geo_Code"].tolist()[0]
        df = get_quintile_info(geo_code)
    except:
        # No data for the selected region
        no_data = f"No Data for {geo}, please try CD/Provincial level"
        table = pd.DataFrame({no_data: [""]})
        return [{"name": no_data, "id": no_data}], table.to_dict("records"), [], [], style_header_conditional
    # Generating callback output to update table
    col_list = []
    for i in df.columns:
        col_list.append({"name": [geo, i],
                         "id": i,
                         "type": 'numeric',
                         "format": Format(
                             group=Group.yes,
                             scheme=Scheme.fixed,
                             precision=0
                         )})

    style_cell_conditional = [
                                 {
                                     'if': {'column_id': c},
                                     'backgroundColor': columns_color_fill[1],

                                     # "maxWidth" : "100px"
                                 } for c in df.columns[1:]
                             ] + [
                                 {
                                     'if': {'column_id': df.columns[0]},
                                     'backgroundColor': columns_color_fill[0],

                                 }
                             ] + [
                             ]
    return col_list, df.to_dict(
        'records'), style_data_conditional, style_cell_conditional, style_header_conditional


clientside_callback(
    """
    async function (input) {
        if (input > 0) {
            console.log("Downloading page")
            html2canvas(document.body, { allowTaint: true , scrollX:0, scrollY: 0  }).then(function(canvas) {
                saveAs(canvas.toDataURL(), 'PublicTransit.png');
            });
        }
        
        return "";
    }
    """,
    Output("placeholder-pg6", "children"),
    Input("ov7-download-csv-pg6", "n_clicks"),
)


@callback(
    Output("ov7-download-text-pg6", "data"),
    Input("ov7-download-csv-pg6", "n_clicks"),
    State('main-area', 'data'),
    State('comparison-area', 'data'),
    State('area-scale-store', 'data'),
    State('year-comparison', 'data'),
    config_prevent_initial_callbacks=True,
)
def func_ov7(n_clicks, geo, geo_c, scale, year_comparison):
    # When no area is selected
    if geo == None and geo_c != None:
        geo = geo_c
    elif geo == None and geo_c == None:
        geo = default_value
    if not geo_c:
        # Area Scaling up/down when user clicks area scale button on page 1
        geo = area_scale_primary_only(geo, scale)
    else:
        geo, geo_c = area_scale_comparison(geo, geo_c, scale)

    # else:
    # if len(geo) != 7 or (geo_c and len(geo_c) != 7):
    #     return dash.no_update
    geo_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo, :]["Geo_Code"].tolist()[0]
    df = transit_distance[transit_distance['CSDUID'].astype(str).str.startswith(str(geo_code))]
    if geo_c:
        geo_c_code = mapped_geo_code.loc[mapped_geo_code['Geography'] == geo_c, :]["Geo_Code"].tolist()[0]
        df_c = transit_distance[transit_distance['CSDUID'].astype(str).str.startswith(str(geo_c_code))]
        df = pd.concat([df, df_c])
    return dcc.send_data_frame(df.to_csv, "result.csv")
