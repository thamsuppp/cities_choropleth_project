<div id="table-of-contents">
<h2>Table of Contents</h2>
<div id="text-table-of-contents">
<ul>
<li><a href="#sec-1">Dash Choropleth Map Project</a>
<ul>
<li><a href="#sec-1-1">Description</a></li>
<li><a href="#sec-1-2">Installation</a></li>
</ul>
</ul>
</div>
</div>


# Dash Choropleth Map Project <a id="sec-1" name="sec-1"></a>

I love geography. Maps have fascinated me since young, and I love analyzing trends across space, particularly in the cities. As an international student coming to study in America, I definitely brought many preconceived notions about urban spatial patterns that I slowly discovered were totally different in America.

While learning about data science, I was introduced to an amazing Python package called USZipcode (https://pypi.org/project/uszipcode/). With just one function call through the API, you can obtain a treasure trove of information about any zipcode in the US. The information was geographical: zipcode radius, area and boundary coordinates, demographic: population by age/gender/race/education, and economic: income, median home prices, all scraped from various data sources and collated neatly into JSON format. Surprisingly, there has not been much attention given to this awesome package in the Towards Data Science community, incorporating it into a mapping project to visualize the immense amount of data available. (a quick Google search only yielded this one article (https://towardsdatascience.com/mapping-inequality-in-peer-2-peer-lending-using-geopandas-part-1-b8c7f883d1ba). From what I understand, the data has not been updated since 2015, which is very unfortunate, but 2015 data is definitely still valuable in helping us understand spatial trends in American cities, such as the distribution of income, property prices and racial segregation.

Plotly Dash is an excellent reactive framework in Python that allows you to make interactive dashboards that enable users to interact with and understand data in whole new ways. It runs React.js under-the-hood so users can access its powerful interactive capabilities without needing to code a single line of JavaScript. The visualizations utilize the Plotly visualization module which supports a wide range of plots, such as scatterplots, line graphs and even mapping. Having used Dash for month on a summer internship project, I found Dash to be the perfect tool to implement an interactive city data dashboard. This will not be a comprehensive tutorial on Dash, if you’re looking to get started, Dash has a really detailed User Guide as well as many Towards Data Science posts on Dash such as this (https://towardsdatascience.com/how-to-build-a-complex-reporting-dashboard-using-dash-and-plotl-4f4257c18a7f).

Plotly does have fantastic state and county level choropleth mapping tools, but there have been few attempts to incorporate choropleth map data at a zipcode level into Plotly, especially with custom shape files and geometries. The only example I’ve seen of overlaying choropleth maps on Dash is this (https://github.com/ConnectedSystems/Dash-Choropleth-Example), but it does not attempt to dynamically change the overlay’s data using callbacks.

The purposes of publishing my project are threefold: Firstly, by visualizing these spatial data, it makes urban trends more understandable and it is my hope that it will make the public acutely aware of issues such as inequality and segregation. Secondly, I wanted to showcase the power of Dash and the Mapbox interface to create amazing visualizations. Thirdly, I hope that my project can be a spark for many other spatial data visualization projects in the future (ideas for which I will touch on at the end), especially as overlaying a choropleth and scatterplot on a city map can be so informative.





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

The main code base is written in python 3.6. 

