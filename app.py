import dash
from dash import  dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd  

import numpy as np
import plotly.graph_objects as go
import pandas as pd
import numpy as np


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#C6C4C4"
}


# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout about content", className="lead"
        ),
        
    ],
    style=SIDEBAR_STYLE,
)

# path = "C:/Users/KD169FE/OneDrive - EY/Desktop/Call for  code/Application/"
raw_data = pd.ExcelFile("Call_for_code_Data.xlsx")
emis = pd.ExcelFile("emissions.xlsx")

app = dash.Dash(__name__) 

colors = {
    'background': '#fffcfc',
    'text': '#ffdb58',
    'text1':'#000000'
}

## create data 
df1 = pd.DataFrame()
for sheet in emis.sheet_names[2:]:
    emis_df = emis.parse(sheet_name = sheet)
    # so2 emissions for stated policy
    so2 = emis_df.iloc[6:11,:6].reset_index(drop=True)

    so2.columns = ["Industry","2018","2025","2030","2035","2040"]
    so2["Scenario"] = "Stated Policy"
    so2["Country"] = sheet
    so2["Emission"] = "SO2"

    # nox emissions for stated policy
    nox = emis_df.iloc[13:18,:6].reset_index(drop=True)

    nox.columns = ["Industry","2018","2025","2030","2035","2040"]
    nox["Scenario"] = "Stated Policy"
    nox["Country"] = sheet
    nox["Emission"] = "NOx"

    # pm emissions for stated policy
    pm = emis_df.iloc[20:25,:6].reset_index(drop=True)

    pm.columns = ["Industry","2018","2025","2030","2035","2040"]
    pm["Scenario"] = "Stated Policy"
    pm["Country"] = sheet
    pm["Emission"] = "PM"
    
    stated_policy = pd.concat([so2,nox,pm],ignore_index=True)
    
    # so2 emissions for current policy
    so2_current = emis_df.iloc[6:11,[12,13,14,15]].reset_index(drop=True)

    so2_current.columns = ["Industry","2025","2030","2040"]
    so2_current["Scenario"] = "Current Policy"
    so2_current["Country"] = sheet
    so2_current["Emission"] = "SO2"

    # nox emissions for current policy
    nox_current = emis_df.iloc[13:18,[12,13,14,15]].reset_index(drop=True)

    nox_current.columns = ["Industry","2025","2030","2040"]
    nox_current["Scenario"] = "Current Policy"
    nox_current["Country"] = sheet
    nox_current["Emission"] = "NOx"

    # pm emissions for current policy
    pm_current = emis_df.iloc[20:25,[12,13,14,15]].reset_index(drop=True)

    pm_current.columns = ["Industry","2025","2030","2040"]
    pm_current["Scenario"] = "Current Policy"
    pm_current["Country"] = sheet
    pm_current["Emission"] = "PM"
    
    current_policy = pd.concat([so2_current,nox_current,pm_current],ignore_index=True)
    
    # so2 emissions for sustainable development policy
    so2_sus = emis_df.iloc[6:11,[12,20,21,22]].reset_index(drop=True)

    so2_sus.columns = ["Industry","2025","2030","2040"]
    so2_sus["Scenario"] = "Sustainable Development"
    so2_sus["Country"] = sheet
    so2_sus["Emission"] = "SO2"

    # nox emissions for sustainable development policy
    nox_sus = emis_df.iloc[13:18,[12,20,21,22]].reset_index(drop=True)

    nox_sus.columns = ["Industry","2025","2030","2040"]
    nox_sus["Scenario"] = "Sustainable Development"
    nox_sus["Country"] = sheet
    nox_sus["Emission"] = "NOx"

    # pm emissions for sustainable development policy
    pm_sus = emis_df.iloc[20:25,[12,20,21,22]].reset_index(drop=True)

    pm_sus.columns = ["Industry","2025","2030","2040"]
    pm_sus["Scenario"] = "Sustainable Development"
    pm_sus["Country"] = sheet
    pm_sus["Emission"] = "PM"
    
    sus_policy = pd.concat([so2_sus,nox_sus,pm_sus],ignore_index=True)
    df = pd.concat([stated_policy,current_policy,sus_policy],ignore_index=True)
    df1 = pd.concat([df1,df],ignore_index=True)

df1 = df1.fillna(0)

countries = df1.Country.unique()

# Line Chart
line_chart = pd.melt(df1,
                    id_vars=["Industry","Scenario","Country","Emission"],
                    var_name="Year",
                    value_name="Emissions")
agg_view = line_chart.groupby(["Scenario","Country","Emission","Year"])["Emissions"].sum().reset_index()




# Landing Page
# color_discrete_map={'(?)':'black', 'Lunch':'gold', 'Dinner':'darkblue'}

content  = html.Div(style={'backgroundColor': colors['background']},children=[
    html.Div(children=[
        html.H1(children='Enabling Responsible production and Green consumption', style={'textAlign': 'center','color': colors['text'],"margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem"}),
        ### Sunburst chart 
        

        html.Div(children='''
        Emissions of sunburst
        ''',style={'textAlign': 'center',
        'color': colors['text1'],
        'fontSize': 20,
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem"}),
        dcc.Dropdown(id = 'sunburst',multi = True,
        options = [{'label':x ,'value':x} for x in sorted (df1.Country.unique())],
        value = ['US','Europe'],style={'textAlign': 'center',
        'color': colors['text1'],
        'fontSize': 20,
        'width':'50%',
        "margin-left": "4rem",
        "margin-right": "2rem",
        "padding": "10px 10px"}),

        dcc.Graph(
            id='graph1',
            figure = {},
            style={'textAlign': 'center',
        'color': colors['text1'],
        'fontSize': 20,
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem"}
            
        )       
    ]),
    ### Aggregate_Area  chart 
    html.Div(children='''
        Emissions of agg_area chart
        ''',style={'textAlign': 'center',
        'color': colors['text1'],
        'fontSize': 20,
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem"}),
        dcc.Dropdown(id = 'agg_area',multi = True,
        options = [{'label':x ,'value':x} for x in sorted (df1.Emission.unique())],
        value = ['US','Europe'],style={'textAlign': 'center',
        'color': colors['text1'],
        'fontSize': 20,
        'width':'50%',
        "margin-left": "4rem",
        "margin-right": "2rem",
        "padding": "10px 10px"}),

        dcc.Graph(
            id='graph2',
            figure = {},
            style={'textAlign': 'center',
        'color': colors['text1'],
        'fontSize': 20,
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem"}
            
        ) ,
        ### Line  chart
       html.Div(children='''
        Emissions of line chart
        ''',style={'textAlign': 'center',
        'color': colors['text1'],
        'fontSize': 20,
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem"}),
        dcc.Dropdown(id = 'country',
        options = [{'label':x ,'value':x} for x in sorted (df1.Country.unique())],
        value = 'US',style={'textAlign': 'center',
        'color': colors['text1'],
        'fontSize': 20,
        'width':'50%',
        "margin-left": "4rem",
        "margin-right": "2rem",
        "padding": "10px 10px"}),
        dcc.Dropdown(id = 'emission',
        options = [{'label':x ,'value':x} for x in sorted (df1.Emission.unique())],
        value = 'US',style={'textAlign': 'center',
        'color': colors['text1'],
        'fontSize': 20,
        'width':'50%',
        "margin-left": "4rem",
        "margin-right": "2rem",
        "padding": "10px 10px"}),

        dcc.Graph(
            id='graph3',
            figure = {},
            style={'textAlign': 'center',
        'color': colors['text1'],
        'fontSize': 20,
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem"}
            
        ) 
])
@app.callback(
    Output(component_id = 'graph1' ,component_property = 'figure' ),
    [Input(component_id = 'sunburst',component_property = 'value')])

def update_sunburst(val):
    fig1 = px.sunburst(df1[df1["Country"].isin(val)], 
                  path=['Country', 'Emission','Industry'], 
                  values='2018',
                  hover_data=["Emission"],
                  title = "Current emissions of air pollutants")
    fig1.update_layout(paper_bgcolor=colors['background'])
    return fig1

@app.callback(
    Output(component_id = 'graph2' ,component_property = 'figure' ),
    [Input(component_id = 'agg_area',component_property = 'value')]
)

def update_agg(val):
    fig2 = px.area(agg_view[(agg_view["Country"].isin(["US","CHINA","INDIA"]))&
             (agg_view["Year"].isin(["2025","2030","2040"]))&
             (agg_view["Emission"].isin(val))],
             x="Year", 
              y="Emissions",
              title="Current and projected emissions: ",
              color="Country")
 
    fig2.update_layout(paper_bgcolor=colors['background'])
    return fig2

@app.callback(
    Output(component_id = 'graph3' ,component_property = 'figure' ),
    [Input(component_id = 'country',component_property = 'value'),
    Input(component_id = 'emission',component_property = 'value')]
)

def update_line(country,emission):
    fig3 = px.line(line_chart[(line_chart.Year.isin(['2018','2025','2030','2040']))&
                          (line_chart["Country"]== country )&
                          (line_chart["Emission"]== emission)].
              groupby(["Year","Country","Emission","Scenario"]).
              agg({'Emissions':sum}).
              reset_index(), 
              
              x="Year", 
              y="Emissions", 
              color='Scenario')
    fig3.update_layout(paper_bgcolor=colors['background'])
    return fig3

app.layout = html.Div([ sidebar, content])



if __name__ == '__main__':
    app.run_server(debug=True,host='0.0.0.0', port=8050)
