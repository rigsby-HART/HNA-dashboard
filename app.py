# Import necessary libraries
import dash
from dash import html, dcc

# Connect to main app_file.py file
from app_file import app
from helpers.table_helper import storage_variables

# Define the index page layout

app.layout = html.Div(
    storage_variables() + [
        dcc.Location(id='url', refresh=False),
        dash.page_container
    ])
server = app.server

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port="8000")
