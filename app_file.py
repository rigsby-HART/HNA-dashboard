# Defining the Dash App and it's attributes
import dash
import dash_bootstrap_components as dbc
import diskcache
import sys
from os import path as path




# Diskcache for non-production apps when developing locally

# Disable cache if we're doing local development.  This creates a class that mimics our cache decorator
# However, this one doesn't do anything to memoize
if path.basename(sys.argv[0]) == "app.py":
    class Cache:
        def memoize(self, *args):
            return lambda func: func
    cache = Cache()
# In prod, the server is hosted by a Gunicorn WSGI which means the originally called python file is no longer our app.py
else:
    cache = diskcache.Cache("./cache")


app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP], 
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                # background_callback_manager=background_callback_manager,
                use_pages=True
                )
