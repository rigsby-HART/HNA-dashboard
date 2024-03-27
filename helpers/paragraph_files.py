import re
from typing import List, Dict

# So I can apply a function to all the string in this file
strings: Dict[str, str] = {}

# Core Housing Need (Page 2)

strings["income-categories-page2"] = 'Income categories are determined by their relationship with each geography’s Area Median Household Income (AMHI). The following table shows the range of household incomes and affordable housing costs that make up each income category, in 2020 dollar values. It also shows what the portion of total households that fall within each category.'
strings["percentage-CHN-by-income-table-page2"] = 'The following chart shows the percentage of households in each income category that are in Core Housing Need (CHN). When there is no bar for an income category, it means that either there are no households in CHN within an income category, or that there are too few households to report. '
strings["percentage-CHN-by-income-graph-page2"] = 'The following chart examines those households in CHN and shows their relative distribution by household size (i.e. the number of individuals in a given household for each household income category. When there is no bar for an income category, it means that either there are no households in CHN within an income category, or that there are too few households to report. '
strings["housing-deficit-page2"] = 'The following table shows the total number of households in CHN by household size and income category, which may be considered as the existing deficit of housing options in the community. '
strings["housing-deficit-bedrooms-page2"] = 'The following table converts the above figures into the total number of homes by number of bedrooms and maximum cost required to satisfy the existing deficit. To learn more about how we converted household size to number of bedrooms, view our unit mix methodology. Due to rounding and data suppression, the CHN totals may not match up with the above table. '
strings["percentage-CHN-by-priority-population-page2"] = 'The following chart compares the rates of CHN across populations that are at high risk of experiencing housing need. The "Community (all HH)" bar represents the rate of CHN for all households in the selected community to act as a point of reference. The population with the greatest rate of CHN is highlighted in dark blue. When there is no bar for a priority population, it means that either there are no households in CHN within that priority population, or that there are too few households to report. '
strings["percentage-CHN-by-pp-income-page2"] = 'The following chart looks at those households in CHN for each priority population and shows their relative distribution by household income category. When there is no bar for a priority population, it means that either there are no households in CHN within that priority population, or that there are too few households to report. '

# Projections (Page 3)

strings["projections-by-income-category-page3"] = 'The following table shows the total number of households in 2021, for each household income category, the projected gain (positive) or loss (negative) of households between 2021 and 2031, and the total projected households in 2031.  '
strings["projections-by-income-category-graph-page3"] = 'The following graph illustrates the above table, displaying the total number of households in 2021, for each income category, with the projected gain of households between 2021 and 2031 stacked on top, and the projected loss of households stacked underneath. '

strings["projections-by-household-size-page3"] = 'The following table shows the total number of households in 2021, for each household size, the projected gain (positive) or loss (negative) of households over the period between 2021 and 2031, and the total projected households in 2031. '
strings["projections-by-household-size-graph-page3"] = 'The following graph illustrates the above table, displaying the total number of households in 2021, for each household size, with the projected gain of households between 2021 and 2031 stacked on top, and the projected loss of households stacked underneath. '

strings["projections-by-hh-size-IC-page3"] = 'The following table shows the projected total number of households in 2031 by household size and income category. '
strings["projections-by-hh-size-IC-warning-page3"] = 'In this table, we project forward using the line of best fit to the **combined** income and household size category. Since the combined categories have unique values, and are also subject to Statistics Canada’s random rounding, the resulting Totals here may not match the Totals when projecting households by either income or household size alone (as done in previous tables above).'
strings["projections-by-hh-size-IC-graph-page3"] = 'The following graph illustrates the above table, displaying the projected total number of households in 2031 by household size and income category. Each bar is broken out by the projected total number of households within each income category. '

strings["projected-hh-delta-page3"] = 'The following table shows the projected gain or loss of households by household size and income. These values represent projections of total households for the period between 2021 and 2031. Please note that gains and losses represent both increases or decreases in population, as well as mobility between income categories and household sizes. For this reason, growth and decline in  the lower incomes may be especially impacted by CERB. '
strings["projections-hh-delta-graph-page3"] = 'The following graph illustrates the above table, displaying the projected gain or loss of households between 2021 and 2031 for each size of household. Each bar is broken out by the projected number of households within each income category. Projected loss of households are stacked underneath. '

strings["bedroom-projections-page3"] = 'The following table shows the projected total number of households in 2031 by bedroom count and income category. '
strings["bedroom-projections-graph-page3"] = 'The following graph illustrates the above table, displaying the projected total number of households in 2031 by household size and bedroom count. Each bar is broken out by the projected number of households within each income category. '

strings["projected-bedroom-hh-delta-page3"] = 'The following table shows the projected gain or loss of households by bedroom count and income. These values represent projections for the period between 2021 and 2031. '
strings["projections-bedroom-hh-delta-graph-page3"] = 'The following graph illustrates the above table, displaying the projected gain or loss of households between 2021 and 2031 for each size of household. Each bar is broken out by the projected number of households within each income category. Projected loss of households are stacked underneath. '

strings["municipal-description-page3"] = 'Comparing a local community’s projected rate of growth to that of the region provides insight on the community’s alignment to broader growth patterns. There are numerous potential causes for discrepancies, which are further discussed in the project methods. '

strings["municipal-vs-regional-income-page3"] = 'The following table illustrates the projected total household growth rates between 2021 and 2031 in the community and its surrounding region for each income category. '
strings["municipal-vs-regional-income-graph-page3"] = 'The following graph illustrates the above table, displaying the projected household growth rates between 2021 and 2031 in the community and its surrounding region for each income category. '

strings["municipal-vs-regional-hh-page3"] = 'The following table illustrates the projected household growth rates between 2021 and 2031 in the community and its surrounding region for each household size. '
strings["municipal-vs-regional-hh-graph-page3"] = 'The following graph illustrates the above table, displaying the projected household growth rates between 2021 and 2031 in the community and its surrounding region for each income category. '

# Indigenous CHN (page4)

strings["income-categories-page4"] = 'The following table shows the range of Indigenous household incomes and affordable shelter costs for each income category, in 2020 dollar values. It also shows the portion of total households that fall within each category. '
# strings["percentage-CHN-by-income-table-page4"]
strings["percentage-CHN-by-income-graph-page4"] = 'The following chart shows the percentage of Indigenous households in each income category that are in Core Housing Need (CHN). When there is no bar for an income category, it means that either there are no households in CHN within an income category, or that there are too few households to report. '
strings["percentage-CHN-by-IC-HH-size-page4"] = 'The following graph looks at those Indigenous households in CHN and shows their relative distribution by household size (i.e. the number of individuals in a given household) for each household income category. Where there are no reported households in CHN, there are too few households to report. '
strings["housing-deficit-page4"] = 'The following table shows the total number of Indigenous households in CHN by household size and income category, which may be considered as the existing deficit of housing options in the community. Where there are no reported households in CHN, there are none, or too few households to report. '

# Renter vs Owners (page5)

strings["income-categories-page5"] = 'Income categories are determined by their relationship with each geography’s Area Median Household Income (AMHI). The following table shows the range of household incomes and affordable housing costs that make up each income category, in 2020 dollar values. It also shows the portion of total households that fall within each category for both homeowners and renters. '
strings["percentage-CHN-by-income-graph-page5"] = 'The following chart shows the percentage of owner and renter households in each income category that are in Core Housing Need (CHN). When there is no bar for an income category, it means that either there are no households in CHN within an income category, or that there are too few households to report. '

strings["percentage-CHN-by-IC-HH-size-page5"] = 'The following chart looks at those owner and renter households in CHN and their relative distribution for each household income category. When there is no bar for an income category, it means that either there are no households in CHN within an income category, or that there are too few households to report. '

strings["housing-deficit-page5"] = 'The following table shows the total number of owner and renter households in CHN by income category, which may be considered as the existing deficit of housing options in the community. '

# Subsidized half (unused for now)
strings["income-categories-subsidized-page5"] = 'The following table shows the range of household incomes and affordable shelter costs for each income category, in 2020 dollar values, as well compares subsidized and unsubsidized renters for what percentage of the total number of households falls within each category. '
strings["percentage-CHN-by-income-graph-subsidized-page5"] = 'The following chart shows the percentage of subsidized and unsubsidized renter households in each income category that are in CHN. When there is no bar for an income category, it means that either there are no households in CHN within an income category, or that there are too few households to report. '

strings["percentage-CHN-by-IC-HH-size-subsidized-page5"] = 'The following chart looks at those subsidized and unsubsidized renter households in CHN and their relative distribution within household income category. When there is no bar for an income category, it means that either there are no households in Core Housing Need within an income category, or that there are too few households to report. '

strings["housing-deficit-subsidized-page5"] = 'The following table shows the total number of subsidized and unsubsidized renter households in CHN by income category, which may be considered as the existing deficit of housing options in the community. '

# Transportation Distance (page6)
strings["table-description-page6"] = 'The following table shows the total number of subsidized and unsubsidized renter households in CHN by income category, which may be considered as the existing deficit of housing options in the community. '


# Link map
links: Dict[str, str] = {
    'too few households to report': 'https://hart.ubc.ca/housing-glossary/#data-suppression',
    'Core Housing Need (CHN)': 'https://hart.ubc.ca/housing-glossary/#chn',
    'Area Median Household Income (AMHI)': 'https://hart.ubc.ca/housing-glossary/#amhi',
    'the project methods': 'https://hart.ubc.ca/hna-methodology/',
    'impacted by CERB': 'https://hart.ubc.ca/understanding-2021-core-housing-need-data/',
    'high risk of experiencing housing need': 'https://hart.ubc.ca/housing-glossary/#priority-populations',
    'unit mix methodology': 'https://hart.ubc.ca/HNA-Methodology.pdf#page=27',
}
# These are the quirky ones im gonna regex to do
re_links: Dict[str, str] = {
    r' (subsidized) ': 'https://hart.ubc.ca/housing-glossary/#subsidized-housing',
    r' (CHN) ': 'https://hart.ubc.ca/housing-glossary/#chn',
}

key: str
string: str
# Insert all paragraph formatting
for key, string in zip(strings.keys(),strings.values()):

    # Add all links here
    for text, link in zip(links.keys(),links.values()):
        string = string.replace(text, f'[{text}]({link})')
    for pattern, link in zip(re_links.keys(), re_links.values()):
        string = re.sub(pattern, fr' [\1]({link}) ', string)

    # Make it H6
    string = "###### " + string
    strings[key] = string
