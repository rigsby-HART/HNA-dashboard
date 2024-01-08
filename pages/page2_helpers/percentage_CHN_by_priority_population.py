# Percentage of Households in Core Housing Need by Priority Population, 2021
import math

import pandas as pd
import plotly.graph_objects as go
from dash import Output, Input, State, callback
from plotly.subplots import make_subplots

from app_file import cache
from helpers.create_engine import default_year, default_value, income_partners_year
from helpers.localization import localization
from helpers.style_helper import modebar_color, modebar_activecolor
from helpers.table_helper import query_table, get_language, area_scale_primary_only, area_scale_comparison, \
    error_region_figure

# Preparing global variables for the table

hh_category_dict = {
    'Percent Single Mother led HH in core housing need': 'Single mother-led HH',
    'Percent Women-led HH in core housing need': 'Women-led HH',
    'Percent Indigenous HH in core housing need': 'Indigenous HH',
    'Percent Visible minority HH in core housing need': 'Visible minority HH',
    'Percent Black-led HH in core housing need': 'Black-led HH',
    'Percent New migrant-led HH in core housing need': 'New migrant-led HH',
    'Percent Refugee claimant-led HH in core housing need': 'Refugee claimant-led HH',
    'Percent HH head under 25 in core housing need': 'HH head under 25',
    'Percent HH head over 65 in core housing need': 'HH head over 65',
    'Percent HH head over 85 in core housing need': 'HH head over 85',
    'Percent HH with physical act. limit. in core housing need': 'HH with physical activity limitation',
    'Percent HH with cognitive, mental, or addictions activity limitation in core housing need': 'HH with cognitive, mental,<br>or addictions activity limitation',
    'Percent of Transgender HH in core housing': 'Transgender or Non-binary HH',
    'Percent HH in core housing need': 'Community (all HH)'
}

hh_columns = hh_category_dict.keys()
hh_categories = list(hh_category_dict.values())
hh_type_color = ['#002145', '#3EB549', '#39C0F7']

# Plot dataframe generator

def plot_df_core_housing_need_by_priority_population(geo, language: str, year: int = default_year):
    geo, joined_df_filtered = query_table(geo, year, income_partners_year)
    if year == 2016:
        columns = list(hh_columns)
        columns.remove('Percent of Transgender HH in core housing')
        percent_hh = [joined_df_filtered[c].tolist()[0] for c in columns]

        categories = [localization[language][category] for category in hh_categories]
        categories.remove(localization[language]["Transgender or Non-binary HH"])
        plot_df = pd.DataFrame({'HH_Category': categories, 'Percent_HH': percent_hh})
    else:
        percent_hh = [joined_df_filtered[c].tolist()[0] for c in hh_columns]
        categories = [localization[language][category] for category in hh_categories]
        plot_df = pd.DataFrame({'HH_Category': categories, 'Percent_HH': percent_hh})
        plot_df['Percent_HH'] = plot_df['Percent_HH'].fillna(0)

    return plot_df


# Plot bar color generator

def color_dict_core_housing_need_by_priority_population(plot_df):
    color_dict = {}

    for h in plot_df['HH_Category'].unique():

        if plot_df['Percent_HH'].max() == 0:
            color_dict[h] = hh_type_color[2]
        else:
            if h == plot_df.loc[plot_df['Percent_HH'] == plot_df['Percent_HH'].max(), 'HH_Category'].tolist()[0]:
                color_dict[h] = hh_type_color[0]
            elif h == 'Community (all HH)':
                color_dict[h] = hh_type_color[1]
            else:
                color_dict[h] = hh_type_color[2]

    return color_dict


# Callback logic for the plot update


@callback(
    Output('graph5', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
@cache.memoize()
def update_geo_figure5(geo, geo_c, year_comparison: str, scale, lang_query, refresh):
    language = get_language(lang_query)

    if (geo == geo_c or geo_c == None or (geo == None and geo_c != None)) and not year_comparison:

        # When no area is selected

        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1

        geo = area_scale_primary_only(geo, scale)

        # Generating dataframe for plot and color lists
        if error_region_figure(geo, default_year, language):
            return error_region_figure(geo, default_year, language)
        plot_df = plot_df_core_housing_need_by_priority_population(geo, language)
        color_dict = color_dict_core_housing_need_by_priority_population(plot_df)

        # Generating plot

        fig5 = go.Figure()
        for i in [localization[language][category] for category in hh_categories]:
            plot_df_frag = plot_df.loc[plot_df['HH_Category'] == i, :]
            fig5.add_trace(go.Bar(
                y=plot_df_frag['HH_Category'],
                x=plot_df_frag['Percent_HH'],
                name=i,
                marker_color=color_dict[i],
                orientation='h',
                hovertemplate='%{y} - ' + '%{x: .2%}<extra></extra>',
            ))

        # Plot layout settings
        fig5.update_layout(
            yaxis=dict(autorange="reversed"),
            width=900,
            height=500,
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            showlegend=False,
            plot_bgcolor='#F8F9F9',
            title=localization[language][
                      'Percentage of Households in Core Housing Need by Priority Population,'] + f' {default_year}<br>{geo}',
            legend_title="HH Category"
        )
        fig5.update_xaxes(
            title_font=dict(size=10),
            fixedrange=True,
            tickformat=',.0%',
            range=[0, math.ceil(plot_df['Percent_HH'].max() * 10) / 10],
            title=localization[language]["% of Priority Population HH"]
        )
        fig5.update_yaxes(
            fixedrange=True,
            tickfont=dict(size=10)
        )

        return fig5

    # Comparison mode

    else:
        if year_comparison:
            original_year, compared_year = year_comparison.split("-")
            geo = area_scale_primary_only(geo, scale)
        # Area Scaling up/down when user clicks area scale button on page 1
        else:
            geo, geo_c = area_scale_comparison(geo, geo_c, scale)
            original_year, compared_year = default_year, default_year

        # Subplot setting for the comparison mode
        fig5 = make_subplots(rows=1, cols=2, subplot_titles=(f"{geo + ' ' + compared_year if year_comparison else geo}",
                                                             f"{geo + ' ' + original_year if year_comparison else geo_c}"),
                             shared_yaxes=True, shared_xaxes=True)

        # Main Plot

        # Generating dataframe for main plot and color list

        if year_comparison:
            if error_region_figure(geo, int(compared_year), language):
                return error_region_figure(geo, int(compared_year), language)
        else:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        plot_df = plot_df_core_housing_need_by_priority_population(geo, language,
                                                                   int(compared_year) if year_comparison else
                                                                   default_year)
        color_dict = color_dict_core_housing_need_by_priority_population(plot_df)

        # Generating main plot

        for i in plot_df["HH_Category"]:
            plot_df_frag = plot_df.loc[plot_df['HH_Category'] == i, :]
            fig5.add_trace(go.Bar(
                y=plot_df_frag['HH_Category'],
                x=plot_df_frag['Percent_HH'],
                name=i,
                marker_color=color_dict[i],
                orientation='h',
                hovertemplate='%{y} - ' + '%{x: .2%}<extra></extra>',
            ), row=1, col=1)

        # Comparison Plot

        # Generating dataframe for comparison plot and color list

        if year_comparison:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        else:
            if error_region_figure(geo_c, default_year, language):
                return error_region_figure(geo_c, default_year, language)
        plot_df_c = (
            plot_df_core_housing_need_by_priority_population(geo, language, int(original_year)) if year_comparison else
            plot_df_core_housing_need_by_priority_population(geo_c, language)
        )
        color_dict = color_dict_core_housing_need_by_priority_population(plot_df_c)

        # Generating comparison plot

        for i in [localization[language][category] for category in hh_categories]:
            plot_df_frag_c = plot_df_c.loc[plot_df_c['HH_Category'] == i, :]
            fig5.add_trace(go.Bar(
                y=plot_df_frag_c['HH_Category'],
                x=plot_df_frag_c['Percent_HH'],
                name=i,
                marker_color=color_dict[i],
                orientation='h',
                hovertemplate='%{y} - ' + '%{x: .2%}<extra></extra>',
            ), row=1, col=2)

        # Plot layout settings

        fig5.update_layout(
            title=localization[language][
                      'Percentage of Households in Core Housing Need by Priority Population,'] +
                  (f'<br>{geo} 2016 {localization[language]["vs"]} 2021' if year_comparison
                   else f'{geo} {localization[language]["vs"]} {geo_c}'),
            width=900,
            height=500,
            legend=dict(font=dict(size=8)),
            yaxis=dict(autorange="reversed"),
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            showlegend=False,
            plot_bgcolor='#F8F9F9',
            legend_title="HH Category"
        )
        fig5.update_xaxes(
            title_font=dict(size=10),
            tickfont=dict(size=8),
            tickformat=',.0%',
            fixedrange=True,
            range=[0, math.ceil(max(plot_df['Percent_HH'].max(), plot_df_c['Percent_HH'].max()) * 10) / 10],
            title=localization[language]["% of Priority Population HH"]
        )
        fig5.update_yaxes(
            fixedrange=True,
            tickfont=dict(size=10)
        )

        return fig5