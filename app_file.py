
# Defining the Dash App and it's attributes

import dash
import dash_bootstrap_components as dbc
import diskcache
from dash import DiskcacheManager
# cache = diskcache.Cache("./cache")
# background_callback_manager = DiskcacheManager(
#     cache, cache_by=[], expire=300
# )
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True,
                # background_callback_manager = background_callback_manager,
                # use_pages=True
                )