# import packages
import os
import pandas as pd
import numpy as np
from collections import Counter
from math import pi
from bokeh.transform import cumsum


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
from bokeh.models import ColumnDataSource, Div, HoverTool, LabelSet, Label, Legend, LegendItem

from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.io import output_notebook, show

pd.options.mode.chained_assignment = None

# import themes from within the directory
from pyADVISE.Visualize.Themes.USAID_themes import USAID_style
from pyADVISE.Visualize.General import empty_plot

 
 
    
    
    
    
    
    
    
# Function which stacks area charts
def  stacked(df):
    df_top = df.cumsum(axis=1)
    df_bottom = df_top.shift(axis=1).fillna({'yy0': 0})[::-1]
    df_stack = pd.concat([df_bottom, df_top], ignore_index=True)
    return df_stack








##################################################################
##################################################################
#############       Stacked Area Plot 
##################################################################
##################################################################


def gen_area_stack(data, areas_sel, focus_sel, year_sel=(2000,2017), areas_var='series_id', 
                   focus_var='country_id', value_var='value_start', year_var='year', font="Gill Sans MT", 
                  prop=False, colors='default', title_text = 'Area Chart', fill_alpha =.5, 
                  area_labels = ['default'], plot_dim=(350, 550), scale=1, no_tools=False, print_details=False):
    
    
    ########################
    ### Set color scheme 
    palette = {'USAID Blue': '#002F6C', 'Medium Blue': '#0067B9','Light Blue': '#A7C6ED', 
               'Light Gray': '#CFCDC9', 'USAID Red': '#BA0C2F','Dark Red': '#651D32', 
               'Medium Gray': '#8C8985', 'Rich Black': '#212721',  
               'Dark Gray': '#6C6463'}


    
    if colors == 'default': 
        colors = list(palette.keys())
        
    ###############################
    ####   select observations (countries) and variables 
     
    data = data[data[focus_var]==focus_sel[0]]
    data = data[data[areas_var].isin(areas_sel)]
    data = data[data[year_var].between(year_sel[0], year_sel[1])]

    # sort values on year
    # length of dataset at pivot 
    detail_1 = len(data)
    ## detail 3: data
    detail_2 = data
    
    
    # sort values on year
    # length of dataset at pivot 
    detail_1 = len(data)
    ## detail 3: data
    detail_2 = data
    
    
    
    # rename series_ids to thier order in the list 
    for i in range(0, len(areas_sel)): 
        data.loc[data[areas_var]==areas_sel[i], areas_var] = i
    data.sort_values([areas_var, year_var], inplace=True)
    #print(data)
    
    # try, catch if insufficient data
    try:
        ################################
        ###   Change data into panel 
        ################################

        # select only the data we need
        data = data[[focus_var, areas_var, year_var, value_var]]
        # shift data into panel format 
        data = data.pivot_table(values=value_var, index=[focus_var, year_var], 
                                            columns=areas_var, aggfunc=np.sum).reset_index()

        # drop focus var (no longer needed)
        data.drop(focus_var, axis=1, inplace=True)
        # sort on year_var, drop missing values
        data = data.sort_values(year_var).dropna()

        # select the min and max year for the plot 
        years = (data[year_var].min(), data[year_var].max())

        # set index to year 
        data.set_index(year_var, inplace=True)


        #################################
        ##### Proportion or normal stack
        #################################


        if prop==True: 

            num = data[list(range(0, len(areas_sel)))].sum(axis=1).to_frame()

            # generate a sum variable 
            data['total'] = data[list(range(0, len(areas_sel)))].sum(axis=1)
            # replace variable values with the proportions 
            for i in list(range(0, len(areas_sel))):
                data[i] = data[i]/data['total']*100
            #drop total when finished 

            data.drop('total', inplace=True, axis=1)

        # change all variable names to an iterable (y0, y1, etc)
        ys = ['yy'+str(i) for i in range(0, len(areas_sel))]
        data.columns = ys

        ####################################
        ##### Generate Area Plot 


        # generate the numeric basics of the plot for input into patches 
        areas = stacked(data)

        # generate a max value for the y axis position
        max_value = np.nanmax(areas.values)
        max_value = np.round(max_value, 0) 
        max_value = int(max_value)
        
        ## detail 2: max value  
        detail_2 = max_value
        


        ##############################################
        ### generate y_range if prop ==True
        ###############################################

        #### scale plot 
        plot_dim = (plot_dim[0]*scale, plot_dim[1]*scale)


        ######## Try to make the plot, if fail due to value error (insufficient data), 
        ######## send back empty plot which starts that there is no data. 

        if prop ==True: 
            p = figure(x_range=years,y_range=(0, 100), plot_height=plot_dim[0], plot_width=plot_dim[1])
        else: 
            p = figure(x_range=years, y_range=(0, max_value),  plot_height=plot_dim[0], plot_width=plot_dim[1]) 


        ### generate the stack coordinates 
        x2 = np.hstack((data.index[::-1], data.index))

        # plot the patches 
        p.patches([x2] * areas.shape[1], [areas[c].values for c in areas],
                  color=[palette[i] for i in colors], fill_alpha=fill_alpha, line_width=3*scale) 


        # generate the hover line 
        source = ColumnDataSource(data)
        p.line(x='year', y='yy0',source=source, color=palette['USAID Blue'], line_width=.2)

        #######################################
        ### Generate the Legend and Hover
        #######################################

        if area_labels  == ['default']: 
            names = [str(i) for i in areas_sel]
        else: 
            names = area_labels 
        labels = []

        # iterate over the areas and plot the visual 
        for i, area in enumerate(areas):
            # save the meta data from each p in [r]
            r = p.patch(x2, areas[area], color=palette[colors[i]], alpha=0.8, line_color=None)
            # generate a seperate label based on the r meta data. 

            labels.append(LegendItem(label=dict(value=names[i]), renderers=[r]))

        # plot the legend on the right of the plot 
        legend = Legend(items=labels, location=(0, 10), orientation='horizontal')
        p.add_layout(legend, 'above')


        ########### Hover 
        tooltips1 = []
        for i in range(0, len(areas_sel)): 
                tip = (names[i], '@'+'yy'+str(i)+'{0.00 a}')
                tooltips1.append(tip) 


        hover = HoverTool(
        tooltips=tooltips1,
        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline')

        p.add_tools(hover)

        p = USAID_style(p, font=font)

        p.title.text = title_text
        p.legend.background_fill_alpha = 0
        p.legend.border_line_color=None
        p.xgrid.visible = True
        p.legend.glyph_height = 30
        p.legend.glyph_width= 30

        ######## drop tools if prompted 
        if no_tools==True: 
            p.toolbar.logo = None
            p.toolbar_location = None
            
        if print_details == True: 
            print('The length of the dataset')
            print(detail_1)
            print('The max value of the dataset')
            print(detail_2)
            print('The dataset')
            print(detail_3)
        
    except: 
        plot_dim = (plot_dim[0]*scale, plot_dim[1]*scale)
        p = empty_plot(plot_dim, title=title_text, scale = scale)
        
        # print details if asked. 
        if print_details == True: 
            print('The length of the dataset')
            print(detail_1)
            print('Dataset to plot:')
            print(detail_2)

    return p
    
    
    

    
########################################
#### Generate pie chart 
#########################################



def gen_counter(data, key_var, value_var, agg_option='sum'): 
    '''Define function to generate dictionary for Counter in the pie chart. 
    the function takes a data source with two columns - the column which will 
    be the keys of the Counter dictionary and the value_var which will be the 
    values as standalone floats. 
    
    *** choose the aggregation option if the key_var is not unique: options are to 
    sum the values or average the values.'''
    
    # generate the counts dataset using the groupby() function and .sum() if 'sum'
    if agg_option =='sum':
        counts = data.groupby(key_var).sum().reset_index()
    elif agg_option =='mean':
        counts = data.groupby(key_var).mean().reset_index()
        counts[value_var] = np.round(counts[value_var], 1)
    else: 
        print('Invalid agg_options value.')
    
    
    # generate numpy array of values for keys and values variables 
    keys = counts[key_var].values
    values = counts[value_var].values
    
    # use dict comprehension to generate counter dict 
    counter_dict = {keys[i]: values[i] for i in range(0,len(keys))}
    
    
    return counter_dict


def gen_pie(data, cat_sel = [], focus_sel = [], cat_labels = [], cat_var='series_id', 
            focus_var='country_id', value_var='value_start', 
           agg_option='sum', title_text='Pie Chart', fill_alpha=0.5, font='Gill Sans MT', 
           print_details=False, plot_dim=(500, 500),  scale=1, no_tools=False, 
            legend_location='top_right', line_color='white', line_width=3, 
           legend_orientation='vertical'): 
    
    
    
    '''Generate a pie chart given a data selection, cat_sel refers to the categories 
    which will be divided within the pie chart (the colors of the pie), value_var_name
    is the column which will determine the proportion of the pie. obs_sel will determine
    the country or region observations selected (these will be averaged or summed 
    dependending of the agg_option selection). The plot returns a pie chart.'''
    
    ##################################
    ##### generate the underlying data
    ##################################
    
    # select the categories and observations of interest
    data = data[data[cat_var].isin(cat_sel) &
               data[focus_var].isin(focus_sel)]
    
    # for each category 
    for i in range(0, len(cat_labels)): 
        # replace the cat_var with the category name
        data.loc[data[cat_var]== cat_sel[i], cat_var] = cat_labels[i];
    
    # generate the counter dictionary
    counter_dict = gen_counter(data, cat_var, value_var, agg_option)
    
    # use the counter function to generate x for the plot
    x = Counter(counter_dict)
     
    # place 'x' into a dataframe called data (replace the old data for efficiency)
    data = pd.DataFrame.from_dict(dict(x), orient='index').reset_index().rename(index=str, columns={0:'value', 'index':'category'})
    
    # generate the angle of each slice
    data['angle'] = data['value']/sum(x.values()) * 2*pi
    
    # add colors based on USAID color scheme         
    palette = {'USAID Blue': '#002F6C', 'USAID Red': '#BA0C2F', 'Rich Black': '#212721', 'Medium Blue': '#0067B9',
        'Light Blue': '#A7C6ED', 'Dark Red': '#651D32', 'Dark Gray': '#6C6463', 'Medium Gray': '#8C8985', 'Light Gray': '#CFCDC9'}
    # select colors based on the length of 
    #### decide whether this should fail or not if there are missing values in the cat_sel 
    #### this will fail in its curren state (address later...)
    data['color'] = [palette[i] for i in list(palette.keys())[0:len(cat_sel)]]

    ### detail_1 = dataset 
    detail_1 = data
    
    #### scale plot
    plot_dim = (plot_dim[0]*scale, plot_dim[1]*scale)
    line_width = line_width*scale 
    
    try: 
       
        ####################################
        ###### Generate the plot 
        ####################################

        # generate figure with simple tooltip (need to add style later)
        p = figure(plot_height=plot_dim[0], plot_width=plot_dim[1], title=title_text, 
                   tools="save,hover", tooltips="@category: @value{0.0}")

        # generate the wedges for the pie chart. 
        p.wedge(x=0, y=1, radius=0.4,
                start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                line_color=line_color, line_width=line_width,
                fill_color='color', fill_alpha=0.9,legend='category', source=data)

        # basic formatting of the chart. 
        p.axis.axis_label=None
        p.axis.visible=False
        p.grid.grid_line_color = None
        
        p = USAID_style(p, font=font)
        
        p.legend.orientation = legend_orientation
        
        if legend_location =='outside': 
            p.legend.location = 'center'
            new_legend = p.legend[0]
            p.legend[0].plot = None
            p.add_layout(new_legend, 'right')

        else:
            p.legend.location = legend_location


        ######## drop tools if prompted 
        if no_tools==True: 
            p.toolbar.logo = None
            p.toolbar_location = None
            
            
        # print details if asked. 
        if print_details == True: 
            print('The dataset:')
            print(detail_1)
    
    except: 
        plot_dim = (plot_dim[0]*scale, plot_dim[1]*scale)
        p = empty_plot(plot_dim, title=title_text, scale = scale)
        
        # print details if asked. 
        if print_details == True: 
            print('The dataset:')
            print(detail_1)
    
    return p


