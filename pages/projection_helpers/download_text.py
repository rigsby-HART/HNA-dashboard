from dash import Output, callback, Input, State, ctx

from app_file import cache
from helpers.table_helper import area_scale_primary_only
from pages.page3 import default_value


@callback(
    Output('graph9', 'config'),
    Output('graph10', 'config'),
    Output('graph-h', 'config'),
    Output('graph11', 'config'),
    Output('graph12', 'config'),
    Output('graph13', 'config'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('projected-hh-by-hh-size-income', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
@cache.memoize()
def change_download_names(geo: str, geo_c: str, year_comparison: str, scale, lang_query, update):
    print("TRIGGERED")
    print(str(ctx.triggered_prop_ids))
    print(str(ctx.triggered_id))
    print(str(ctx.triggered))
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

    if year_comparison:
        original_year, compared_year = year_comparison.split("-")
        return (
            {**config, 'toImageButtonOptions':
                {'filename': f'{geo}_Household Projections by Income Category_{compared_year}vs{original_year}'}},
            {**config, 'toImageButtonOptions':
                {'filename': f'{geo}_Household Projections by Household Size_{compared_year}vs{original_year}'}},
            {**config, 'toImageButtonOptions':
                {'filename': f'{geo}_Household Projections by Household Size and Income Category_{compared_year}vs{original_year}'}},
            {**config, 'toImageButtonOptions':
                {'filename': f'{geo}_Projected Household Gain/Loss_{compared_year}vs{original_year}'}},
            {**config, 'toImageButtonOptions':
                {'filename': f'{geo}_Percentage of Households in Core Housing Need, by Priority Population_{compared_year}vs{original_year}'}},
            {**config, 'toImageButtonOptions':
                {'filename': f'{geo}_Percentage of Households in Core Housing Need, by Priority Population and Income Category_{compared_year}vs{original_year}'}},
        )
    return (
        {**config, 'toImageButtonOptions':
            {'filename': f'{geo}_Percentage of Households in Core Housing Need, by Income Category_2021'}},
        {**config, 'toImageButtonOptions':
            {'filename': f'{geo}_Percentage of Households in Core Housing Need, by Income Category and HH Size_2021'}},
        {**config, 'toImageButtonOptions':
            {'filename': f'{geo}_Percentage of Households in Core Housing Need, by Priority Population_2021'}},
        {**config, 'toImageButtonOptions':
            {'filename': f'{geo}_Percentage of Households in Core Housing Need, by Priority Population and Income Category_2021'}},
        {**config, 'toImageButtonOptions':
            {'filename': f'{geo}_Percentage of Households in Core Housing Need, by Priority Population_2021'}},
        {**config, 'toImageButtonOptions':
            {'filename': f'{geo}_Percentage of Households in Core Housing Need, by Priority Population and Income Category_2021'}},
    )