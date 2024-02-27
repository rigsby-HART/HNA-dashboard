import dash_bootstrap_components as dbc
from dash import dcc, html

disclaimer = dbc.Modal(
    children=[
        dbc.ModalHeader(
            dcc.Markdown(
                "### Projection Disclaimer"
            )),
        dbc.ModalBody(
            [
                html.H6('Making Household Projections is not a precise science. Many organizations and government '
                        'bodies do some kind of population projections (see Statistics Canada) using a number of '
                        'variables ranging from fertility, age distribution, migration patterns, employment, '
                        'and even building permits.  '),
                html.H6(['HART projections are done assuming "Business as Usual", which means that we have not '
                         'accounted for any changes in the policy or population landscape (let alone the dramatic '
                         'shifts since 2021). Our projections estimate the increase or decrease in the total number of '
                         'households (',
                         html.U([html.B('not ', style={"font-weight": "bold"}), 'housing need']),
                         ') using a “line of best fit” between 2006, 2016, '
                         'and 2021 census. To learn more about our projections, please see our ',
                         html.A('methodology here.',
                                href='https://hart.ubc.ca/HNA-Methodology#page=9',
                                target='_blank')
                         ]),
                html.H6(['These projections are simple guides to give an idea'
                         ' of how a community might grow or decline if ',
                         html.I('past trends continue into the future'),
                         ', not definitive assessments on which targets should be based.'])
            ]
        ),
    ],
    id="projection-modal",
    is_open=True,
    size="lg"
)
