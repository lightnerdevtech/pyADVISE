########################################################
####  This generages the pyADVISE visualize package
########################################################

# import packages
import os
from math import pi
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Div, HoverTool, LabelSet, Label, Legend, LegendItem
from bokeh.plotting import figure, show
from bokeh.core.properties import value
from bokeh.transform import dodge


# new packages for the pyADIVSE package 
from bokeh.transform import factor_cmap


# import themes from within the directory
from pyADVISE.Visualize.Themes.USAID_themes import USAID_style

# bring in empty plot 
from pyADVISE.Visualize.General import empty_plot







#####################################################
#####################################################
#### STACKED BAR
####################################################
#####################################################


def gen_stacked_bar(data, cat_sel, stacked_sel, stacked_labels, cat_labels, cat_var='country_id', stacked_var='series_id', 
                              value_var='value_start', colors = 'default', x_axis_label='', y_axis_label='', 
                              title_text='stacked bar', orientation='x-axis', fill_alpha=0.8, line_width=2, 
                               plot_dim=(300,500), year_sel=(2016, 2017), year_var='year', scale=1, 
                               legend_location='center', bar_gap =0.4, prop=False, no_tools=False,  major_label_orientation='horizontal', 
                               print_details=False, font='Gill Sans MT'): 
    
    '''This function generates a stacked bar given data and three variables in long form. The 
    user can also choose whether the stack is vertical or horizontal in orientation. '''
    
    palette = {'USAID Blue': '#002F6C', 'Medium Blue': '#0067B9',  'Light Blue': '#A7C6ED', 'Medium Gray': '#8C8985', 'Light Gray': '#CFCDC9', 
               'USAID Red': '#BA0C2F', 'Rich Black': '#212721', 'Medium Blue': '#0067B9',
    'Light Blue': '#A7C6ED', 'Dark Red': '#651D32', 'Dark Gray': '#6C6463', 'Medium Gray': '#8C8985', 'Light Gray': '#CFCDC9'}
    
    # select only the observations of interest
    data = data[(data[cat_var].isin(cat_sel))]
    data = data[data[stacked_var].isin(stacked_sel)]
    data = data[data[year_var].between(year_sel[0], year_sel[1])]
    
    
    for i in range(0, len(cat_sel)): 
        data.loc[data[cat_var] == cat_sel[i], cat_var] = cat_labels[i]
    
    # generate the lists for labels 
    bars=list(data[cat_var].unique())
    stacks = [str(i) for i in stacked_sel]
    
    if colors == 'default': 
        colors = list(palette.values())[0:len(stacks)]

        
        
    # generate the dictionary of data points 
    d = {'bars': bars}
    

    
    for i in range(0, len(stacks)): 
        d[stacked_labels[i]] = list(data[data[stacked_var]==int(stacks[i])][value_var].values)
  
    

    #############################
    #### Adjust indicators to equal 100 if prop plot
    #############################
    
    # generate dataset of values 
    values_dict = {i: d[i] for i in stacked_labels}
    values_df = pd.DataFrame(values_dict)
    values_df['total'] = values_df[stacked_labels].sum(axis=1)
    
    
    
    
    # length of dataset at pivot 
    detail_1 = len(values_df)
    ## detail 3: data
    detail_3 = values_df
    
    #################################
    ##### Proportion or normal stack
    #################################
    
    # try, catch if insufficient data
    try:

        # if we want to turn into a proportion chart. 
        if prop==True: 

            # alter values to proportion 
            # generate a sum variable 
            values_df['total'] = values_df[stacked_labels].sum(axis=1)
            # replace variable values with the proportions 
            for i in stacked_labels:
                values_df[i] = values_df[i]/values_df['total']*100
            #drop total when finished 
            values_df.drop('total', inplace=True, axis=1)


            # return to dictionary as d

            d = {stacked_labels[i]: values_df.iloc[0].tolist() for i in range(0, len(stacked_labels))}

            # place bars back into the dataset.
            d['bars'] = bars

        # generate a max value for the y axis position 
        ### gen dataframe 
        max_value = np.nanmax(values_df.values) + .05*np.nanmax(values_df.values)
        max_value = np.round(max_value, 0) 
        max_value = int(max_value)

        ## detail 2: max value  
        detail_2 = max_value

        #############################
        # generate the plot 
        ##############################

        #### scale plot 
        plot_dim = (plot_dim[0]*scale, plot_dim[1]*scale)
        line_width = line_width*scale 

        # legend titles because they cannot be perfectly the same as the label names, we add a space to the end 
        legend_names = [i+' ' for i in stacked_labels]


        ###### Generate the figure
        if prop ==True: 
            p = figure(x_range=bars,y_range=(0, 100), plot_height=plot_dim[0], plot_width=plot_dim[1])
        else: 
            p = figure(x_range=bars, y_range=(0, max_value),  plot_height=plot_dim[0], plot_width=plot_dim[1]) 


        # generate stack
        if orientation=='x-axis' : 
            p.vbar_stack(stacked_labels, x='bars', width=bar_gap, line_width=line_width, color=colors, source=d, fill_alpha=fill_alpha, legend=legend_names)
        else:
            print('y-axis plot in construction.')


        #######################
        ###### hover tool 
        #######################

        tooltips = [(i, '@'+i+'{0.0}') for i in stacked_labels]

        tooltips = HoverTool(
        tooltips=tooltips, 
        mode = 'mouse',
        point_policy = 'follow_mouse'
        )
        p.add_tools(tooltips)


        ######################
        #### style choices
        ######################


        p = USAID_style(p, font=font)

        p.yaxis.visible = True  
        p.xaxis.visible = True


        if major_label_orientation !='horizontal': 
            p.xaxis.major_label_orientation = pi / 2.5

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
    
    except: 
        plot_dim = (plot_dim[0]*scale, plot_dim[1]*scale)
        p = empty_plot(plot_dim, title=title_text, scale = scale)
        
        # print details if asked. 
        if print_details == True: 
            print('The length of the dataset')
            print(detail_1)
            print('The max value of the dataset')
            print(detail_2)
            print('The dataset')
            print(detail_3)
        
    return p


#####################################################
#####################################################
#### Grouped BAR
####################################################
#####################################################




def gen_grouped_bar(data, cat_var_member, cat_var_group, value_var ='value_start', 
                    cat_var_member_name='series_name', cat_var_group_name='country_id', 
                   title_text='Grouped Bar - Example', line_width=3, fill_alpha=.5, 
                   plot_dim=(300, 800), scale=1, no_tools=False, major_label_orientation='horizontal', font='Gill Sans MT'): 
    ''' this function generated a group bar chart where the the cat_var_member data are 
    nested under the group variables, colored by group variables. Can change which varaibles refer to 
    the group var and the member by changing the (*name) varialbes'''
    
    
    ########################
    #### prep data 
    ########################

    # select the data of interest
    data = data[data[cat_var_member_name].isin(cat_var_member) &
               data[cat_var_group_name].isin(cat_var_group)]
    
    
    # make sure cat_vars are strings types (object)
    data[cat_var_member_name] = data[cat_var_member_name].astype(str)
    data[cat_var_group_name] = data[cat_var_group_name].astype(str)
    
    # generate groupby 
    group = data.groupby((cat_var_group_name, cat_var_member_name))

    ###### generate palette 
    palette = {'USAID Blue': '#002F6C', 'USAID Red': '#BA0C2F', 'Rich Black': '#212721', 'Medium Blue': '#0067B9',
    'Light Blue': '#A7C6ED', 'Dark Red': '#651D32', 'Dark Gray': '#6C6463', 'Medium Gray': '#8C8985', 'Light Gray': '#CFCDC9'}
    palette = [palette[i] for i in list(palette.keys())[0:len(cat_var_group)]]
    
    
        
    # generate factor_cmap based on the group member (the name can be anything - just referable)
    name = cat_var_group_name + '_'+ cat_var_member_name
    index_cmap = factor_cmap(name, palette=palette, factors=sorted(data[cat_var_group_name].unique()), end=1)
    
    name_tip= '@'+name
    value_tip = '@'+value_var+'_mean{0.0}'
    ##########################
    ##### Generate plot 
    ##########################
    
    #### scale plot 
    plot_dim = (plot_dim[0]*scale, plot_dim[1]*scale)
    line_width = line_width*scale 
    
    
    # generate figure 
    p = figure(plot_width=plot_dim[1], plot_height=plot_dim[0], title="Mean MPG by # Cylinders and Manufacturer",
           x_range=group, toolbar_location=None, tooltips=[('Category: ', name_tip), 
                                                           ('Value: ', value_tip)])
    
    
    # generate bar graph
    p.vbar(x=name, top=value_var+'_mean', width=.8, source=group,
           color=index_cmap, line_width=line_width,fill_alpha=fill_alpha)
        
    ##########################
    #### style the plot 
    ##########################
    
    p.y_range.start = 0
    p.x_range.range_padding = 0.05
    p.xgrid.grid_line_color = None
    p.xaxis.major_label_orientation = 1.2
    p.outline_line_color = None
    
    p = USAID_style(p, font=font)
    
    ## title 
    p.title.text_font_size= '15pt'
    p.title.text = title_text   
    
    if major_label_orientation !='horizontal': 
        p.xaxis.major_label_orientation = pi / 2.5
    ######## drop tools if prompted 
    if no_tools==True: 
        p.toolbar.logo = None
        p.toolbar_location = None
        
        
    return p


    



#####################################################
#####################################################
####   MULTI BAR
####################################################
#####################################################




### Generate (janky) spacing algorithm for bar charts
def spacing_alg(C_list):
    if len(C_list)>3:
        b = -.28-(.8/len(C_list))
        spacing = []
        for i in range(0,len(C_list)):
            b = b+(.8/len(C_list))
            spacing = spacing+[b]
    if len(C_list)==3:
        spacing = [-.25, 0, .25]
    if len(C_list)==2:
        spacing = [-.15, .15]
    if len(C_list)==1:
        spacing = [0]
    return spacing


def gen_multi_bar(data, obs_sel, cat_sel, cat_labels, obs_labels, obs_var='country_id', cat_var='series_id', 
                              value_var='value_start', colors = 'default', x_axis_label='', y_axis_label='', 
                              title_text='Multiple bar', plot_orientation='vertical', fill_alpha=0.8, line_width=2, 
                               plot_dim=(300,500), year_sel=(2016, 2017), year_var='year', scale=1, legend_orientation='vertical', 
                               legend_location='center', bar_width =0.2, major_label_orientation='horizontal',  print_details=False, font='Gill Sans MT'): 
    
    '''This function generates a multi bar given data and three columns in long form. The 
    user can also choose whether the stack is vertical or horizontal in orientation. '''
    
    
    palette = {'USAID Blue': '#002F6C', 'Medium Blue': '#0067B9',  'Light Blue': '#A7C6ED', 'Medium Gray': '#8C8985', 'Light Gray': '#CFCDC9', 
               'USAID Red': '#BA0C2F', 'Rich Black': '#212721', 'Medium Blue': '#0067B9',
    'Light Blue': '#A7C6ED', 'Dark Red': '#651D32', 'Dark Gray': '#6C6463', 'Medium Gray': '#8C8985', 'Light Gray': '#CFCDC9'}
    
    # select only the observations of interest
    data = data[(data[obs_var].isin(obs_sel)) & 
               (data[cat_var].isin(cat_sel)) &
               (data[year_var].between(year_sel[0], year_sel[1]))]
    
    #####################
    ### deal with missings 
    ######################
    
    # replace all obs_sel with obs_labels 
    for i in range(0, len(obs_sel)): 
        data.loc[data[obs_var] == obs_sel[i], obs_var] = obs_labels[i]

    # generate dataframe unqiue for cat_var and obs_var
    a = []
    for i in obs_labels: 
        for f in cat_sel: 
            a.append((i, f))        
    df = pd.DataFrame(a)
    df.columns = [obs_var, cat_var]

    # merge in data_small 
    data = pd.merge(df, data, on=[obs_var, cat_var], how='left')

    # replace missing with zero 
    data = data.fillna(0)
    

    
    #####################
    ### prep data for visual  
    ######################

    
    # generate the lists for labels 
    observations =list(data[obs_var].unique())
    categories = [str(i) for i in cat_sel]
    
    if colors == 'default': 
        colors = list(palette.values())[0:len(categories)]

        
        
    # generate the dictionary of data points 
    d = {'obs': observations}

    # for each category 
    for i in range(0, len(categories)): 
        # place the values of this category in a dictionary of its name. 
        d[cat_labels[i]] = list(data[data[cat_var]==int(categories[i])][value_var].values)
        
    # detail 1 is the dictionary 
    detail_1 = d

    # try to generate the plot: 
    try:

        
        # make into dataframe, add to Colomn source list 
        df_final = pd.DataFrame(d)    
        source = ColumnDataSource(df_final)
     

        # generate max vlaue to we can start the plot at zero 
        values_df = df_final.drop('obs', axis=1)
        max_value = np.nanmax(values_df.values) + .05*np.nanmax(values_df.values)
        max_value = np.round(max_value, 0) 
        max_value = int(max_value)



        #############################
        # generate the plot 
        ##############################

        #### scale plot 
        plot_dim = (plot_dim[0]*scale, plot_dim[1]*scale)
        line_width = line_width*scale 

        # legend titles because they cannot be perfectly the same as the label names, we add a space to the end 
        legend_names = [i+' ' for i in cat_labels]

        # generate the spacing between the plots 
        spacing = spacing_alg(categories)



        if plot_orientation=='vertical': 

            # generate figrue
            p = figure(x_range=observations, y_range=(0, max_value), plot_height=plot_dim[0], plot_width=plot_dim[1],
               toolbar_location=None, title=title_text)

            # place bars
            for i in range(0, len(categories)): 
                p.vbar(x=dodge('obs', spacing[i], range=p.x_range), top=cat_labels[i], width=bar_width, source=source, fill_alpha=fill_alpha, line_width=line_width, 
                       color=colors[i], legend=value(legend_names[i]))
        else: 
            # generate figure
            p = figure(y_range=observations, x_range=(0, max_value),plot_height=plot_dim[0], plot_width=plot_dim[1],
               toolbar_location=None, title=title_text)      

            # place bars
            for i in range(0, len(categories)): 
                p.hbar(y=dodge('obs', spacing[i], range=p.y_range), right=cat_labels[i], height=bar_width, left=0, source=source,  fill_alpha=fill_alpha, line_width=line_width,
                       color=colors[i], legend=value(legend_names[i]))        



        #######################
        ###### hover tool 
        #######################

        tooltips = [(i, '@'+i+'{0.0}') for i in cat_labels]

        tooltips = HoverTool(
        tooltips=tooltips, 
        mode = 'mouse',
        point_policy = 'follow_mouse'
        )
        p.add_tools(tooltips)

        p = USAID_style(p, font=font)

        ######################
        #### style choices
        ######################

        p.yaxis.visible = True  
        p.xaxis.visible = True
        if major_label_orientation !='horizontal': 
            p.xaxis.major_label_orientation = pi / 2
        ########################
        ### legend options 
        ########################

        p.legend.orientation = legend_orientation

        if legend_location =='outside': 
            # set legend location outside the plot (change the 'above' to change to the sides)
            p.legend.location = 'center'
            new_legend = p.legend[0]
            p.legend[0].plot = None
            p.add_layout(new_legend, 'above')
            p.legend.border_line_color=None

        else:
            # set the legend location within the plot in this location 
            p.legend.location = legend_location

        # print details of if prompted
        if print_details ==True: 
            print('Dictionary of values')
            print(detail_1)



    except ValueError: 
        plot_dim = (plot_dim[0]*scale, plot_dim[1]*scale)
        p = empty_plot(plot_dim, title=title_text, scale = scale)
        
        
        # print details of if prompted
        if print_details ==True: 
            print('Dictionary of values')
            print(detail_1)

        
    
    return p
