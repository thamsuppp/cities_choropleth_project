<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">PWBM Visualization Tool Project</a>
<ul>
<li><a href="#sec-1-1">Description</a></li>
<ul>
<li><a href="#sec-1-1-1">Aims</a></li>
</ul>
<li><a href="#sec-1-2">Installation</a>
<li><a href="#sec-1-3">Usage</a>
<ul>
<li><a href="#sec-1-3-1">Project structure</a></li>
<li><a href="#sec-1-3-2">Flask and Dash</a></li>
<li><a href="#sec-1-3-3">User Functions</a></li>
<li><a href="#sec-1-3-4">Code Structure</a></li>
<li><a href="#sec-1-3-5">In Progress</a></li>
</ul>
</li>
<li><a href="#sec-1-4">Notes</a></li>
<li><a href="#sec-1-5">Contributing</a></li>
<li><a href="#sec-1-6">Credits</a></li>
<li><a href="#sec-1-7">License</a></li>
</ul>
</li>
</ul>
</div>
</div>


# Dash Choropleth Map Project <a id="sec-1" name="sec-1"></a>


**Medium Article**

Para 1: Visualizing spatial data

Para 2: Introducing Dash
Plotly Dash is an excellent reactive framework in Python that allows you to make powerful interactive dashboards that enable users to interact with and understand data in whole new ways. It runs React.js under-the-hood  The visualizations utilize the Plotly visualization module which supports a wide range of plots, such as scatterplots, line graphs and even mapping. 

Para 3: USZipcode data

Another really powerful package that I was introduced to by a senior was USZipCode. It is a massive treasure trove of zipcode-level information - geographical: zipcode radius, area, demographics: population by age/gender/education, economic: income, median home prices. 

From what I understand, the data has not been updated since 2015, which is very unfortunate, but 2015 data is definitely still valuable in helping us understand spatial trends in American cities. 
It even includes a coordinate list that 


Para 4: Why?

My references:

Using Plotly Choropleth maps for state/county/country level
https://plot.ly/python/choropleth-maps/
Weaknesses:
Cannot import custom shapefiles/geometries and is hence inflexible for use cases such as zipcode level

https://plot.ly/~empet/14692/mapbox-choropleth-that-works-with-plotly/#/
Works using TOPOJson files, integrates counties with Plotly but not with Dash 

https://plot.ly/~jackp/18292.embed


The only example on the Internet so far of overlaying choropleth maps on Dash
https://github.com/ConnectedSystems/Dash-Choropleth-Example


Para 5: 





## Description<a id="sec-1-1" name="sec-1-1"></a>

### Aims<a id="sec-1-1-1" name="sec-1-3-1"></a>

**Public Goals**

1. Interactive visualization of spatial (and temporal) trends across zipcodes in cities across America - making data understandable and accessible to the public
2. This can be joined with so many other spatial scatterplot datasets to uncover many trends
3. To show the power of Plotly Dash and Mapbox interface

**Personal Goals**

1. Learn a valuable skill in creating interactive spatial visualizations that can be extended in so many ways
2. Personal project that I'm passionate about
3. Creating a blog post (first Medium post) about it to showcase my skills, develop communication and writing, and engage with other data scientists, urban geographers and economists

**Progress**
1. Improve map layout (7/12)
2. Checkbox to add and remove layers (7/13)
3. Slider to toggle opacity (7/13)
4. Displaying a color scale (7/13)
5. Dropdown of different variables (7/13)
6. Automatically detect possible variables in the cities list without hardcoding all of them (7/13)
7. For multi-variables, detect them, and another dropdown will automatically come out for the second variable (set first value by default) (7/24)
8. Add simple transformations of the data - e.g. over population, over land area (7/24)
9. Extend this to multiple cities - Using dataset of American cities and their zipcodes, allow for city search, which pulls the relevant zipcodes data, and draw the graph (7/24) (still fixing bugs)


**Long-term Goals**

1. Fix the bug involving incomplete polygon shapes
2. Add a checkbox of added variables that people can just check and uncheck 
3. Animations of the chloropleth values over time
4. Allow for users to input their own transformations on the variables
5. Regressions on the variables - compare correlations between cities - e.g. to see how strongly poverty is to crime rate in different cities
6. Compare cities - variance (inequality) of income/education?
7. Joining with scatterplot data:
	1. Crime incidents
	2. Restaurants (Yelp data) - average prices


## Installation<a id="sec-1-2" name="sec-1-2"></a>

The main code base is written in python 3.6. A list of required packages is included in the requirements.txt file.





## Usage<a id="sec-1-3" name="sec-1-3"></a>

### Project structure<a id="sec-1-3-1" name="sec-1-3-1"></a>



    +-- flask_app.py                    # Main flask framework (routes)
    +-- app1.py                         # Time-series Data (FRED) Dashboard
    +-- app2.pay                        # Cross-sectional/Panel Data Dashboard
    +-- SocialMedia.py                  # Package that connects to social media  
    +-- wsgi.py                         # DispatcherMiddleware
    +-- run.py                          # Runs the application
    +-- README.md                       # README file
    +-- requrements.txt                 # Required packages
    +-- templates                       # Contains website html pages
    ¦   +-- base.html                   # Navigation bar inherited by all webpages
    ¦   +-- index.html                  # Home Page
    ¦   +-- guide.html                  # Guide Page
    ¦   +-- about.html                  # About Page
    +-- static                          # Website's static files
    ¦   +-- css                         # CSS styling
    ¦   ¦   +-- bootstrap.min.css       # Bootstrap css
    ¦   ¦   +-- style.css               # Customized css 
    ¦   +-- images                      # Image files
    ¦   ¦   +--logo.png                 # Penn logo
    +-- assets                          # Dash apps' static files
    ¦   +-- btstrap.css                 # CSS styling
    ¦   +-- images                      # Image files for social media icons
  

    
### Flask and Dash<a id="sec-1-3-2" name="sec-1-3-2"></a>

Dash itself uses a Flask web framework under the hood. In this application, two Dash apps (app1.py and app2.py) are embedded into a Flask app using Werkzeug's DispatcherMiddleWare (wsgi.py).

| Apps | Description |
| --- | --- |
| ![Alt Text](assets/ezgif.com-video-to-gif.gif)| App1 is used for time-series analysis |
| ![Alt Text](assets/ezgif.com-optimize.gif) | App2 is used for cross-sectional and panel data analysis |

### User Functions <a id="sec-1-3-3" name="sec-1-3-3"></a>

Dash App 1:  
* Search for data (FRED API) and/or upload own data
    * Enter search term in searchbox and select time series from dropdown
    * Drag or select own data at top middle of page to upload 

### Code Structure <a id="sec-1-3-4" name="sec-1-3-4"></a>

**Layout**

1. Dropdown: overlay_variable_dropdown
2. Dropdown: multi_variable_levels_dropdown
3. Checkbox: layer_checkbox
4. Slider: layer_opacity_slider
5. Graph: map

**Helper Functions**

1. get_polygon
2. create_gdf
3. set_overlay_colors
4. set_variables_by_type
5. prepare_gdf
6. Working with Multi-variables:
    1. get_multi_var_df
    2. get_multi_var_df_all_districts
    3. get_multi_var_levels
    4. get_multi_var_level_df

**Callbacks**

1. update_figure
2. set_levels_dropdown_options




Concept Map of code base
(under construction)

### In Progress <a id="sec-1-3-5" name="sec-1-3-5"></a>

