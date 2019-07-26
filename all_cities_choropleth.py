import os
import dash
import us
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go

import json
import requests

import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.colors as mcolors
import matplotlib.cm as cm

from stringcase import titlecase

mapbox_access_token = "pk.eyJ1IjoicHJpeWF0aGFyc2FuIiwiYSI6ImNqbGRyMGQ5YTBhcmkzcXF6YWZldnVvZXoifQ.sN7gyyHTIq1BSfHQRBZdHA"


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__,external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True


if 'DYNO' in os.environ:
    app_name = os.environ['DASH_APP_NAME']
else:
    app_name = 'dash-scattermapboxplot'


#Load uszips.csv
zipcodes = pd.read_csv('uszips.csv')

#Load USZipcode engine
from uszipcode import SearchEngine, Zipcode


#Load philly district data from USZipCodes
with open('Philly Data.json') as json_file:  
    philly = json.load(json_file)

#Coordinate list -> polygon
def get_polygon(coordinate_list):
    if len(coordinate_list) == 1:
        coordinate_list = coordinate_list[0]
    lat_coordinates = [e[0] for e in coordinate_list]
    lon_coordinates = [e[1] for e in coordinate_list]
    try:
        polygon = Polygon(zip(lat_coordinates, lon_coordinates))
    except:
        polygon = None
    return polygon


#Description: Converts district files in USZipcodes to GeoDataFrames
#Input: List of district dictionaries, list of properties to include
#Ouput: Geodataframe
def create_gdf(district_list, properties_list):
    geo_dict = []
    for district in district_list:
        #Create dictionary of key:value mappings for properties for each district
        district_dict = {e: district[e] for e in properties_list}
        #Add in geometry
        district_dict['geometry'] = get_polygon(district['polygon'])
        geo_dict.append(district_dict)
    
    gdf = gpd.GeoDataFrame(geo_dict)
    return gdf

#Set overlay colors for data
def set_overlay_colors(dataset):
    """Create overlay colors based on values
    :param dataset: gpd.Series, array of values to map colors to
    :returns: dict, hex color value for each language or index value
    """
    minima = dataset.min()
    maxima = dataset.max()
    #norm is the normalized color scale
    norm = mcolors.Normalize(vmin=minima, vmax=maxima, clip=True)
    #mapper object
    mapper = cm.ScalarMappable(norm=norm, cmap= 'PuBu')
    #mapper object maps every value in dataset to color
    colors = [mcolors.to_hex(mapper.to_rgba(v)) for v in dataset]
    #Dictionary of index:color mapping
    overlay_color = {
        idx: shade
        for idx, shade in zip(dataset.index, colors)
    }

    return overlay_color

#--------------------------------------------------------------------------#

#Overlay variables
#From district_list (e.g. Philly), sort variables into single-value or multi-value type
def sort_variables_by_type(district_list):
    district = district_list[0]
    single_variables = []
    multi_variables = []
    for variable in district.keys():
        if type(district[variable]) == float or type(district[variable]) == int:
            single_variables.append(variable)
        elif type(district[variable]) == list and type(district[variable][0]) == dict:
            multi_variables.append(variable)
    return single_variables, multi_variables

single_var, multi_var = sort_variables_by_type(philly)

all_vars = single_var + multi_var + ['zipcode']

overlay_variables = [{'label': titlecase(e), 'value': e} for e in all_vars]



###HELPER FUNCTIONS for multi-value variables
#Extract dataframe of ONE multi-value variable from ONE DISTRICT
def get_multi_var_df(district, variable_name):

    df = pd.DataFrame(district[variable_name][0]['values'])
    df.columns = ['x', variable_name]
    df['zipcode'] = district['zipcode']
    
    return df

#Extract dataframe of ONE multi-value variable from ALL DISTRICTS
def get_multi_var_df_all_districts(district_list, variable_name):
    df_all_districts = pd.DataFrame()
    for district in district_list:
        if district[variable_name] is not None:
            df_district = get_multi_var_df(district, variable_name)
            df_all_districts = pd.concat([df_all_districts, df_district])
    
    return df_all_districts

#Get the levels of the multi-value variable
def get_multi_var_levels(district_list, variable_name):
    
    district = district_list[0]
    df_district = get_multi_var_df(district, variable_name)
    return list(df_district.x.unique())

#Extract dataframe of ONE LEVEL of ONE multi-value variable from ALL DISTRICTS:
def get_multi_var_level_df(district_list, variable_name, level_name):
    df_all_districts = get_multi_var_df_all_districts(district_list, variable_name)

    df_all_districts_filtered = df_all_districts.loc[df_all_districts['x'].astype(str) == str(level_name), :]

    return df_all_districts_filtered



#Wrapper function that creates GDF only with requested variables and processes it - basically a new GDF is generated EVERY time a new variable is selected in dropdown
def prepare_gdf(district_list, variable_name, level_name):

    #Check whether single or multi variable
    single_var, multi_var = sort_variables_by_type(district_list)

    #Single variable:
    if variable_name in single_var:
        vars_to_include = [variable_name] + ['zipcode']

        #Create GDF with district_list data
        gdf = create_gdf(district_list, vars_to_include)
        gdf = gdf.dropna()

    #Multi variable
    else:
        gdf = create_gdf(district_list, ['zipcode'])
        gdf = gdf.dropna()
        multi_var_level_df = get_multi_var_level_df(district_list, variable_name, level_name)
        gdf = gdf.merge(multi_var_level_df, on = 'zipcode', how = 'inner')

    #Generate centroids for each polygon to use as marker locations
    gdf['lon_lat'] = gdf['geometry'].apply(lambda row: row.centroid)
    gdf['LON'] = gdf['lon_lat'].apply(lambda row: row.x)
    gdf['LAT'] = gdf['lon_lat'].apply(lambda row: row.y)
    gdf = gdf.drop('lon_lat', axis = 1)

    return gdf





# philly_gdf 
# original columns: geometry, population, zipcode
# added columns: LON, LAT, hover_text

### APP LAYOUT ###
app.layout = html.Div([
    html.Div([html.H1("Explore US Cities")],
             style={'textAlign': "center", "padding-bottom": "10", "padding-top": "10"}),
    html.Div([
        dcc.Input(id = 'city_search_input', placeholder = 'Search US city...'),
        html.Button('Search', id = 'city_search_button'),
        html.Div(children = 'Philadelphia', id = 'city_div'),
        dcc.Store('df_store')
    ]),
    html.H2('Overlay Options'),
    dcc.Dropdown(id = 'overlay_variable_dropdown', options = overlay_variables, value = 'population'),
    dcc.Dropdown(id = 'multi_variable_levels_dropdown', options = []),
    dcc.Dropdown(
        id = 'transform_dropdown',
        options = [
            {'label': 'Value', 'value': 'Value'},
            {'label': '% of Population', 'value': '% of Population'},
            {'label': 'Density (per square mile)', 'value': 'Density (per square mile)'},
            {'label': '% of Median Household Income', 'value' : '% of Median Household Income'}],
        value = 'Value'
        ),
    dcc.Checklist(
        id = 'layer_checkbox',
        options = [{'label': 'Show Overlay', 'value': True}],
        values = [True]
    ),
    html.Div(children = 'Opacity'),
    dcc.Slider(id = 'layer_opacity_slider', min = 0, max = 1, step = 0.1, value = 0.8),
    html.Div(dcc.Graph(id="map"))
], className="container")

### APP CALLBACKS ###




#Function that gets zipcodes from cities
def get_city_zipcodes(city_name):
    city_zipcodes = zipcodes.loc[zipcodes.city == city_name, 'zip']
    #Filter outliers (using median)
    city_zipcodes = city_zipcodes[city_zipcodes.transform(lambda x: np.abs(x - x.median()) < 100)].tolist()
    return city_zipcodes

def get_district_list(city_name):
    city_zipcodes = get_city_zipcodes(city_name)
    search = SearchEngine(simple_zipcode = False)
    district_list = [search.by_zipcode(e).to_dict() for e in city_zipcodes]
    return district_list



# CALLBACK 0: Search for city in uszipcodes database

@app.callback(
     Output('city_div', 'children'),
    [Input('city_search_button', 'n_clicks')],
    [State('city_search_input', 'value')]
)
def get_city_name(n_clicks, search_value):

    return search_value

# CALLBACK 0: Search for city in uszipcodes database

@app.callback(
     Output('df_store', 'data'),
    [Input('city_div', 'children')]
)
def get_district_data(city_name):

    if city_name is not None:
        district_list = get_district_list(city_name)
    else:
        district_list = get_district_list('Philadelphia')

    print('Done downloading district list for {}'.format(city_name))

    return json.dumps(district_list)


# CALLBACK 1: Draws the map with layers based on the selected overlay variable, level (for multi-variables), 
# and transformation
@app.callback(
    Output("map", "figure"),
    [Input('df_store', 'data'),
     Input("layer_opacity_slider", "value"),
     Input("multi_variable_levels_dropdown", "value"),
     Input('layer_checkbox', 'values'),
     Input('transform_dropdown', 'value')],
     [State('overlay_variable_dropdown', 'value')])
def update_figure(df_store, layer_opacity_slider_value, multi_variable_levels_dropdown_value, layer_checkbox_value, 
transform_dropdown_value, variable_dropdown_value):

    #Load city data from df_store
    city_data = json.loads(df_store)

    #Create GDF with desired variable
    gdf = prepare_gdf(city_data, variable_dropdown_value, multi_variable_levels_dropdown_value)

    #Read what transformation the user is requesting
    if transform_dropdown_value != 'Value':
        if transform_dropdown_value == '% of Population':
            population_gdf = prepare_gdf(city_data, 'population', None)
            transformer_gdf = population_gdf.loc[:, ['zipcode', 'population']]
            transformer_gdf['population'] = transformer_gdf['population'] / 100
        elif transform_dropdown_value == 'Density (per square mile)':
            land_area_gdf = prepare_gdf(city_data, 'land_area_in_sqmi', None)
            transformer_gdf = land_area_gdf.loc[:, ['zipcode', 'land_area_in_sqmi']]
        elif transform_dropdown_value == '% of Median Household Income':
            household_income_gdf = prepare_gdf(city_data, 'median_household_income', None)
            transformer_gdf = household_income_gdf.loc[:, ['zipcode', 'median_household_income']]
            transformer_gdf['median_household_income'] = transformer_gdf['median_household_income'] / 100

        transformer_gdf.columns = ['zipcode', 'transformer']

        #Merge two dataframes
        gdf = gdf.merge(transformer_gdf, on = 'zipcode', how = 'inner')
        gdf[variable_dropdown_value] = gdf[variable_dropdown_value] / gdf['transformer']

        #Drop transformer row from gdf
        gdf = gdf.drop('transformer', axis = 1)
        gdf = gdf.replace([np.inf, -np.inf], np.nan)
        gdf = gdf.dropna()

    #Get color map (based on variable selected in dropdown)
    colors = set_overlay_colors(gdf[variable_dropdown_value])

    #Set hover text (based on variable selected in dropdown)
    gdf['hover_text'] = 'Zipcode: ' + gdf['zipcode'] + '<br /> ' + variable_dropdown_value + ': ' + round(gdf[variable_dropdown_value], 1).astype(str)


    is_layer_visible = len(layer_checkbox_value) == 1

    #Layers: District polygons, each with different colors defined by color map
    layers=[{
        'name': 'Population',
        'sourcetype': 'geojson',
        'visible': is_layer_visible,
        'source': json.loads(gdf.loc[gdf.index == i, :].to_json()),
        'type': 'fill',   
        'color': colors[i],
        'opacity': layer_opacity_slider_value
        } for i in gdf.index]

    
    data = [go.Scattermapbox(
            lat=gdf['LAT'], 
            lon=gdf['LON'], 
            mode='markers', 
            marker={'opacity': 0},
            text=gdf['hover_text'], 
            hoverinfo='text', 
            name= 'Philadelphia Districts')]

    return {"data": data,
            "layout": go.Layout(
                autosize=True, 
                hovermode='closest', 
                showlegend=False, 
                height=700,
                mapbox={
                    'accesstoken': mapbox_access_token, 
                    'bearing': 0, 
                    'layers': layers,
                    'center': {'lat': gdf['LAT'][0], 'lon': gdf['LON'][0]}, 
                    'pitch': 0, 'zoom': 10,
                    "style": 'mapbox://styles/mapbox/streets-v10'
                    }
                )
            }


#CALLBACK 2: For multi-variables, sets the dropdown options that allow user to choose which level to display the choropleth map for.
@app.callback(
    [Output("multi_variable_levels_dropdown", "options"),
     Output("multi_variable_levels_dropdown", "value"),
     Output("multi_variable_levels_dropdown", "style"),],
    [Input('df_store', 'data'),
    Input('overlay_variable_dropdown', 'value')])
def set_levels_dropdown_options(df_store, variable_dropdown_value):

    #Load city data
    city_data = json.loads(df_store)

    #Check whether single or multi variable
    single_var, multi_var = sort_variables_by_type(city_data)

    if variable_dropdown_value in multi_var:

        levels = get_multi_var_levels(city_data, variable_dropdown_value)

        options = [{'label': titlecase(e), 'value': e} for e in levels]
        value = options[0]['value']
        
        return options, value, {'display': 'block'}
    
    else:
        return [], [], {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=False)