# Percentage of Indigenous Households in Core Housing Need, by Income Category, 2021
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Output, Input, State, callback
from plotly.subplots import make_subplots

from app_file import cache
from helpers.create_engine import default_year, default_value, income_indigenous_year
from helpers.localization import localization
from helpers.style_helper import colors, modebar_color, modebar_activecolor
from helpers.table_helper import query_table, get_language, area_scale_primary_only, area_scale_comparison, \
    error_indigenous_figure

x_base_echn = [
    '20% or under of area median household income (AMHI)-Households examined for core housing need',
    '21% to 50% of AMHI-Households examined for core housing need',
    '51% to 80% of AMHI-Households examined for core housing need',
    '81% to 120% of AMHI-Households examined for core housing need',
    '121% or more of AMHI-Households examined for core housing need'
]
x_base_chn = [
    '20% or under of area median household income (AMHI)-Households in core housing need',
    '21% to 50% of AMHI-Households in core housing need',
    '51% to 80% of AMHI-Households in core housing need',
    '81% to 120% of AMHI-Households in core housing need',
    '121% or more of AMHI-Households in core housing need'
]

x_columns = ['Rent 20% of AMHI',
             'Rent 50% of AMHI',
             'Rent 80% of AMHI',
             'Rent 120% of AMHI',
             'Rent 120% of AMHI'
             ]

amhi_range = ['20% or under of AMHI', '21% to 50% of AMHI', '51% to 80% of AMHI', '81% to 120% of AMHI',
              '121% and more of AMHI']

x_base = ['Very Low Income',
          'Low Income',
          'Moderate Income',
          'Median Income',
          'High Income',
          ]

column_format = 'Aboriginal household status-Total - Private households by tenure including presence of mortgage payments and subsidized housing-Households with income '
echn_columns = [column_format + e for e in x_base_echn]
chn_columns = [column_format + c for c in x_base_chn]


# Plot dataframe generator
def plot_df_core_housing_need_by_income(geo, IsComparison, language, year: int = default_year):
    geo, joined_df_filtered = query_table(geo, year, income_indigenous_year)

    x_list = []

    i = 0
    row_labels = ["Very Low Income", "Low Income", "Moderate Income", "Median Income", "High Income"]
    base = [localization[language][label] for label in row_labels]
    for income_category, c in zip(base, x_columns):
        value = str(joined_df_filtered[c].tolist()[0])
        if i < 4:
            if IsComparison != True:
                x = localization[language]["{b}<br> (${value})"].format(b=income_category, value=value)
            else:
                x = localization[language][" (${value}) "].format(b=income_category, value=value)
            x_list.append(x)
        else:
            if IsComparison != True:
                x = localization[language]["{b}<br> (>${value})"].format(b=income_category, value=value)
            else:
                x = localization[language][" (>${value}) "].format(b=income_category, value=value)
            x_list.append(x)
        i += 1

    x_list = [sub.replace('$$', '$') for sub in x_list]
    x_list = [sub.replace('.0', '') for sub in x_list]

    plot_df = pd.DataFrame({
        'Income_Category': x_list,
        'ECHN': joined_df_filtered[echn_columns].T.iloc[:, 0].tolist(),
        'CHN': joined_df_filtered[chn_columns].T.iloc[:, 0].tolist()
    })

    plot_df['Percent HH'] = np.round(plot_df['CHN'] / plot_df['ECHN'], 2)
    plot_df = plot_df.replace([np.inf, -np.inf], 0)
    plot_df = plot_df.fillna(0)
    plot_df = plot_df.drop(columns=['ECHN', 'CHN'])

    return plot_df


# Callback logic for the plot update

@callback(
    Output('graph_ind', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    Input('datatable-interactivity_ind', 'selected_columns'),
    State('url', 'search'),
    cache_args_to_ignore=[4]
)
@cache.memoize()
def update_geo_figure(geo, geo_c, year_comparison, scale, refresh, lang_query):
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
        if error_indigenous_figure(geo, default_year, language):
            return error_indigenous_figure(geo, default_year, language)
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
            title=f'{localization[language]["Percentage of Indigenous Households in Core Housing Need, by Income Category"]}, {default_year}<br>{geo}',
            legend_title="Income",
        )
        fig.update_xaxes(
            fixedrange=True,
            range=[0, 1],
            tickformat=',.0%',
            title=localization[language]["% of Indigenous HH"],
            tickfont=dict(size=10)
        )
        fig.update_yaxes(
            tickfont=dict(size=10),
            fixedrange=True,
            title=f'{localization[language]["Income Category"]}<br>{localization[language]["(Max. affordable shelter costs)"]}'
        )

        return fig

    # Comparison mode
    else:

        # Area Scaling up/down when user clicks area scale button on page 1
        if year_comparison:
            original_year, compared_year = year_comparison.split("-")
            geo = area_scale_primary_only(geo, scale)
        # Area Scaling up/down when user clicks area scale button on page 1
        else:
            geo, geo_c = area_scale_comparison(geo, geo_c, scale)
            original_year, compared_year = default_year, default_year

        # Subplot setting for the comparison mode
        fig = make_subplots(rows=1, cols=2, subplot_titles=(
            f"{geo} {compared_year}" if year_comparison else geo,
            f"{geo} {original_year}" if year_comparison else geo_c),
                            shared_xaxes=True)

        # Main Plot

        # Generating dataframe for main plot
        if year_comparison:
            if error_indigenous_figure(geo, int(compared_year), language):
                return error_indigenous_figure(geo, int(compared_year), language)
        else:
            if error_indigenous_figure(geo, default_year, language):
                return error_indigenous_figure(geo, default_year, language)
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

        fig.update_yaxes(title=f'{localization[language]["Income Category"]}<br>'
                               f'{localization[language]["(Max. affordable shelter costs)"]}', row=1, col=1)

        # Comparison plot

        # Generating dataframe for comparison plot
        if year_comparison:
            if error_indigenous_figure(geo, default_year, language):
                return error_indigenous_figure(geo, default_year, language)
        else:
            if error_indigenous_figure(geo_c, default_year, language):
                return error_indigenous_figure(geo_c, default_year, language)
        plot_df_c = (
            plot_df_core_housing_need_by_income(geo, True, language, int(original_year)) if year_comparison else
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
            title=f'{localization[language]["Percentage of Indigenous Households in Core Housing Need, by Income Category"]}, {default_year}',
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
            title=localization[language]["% of Indigenous HH"],
            title_font=dict(size=10),
            tickfont=dict(size=10)
        )

        return fig