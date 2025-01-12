#---------------------------------------------------------------------------------------------
# Dependencies
#---------------------------------------------------------------------------------------------

import dash
from dash import dcc, html, dash_table, ctx, callback
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc

import base64
import io

import pandas as pd
import dynamicsector as ds

#---------------------------------------------------------------------------------------------
# App
#---------------------------------------------------------------------------------------------

# Register app
app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)

# Define wrapper
app.layout = html.Div(style={'borderTop': '5px solid #728896',
                                  'borderBottom': '5px solid #728896',
                                  'background-image': 'url("/assets/background.png")',
                                  'background-size': 'cover',
                                  'background-repeat': 'no-repeat',
                                  'background-position': 'center',
                                  'height': 'auto'},
            children=[
                dbc.Row([
                    dbc.Col([
                        html.Div([html.Img(src=app.get_asset_url('logo_white.png'), 
                                            style={'height': '7vh',
                                                  'display':'block',
                                                  'margin-top':'7px',
                                                  'margin-left':'15px',
                                                  'margin-bottom':'7px'})
                                        ], className='header')
                                    ]),
                    
                    dbc.Col([
                        dbc.Row([
                            dcc.Upload([html.A('System Data')], 
                                    id='upload_system_data',
                                    multiple=False,
                                    style={'display': 'block',
                                           'margin': 'auto',
                                           'width': 'auto',
                                           'height': '3.5vh',
                                           'fontSize': '1.75vh',
                                           'borderColor': 'rgba(100,100,100,0.8)',
                                           'borderWidth': '1px',
                                           'borderStyle': 'dashed',
                                           'borderRadius': '5px',
                                           'color': 'rgba(150,150,150,0.8)',
                                           'textAlign': 'center',
                                           'background-color':'rgba(0,0,0,0.75)',
                                           'padding':'4px'}),
                            dcc.Store(id='system_data', storage_type='session', data={})
                                ], style={'padding':'10px'}),
                        dbc.Row(id='stored_system_data')
                        ]),
                    
                    dbc.Col([
                        dbc.Row([
                            dcc.Upload([html.A('Sector Map')],
                                    id='upload_sector_map',
                                    multiple=False, 
                                    style={'display': 'block',
                                           'margin': 'auto',
                                           'width': 'auto',
                                           'height': '3.5vh',
                                           'fontSize': '1.75vh',
                                           'borderColor': 'rgba(100,100,100,0.8)',
                                           'borderWidth': '1px',
                                           'borderStyle': 'dashed',
                                           'borderRadius': '5px',
                                           'color': 'rgba(150,150,150,0.8)',
                                           'textAlign': 'center',
                                           'background-color':'rgba(0,0,0,0.75)',
                                           'padding':'4px'}),
                            dcc.Store(id='sector_map', storage_type='session', data={})
                                ], style={'padding':'10px'}),
                        dbc.Row(id='stored_sector_map')
                        ]),            
                                ], style={'background-color':'rgba(0,0,0,0.75)',
                                          'borderBottom': '3px solid #728896',
                                          'padding': '5px 0px 5px 0px'}),   
                
                html.Div(id='output_display',
                    style={'height':'76vh',
                           'width':'auto',
                           'padding':'5px 10px 5px 10px'}),
                
                dbc.Row([
                    html.P(["The ",
                            html.B("DynamicSector"),
                            " dashboard is intended to support science fiction or otherwise interstellar roleplaying games. It takes topological 'network' data (xls, csv, and pkl), converts the data into a NetworkX object, and visualizes the results as a 3D 'star map'. The resulting visualizations are navigable using a mouse and keyboard and includes tooltips describing each of the planets and stars (if the descriptions are provided). ",
                            html.B(["Instructions on how to properly format the data are provided at ",
                                    html.A("thomasbryansmith/DynamicSector",
                                        href='https://github.com/thomasbryansmith/DynamicSector'),
                                    "."])],
                        style={'textAlign': 'center',
                               'color': 'rgba(255,255,255,0.8)',
                               'font-family': 'monospace',
                               'font-size': '0.85vw',
                               'borderRadius': '5px',
                               'background-color': 'rgba(0,0,0,0.5)',
                               'padding': '7px'})
                        ], style={'padding': '5px 30px 0px 30px'})   
                ])

#---------------------------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------------------------
     
def read_and_check_upload(contents, filename):
    content_string = contents.split(',')[1]
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'pkl' in filename:
            df = pd.read_pickle(io.BytesIO(decoded))
    except Exception:
        return html.P('ERROR',
                    style={'color':'rgba(255,74,74,0.85)',
                           'font-size': '0.8vw',
                           'text-align': 'center'})
    children = html.P([html.B('Stored: '), filename],
                      style={'color': 'rgba(255,255,255,0.7)',
                             'font-size': '0.8vw',
                             'text-align': 'center'})
    return children, df.to_json()

#---------------------------------------------------------------------------------------------
# Callbacks
#---------------------------------------------------------------------------------------------

@app.callback(
    Output('system_data', 'data'),
    Input('upload_system_data', 'contents'),
    State('upload_system_data', 'filename'))
def system_data_store(contents, filename):
    if contents is not None:
        data = read_and_check_upload(contents, filename)[1]
        return data
    
@app.callback(
    Output('sector_map', 'data'),
    Input('upload_sector_map', 'contents'),
    State('upload_sector_map', 'filename'))
def sector_map_store(contents, filename):
    if contents is not None:
        data = read_and_check_upload(contents, filename)[1]
        return data
    
@app.callback(
    Output('stored_system_data', 'children'),
    Input('upload_system_data', 'contents'),
    State('upload_system_data', 'filename'))
def stored_system_data(contents, filename):
    if contents is not None:
        return read_and_check_upload(contents, filename)[0]
    
@app.callback(
    Output('stored_sector_map', 'children'),
    Input('upload_sector_map', 'contents'),
    State('upload_sector_map', 'filename'))
def stored_sector_map(contents, filename):
    if contents is not None:
        return read_and_check_upload(contents, filename)[0]
    
@app.callback(
    Output('output_display', 'children'),
    [Input('system_data', 'data'),
     Input('sector_map', 'data')],
    prevent_initial_call=True
)
def update(system_data, sector_map):
    if system_data and sector_map is not None:
        return dcc.Graph(figure=ds.dynamic_sector_3d(pd.read_json(io.StringIO(system_data)), 
                                                     pd.read_json(io.StringIO(sector_map))),
                         config={'displayModeBar': False,
                                 'scrollZoom': True,
                                 'responsive': True},
                         style={'backgroundColor':'rgba(0,0,0,0.80)',
                                'height':'75vh'})

#---------------------------------------------------------------------------------------------
# Compile App
#---------------------------------------------------------------------------------------------

server = app.server

if __name__ == '__main__':
    app.run_server(debug=False)