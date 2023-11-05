import dash
from dash import Dash, html, dcc, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go



# df1 = pd.read_csv('Data\\PdM_errors.csv')
# df2 = pd.read_csv('Data\\PdM_telemetry.csv')
# df3 = pd.read_csv('Data\\PdM_failures.csv')
# df4 = pd.read_csv('Data\\PdM_machines.csv')
# df5 = pd.read_csv('Data\\PdM_maint.csv')


# output1 = pd.merge(df2, df1, on=['datetime','machineID'],how='left')
# output2 = pd.merge(output1, df3, on=['datetime','machineID'],how='left')
# output3 = pd.merge(output2, df5, on=['datetime','machineID'],how='left')
# merged_data = pd.merge(output3, df4, on=['machineID'],how='left')

# merged_data = merged_data.replace(np.nan, 0)
# merged_data = merged_data.groupby(['machineID','datetime']).max()
# merged_data=merged_data.reset_index()
# merged_data.to_csv('Data/merged_data.csv', index=False)


# Create the Dash app
# app = dash.Dash(
#     __name__,
#     external_stylesheets=[dbc.themes.BOOTSTRAP],
#     meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}]
# )

# Read the CSV file into a DataFrame
df = pd.read_csv('Data\\merged_data.csv')


external_stylesheets = [dbc.themes.SPACELAB, dbc.icons.BOOTSTRAP]


# Create the Dash app
app = Dash(__name__, external_stylesheets = external_stylesheets)
app.title= 'PMIM Dashboard'

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "relative",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "auto",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "1rem",
    "margin-right": "1rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
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



banner = dbc.Card(
    dbc.CardBody(
        [
            html.H1('PMIM Interactive Dashboard'),
            html.H5('Predictive Maintenance Industrial Machines')
        ], 
    ), color="success", inverse=True,
    className='text-center bg-secondary text-light border border-3 align-self-center'
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

fig2 = {'data': [{'x': [1,2,3], 'y': [4,1,2], 'type': 'scatter'}]}
fig3 = pd.DataFrame([{'x': [1,2,3], 'y': [4,1,2]}])

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

content_1 = html.Div([
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
                dbc.Col([dbc.Card(dcc.Graph(id= 'graph1'),style={'height':300}),
                         dbc.Card(dcc.Graph(id = 'graph4'),style={'height':300})], width=6),
                # dbc.Col([dbc.Card(px.pie(df, values= 'age', names= 'machineID'))]),            
            ]),
        ], style=CONTENT_STYLE)
# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row(banner),
    dbc.Row([
        # to be used as a sidebar
        dbc.Col(html.Div([dcc.Location(id="url"), sidebar])),
        dbc.Col(content_1, width=10),
    ], className='p-2 align-items-stretch')
], fluid=True)

@app.callback(
    [
    Output("graph1", "figure"), 
    Output("graph4", "figure"),   
    Output("age_mac", "children"), 
    Output("age_title", "children"),
    Output("model_mac", "children"), 
    Output("model_title", "children"),
    Output("failure_title", "children"),
    Output("error_title", "children")
    ], 
    [Input("url", "pathname"),
    Input("dropdown-1", "value"),
    Input("dropdown-2", "value"),    
    Input("machine_id", "value"),]
    )
def render_page_content(pathname,value, type, id):
    if pathname == "/":
        #subset the data frame based on the entered machineID
        dff = df.loc[df["machineID"] == id]
        a = dff["age"].unique()
        a= a[0]
        b = dff["model"].unique()
        b = b[0]
        c = df.loc[(df["machineID"] == id) & (df["failure"] != "0")]
        d = df.loc[(df["machineID"] == id) & (df["errorID"] != "0")]
            
        df_type = pd.DataFrame(d) if type == "errorID" else pd.DataFrame(c)
            
        df_failure = pd.DataFrame(c)
        df_error = pd.DataFrame(d)
        count_df_failure = df_failure.shape[0]
        count_df_error = df_error.shape[0]
        return px.line(dff, x = 'datetime', y = value), px.bar(df_type, x = type),  html.P(f'The machine ID {id}  is {a}  years old'), html.P(f'{a}'), html.P(f'The machine ID {id} is {b}'), html.P(f'{b}'), html.P(f'{count_df_failure}'), html.P(f'{count_df_error}')
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
        fig.add_trace(go.Scatter(mode="markers", x=dff["datetime"], y=dff[variable], name="Failure Date"))
        fig.update_traces(marker=dict(size=12, color = dfff["colorCode"],line=dict(width=2, color='DarkSlateGrey')),
                          selector=dict(mode='markers'))
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
        # fig.update_traces(marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')),
        #                   selector=dict(mode='markers'))
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
