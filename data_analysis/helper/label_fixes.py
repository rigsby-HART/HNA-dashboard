# 2016 data and 2021 data are labelled differently.  Hopefully I can solve that issue here
def translate(year, phrase):
    if year == 2021:
        return phrase
    if year == 2016:
        # Throw exception if not in dict
        return map_2016_2021[phrase]


map_2016_2021 = {
    'Total \x96 Private households by household income proportion to AMHI_1': 'Total - Private households by Household income as a proportion to Area Median Household Income (AMHI)_1',
    'Households with income 20% or under of area median household income (AMHI)': 'Households with household income 20% or under of area median household income (AMHI)',
    'Households with income 21% to 50% of AMHI': 'Households with household income 21% to 50% of AMHI',
    'Households with income 51% to 80% of AMHI': 'Households with household income 51% to 80% of AMHI',
    'Households with income 81% to 120% of AMHI': 'Households with household income 81% to 120% of AMHI',
    'Households with income 121% or more of AMHI': 'Households with household income 121% and over of AMHI',
    'Total - Private households by core housing need status': 'Total - Private Households by core housing need status',
    'Households examined for core housing need': 'Households examined for core housing need status',
    'Households in core housing need': 'Households in core housing need status',
    'Subsidized housing': 'Subsidized housing',
    'Not subsidized housing': 'Not subsidized housing',
}