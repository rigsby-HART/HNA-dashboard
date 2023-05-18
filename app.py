# Import necessary libraries 
from dash import html, dcc
from dash.dependencies import Input, Output

# Connect to main app_file.py file
from app_file import app

# Connect to app pages
from pages import page1, page2, page3, page4

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=[]), 
])
server = app.server

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout
    if pathname == '/page2':
        return page2.layout
    if pathname == '/page3':
        return page3.layout
    if pathname == '/page4':
        return page4.layout
    else: # if redirected to unknown link
        return "404 Page Error! Please choose a link" 

# Run the app on localhost:8050
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')