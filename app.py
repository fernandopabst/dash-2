import dash
import dash_auth
import plotly.express as px
import pandas as pd
import numpy as np
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

VALID_USERNAME_PASSWORD_PAIRS = {
    'user': 'Password1!'
}

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CERULEAN])
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server = app.server

df = pd.read_csv("ethics.csv")
df.sort_values('Type', inplace=True)

dfa = pd.read_csv("ethics.csv")
dfa.sort_values(by=['Health of Sport?'], inplace=True)

dfb = pd.read_csv("ethics.csv")
low = dfb['ID'].tolist()
high = np.array(dfb['ID'])+20

trace1 = go.Scatter(x=dfb.Created[:2],
                    y=low[:2],
                    mode='lines',
                    line=dict(width=3))

frames = [dict(data= [dict(type='scatter',
                           x=dfb.Created[:k+1],
                           y=low[:k+1])],
               traces= [0], 
              )for k  in  range(1, len(low)-1)] 

layout = go.Layout(width=1200,
                   height=500,
                   showlegend=False,
                   hovermode='closest',
                   updatemenus=[dict(type='buttons', showactive=False,
                                y=1.05,
                                x=1.15,
                                xanchor='right',
                                yanchor='top',
                                pad=dict(t=0, r=10),
                                buttons=[dict(label='Start',
                                              method='animate',
                                              args=[None, 
                                                    dict(frame=dict(duration=1, 
                                                                    redraw=False),
                                                         transition=dict(duration=0),
                                                         fromcurrent=True,
                                                         mode='immediate')])])])


layout.update(xaxis =dict(range=[dfb.Created[0], dfb.Created[len(dfb)-1]], autorange=False),
              yaxis =dict(range=[min(low)-0.5, high.max()+0.5], autorange=False));
fig = go.Figure(data=[trace1], frames=frames, layout=layout)

app.layout=html.Div([
        html.Center(
            children= html.H1("CSSHS Ethics Application Analysis - up to 1 May 2021")),
        dbc.Tabs(
            [
                dbc.Tab(
                    label="Total count by Type",
                    children=[
                        dcc.Graph(id='my-graph1',figure=px.histogram(data_frame=df, x='Type',color='Type'))]),
                dbc.Tab(
                    label="Status/Outcome by Sub-Panel",
                    children=[
                        dcc.Graph(id='my-graph2', figure=px.histogram(data_frame=df, x="Project Status",color="Health of Sport?"))]),
                dbc.Tab(
                    label="Type by Sub-Panel (filters)",
                    children=[
                        dcc.Checklist(
                            id='my_checklist',
                            options=[
                                {'label': '2021', 'value': 2021},
                                {'label': '2020', 'value': 2020},
                                {'label': '2019', 'value': 2019},
                                {'label': '2018', 'value': 2018}],
                            value=[2021, 2020,2019,2018],
                            labelStyle={'display': 'inline-block','text-align': 'justify','margin-right':10,'margin-left':10}),
                        dcc.Graph(id='the-graph')]),
                dbc.Tab(
                    label="Type by Supervisor",
                    children=[
                        dcc.Graph(id='my-graph4', figure=px.bar(data_frame=df, x="Supervisor",color="Type",height=400,hover_data={"Project Title"}))]),
                dbc.Tab(
                    label="Resubmissions by Sub-Panel",
                    children=[
                        dcc.Graph(id='my-graph5', figure=px.histogram(data_frame=df, x="Health of Sport?",opacity=0.8,color="Re Submission",barmode='group'))]),
                dbc.Tab(
                    label="Type of Approval Sought",
                    children=[
                        dcc.Graph(id='my-graph6', figure=px.histogram(data_frame=df,x="Health of Sport?",color="Approval Requirement By"))]),
                dbc.Tab(
                    label="Total applications (animated)",
                    children=[
                        dcc.Graph(id="graph", figure=fig),
            ])])
])

@app.callback(
    Output(component_id='the-graph', component_property='figure'),
    [Input(component_id='my_checklist', component_property='value')]
)

def update_graph(options_chosen):

    dff = dfa[dfa['Year'].isin(options_chosen)]

    histochart=px.histogram(data_frame=dff, x="Health of Sport?",color="Type",barmode='group')

    return (histochart)



if __name__=='__main__':
    app.run_server()