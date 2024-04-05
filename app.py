# Import necessary libraries

import dash
from dash import html, dcc

import flask
from pathlib import Path
from flask import send_from_directory

# Connect to main app_file.py file
from app_file import app
from helpers.table_helper import storage_variables

# Define the index page layout

app.layout = html.Div(dash.page_container)
server = app.server

# Elearning content
HERE = Path(__file__).parent


# Serve all files in the 'static' directory
@app.server.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port="8000")
