# Income Categories and Affordable Shelter Costs, 2021
import pandas as pd
import plotly.graph_objects as go
from dash import Output, Input, State, callback
from plotly.subplots import make_subplots

from app_file import cache
from helpers.create_engine import default_year, default_value, partner_table
from helpers.localization import localization
from helpers.style_helper import modebar_color, modebar_activecolor, colors
from helpers.table_helper import query_table, get_language, area_scale_primary_only, area_scale_comparison, \
    error_region_figure

# Base is what we actually label the groups as, columns is what the column the data lays in is called in the hart.db
x_base = ['Very Low Income',
          'Low Income',
          'Moderate Income',
          'Median Income',
          'High Income',
          ]

x_columns = ['Rent 20% of AMHI',
             'Rent 50% of AMHI',
             'Rent 80% of AMHI',
             'Rent 120% of AMHI',
             'Rent 120% of AMHI'
             ]

hh_p_num_list = [1, 2, 3, 4, '5 or more']

amhi_range = ['20% or under of AMHI', '21% to 50% of AMHI', '51% to 80% of AMHI', '81% to 120% of AMHI',
              '121% and more of AMHI']

income_ct = [x + f" ({a})" for x, a in zip(x_base, amhi_range)]

columns = ['Percent HH with income 20% or under of AMHI in core housing need',
           'Percent HH with income 21% to 50% of AMHI in core housing need',
           'Percent HH with income 51% to 80% of AMHI in core housing need',
           'Percent HH with income 81% to 120% of AMHI in core housing need',
           'Percent HH with income 121% or more of AMHI in core housing need'
           ]


# Percentage of Households in Core Housing Need, by Income Category, 2021

# Plot dataframe generator
def plot_df_core_housing_need_by_income(geo: str, is_second: bool, language, year: int = default_year, ):
    geo, joined_df_filtered = query_table(geo, year, partner_table)

    x_list = []

    # Adds labels to first four groups
    i = 0
    row_labels = ["Very Low Income", "Low Income", "Moderate Income", "Median Income", "High Income"]
    base = [localization[language][label] for label in row_labels]
    for income_category, income_query_string in zip(base, x_columns):
        value = str(joined_df_filtered[income_query_string].tolist()[0])
        # print(i, b,c, value, type(value))
        if i < 4:
            if is_second is False:
                x = localization[language]["{b}<br> (${value})"].format(b=income_category, value=value)
                # print(x)
            else:
                x = localization[language][" (${value}) "].format(b=income_category, value=value)
            x_list.append(x)
        else:
            if is_second is False:
                x = localization[language]["{b}<br> (>${value})"].format(b=income_category, value=value)
            else:
                x = localization[language][" (>${value}) "].format(b=income_category, value=value)
            x_list.append(x)
        i += 1

    x_list = [sub.replace('$$', '$') for sub in x_list]
    x_list = [sub.replace('.0', '') for sub in x_list]
    plot_df = pd.DataFrame({"Income_Category": x_list, 'Percent HH': joined_df_filtered[columns].T.iloc[:, 0].tolist()})

    return plot_df


# Callback logic for the plot update

@callback(
    Output('graph', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    State('url', 'search'),
    Input('income-category-affordability-table', 'selected_columns'),
    cache_args_to_ignore=[-1]
)
@cache.memoize()
def update_geo_figure(geo: str, geo_c: str, year_comparison: str, scale, lang_query, refresh):
    # Use regex to extract the value of the 'lang' parameter
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
        plot_df = plot_df_core_housing_need_by_income(geo, False, language)

        # Generating plot
        fig = go.Figure()
        for i, c in zip(plot_df['Income_Category'], colors):
            plot_df_frag = plot_df.loc[plot_df['Income_Category'] == i, :]
            fig.add_trace(go.Bar(
                y=plot_df_frag['Income_Category'],
                x=plot_df_frag['Percent HH'],
                name=i,
                marker_color=c,
                orientation='h',
                hovertemplate='%{y} - ' + '%{x: .2%}<extra></extra>'
            ))

        # Plot layout settings
        fig.update_layout(
            width=900,
            showlegend=False,
            legend=dict(font=dict(size=9)),
            yaxis=dict(autorange="reversed"),
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            plot_bgcolor='#F8F9F9',
            title=localization[language][
                      'Percentage of Households in Core Housing Need, by Income Category,'] + f" {default_year}<br>{geo}",
            legend_title=localization[language]["Income"],
        )
        fig.update_xaxes(
            fixedrange=True,
            range=[0, 1],
            tickformat=',.0%',
            title=localization[language]["% of HH"],
            tickfont=dict(size=10)
        )
        fig.update_yaxes(
            tickfont=dict(size=10),
            fixedrange=True,
            title=localization[language]["Income Category"] + '<br>' + localization[language][
                "(Max. affordable shelter costs)"]
        )

        return fig

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
        fig = make_subplots(rows=1, cols=2,
                            subplot_titles=(
                                f"{geo + ' ' + compared_year if year_comparison else geo}",
                                f"{geo + ' ' + str(original_year) if year_comparison else geo_c}"),
                            shared_xaxes=True)

        # Main Plot

        # Generating dataframe for main plot
        if year_comparison:
            if error_region_figure(geo, int(compared_year), language):
                return error_region_figure(geo, int(compared_year), language)
        else:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        plot_df = (
            plot_df_core_housing_need_by_income(geo, False, language, int(compared_year)) if year_comparison else
            plot_df_core_housing_need_by_income(geo, False, language)
        )

        # Generating main plot
        n = 0
        for i, c, b in zip(plot_df['Income_Category'], colors, x_base):
            plot_df_frag = plot_df.loc[plot_df['Income_Category'] == i, :]
            fig.add_trace(go.Bar(
                y=plot_df_frag['Income_Category'],
                x=plot_df_frag['Percent HH'],
                name=b.replace(" Income", ""),
                marker_color=c,
                orientation='h',
                hovertemplate='%{y} - ' + '%{x: .2%}<extra></extra>',
                legendgroup=f'{n}'
            ), row=1, col=1)
            n += 1

        fig.update_yaxes(title=localization[language]["Income Category"] +
                               '<br>' + localization[language]["(Max. affordable shelter costs)"], row=1, col=1)

        # Comparison plot

        # Generating dataframe for comparison plot
        if year_comparison:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        else:
            if error_region_figure(geo_c, default_year, language):
                return error_region_figure(geo_c, default_year, language)
        plot_df_c = (
            plot_df_core_housing_need_by_income(geo, True, language) if year_comparison else
            plot_df_core_housing_need_by_income(geo_c, True, language)
        )

        # Generating comparison plot
        n = 0
        for i, c, b in zip(plot_df_c['Income_Category'], colors, x_base):
            plot_df_frag_c = plot_df_c.loc[plot_df_c['Income_Category'] == i, :]
            fig.add_trace(go.Bar(
                y=plot_df_frag_c['Income_Category'],
                x=plot_df_frag_c['Percent HH'],
                name=b.replace(" Income", ""),
                marker_color=c,
                orientation='h',
                hovertemplate='%{y} - ' + '%{x: .2%}<extra></extra>',
                legendgroup=f'{n}',
                showlegend=False,
            ), row=1, col=2)
            n += 1

        # Plot layout settings
        fig.update_layout(
            title=localization[language][
                      'Percentage of Households in Core Housing Need, by Income Category,'] + f" {geo}" +
                  (f' {compared_year} {localization[language]["vs"]} {original_year}' if year_comparison
                   else f" {default_year}"),
            showlegend=False,
            width=900,
            legend=dict(font=dict(size=8)),
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            plot_bgcolor='#F8F9F9',
            legend_title="Income"
        )
        fig.update_yaxes(
            fixedrange=True,
            autorange="reversed",
            title_font=dict(size=10),
            tickfont=dict(size=10)
        )
        fig.update_xaxes(
            fixedrange=True,
            range=[0, 1],
            tickformat=',.0%',
            title=localization[language]["% of HH"],
            title_font=dict(size=10),
            tickfont=dict(size=10)
        )

        return fig
