from dash import Output, callback, Input, State, ctx

from app_file import cache
from helpers.create_engine import default_year
from helpers.table_helper import area_scale_primary_only
from pages.page3 import default_value


@callback(
    Output('graph_ind', 'config'),
    Output('graph2_ind', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('datatable-interactivity_ind', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
@cache.memoize()
def change_download_names(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    # When no area is selected
    if geo == None and geo_c != None:
        geo = geo_c
    elif geo == None and geo_c == None:
        geo = default_value

    # Area Scaling up/down when user clicks area scale button on page 1
    geo = area_scale_primary_only(geo, scale)
    if geo_c:
        geo = geo + "vs" + geo_c
    config = {
        'displayModeBar': True, 'displaylogo': False,
        'modeBarButtonsToRemove': ['zoom', 'lasso2d', 'pan', 'select', 'zoomIn', 'zoomOut', 'autoScale',
                                   'resetScale'],
        "toImageButtonOptions": {
            "filename": 'la mao'
        }
    }

    year = default_year
    if year_comparison:
        original_year, compared_year = year_comparison.split("-")
        year = f"{compared_year} vs {original_year}"
    return (
        {**config, 'toImageButtonOptions':
            {'filename': f'{geo}_Percentage of Indigenous Households in Core Housing Need, by Income Category_{year}'}},
        {**config, 'toImageButtonOptions':
            {'filename': f'{geo}_Percentage of Indigenous Households in Core Housing Need, by Income Category and HH Size_{year}'}},
    )