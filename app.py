import dash
from dash import dcc, html

app = dash.Dash(__name__)

app.layout = html.Div(style={'borderTop': '5px solid #728896',
                             'borderBottom': '5px solid #728896'},
    children=[
    
        html.Img(src=app.get_asset_url('logo_white.png'), className = 'center'),

   
])

if __name__ == '__main__':
   app.run_server(debug=False)