# Percentage of Households in Core Housing Need, by Income Category and HH Size, 2021

import pandas as pd
import plotly.graph_objects as go
from dash import Output, Input, State, callback
from plotly.subplots import make_subplots

from app_file import cache
from helpers.create_engine import default_year, default_value, income_ownership_year
from helpers.localization import localization
from helpers.style_helper import modebar_color, modebar_activecolor, hh_colors, colors, owner_blue, renter_green
from helpers.table_helper import query_table, get_language, area_scale_primary_only, area_scale_comparison, \
    error_region_figure

x_columns = ['Rent 20% of AMHI',
             'Rent 50% of AMHI',
             'Rent 80% of AMHI',
             'Rent 120% of AMHI',
             'Rent 120% of AMHI'
             ]

x_base = ['Very Low Income',
          'Low Income',
          'Moderate Income',
          'Median Income',
          'High Income',
          ]

hh_type_colors = [owner_blue, renter_green]

# Plot dataframe generator
def plot_df_core_housing_need_by_amhi(geo: str, IsComparison: bool, language: str, year: int = default_year):
    geo, joined_df_filtered = query_table(geo, year, income_ownership_year)

    x_list = []

    i = 0
    row_labels = ["Very Low Income", "Low Income", "Moderate Income", "Median Income", "High Income"]
    base = [localization[language][label] for label in row_labels]
    for b, c in zip(base, x_columns):
        value = str(joined_df_filtered[c].tolist()[0])
        if i < 4:
            if IsComparison is False:
                x = localization[language]["{b}<br> (${value})"].format(b=b, value=value)
            else:
                x = localization[language][" (${value}) "].format(b=b, value=value)
            x_list.append(x)
        else:
            if IsComparison is False:
                x = localization[language]["{b}<br> (>${value})"].format(b=b, value=value)
            else:
                x = localization[language][" (>${value}) "].format(b=b, value=value)
            x_list.append(x)
        i += 1

    income_lv_list = ['20% or under', '21% to 50%', '51% to 80%', '81% to 120%', '121% or more']
    x_list = [sub.replace('$$', '$') for sub in x_list]
    x_list = [sub.replace('.0', '') for sub in x_list]

    h_hold_value = []
    hh_p_num_list_full = []
    hh_column_name = ['owner', 'renter']
    hh_labels = [localization[language][hh] for hh in ["Owner Households", "Renter Households"]]
    for h, hc in zip(hh_column_name, hh_labels):
        for i in income_lv_list:
            column = f'Per HH with income {i} of AMHI in core housing need that are {h} HH'
            h_hold_value.append(joined_df_filtered[column].tolist()[0])
            hh_p_num_list_full.append(hc)

    plot_df = pd.DataFrame({'HH_Size': hh_p_num_list_full, 'Income_Category': x_list * 2, 'Percent': h_hold_value})

    return plot_df


# Callback logic for the plot update

@callback(
    Output('graph2-pg5', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    Input('income-category-affordability-table-pg5', 'selected_columns'),
    State('url', 'search'),
    cache_args_to_ignore=[4]
)
@cache.memoize()
def update_geo_figure2(geo, geo_c, year_comparison: str, scale, refresh, lang_query):
    # Single area mode
    language = get_language(lang_query)
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
        plot_df = plot_df_core_housing_need_by_amhi(geo, False, language)

        # Generating plot
        fig2 = go.Figure()

        for h, c in zip(plot_df['HH_Size'].unique(), hh_type_colors):
            plot_df_frag = plot_df.loc[plot_df['HH_Size'] == h, :]
            fig2.add_trace(go.Bar(
                y=plot_df_frag['Income_Category'],
                x=plot_df_frag['Percent'],
                name=h,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y}, ' + f'HH Type: {h} - ' + '%{x: .2%}<extra></extra>',
            ))

        # Plot layout settings
        fig2.update_layout(
            legend_traceorder='normal',
            width=900,
            legend=dict(font=dict(size=9)),
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            yaxis=dict(autorange="reversed"),
            barmode='stack',
            plot_bgcolor='#F8F9F9',
            title=localization[language][
                      'Percentage of Households in Core Housing Need, by Income Category and HH Type,'] + f'<br>{default_year} {geo}',
            legend_title=localization[language]["Housing Type"]
        )
        fig2.update_yaxes(
            tickfont=dict(size=10),
            fixedrange=True,
            title=localization[language]["Income Category"] + '<br>' + localization[language][
                "(Max. affordable shelter costs)"]
        )
        fig2.update_xaxes(
            fixedrange=True,
            tickformat=',.0%',
            title=localization[language]["% of HH"],
            tickfont=dict(size=10)
        )

        return fig2


    # Comparison mode
    else:
        if year_comparison:
            geo = area_scale_primary_only(geo, scale)
            original_year, compared_year = year_comparison.split("-")
        # Area Scaling up/down when user clicks area scale button on page 1
        else:
            geo, geo_c = area_scale_comparison(geo, geo_c, scale)
            original_year, compared_year = default_year, default_year

        # Subplot setting for the comparison mode
        fig2 = make_subplots(rows=1, cols=2,
                             subplot_titles=(
                                 f"{geo + ' ' + compared_year if year_comparison else geo}",
                                 f"{geo + ' ' + original_year if year_comparison else geo_c}"),
                             shared_xaxes=True)

        # Main Plot

        if year_comparison:
            if error_region_figure(geo, int(compared_year), language):
                return error_region_figure(geo, int(compared_year), language)
        else:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        # Generating dataframe for main plot
        plot_df = (
            plot_df_core_housing_need_by_amhi(geo, False, language, int(compared_year)) if year_comparison else
            plot_df_core_housing_need_by_amhi(geo, False, language)
        )

        # Generating main plot
        n = 0
        for h, c in zip(plot_df['HH_Size'].unique(), hh_type_colors):
            plot_df_frag = plot_df.loc[plot_df['HH_Size'] == h, :]
            fig2.add_trace(go.Bar(
                y=plot_df_frag['Income_Category'],
                x=plot_df_frag['Percent'],
                name=h,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y}, ' + f'HH Size: {h} - ' + '%{x: .2%}<extra></extra>',
                legendgroup=f'{n}'
            ), row=1, col=1)
            n += 1

        fig2.update_yaxes(title=localization[language]["Income Category"] +
                                '<br>' + localization[language]["(Max. affordable shelter costs)"], row=1, col=1)

        # Comparison plot

        if year_comparison:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        else:
            if error_region_figure(geo_c, default_year, language):
                return error_region_figure(geo_c, default_year, language)
        # Generating dataframe for comparison plot
        plot_df_c = (
            plot_df_core_housing_need_by_amhi(geo, True, language) if year_comparison else
            plot_df_core_housing_need_by_amhi(geo_c, True, language)
        )

        # Generating comparison plot
        n = 0
        for h, c in zip(plot_df_c['HH_Size'].unique(), hh_type_colors):
            plot_df_frag_c = plot_df_c.loc[plot_df_c['HH_Size'] == h, :]
            fig2.add_trace(go.Bar(
                y=plot_df_frag_c['Income_Category'],
                x=plot_df_frag_c['Percent'],
                name=h,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y}, ' + f'HH Size: {h} - ' + '%{x: .2%}<extra></extra>',
                legendgroup=f'{n}',
                showlegend=False,
            ), row=1, col=2)
            n += 1

        # Plot layout settings
        fig2.update_layout(
            font=dict(size=10),
            title=localization[language][
                      'Percentage of Households in Core Housing Need, by Income Category and HH Type,'] + f" {geo}" +
                  (f' {compared_year} {localization[language]["vs"]} {original_year}' if year_comparison
                   else f" {default_year}"),
            legend_traceorder='normal',
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            barmode='stack',
            plot_bgcolor='#F8F9F9',
            legend_title=localization[language]["Housing Type"],
            legend=dict(font=dict(size=8))
        )
        fig2.update_yaxes(
            title_font=dict(size=10),
            tickfont=dict(size=10),
            fixedrange=True,
            autorange="reversed"
        )
        fig2.update_xaxes(
            title_font=dict(size=10),
            fixedrange=True,
            tickformat=',.0%',
            title=localization[language]["% of HH"],
            tickfont=dict(size=10)
        )

        return fig2
