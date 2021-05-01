import dash
import dash_auth
import plotly.express as px
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

VALID_USERNAME_PASSWORD_PAIRS = {
    'user': 'Password1!'
}

df = pd.read_csv("ethics.csv")

app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

server = app.server

app.layout=html.Div([
    html.H1("CSSHS Ethics application analysis up to 1 May 2021"),
    html.H2("Total count by Type"),
    dcc.Graph(id='my-graph1',
              figure=px.histogram(data_frame=df, x="Type",color="Type")),
    html.H2("Status/Outcome by Sub-Panel"),
    dcc.Graph(id='my-graph2',
              figure=px.histogram(data_frame=df, x="Project Status",color="Health of Sport?")),
    html.H2("Type by Sub-Panel"),
    dcc.Graph(id='my-graph3',
              figure=px.histogram(data_frame=df, x="Health of Sport?",color="Type")),
    html.H2("Type by Supervisor"),
    dcc.Graph(id='my-graph4',
              figure=px.histogram(data_frame=df, x="Supervisor",color="Type")),
    html.H2("Resubmissions by Sub-Panel"),
    dcc.Graph(id='my-graph5',
              figure=px.histogram(data_frame=df, x="Health of Sport?",color="Re Submission")),
    html.H2("Type of Approval Sought"),
    dcc.Graph(id='my-graph6',
              figure=px.histogram(data_frame=df, x="Health of Sport?",color="Approval Requirement By")),
])

if __name__=='__main__':
    app.run_server()