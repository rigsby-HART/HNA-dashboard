# Percentage of Households in Core Housing Need by Priority Population and Income Category, 2021
import copy

import pandas as pd
import plotly.graph_objects as go
from dash import Output, Input, State, callback
from plotly.subplots import make_subplots

from app_file import cache
from helpers.create_engine import default_year, default_value, partner_table
from helpers.localization import localization
from helpers.style_helper import colors, modebar_color, modebar_activecolor
from helpers.table_helper import query_table, get_language, area_scale_primary_only, area_scale_comparison, \
    error_region_figure

# Preparing global variables for the table

hh_category_dict2 = {
    'Percent of Single Mother led HH in core housing need': 'Single mother-led HH',
    'Percent of Women-led HH in core housing need': 'Women-led HH',
    'Percent of Indigenous HH in core housing need': 'Indigenous HH',
    'Percent of Visible minority HH in core housing need': 'Visible minority HH',
    'Percent of Black-led HH in core housing need': 'Black-led HH',
    'Percent of New migrant-led HH in core housing need': 'New migrant-led HH',
    'Percent of Refugee claimant-led HH in core housing need': 'Refugee claimant-led HH',
    'Percent of HH head under 25 in core housing need': 'HH head under 25',
    'Percent of HH head over 65 in core housing need': 'HH head over 65',
    'Percent of HH head over 85 in core housing need': 'HH head over 85',
    'Percent of HH with physical act. limit. in core housing need': 'HH with physical activity limitation',
    'Percent of HH with with cognitive, mental, or addictions activity limitation in core housing need': 'HH with cognitive, mental,<br>or addictions activity limitation',
}

hh_category_dict3 = {
    'Percent of Single Mother led HH core housing': 'Single mother-led HH',
    'Percent of Women-led HH core housing': 'Women-led HH',
    'Percent of Indigenous HH in core housing': 'Indigenous HH',
    'Percent of Visible minority HH core housing': 'Visible minority HH',
    'Percent of Black-led HH core housing': 'Black-led HH',
    'Percent of New migrant-led HH core housing': 'New migrant-led HH',
    'Percent of Refugee claimant-led HH core housing': 'Refugee claimant-led HH',
    'Percent of HH head under 25 core housing': 'HH head under 25',
    'Percent of HH head over 65 core housing': 'HH head over 65',
    'Percent of HH head over 85 core housing': 'HH head over 85',
    'Percent of HH with physical act. limit. in core housing': 'HH with physical activity limitation',
    'Percent of HH with cognitive, mental, or addictions activity limitation in core housing': 'HH with cognitive, mental,<br>or addictions activity limitation',
}

hh_category_dict4 = {
    'Percent of Single Mother led HH in core housing': 'Single mother-led HH',
    'Percent of Women-led HH in core housing': 'Women-led HH',
    'Percent of Indigenous HH in core housing': 'Indigenous HH',
    'Percent of Visible minority HH in core housing': 'Visible minority HH',
    'Percent of Black-led HH in core housing': 'Black-led HH',
    'Percent of New migrant-led HH in core housing': 'New migrant-led HH',
    'Percent of Refugee claimant-led HH in core housing': 'Refugee claimant-led HH',
    'Percent of HH head under 25 in core housing': 'HH head under 25',
    'Percent of HH head over 65 in core housing': 'HH head over 65',
    'Percent of HH head over 85 in core housing': 'HH head over 85',
    'Percent of HH with physical act. limit. in core housing': 'HH with physical activity limitation',
    'Percent of HH with cognitive, mental, or addictions activity limitation in core housing': 'HH with cognitive, mental,<br>or addictions activity limitation',
}

columns2 = hh_category_dict2.keys()
columns3 = hh_category_dict3.keys()
columns4 = hh_category_dict4.keys()

income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']


# Plot dataframe generator

def plot_df_core_housing_need_by_priority_population_income(geo: str, language: str, year=default_year):
    geo, joined_df_filtered = query_table(geo, year, partner_table)

    income_col = []
    percent_col = []
    hh_cat_col = []

    col2 = columns2
    col3 = columns3
    col4 = columns4

    dict2 = hh_category_dict2
    dict3 = hh_category_dict3
    dict4 = hh_category_dict4
    if year != 2016:
        dict2 = copy.deepcopy(dict2)
        dict3 = copy.deepcopy(dict3)
        dict4 = copy.deepcopy(dict4)
        dict2['Percent of Transgender HH in core housing'] = 'Transgender or Non-binary HH'
        dict3['Percent of Transgender HH in core housing'] = 'Transgender or Non-binary HH'
        dict4['Percent of Transgender HH in core housing'] = 'Transgender or Non-binary HH'
        col2 = dict2.keys()
        col3 = dict3.keys()
        col4 = dict4.keys()
    dict2 = {key: localization[language][value] for key, value in zip(dict2.keys(), dict2.values())}
    dict3 = {key: localization[language][value] for key, value in zip(dict3.keys(), dict3.values())}
    dict4 = {key: localization[language][value] for key, value in zip(dict4.keys(), dict4.values())}
    row_labels = ["Very Low Income", "Low Income", "Moderate Income", "Median Income", "High Income"]
    base = [localization[language][label] for label in row_labels]
    for c, c2, c3 in zip(col2, col3, col4):
        for index, i in enumerate(income_lv_list):
            if i == '20% or under':
                p_hh = joined_df_filtered[f'{c} with income {i} of the AMHI'].tolist()[0]
                hh_cat_col.append(dict2[c])
            elif i == '21% to 50%':
                p_hh = joined_df_filtered[f'{c2} with income {i} of AMHI'].tolist()[0]
                hh_cat_col.append(dict3[c2])
            else:
                p_hh = joined_df_filtered[f'{c3} with income {i} of AMHI'].tolist()[0]
                hh_cat_col.append(dict4[c3])

            income_col.append(base[index])
            percent_col.append(p_hh)

    plot_df = pd.DataFrame({'Income_Category': income_col, 'HH_Category': hh_cat_col, 'Percent': percent_col})

    return plot_df


# Callback logic for the plot update


@callback(
    Output('graph6', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
@cache.memoize()
def update_geo_figure6(geo, geo_c, year_comparison, scale, lang_query, refresh):
    # Overried income category values
    income_category_override = ['Very Low', 'Low', 'Moderate', 'Median', 'High']

    language = get_language(lang_query)
    # Single area mode

    if not year_comparison and (geo == geo_c or geo_c == None or (geo == None and geo_c != None)):
        # When no area is selected
        if geo == None and geo_c != None:
            geo = geo_c
        elif geo == None and geo_c == None:
            geo = default_value

        # Area Scaling up/down when user clicks area scale button on page 1
        geo = area_scale_primary_only(geo, scale)

        # Generating dataframe for plot
        if error_region_figure(geo, default_year, language):
            return error_region_figure(geo, default_year, language)
        plot_df = plot_df_core_housing_need_by_priority_population_income(geo, language)

        # Generating plot
        fig6 = go.Figure()

        for i, c, o in zip(plot_df['Income_Category'].unique(), colors, income_category_override):
            plot_df_frag = plot_df.loc[plot_df['Income_Category'] == i, :]
            fig6.add_trace(go.Bar(
                y=plot_df_frag['HH_Category'],
                x=plot_df_frag['Percent'],
                name=o,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y}, ' + f'{o} Income - ' + '%{x: .2%}<extra></extra>',
            ))

        # Plot layout settings
        fig6.update_layout(
            width=900,
            height=500,
            legend_traceorder="normal",
            font=dict(size=10),
            legend=dict(font=dict(size=9)),
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            yaxis=dict(autorange="reversed"),
            barmode='stack',
            plot_bgcolor='#F8F9F9',
            title=localization[language][
                      "Percentage of Households in Core Housing Need by Priority Population and Income Category,"] + f' {default_year}<br>{geo}',
            legend_title=localization[language]["Income Category"]
        )
        fig6.update_xaxes(
            title_font=dict(size=10),
            fixedrange=True,
            tickformat=',.0%',
            title=localization[language]["% of HH"]
        )
        fig6.update_yaxes(
            fixedrange=True,
            tickfont=dict(size=10)
        )

        return fig6

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
        fig6 = make_subplots(rows=1, cols=2,
                             subplot_titles=(f"{geo + ' ' + compared_year if year_comparison else geo}",
                                             f"{geo + ' ' + original_year if year_comparison else geo_c}"),
                             shared_yaxes=True, shared_xaxes=True)

        # Main Plot
        if year_comparison:
            if error_region_figure(geo, int(compared_year), language):
                return error_region_figure(geo, int(compared_year), language)
        else:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        # Generating dataframe for main plot
        plot_df = (
            plot_df_core_housing_need_by_priority_population_income(geo, language,
                                                                    int(compared_year) if year_comparison else
                                                                    int(original_year))
        )

        # Generating main plot

        n = 0
        for i, c, o in zip(plot_df['Income_Category'].unique(), colors, income_category_override):
            plot_df_frag = plot_df.loc[plot_df['Income_Category'] == i, :]
            fig6.add_trace(go.Bar(
                y=plot_df_frag['HH_Category'],
                x=plot_df_frag['Percent'],
                name=i,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y}, ' + f'{i} Income - ' + '%{x: .2%}<extra></extra>',
                legendgroup=f'{n}'
            ), row=1, col=1)
            n += 1

        # Comparison plot

        # Generating dataframe for comparison plot
        if year_comparison:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        else:
            if error_region_figure(geo_c, default_year, language):
                return error_region_figure(geo_c, default_year, language)
        plot_df_c = (
            plot_df_core_housing_need_by_priority_population_income(geo, language, int(original_year))
            if year_comparison
            else plot_df_core_housing_need_by_priority_population_income(geo_c, language)
        )

        # Generating comparison plot

        n = 0
        for i, c, o in zip(plot_df['Income_Category'].unique(), colors, income_category_override):
            plot_df_frag_c = plot_df_c.loc[plot_df_c['Income_Category'] == i, :]
            fig6.add_trace(go.Bar(
                y=plot_df_frag_c['HH_Category'],
                x=plot_df_frag_c['Percent'],
                name=i,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y}, ' + f'{i} Income - ' + '%{x: .2%}<extra></extra>',
                legendgroup=f'{n}',
                showlegend=False
            ), row=1, col=2)
            n += 1

        # Plot layout settings

        fig6.update_layout(
            title=localization[language][
                      "Percentage of Households in Core Housing Need by Priority Population and Income Category,"] +
                  (f'<br>{geo} 2016 {localization[language]["vs"]} 2021' if year_comparison
                   else f'{geo} {localization[language]["vs"]} {geo_c}'),
            width=900,
            height=500,
            font=dict(size=10),
            legend=dict(font=dict(size=8)),
            legend_traceorder="normal",
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            yaxis=dict(autorange="reversed"),
            barmode='stack',
            plot_bgcolor='#F8F9F9',
            legend_title=localization[language]["Income Category"]
        )
        fig6.update_xaxes(
            title_font=dict(size=10),
            tickfont=dict(size=8),
            fixedrange=True,
            tickformat=',.0%',
            title=localization[language]["% of HH"]
        )
        fig6.update_yaxes(
            fixedrange=True,
            tickfont=dict(size=10)
        )

        return fig6
