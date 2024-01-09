# Percentage of Households in Core Housing Need, by Income Category, 2021
import pandas as pd
import plotly.graph_objects as go
from dash import Output, Input, State, callback
from plotly.subplots import make_subplots

from app_file import cache
from helpers.create_engine import default_year, default_value, income_ownership_year
from helpers.localization import localization
from helpers.style_helper import colors, modebar_color, modebar_activecolor, hh_colors
from helpers.table_helper import query_table, get_language, area_scale_primary_only, area_scale_comparison, \
    error_region_figure

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

columns = ['Percent HH with income 20% or under of AMHI in core housing need',
           'Percent HH with income 21% to 50% of AMHI in core housing need',
           'Percent HH with income 51% to 80% of AMHI in core housing need',
           'Percent HH with income 81% to 120% of AMHI in core housing need',
           'Percent HH with income 121% or more of AMHI in core housing need'
           ]

renter_columns = ["Renter households " + column for column in columns]
owner_columns = ["Owner households " + column for column in columns]


# Plot dataframe generator
def plot_df_core_housing_need_by_income(geo: str, rental: bool, right_side: bool, language, year: int = default_year, ):
    geo, joined_df_filtered = query_table(geo, year, income_ownership_year)

    x_list = []

    # Adds labels to first four groups
    i = 0
    row_labels = ["Very Low Income", "Low Income", "Moderate Income", "Median Income", "High Income"]
    base = [localization[language][label] for label in row_labels]
    for income_category, income_query_string in zip(base, x_columns):
        value = str(joined_df_filtered[income_query_string].tolist()[0])
        # print(i, b,c, value, type(value))
        if i < 4:
            if right_side is False:
                x = localization[language]["{b}<br> (${value})"].format(b=income_category, value=value)
            else:
                x = localization[language][" (${value}) "].format(b=income_category, value=value)
            x_list.append(x)
        else:
            if right_side is False:
                x = localization[language]["{b}<br> (>${value})"].format(b=income_category, value=value)
            else:
                x = localization[language][" (>${value}) "].format(b=income_category, value=value)
            x_list.append(x)
        i += 1

    x_list = [sub.replace('$$', '$') for sub in x_list]
    x_list = [sub.replace('.0', '') for sub in x_list]
    if rental:
        plot_df = pd.DataFrame(
            {"Income_Category": x_list, 'Percent HH': joined_df_filtered[renter_columns].T.iloc[:, 0].tolist()})
    else:
        plot_df = pd.DataFrame(
            {"Income_Category": x_list, 'Percent HH': joined_df_filtered[owner_columns].T.iloc[:, 0].tolist()})

    return plot_df


# Callback logic for the plot update


@callback(
    Output('graph-pg5', 'figure'),
    Input('main-area', 'data'),
    Input('comparison-area', 'data'),
    Input('year-comparison', 'data'),
    Input('area-scale-store', 'data'),
    Input('income-category-affordability-table-pg5', 'selected_columns'),
    State('url', 'search'),
    cache_args_to_ignore=[4]
)
@cache.memoize()
def update_geo_figure(geo: str, geo_c: str, year_comparison: str, scale, refresh, lang_query):
    # Use regex to extract the value of the 'lang' parameter
    language = get_language(lang_query)
    # Single area mode
    # For now, it'll just be owner vs renter no matter what
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
        plot_df = plot_df_core_housing_need_by_income(geo, False, False, language)
        plot_df_c = plot_df_core_housing_need_by_income(geo, True, False, language)

        # Generating plot
        data = []
        data.append(go.Bar(
            y=plot_df['Income_Category'],
            x=plot_df['Percent HH'],
            name=localization[language]["Owner Households"],
            marker_color=colors,
            orientation='h',
            hovertemplate='%{y}, ' + f'HH Type: {localization[language]["Owner Households"]} - ' + '%{x: .2%}<extra></extra>',
            showlegend=False,
        ))
        data.append(go.Bar(
            y=plot_df_c['Income_Category'],
            x=plot_df_c['Percent HH'],
            name=localization[language]["Renter Households"],
            marker_color=hh_colors,
            orientation='h',
            hovertemplate='%{y}, ' + f'HH Type: {localization[language]["Renter Households"]} - ' + '%{x: .2%}<extra></extra>',
            showlegend=False,
        ))
        fig = go.Figure(data=data)
        # Create a separate trace for the custom legend
        legend_trace = go.Bar(
            x=[None],
            y=[None],
            marker_color=colors[1],  # Customize marker color
            # showlegend=True,  # Show legend only for this trace
            name=localization[language]["Owner Households"]   # Set custom legend label
        )
        fig.add_trace(legend_trace)
        legend_trace = go.Bar(
            x=[None],
            y=[None],
            marker_color=hh_colors[1],  # Customize marker color
            showlegend=True,  # Show legend only for this trace
            name=localization[language]["Renter Households"]  # Set custom legend label
        )

        # Add the custom legend trace to the figure
        fig.add_trace(legend_trace)

        # Plot layout settings
        fig.update_layout(
            title=localization[language]['Percentage of Households in Core Housing Need, by Income Category,'] + f"{'<br>' if language == 'en' else ' '}{geo}" +
                  (f' {localization[language]["Renter Households"]} {localization[language]["vs"]} '
                   f'{localization[language]["Owner Households"]}'),
            height=450,
            legend=dict(font=dict(size=9)),
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            plot_bgcolor='#F8F9F9',
            legend_title=localization[language]["Housing Type"]
        )
        fig.update_yaxes(
            title=localization[language]["Income Category"] + '<br>' + localization[language]["(Max. affordable shelter costs)"],
            fixedrange=True,
            autorange="reversed",
            title_font=dict(size=10),
            tickfont=dict(size=10)
        )
        fig.update_xaxes(
            fixedrange=True,
            tickformat=',.0%',
            title=localization[language]["% of HH"],
            title_font=dict(size=10),
            tickfont=dict(size=10)
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
                                f"{compared_year if year_comparison else geo}, "
                                f"{localization[language]['Owner Households']}",
                                f"{original_year if year_comparison else geo_c}, "
                                f"{localization[language]['Renter Households']}",),
                            shared_xaxes=True,)

        # Main Plot

        # Generating dataframe for main plot
        if year_comparison:
            if error_region_figure(geo, int(compared_year), language):
                return error_region_figure(geo, int(compared_year), language)
        else:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        plot_df = (
            plot_df_core_housing_need_by_income(geo, False, False, language, int(compared_year)) if year_comparison else
            plot_df_core_housing_need_by_income(geo, False, False, language)
        )
        plot_df_c = (
            plot_df_core_housing_need_by_income(geo, True, False, language, int(compared_year)) if year_comparison else
            plot_df_core_housing_need_by_income(geo, True, False, language)
        )

        fig.update_yaxes(title=localization[language]["Income Category"] +
                               '<br>' + localization[language]["(Max. affordable shelter costs)"], row=1, col=1)

        # Generating Left Plot
        fig.add_trace(go.Bar(
            y=plot_df['Income_Category'],
            x=plot_df['Percent HH'],
            name=localization[language]["Owner Households"],
            marker_color=colors,
            orientation='h',
            hovertemplate='%{y}, ' + f'HH Type: {localization[language]["Owner Households"]} - ' + '%{x: .2%}<extra></extra>',
            showlegend=False,
        ), row=1, col=1)
        fig.add_trace(go.Bar(
            y=plot_df_c['Income_Category'],
            x=plot_df_c['Percent HH'],
            name=localization[language]["Renter Households"],
            marker_color=hh_colors,
            orientation='h',
            hovertemplate='%{y}, ' + f'HH Type: {localization[language]["Renter Households"]} - ' + '%{x: .2%}<extra></extra>',
            showlegend=False,
        ), row=1, col=1)
        # Create a separate trace for the custom legend
        fig.add_trace(go.Bar(
            x=[None],
            y=[None],
            marker_color=colors[1],  # Customize marker color
            # showlegend=True,  # Show legend only for this trace
            name=localization[language]["Owner Households"]  # Set custom legend label
        ), row=1, col=1)
        fig.add_trace(go.Bar(
            x=[None],
            y=[None],
            marker_color=hh_colors[1],  # Customize marker color
            showlegend=True,  # Show legend only for this trace
            name=localization[language]["Renter Households"]  # Set custom legend label
        ), row=1, col=1)
        # Comparison plot

        # Generating dataframe for owner newplot
        if year_comparison:
            if error_region_figure(geo, default_year, language):
                return error_region_figure(geo, default_year, language)
        else:
            if error_region_figure(geo_c, default_year, language):
                return error_region_figure(geo_c, default_year, language)
        plot_df = (
            plot_df_core_housing_need_by_income(geo, False, True, language) if year_comparison else
            plot_df_core_housing_need_by_income(geo_c, False, True, language)
        )
        plot_df_c = (
            plot_df_core_housing_need_by_income(geo, True, True, language) if year_comparison else
            plot_df_core_housing_need_by_income(geo_c, True, True, language)
        )

        # Generating Left Plot
        fig.add_trace(go.Bar(
            y=plot_df['Income_Category'],
            x=plot_df['Percent HH'],
            name=localization[language]["Owner Households"],
            marker_color=colors,
            orientation='h',
            hovertemplate='%{y}, ' + f'HH Type: {localization[language]["Owner Households"]} - ' + '%{x: .2%}<extra></extra>',
            showlegend=False,
        ), row=1, col=2)
        fig.add_trace(go.Bar(
            y=plot_df_c['Income_Category'],
            x=plot_df_c['Percent HH'],
            name=localization[language]["Renter Households"],
            marker_color=hh_colors,
            orientation='h',
            hovertemplate='%{y}, ' + f'HH Type: {localization[language]["Renter Households"]} - ' + '%{x: .2%}<extra></extra>',
            showlegend=False,
        ), row=1, col=2)
        # Plot layout settings
        fig.update_layout(
            title=localization[language]['Percentage of Households in Core Housing Need, by Income Category,'] + f"<br>{geo}" +
                  (f' {compared_year} {localization[language]["vs"]} {original_year}' if year_comparison
                   else f" {default_year}"),
            width=900,
            legend=dict(font=dict(size=8)),
            modebar_color=modebar_color,
            modebar_activecolor=modebar_activecolor,
            plot_bgcolor='#F8F9F9',
            legend_title=localization[language]["Housing Type"]
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