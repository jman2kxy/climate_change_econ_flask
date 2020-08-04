import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets= [dbc.themes.BOOTSTRAP, '/assets/stylesheet.css'])

app.config.suppress_callback_exceptions = True
#app.css.append_css({'external_url': '/assets/stylesheet.css'})
#app.server.static_folder = 'assets'  # if you run app.py from 'root-dir-name' you don't need to specify.

co2_start = pd.read_csv("data_csv/luthico2_start.csv")
co2_middle = pd.read_csv("data_csv/muere_data.csv")
co2_merged = pd.read_csv("data_csv/merged_ice_core_yearly.csv")

co2_kg_gdp = pd.read_csv("data_csv/co2_kg_gdp.csv", encoding='cp1252')
co2_kg_gdp = co2_kg_gdp.melt(id_vars=["Country_Name", "Country_Code", "Indicator Name", "Indicator Code"], var_name="Year", value_name="Emission")
co2_kg_gdp['Year'] = co2_kg_gdp['Year'].astype(int)

co2_kt = pd.read_csv("data_csv/co2_kt.csv")
temp_up2BP = pd.read_csv("data_csv/Marcott.temp.BP.csv")
temp_post1770 = pd.read_csv("data_csv/rhodesTemp_post1770.csv")
temp_merged = pd.read_csv("data_csv/temp_merged.csv")
agri = pd.read_csv("data_csv/crops.csv")
quan_vul = pd.read_csv("data_csv/qntify_vulnerability_192.csv")
read_vul = pd.read_csv("data_csv/readiness_ec_social_gov_192.csv")
antarc_mass = pd.read_csv("data_csv/antarctica_mass.csv")
green_mass = pd.read_csv("data_csv/greenland_mass.csv")
dice_model = pd.read_csv("data_csv/DICE_model.csv")
gsl_merged = pd.read_csv("data_csv/sl_merged.csv")

weather = pd.read_csv("data_csv/weather-events-US-1980-2017.csv")
weather['Year'] = weather['Begin Date'].astype(str)
weather['Year'] = weather['Year'].str.slice(0,4)
weather['Year'] = weather['Year'].astype(int)

nav_menu = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/", id = "home-link", style={"color":"white", "fontWeight":"bold"})),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Carbon Dioxide Concentration", href='/co2', id = "co2-link"),
                dbc.DropdownMenuItem("Carbon Dioxide Emission", href='/co2_emission', id = "co2-emiss-link"),
                dbc.DropdownMenuItem("Surface Temperature", href='/temp', id = "temp-link"),
                dbc.DropdownMenuItem("Antarctica Ice Sheet Mass", href='/antarc', id = "antarc-link"),
                dbc.DropdownMenuItem("Sea Level Rise", href='/sea', id = "sea-link"),
                dbc.DropdownMenuItem("Social Cost of Carbon", href='/scc', id = "scc-link")
            ],
            nav=True,
            in_navbar=True,
            label='Climate Change Charts',
            style={"color":"white", "fontWeight":"bold"}
        ),
        dbc.DropdownMenu(
            children = [
                dbc.DropdownMenuItem("A1 Scenario", href='/A1', id = 'a1-link' ),
                dbc.DropdownMenuItem("A2 Scenario", href='/A2', id = 'a2-link' ),
                dbc.DropdownMenuItem("B1 Scenario", href='/B1', id = 'b1-link' ),
                dbc.DropdownMenuItem("B2 Scenario", href='/B2', id = 'b2-link' )
            ],
            nav=True,
            in_navbar=True,
            label='Grain Production',
            style={"color":"white", "fontWeight":"bold"}
        ),
        dbc.NavItem(dbc.NavLink("Climate Readiness/Vulnerability", href="/readiness", id = "ready-link", style={"color":"white", "fontWeight":"bold"})),
        dbc.NavItem(dbc.NavLink("Cost of Natural Disasters", href="/disaster", id = "disaster-link", style={"color":"white", "fontWeight":"bold"}))
    ],
    style={'background-color':'#2A3F54','fontFamily':'Lato'}

)



#--------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
],style={'backgroundColor':'#EAEAEA'}

)

index_layout = html.Div([
    nav_menu,
    html.H1("Climate Change Economics", style={'text-align':'center','fontFamily':'Lato'})
],style={'fontFamily':'Lato'})

co2_layout = html.Div([
    nav_menu,

    html.H1("Carbon Dioxide Concentration", style={'text-align':'center','fontFamily':'Lato'}),

    dcc.RangeSlider(
        id = 'co2_conc',
        min = min(co2_merged['Year']),
        max = max(co2_merged['Year']),
        step = 1,
        value = [min(co2_merged['Year']), max(co2_merged['Year'])]
    ),

    html.Div(id='output_co_year_range', children=[], style={'text-align':'center'}),
    html.Br(),

    dcc.Graph(id='co2_graph', figure={})


],style={'fontFamily':'Lato'})

co2_choro_layout = html.Div([
    nav_menu,
    html.H1("Carbon Dioxide Emission (kg per 2010 US$ of GDP)", style={'text-align': 'center','fontFamily':'Lato'}),

    html.Div([
        dcc.Graph(id='co2_choropleth')
    ]),

    html.Div([
        dcc.Input(id='input_state', type='number', inputMode='numeric', value=1960,
                  max=2014, min=min(co2_kg_gdp['Year']), step=1, required=True),
        html.Button(id='submit_button',children='Submit'),
        html.Div(id='output_state'),
    ],style={'text-align': 'center','fontFamily':'Lato'}),
],style={'fontFamily':'Lato'})


temp_layout = html.Div([
    nav_menu,
    html.H1("Surface Temperature", style={'text-align':'center','fontFamily':'Lato'}),

    dcc.RangeSlider(
        id = 'temp_year',
        min = min(temp_merged['Year']),
        max = max(temp_merged['Year']),
        step = 1,
        value = [min(temp_merged['Year']), max(temp_merged['Year'])]
    ),

    html.Div(id='output_temp_year_range', children=[], style={'text-align':'center'}),
    html.Br(),

    dcc.Graph(id='temp_graph', figure={})
],style={'fontFamily':'Lato'})

antarc_layout = html.Div([
    nav_menu,
    html.H1("Change in the Mass of Antarctica Since 2002", style={'text-align':'center','fontFamily':'Lato'}),

    dcc.RangeSlider(
        id = 'arc_year',
        min = min(antarc_mass['Time']),
        max = max(antarc_mass['Time']),
        step = 1,
        value = [min(antarc_mass['Time']), max(antarc_mass['Time'])]
    ),

    html.Div(id='output_arc_year_range', children=[], style={'text-align':'center'}),
    html.Br(),

    dcc.Graph(id='arc_graph', figure={})
],style={'fontFamily':'Lato'})

sea_layout = html.Div([
    nav_menu,
    html.H1("Change in Global Sea Level in Common Era", style={'text-align':'center','fontFamily':'Lato'}),

    dcc.RangeSlider(
        id = 'sea_year',
        min = min(gsl_merged['Year']),
        max = max(gsl_merged['Year']),
        step = 1,
        value = [min(gsl_merged['Year']), max(gsl_merged['Year'])]
    ),

    html.Div(id='output_gsl_year_range', children=[], style={'text-align':'center'}),
    html.Br(),

    dcc.Graph(id='gsl_graph', figure={})
],style={'fontFamily':'Lato'})


scc_layout = html.Div([
    nav_menu,
    html.H1("The Projection of the Social Cost of Carbon to the Year 2200", style={'text-align':'center','fontFamily':'Lato'}),

    dcc.RangeSlider(
        id = 'scc_year',
        min = min(dice_model['Year']),
        max = max(dice_model['Year']),
        step = 1,
        value = [min(dice_model['Year']), max(dice_model['Year'])]
    ),

    html.Div(id='output_scc_year_range', children=[], style={'text-align':'center'}),
    html.Br(),

    dcc.Graph(id='scc_graph', figure={})
],style={'fontFamily':'Lato'})

a1_layout = html.Div([
    nav_menu,
    html.H1("A1 Scenario for Grain Production", style={'text-align':'center','fontFamily':'Lato'}),

    dcc.Dropdown(id='a1_scenario',
                 options=[
                     {'label': 'A1FI 2020', 'value': 'A1FI2020'},
                     {'label': 'A1FI 2050', 'value': 'A1FI2050'},
                     {'label': 'A1F1 2080', 'value': 'A1FI2080'}
                 ],
                placeholder="Choose a scenario"),

    html.Div([
        dcc.Graph(id='A1-graph')
    ])
],style={'fontFamily':'Lato'})

a2_layout = html.Div([
    nav_menu,
    html.H1("A2 Scenario for Grain Production", style={'text-align':'center','fontFamily':'Lato'}),

    dcc.Dropdown(id='a2_scenario',
                 options=[
                     {'label': 'A2A 2020', 'value': 'A2A2020'},
                     {'label': 'A2A 2050', 'value': 'A2A2050'},
                     {'label': 'A2A 2080', 'value': 'A2A2080'}
                 ],
                 placeholder="Choose a scenario"),

    html.Div([
        dcc.Graph(id='A2-graph')
    ])
],style={'fontFamily':'Lato'})

b1_layout = html.Div([
    nav_menu,
    html.H1("B1 Scenario for Grain Production", style={'text-align':'center','fontFamily':'Lato'}),

    dcc.Dropdown(id='b1_scenario',
                 options=[
                     {'label': 'B1A 2020', 'value': 'B1A2020'},
                     {'label': 'B1A 2050', 'value': 'B1A2050'},
                     {'label': 'B1A 2080', 'value': 'B1A2080'}
                 ],placeholder="Choose a scenario"),

    html.Div([
        dcc.Graph(id='B1-graph')
    ])
],style={'fontFamily':'Lato'})

b2_layout = html.Div([
    nav_menu,
    html.H1("B2 Scenario for Grain Production", style={'text-align':'center','fontFamily':'Lato'}),

    dcc.Dropdown(id='b2_scenario',
                 options=[
                     {'label': 'B2B 2020', 'value': 'B2B2020'},
                     {'label': 'B2B 2050', 'value': 'B2B2050'},
                     {'label': 'B2B 2080', 'value': 'B2B2080'}
                 ],placeholder="Choose a scenario"),

    html.Div([
        dcc.Graph(id='B2-graph')
    ])
],style={'fontFamily':'Lato'})

readiness_layout = html.Div([
    nav_menu,
    html.H1("Climate Change Readiness/Vulnerability", style={'text-align':'center','fontFamily':'Lato'}),

    dcc.Dropdown(id='readiness',
                 options=[
                     {'label': 'Capacity', 'value': 'Capacity'},
                     {'label': 'Exposure', 'value': 'Exposure'},
                     {'label': 'Sensitivity', 'value': 'Sensitivity'},
                     {'label': 'Vulnerability', 'value': 'Vulnerability'},
                     {'label': 'Economic', 'value': 'Economic'},
                     {'label': 'Governance', 'value': 'Governance'},
                     {'label': 'Social', 'value': 'Social'},
                     {'label': 'Readiness', 'value': 'Readiness'}
                 ],placeholder="Choose a Variable"),

    html.Div([
        dcc.Graph(id='readiness-graph')
    ]),

    html.Div(id='output_year', children=[], style={'text-align':'center'}),

    dcc.Slider(
        id = 'ready_year',
        min = min(read_vul['Year']),
        max = max(read_vul['Year']),
        step = 1,
        value = max(read_vul['Year'])
    )
],style={'fontFamily':'Lato'})

def disaster_output():

    fig = px.scatter(data_frame=weather,
              x = 'Year',
              y = 'Total CPI-Adjusted Cost (Millions of Dollars)',
              size = 'Total CPI-Adjusted Cost (Millions of Dollars)',
              color = 'Disaster',
              hover_name="Name",
              template='seaborn'
              )
    return (fig)


disaster_layout = html.Div([
    nav_menu,
    html.H1("Billion-Dollar Weather and Climate Disasters", style={'text-align':'center','fontFamily':'Lato'}),

    html.Br(),

    dcc.Graph(id='disaster_graph', figure=disaster_output())
],style={'fontFamily':'Lato'})


#--------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/co2':
        return co2_layout
    elif pathname == '/co2_emission':
        return co2_choro_layout
    elif pathname == '/temp':
        return temp_layout
    elif pathname == '/antarc':
        return antarc_layout
    elif pathname == '/sea':
        return sea_layout
    elif pathname == '/scc':
        return scc_layout
    elif pathname == '/A1':
        return a1_layout
    elif pathname == '/A2':
        return a2_layout
    elif pathname == '/B1':
        return b1_layout
    elif pathname == '/B2':
        return b2_layout
    elif pathname == '/readiness':
        return readiness_layout
    elif pathname == '/disaster':
        return disaster_layout
    else:
        return index_layout


@app.callback(
    [Output(component_id='output_co_year_range', component_property='children'),
     Output(component_id='co2_graph', component_property='figure')],
    [Input(component_id='co2_conc', component_property='value')]
)
def co2_output(co2_conc):

    container = "The year range is {}".format(co2_conc)

    co2_merged_range = co2_merged[(co2_merged.Year >= co2_conc[0]) & (co2_merged.Year <= co2_conc[1])]

    fig = px.line(data_frame=co2_merged_range,
              x = 'Year',
              y = ' CO2_ppm',
              template='seaborn'
              )

    return (container, fig)


@app.callback(
    [Output('output_state', 'children'),
    Output(component_id='co2_choropleth', component_property='figure')],
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='input_state', component_property='value')]
)

def co2_choro_output(num_clicks, val_selected):
    if val_selected is None:
        raise PreventUpdate
    else:
        df = co2_kg_gdp.query("Year=={}".format(val_selected))

        fig = px.choropleth(df, locations="Country_Code",
                            color="Emission",
                            hover_name="Country_Name",
                            projection='natural earth',
                            color_continuous_scale=px.colors.sequential.Plasma,
                            template='seaborn')

        fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))

        return ('Hover over a country to see its emission rate in the Year {} '.format(val_selected), fig)

@app.callback(
    [Output(component_id='output_temp_year_range', component_property='children'),
     Output(component_id='temp_graph', component_property='figure')],
    [Input(component_id='temp_year', component_property='value')]
)
def temp_output(temp_year):

    container = "The year range is {}".format(temp_year)

    temp_merged_range = temp_merged[(temp_merged.Year >= temp_year[0]) & (temp_merged.Year <= temp_year[1])]

    fig = px.line(data_frame=temp_merged_range,
              x = 'Year',
              y = 'Temp',
              template='seaborn'
              )
    return container, fig



@app.callback(
    [Output(component_id='output_arc_year_range', component_property='children'),
     Output(component_id='arc_graph', component_property='figure')],
    [Input(component_id='arc_year', component_property='value')]
)
def antarc_output(arc_year):

    container = "The year range is {}".format(arc_year)

    arc_merged_range = antarc_mass[(antarc_mass.Time >= arc_year[0]) & (antarc_mass.Time <= arc_year[1])]

    fig = px.line(data_frame=arc_merged_range,
              x = 'Time',
              y = 'mass_GT',
              template='seaborn'
              )
    return container, fig


@app.callback(
    [Output(component_id='output_gsl_year_range', component_property='children'),
     Output(component_id='gsl_graph', component_property='figure')],
    [Input(component_id='sea_year', component_property='value')]
)
def gsl_output(sea_year):

    container = "The year range is {}".format(sea_year)

    sea_merged_range = gsl_merged[(gsl_merged.Year >= sea_year[0]) & (gsl_merged.Year <= sea_year[1])]

    fig = px.line(data_frame = sea_merged_range,
              x = 'Year',
              y = 'sea_level',
              template='seaborn'
              )
    return container, fig

@app.callback(
    [Output(component_id='output_scc_year_range', component_property='children'),
     Output(component_id='scc_graph', component_property='figure')],
    [Input(component_id='scc_year', component_property='value')]
)
def scc_output(scc_year):

    container = "The year range is {}".format(scc_year)

    scc_merged_range = dice_model[(dice_model.Year >= scc_year[0]) & (dice_model.Year <= scc_year[1])]

    fig = px.line(data_frame = scc_merged_range,
              x = 'Year',
              y = 'Social_Cost_of_Carbon_Optimal_Tax ',
              template='seaborn'
              )
    return container, fig

@app.callback(
    Output(component_id='A1-graph', component_property='figure'),
    [Input(component_id='a1_scenario', component_property='value')]
)
def a1_output(scenario):

    if scenario is None:
        raise PreventUpdate
    else:
        df = agri
        fig = px.choropleth(df, locations="ISO3v10",
                            color=scenario,
                            hover_name="Country",
                            projection='natural earth',
                            color_continuous_scale=px.colors.sequential.Plasma,
                            template='seaborn')

        fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))
        return fig

@app.callback(
    Output(component_id='A2-graph', component_property='figure'),
    [Input(component_id='a2_scenario', component_property='value')]
)
def a2_output(scenario):

    if scenario is None:
        raise PreventUpdate
    else:
        df = agri
        fig = px.choropleth(df, locations="ISO3v10",
                            color=scenario,
                            hover_name="Country",
                            projection='natural earth',
                            color_continuous_scale=px.colors.sequential.Plasma,
                            template='seaborn')

        fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))
        return fig

@app.callback(
    Output(component_id='B1-graph', component_property='figure'),
    [Input(component_id='b1_scenario', component_property='value')]
)
def b1_output(scenario):

    if scenario is None:
        raise PreventUpdate
    else:
        df = agri
        fig = px.choropleth(df, locations="ISO3v10",
                            color=scenario,
                            hover_name="Country",
                            projection='natural earth',
                            color_continuous_scale=px.colors.sequential.Plasma,
                            template='seaborn')

        fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))
        return fig

@app.callback(
    Output(component_id='B2-graph', component_property='figure'),
    [Input(component_id='b2_scenario', component_property='value')]
)
def b2_output(scenario):

    if scenario is None:
        raise PreventUpdate
    else:
        df = agri
        fig = px.choropleth(df, locations="ISO3v10",
                            color=scenario,
                            hover_name="Country",
                            projection='natural earth',
                            color_continuous_scale=px.colors.sequential.Plasma,
                            template='seaborn')

        fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))
        return fig

@app.callback(
    [Output(component_id='output_year', component_property='children'),
     Output(component_id='readiness-graph', component_property='figure')],
    [Input(component_id='readiness', component_property='value'),
     Input(component_id='ready_year', component_property='value')]
)
def readiness_output(variable, year):


    container = "The year is {}".format(year)

    if variable is None:
        raise PreventUpdate
    else:
        df = read_vul[read_vul.Year == year]
        fig = px.choropleth(df, locations="Country",
                            color=variable,
                            hover_name="Country",
                            projection='natural earth',
                            color_continuous_scale=px.colors.sequential.Plasma,
                            template='seaborn')

        fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))
        return container, fig

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
    #app.run_server(debug=True)