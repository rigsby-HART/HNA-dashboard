from dash import Input, Output, html, callback

from helpers.create_engine import default_year


@callback(
    Output("income-categories-title-page2", "children"),
    Output("percent-HH-CHN-title-page2", "children"),
    Output("percent-IC-HH-CHN-title-page2", "children"),
    Output("housing-deficit-page2", "children"),
    Output("pct-pp-hh-chn-page2", "children"),
    Output("pct-pp-ic-chn-page2", "children"),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    Input('income-category-affordability-table', 'selected_columns'),
)
def change_title_labels(geo, geo_c, year_comparison, scale, refresh):
    # change based off of url
    print("page2 change labels")
    if year_comparison:
        original_year, compared_year = year_comparison.split("-")
        return (
            html.Strong(f'Income Categories and Affordable Shelter Costs, {compared_year} vs {original_year}'),
            html.Strong(f'Percentage of Households in Core Housing Need, by Income Category, {compared_year} vs {original_year}'),
            html.Strong(f'Percentage of Households in Core Housing Need, by Income Category and HH Size, {compared_year} vs {original_year}'),
            html.Strong(f'{compared_year} vs {original_year} Affordable Housing Deficit'),
            html.Strong(f'Percentage of Households in Core Housing Need by Priority Population, {compared_year} vs {original_year}'),
            html.Strong(f'Percentage of Households in Core Housing Need by Priority Population and Income Category, {compared_year} vs {original_year}')
        )
    return (
        html.Strong(f'Income Categories and Affordable Shelter Costs, {default_year}'),
        html.Strong(f'Percentage of Households in Core Housing Need, by Income Category, {default_year}'),
        html.Strong(f'Percentage of Households in Core Housing Need, by Income Category and HH Size, {default_year}'),
        html.Strong(f'{default_year} Affordable Housing Deficit'),
        html.Strong(f'Percentage of Households in Core Housing Need by Priority Population, {default_year}'),
        html.Strong(f'Percentage of Households in Core Housing Need by Priority Population and Income Category, {default_year}')
    )