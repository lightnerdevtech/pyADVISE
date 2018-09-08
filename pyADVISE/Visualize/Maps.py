# import packages
import os
import pandas as pd
import numpy as np

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
from bokeh.models import ColumnDataSource, Div, HoverTool, LabelSet, Label, Legend, LegendItem
from bokeh.plotting import figure

# import style 
import sys
package_path = 'C:/Users/alightner/Documents/Shared/'
sys.path.append(package_path)
from pyADVISE.Visualize.Themes.USAID_themes import USAID_style
pd.options.mode.chained_assignment = None
from bokeh.models import Range1d
from bokeh.models import LinearColorMapper, ColorBar, BasicTicker
from bokeh.tile_providers import CARTODBPOSITRON
import ast
from colour import Color


#######################################
### Functions #
####################################






def merge_geo_data(data, left_on=['country_id', 'country_name'], right_on=['country_id', 'country_name'], all_countries=True, detailed=False, 
                   file='C:/Users/alightner/Documents/Shared/', map_type='coords'): 

    ##### select data of interest 
    level = ''
    if detailed==True:
        level = '_detailed'
    
    # file location
    file_loc = file+'pyADVISE/Data/country_'+map_type+level+'.csv'
    
    # read the file which was cleaned and exported in the 'Gen_Map.ipynb'
    df_map = pd.read_csv(file_loc)

    # clean the data - lists were stored as strings. 
    for i, row in df_map.iterrows():

        # lat/long coordinates
        x = ast.literal_eval(row['x_coord'])
        y = ast.literal_eval(row['y_coord'])

        # add values to the dataset 
        df_map.set_value(i,'x_coord', x)
        df_map.set_value(i, 'y_coord', y)
    
    ### data ids as int 
    #data[right_on[0]] = data[right_on[0]].astype('int')
    
    # clean map data 
    df_map = df_map[df_map['country_id'].notnull()]
    # make integer
    df_map['country_id'] = df_map['country_id'].dropna().astype('int')
    
    # merge the df_map to the full dataset 
    # merge to df_map because some country have more than one shape (Japan, Indonesia)
    merged = pd.merge(df_map, data, left_on=left_on, right_on=right_on, how='inner')

        
    return merged







from colour import Color

def gen_map_choropleth_values(data, color_var='value_start', color_high='#550000', 
                              color_low='#FFAAAA', num_color_cats=20,  
                      map_type='OSM', plot_dim=(350,700), background_color='white', color_mapper=True, title_text='', 
                        font='Gill Sans MT', country_outline_color='white', fill_alpha=.7, 
                             line_width=1, hover=True, color_range='default',label_color='black'): 
    #################
    ### color palette 
    #################
    
    ### set first color 
    low = Color(color_low)
    # generate range from 1 to color 2
    colors = list(low.range_to(Color(color_high), num_color_cats))
    # access the html codes for the colors
    colors = [c.hex_l for c in colors]
    # generate color mapper using colors and given data
    if color_range=='default': 
        mapper = LinearColorMapper(palette=colors, low=min(list(data[color_var].unique())), high=max(list(data[color_var].unique())))
    else: 
        mapper = LinearColorMapper(palette=colors, low=color_range[0], high=color_range[1])

    ##################
    ### generate source data 
    ##################
    
    source = ColumnDataSource(data)
    
    
    #####################
    #### generate plot 
    ######################
    
    ## set ranges depending on OSM selection 
    y_range=(-55,78); x_range=(-125,185); 



    if map_type=='OSM':
        p = figure(
            title=title_text, plot_width=plot_dim[1], plot_height=plot_dim[0],
                x_range=(-13000000, 20500000), y_range=(-6000000, 7000000),
            x_axis_location=None, y_axis_location=None, background_fill_color=background_color,
                x_axis_type="mercator", y_axis_type="mercator", tools='save,tap,reset')
        # add tile
        p.add_tile(CARTODBPOSITRON)
    
    
    else: 
        # generate figure 
        p = figure(title=title_text, plot_width=plot_dim[1], plot_height=plot_dim[0],
        x_axis_location=None, y_axis_location=None,background_fill_color = background_color,
            y_range=(y_range[0],y_range[1]), x_range=(x_range[0],x_range[1]), tools='save,tap,reset', logo=None)


    #### Plot data
    p.grid.grid_line_color = None

        
        
    # generate patches 
    r = p.patches('x_coord', 'y_coord', source=source, line_alpha=.5,
                fill_color={'field': color_var, 'transform': mapper},
                fill_alpha=fill_alpha, line_color=country_outline_color, 
                line_width=line_width, 
               
               # set hover_tool properties
                hover_line_color={'field': color_var, 'transform': mapper}, 
                hover_line_alpha=1, 
                hover_fill_color={'field': color_var, 'transform': mapper},
              
               # set visual properties for selected glyphs
               selection_fill_color={'field': color_var, 'transform': mapper},
               selection_line_color={'field': color_var, 'transform': mapper},
               selection_fill_alpha = 1, 
                  
               # set visual properties for non-selected glyphs
               nonselection_fill_alpha=0.5,
               nonselection_fill_color={'field': color_var, 'transform': mapper},
               nonselection_line_color="white",
               nonselection_line_alpha=.5)
    
    ######################
    ### add hover and mapper 
    ######################

    TOOLTIP ="""
    <div style="padding: 0px;"> 

        <div>
            <span style="font-size: 12px; font-family: 'Gill Sans MT', sans-serif; color: black;"><b>@country_name: </b>@value_start{0.0}</span>
        </div>
    </div>
    """
    
    if hover ==True:
        
        hover_circle = HoverTool(
            renderers=[r],
            tooltips=TOOLTIP, 
            point_policy='follow_mouse'
        )
        p.add_tools(hover_circle)

    # mapper
    if color_mapper == True: 
        color_bar = ColorBar(color_mapper=mapper, major_label_text_font_size="10pt",
                     ticker=BasicTicker(desired_num_ticks=5), orientation='vertical',
                     label_standoff=6, border_line_color=None, location=(0, 0), width=10, 
                    major_label_text_font = font, background_fill_color = background_color, 
                    major_label_text_color=label_color)
        p.add_layout(color_bar, 'right')
    
    ##########
    ### style setting s
    ##########
    
    p = USAID_style(p, font=font)
    
    p.grid.grid_line_alpha=.1
    
    return p







def gen_map_country(country_sel, color, color_var='value_start', color_high='#550000', 
                              color_low='#FFAAAA', num_color_cats=20,  map_type='coords', 
                      OSM=False, plot_dim=(350,700), background_color='white', color_mapper=True, 
                        font='Gill Sans MT', country_outline_color='white', fill_alpha=.7, 
                             line_width=1, hover=True, color_range='default', 
                           file='C:/Users/alightner/Documents/Shared/'): 
    
    
    
    # read the file which was cleaned and exported in the 'Gen_Map.ipynb'
    df_map = pd.read_csv(file+'pyADVISE/Data/country_'+map_type+'_detailed.csv')
    
    # select country 
    df_map = df_map[df_map['country_id']==country_sel]
    
    # clean the data - lists were stored as strings. 
    for i, row in df_map.iterrows():

        # lat/long coordinates
        x = ast.literal_eval(row['x_coord'])
        y = ast.literal_eval(row['y_coord'])

        # add values to the dataset 
        df_map.set_value(i,'x_coord', x)
        df_map.set_value(i, 'y_coord', y)
        
    ##################
    ### generate source data 
    ##################
    
    source = ColumnDataSource(df_map)
    
    
    #####################
    #### generate plot 
    ######################
    
    ## set ranges depending on OSM selection  
    if map_type == 'OSM': 
        p = figure(
            title="Practice Map", plot_width=990, plot_height=500,
            x_axis_location=None, y_axis_location=None, background_fill_color =background_color,
                x_axis_type="mercator", y_axis_type="mercator", tools="save", logo=None)
                               
    else: 
        
        # generate figure 
        p = figure(title="Practice Map", plot_width=plot_dim[1], plot_height=plot_dim[0],
        x_axis_location=None, y_axis_location=None, background_fill_color = background_color,
                   tools='save,tap,reset', logo=None)


    
    # generate patches 
    r = p.patches('x_coord', 'y_coord', source=source,
                fill_alpha=fill_alpha, line_color=country_outline_color, 
                line_width=line_width)
    
    ######################
    ### add hover and mapper 
    ######################

    TOOLTIP ="""
    <div style="padding: 10px;"> 

        <div>
            <span style="font-size: 12px; font: 'Gill Sans MT'; color: #002F6C;"><b>@country_name: </b></span>
        </div>
    </div>
    """
    
    if hover ==True:
        
        hover_circle = HoverTool(
            renderers=[r],
            tooltips=TOOLTIP
        )
        p.add_tools(hover_circle)
    
    
    ##########
    ### style setting s
    ##########
    
    p = USAID_style(p, font=font)
    p.grid.grid_line_alpha = 0
    
    return p





def add_cities(p, country_id, map_type='coord', file='C:/Users/alightner/Documents/Shared/', 
               fill_alpha=.5, fill_color='blue', line_color='white', line_width=2, hover=True): 
    
    
    cities = pd.read_csv(file+'pyADVISE/Data/cities_detailed.csv')
    
    cities = cities[cities['country_id']==country_id]
    
    source = ColumnDataSource(cities)
    print(source.data)
    
    if map_type=='OSM':
        r = p.circle('x_coord_OSM', 'y_coord_OSM', source=source, fill_alpha=fill_alpha, fill_color=fill_color, 
            line_color=line_color, line_width=line_width)
    else:
        r = p.circle('x_coord', 'y_coord', source=source, fill_alpha=fill_alpha, fill_color=fill_color, 
            line_color=line_color, line_width=line_width)
    ######################
    ### add hover and mapper 
    ######################

    TOOLTIP ="""
    <div style="padding: 10px;"> 

        <div>
            <span style="font-size: 12px; font: 'Gill Sans MT'; color: #002F6C;"><b>@city_name, @country_name</b></span>
        </div>
    </div>
    """
    
    if hover ==True:
        
        hover_circle = HoverTool(
            renderers=[r],
            tooltips=TOOLTIP
        )
        p.add_tools(hover_circle)
    
    
    return p 