"""
This app creates a simple sidebar layout using inline style arguments and the
dbc.Nav component.

dcc.Location is used to track the current location, and a callback uses the
current location to render the appropriate page content. The active prop of
each NavLink is set automatically according to the current pathname. To use
this feature you must install dash-bootstrap-components >= 0.11.0.

For more details on building multi-page Dash applications, check out the Dash
documentation: https://dash.plot.ly/urls
"""
import dash
from dash import html, dcc, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Read the CSV file into a DataFrame
df = pd.read_csv('Data\\merged_data.csv')

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "10rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("PMIM", className="display-4"),
        html.Hr(),
        html.P(
            "Fully interactive dashboard", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

dropdown_1 = dcc.Dropdown(id = 'dropdown-1',
                        options= ['volt', 'rotate', 'pressure', 'vibration'],
                        value = 'volt', clearable= False)
dropdown_2 = dcc.Dropdown(id = 'dropdown-2',
                        options= ['errorID', 'failure'],
                        value = 'errorID', clearable= False)
inputNum = dcc.Input(id= 'machine_id', type= "number", value= 1, min= 1, max = 100)


    

modal1 = html.Div(
    [
        dbc.Button("Open report", id="open-fs-1"),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Failure Components List")),
                dbc.ModalBody(html.Div([dbc.Row(id = "modal_body_1"), dbc.Row(dcc.Graph(id= 'graph2'))]) ),
            ],
            id="modal-fs-1",
            fullscreen=True,
        ),
    ]
)

modal2 = html.Div(
    [
        dbc.Button("Open report", id="open-fs-2"),
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Failure Components List")),
                dbc.ModalBody(html.Div([dbc.Row(id = "modal_body_2"), dbc.Row(dcc.Graph(id= 'graph3'))]) ),
            ],
            id="modal-fs-2",
            fullscreen=True,
        ),
    ]
)



# generic card
card1 = dbc.Card(
    [
        dbc.CardHeader("Error ID"),
        dbc.CardBody(
            [
                html.H2("Card title", className="card-title", id= "error_title"),
                modal2
            ]
        ),
    ], color="danger", inverse=True,
    className='text-center m-4'
)
card2 = dbc.Card(
    [
        dbc.CardHeader("Failed Component"),
        dbc.CardBody(
            [
                html.H2("Card title", className="card-title", id= "failure_title"),                
                modal1,
            ]
        ),       
    ], color="danger", inverse=True,
    className='text-center m-4'
)
card3 = dbc.Card(
    [
        dbc.CardHeader("Model"),
        dbc.CardBody(
            [
                html.H3("Card title", className="card-title", id= "model_title"),
                html.Div(id = "model_mac"),
            ]
        ),       
    ], color="info", inverse=True,
    className='text-center m-4'
)
card4 = dbc.Card(
    [
        dbc.CardHeader("Age of the Machine"),
        dbc.CardBody(
            [
                html.H3("Card title", className="card-title", id= 'age_title'),
                html.Div(id = 'age_mac'),
            ]
        ),       
    ], color="info", inverse=True,
    className='text-center m-4'
)

content = html.Div(id="page-content", style=CONTENT_STYLE)
home = html.Div([
            dbc.Row([
                dbc.Col(card1),
                dbc.Col(card2),
                dbc.Col(card3),
                dbc.Col(card4)                
            ]),
            dbc.Row([
                dbc.Col([dbc.Card(dropdown_1)]),
                dbc.Col([dbc.Card(dropdown_2)]),
                dbc.Col([dbc.Card(inputNum)])
            ]),
            dbc.Row([
                dbc.Col([dbc.Card(dcc.Graph(id= 'graph1'),style={'height':400}),
                         dbc.Card(dcc.Graph(id = 'graph4'),style={'height':400})], width=6),
                dbc.Col([dbc.Card(dcc.Graph(id= 'graph-3',style={'height':800}))], width=6),            
            ]),
        ], id = "content-1", style=CONTENT_STYLE)
# ML_page = 

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

#callback() for controlling sidebar:
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


#callback() for home page graphs:
@app.callback(
    [Output("graph1", "figure"), 
    Output("graph4", "figure"),
    Output("graph-3", "figure"),   
    ], 
    [Input("dropdown-1", "value"),
    Input("dropdown-2", "value"),    
    Input("machine_id", "value"),]
    )
def render_page_graphs(value, type, id):
    #subset the data frame based on the entered machineID
    dff = df.loc[df["machineID"] == id]
    a = dff["age"].unique() 
    a = a[0]
    b = dff["model"].unique()
    b = b[0]
    c = df.loc[(df["machineID"] == id) & (df["failure"] != "0")]
    d = df.loc[(df["machineID"] == id) & (df["errorID"] != "0")]
    e = pd.DataFrame(d.groupby(["errorID"], as_index=False)["machineID"].count())
    
    df_failure = pd.DataFrame(c)
    df_error = pd.DataFrame(d)
        
            
    df_type = df_error.sort_values(by=['errorID']) if type == "errorID" else df_failure.sort_values(by=['failure'])
    
    
    return px.line(dff, x = 'datetime', y = value), px.bar(df_type, x = type), px.pie(e, values= 'machineID', names= 'errorID') 

# callback() for cards titles:
@app.callback(
    [Output("age_mac", "children"), 
    Output("age_title", "children"),
    Output("model_mac", "children"), 
    Output("model_title", "children"),
    Output("failure_title", "children"),
    Output("error_title", "children")
    ], 
    Input("machine_id", "value"),
    )
def render_page_components(id):
    #subset the data frame based on the entered machineID
    dff = df.loc[df["machineID"] == id]
    a = dff["age"].unique()
    a= a[0]
    b = dff["model"].unique()
    b = b[0]
    c = df.loc[(df["machineID"] == id) & (df["failure"] != "0")]
    d = df.loc[(df["machineID"] == id) & (df["errorID"] != "0")]
    
    
    df_failure = pd.DataFrame(c)
    df_error = pd.DataFrame(d)
        
    count_df_failure = df_failure.shape[0]
    count_df_error = df_error.shape[0]
        
    return html.P(f'The machine ID {id}  is {a}  years old'), html.P(f'{a}'), html.P(f'The machine ID {id} is {b}'), html.P(f'{b}'), html.P(f'{count_df_failure}'), html.P(f'{count_df_error}')



@app.callback(
    Output("modal-fs-1", "is_open"),  
    Input("open-fs-1", "n_clicks"),
    State("modal-fs-1", "is_open"),     
)

def toggle_modal(n, is_open):
    
    return not is_open if n else is_open



@app.callback(
    Output("modal_body_1", "children"),    
    Input("machine_id", "value"),         
)

def data_table(id):
    #subset the data frame based on the entered machineID
        d = df.loc[(df["machineID"] == id) & (df["failure"] != "0")]
        dff = pd.DataFrame(d)
        df_n = dff[["datetime","machineID", "volt", "rotate", "pressure", "vibration", "failure", "model", "age"]]
    
        return dash_table.DataTable(id= 'data-table',
                                    columns= [{"name": col, "id": col} for col in df_n.columns],
                                    data = dff.to_dict('records'),
                                    style_table={'width': '100%'},
                                    style_cell= {'padding':'5px'})    
    
@app.callback(
    Output("graph2", "figure"),
    [Input("machine_id", "value"), 
    Input("dropdown-1", "value")]    
)

def data_table(id, variable):
    #subset the data frame based on the entered machineID
        d = df.loc[(df["machineID"] == id) & (df["failure"] != "0")]
        dff = pd.DataFrame(d)
        dfff = dff.loc[dff["machineID"] == id]
        def condition(x):
            if x == "comp1":
                return 1
            elif x == "comp2":
                return 2
            elif x == "comp3":
                return 3
            else :
                return 4            
            
        dfff["colorCode"] = dfff["failure"].apply(condition)                
        fig =  px.line(dfff, x = 'datetime', y = variable)
        fig.add_trace(go.Scatter(mode="markers", x=dff["datetime"], y=dff[variable], name="Failure Date",
                                 marker=dict(size=12, color = dfff["colorCode"],line=dict(width=2, color='DarkSlateGrey'))))
        return fig
    
@app.callback(
    Output("modal-fs-2", "is_open"),  
    Input("open-fs-2", "n_clicks"),
    State("modal-fs-2", "is_open"),     
)

def toggle_modal(n, is_open):
    
    return not is_open if n else is_open



@app.callback(
    Output("modal_body_2", "children"),    
    Input("machine_id", "value"),         
)

def data_table(id):
    #subset the data frame based on the entered machineID
        d = df.loc[(df["machineID"] == id) & (df["errorID"] != "0")]
        dff = pd.DataFrame(d)
        df_n = dff[["datetime","machineID", "volt", "rotate", "pressure", "vibration", "errorID", "model", "age"]]
    
        return dash_table.DataTable(id= 'data-table',
                                    columns= [{"name": col, "id": col} for col in df_n.columns],
                                    data = dff.to_dict('records'),
                                    style_table={'width': '100%'},
                                    style_cell= {'padding':'5px'})    
    
@app.callback(
    Output("graph3", "figure"),
    [Input("machine_id", "value"), 
    Input("dropdown-1", "value")]    
)

def data_table(id, variable):
    #subset the data frame based on the entered machineID
        d = df.loc[(df["machineID"] == id) & (df["errorID"] != "0")]
        dff = pd.DataFrame(d)
        dfff = dff.loc[dff["machineID"] == id]
        def condition(x):
            if x == "error1":
                return 1
            elif x == "error2":
                return 2
            elif x == "error3":
                return 3
            elif x == "error4":
                return 4
            else:
                return 5
            
            
        dfff["colorCode"] = dfff["errorID"].apply(condition)
        fig =  px.line(dfff, x = 'datetime', y = variable)
        fig.add_trace(go.Scatter(mode="markers", x=dff["datetime"], y=dff[variable], name= "errorID date",
                                 marker=dict(size=12, color = dfff["colorCode"],line=dict(width=2, color='DarkSlateGrey'))))
        
        return fig

    
if __name__ == "__main__":
    app.run_server(port=8888)