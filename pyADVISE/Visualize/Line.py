########################################################
####  This generages the pyADVISE visualize package
########################################################

# import packages
import os
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
from bokeh.plotting import figure
from bokeh.layouts import layout, widgetbox
from bokeh.models import ColumnDataSource, Div, HoverTool, LabelSet, Label, Legend, LegendItem
from bokeh.plotting import figure, show
from bokeh.models import Span
from bokeh.models.glyphs import Ellipse

## add new imports 
from collections import Counter
from math import pi
from bokeh.transform import cumsum

# new packages for the pyADIVSE package 
from bokeh.transform import factor_cmap

# import themes from within the directory
from pyADVISE.Visualize.Themes.USAID_themes import USAID_style

# bring empty plot
from pyADVISE.Visualize.General import empty_plot



##################################################################
##################################################################
#############        GENERAL FUNCTIONS
##################################################################
##################################################################





# define the select data function for the ESDB database style
def select_data(data, obs=('countryname', ['Malawi', 'China']), years=('year', (1995,2015)), 
                focus_vars=('series_id', '3')):
    '''Selects data in the format of the ESDB'''

                # countries
    data = data[data[obs[0]].isin(obs[1])
                # years
                & data[years[0]].between(years[1][0], years[1][1])
                # variables
                & data[focus_vars[0]].isin(focus_vars[1])
               ]

    return data





##################################################################
##################################################################
#############        LINE GRAPHS
##################################################################
##################################################################

########################################################
####  This generages the pyADVISE visualize package
########################################################

# import packages
import os
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
from bokeh.models import Span

# new packages for the pyADIVSE package 
from bokeh.transform import factor_cmap

# import themes from within the directory
from pyADVISE.Visualize.Themes.USAID_themes import USAID_style

# bring 
from pyADVISE.Visualize.General import empty_plot



##################################################################
##################################################################
#############        GENERAL FUNCTIONS
##################################################################
##################################################################





# define the select data function for the ESDB database style
def select_data(data, obs=('countryname', ['Malawi', 'China']), years=('year', (1995,2015)), 
                focus_vars=('series_id', '3')):
    '''Selects data in the format of the ESDB'''

                # countries
    data = data[data[obs[0]].isin(obs[1])
                # years
                & data[years[0]].between(years[1][0], years[1][1])
                # variables
                & data[focus_vars[0]].isin(focus_vars[1])
               ]

    return data



palette = {'USAID Blue': '#002F6C', 'USAID Red': '#BA0C2F', 'Rich Black': '#212721', 'Medium Blue': '#0067B9',
        'Light Blue': '#A7C6ED', 'Dark Red': '#651D32', 'Dark Gray': '#6C6463', 'Medium Gray': '#8C8985', 'Light Gray': '#CFCDC9'}

##################################################################
##################################################################
#############        LINE GRAPHS
##################################################################
##################################################################




def gen_line(data, obs_sel, focus_sel, obs_labels, year_tuple=(2010, 2018),
             title_text= 'Figure 3: Comparison of multiple countries ³', obs_var='country_id', 
             year_var = 'year', focus_var= 'series_id', value_var='value_start', fill_alpha=.5, scale=1, 
             line_width = 5, dots=True, legend_outside=True, legend_location='above', zero_line=False, 
                x_axis_label='X-Axis', y_axis_label='Y-Axis', no_tools=False, print_details=False,
                font='Gill Sans MT', legend_orientation='horizontal', plot_dim=(300, 500)):

    '''This function takes multiple countries, with one indicator variable and compares them accordingly. Or one country and
    multiple indicators. At the moment, the function does not support multiple selections of both countries and indicators. '''



    #############################################
    ####  More than one country
    #############################################


    if len(obs_sel)>=1 & len(focus_sel)==1:
        
        data = select_data(data, obs=(obs_var, obs_sel), years=(year_var, year_tuple), focus_vars=(focus_var, focus_sel))
        
        ##### prep the data in the correct order. 
        # rename series_ids to thier order in the list 
        for i in range(0, len(obs_sel)): 
            data.loc[data[obs_var]==obs_sel[i], obs_var] = i
        data.sort_values([obs_var, year_var], inplace=True)
        
        
        obs_sel=list(range(0, len(obs_sel)))
        ##################################################
        #########  Generate Plot
        ##################################################

        
        ################# set styles 

        palette_names = list(palette.keys())
        
        # generate color palettes
        colors = {obs_sel[i]: palette_names[i] for i in range(0, len(obs_sel))}
        
        # generate empty datasets to be filled
        df = pd.DataFrame()
        circles = pd.DataFrame()
        
        # select observations of interest
        data = data[data[obs_var].isin(obs_sel)]
        
        # interate over index values 
        n = 0 
        
        # for each observation
        for i in data[obs_var].unique():
            # select of a particular country 
            df_small = data[data[obs_var]==i]
            
            # sort values
            df_small= df_small.sort_values([year_var])

            # select indicator of interest
            df_small = df_small[df_small[focus_var]==focus_sel[0]]

            # create empty dataframe to be 
            df1 = pd.DataFrame()

            # place values in brakets so that they are entered as one observation lists.
            df1[obs_var] = [i]
            df1['x'] = [df_small[year_var].values]
            df1['y'] = [df_small[value_var].values]
            df1['color'] = palette[colors[i]]
            df1['label'] = [obs_labels[n]]
            
            n+=1 

            # generate cicle df (the format needs to be panel)
            df_small['color'] = palette[colors[i]]

            circles = circles.append(df_small)

            df = df.append(df1)

        detail_1 = circles
        # generate the largest number of observations by obs_var
        try: 
            length = data[obs_var].value_counts().tolist()[0]
        except: 
            #print(data[obs_var])
            length=0
        
        # only is there is a line for at least one of the observations
        if length>1: 

            ################################
            ### generate the plot 
            ###############################
            
            #### scale plot 
            plot_dim = (plot_dim[0]*scale, plot_dim[1]*scale)
            line_width = line_width*scale
            
            source = ColumnDataSource(df)

            p = figure(plot_height=plot_dim[0], plot_width=plot_dim[1])
			
			
	        ############ add horizontal line at zero if true
            if zero_line==True: 

                zero_line = Span(location=0,
                                        dimension='width', line_color='gray',
                                        line_dash='dashed', line_width=3*scale, line_alpha=0.5)
                p.add_layout(zero_line)

                
            p.multi_line(xs='x', ys='y', legend='label',
                         line_width=line_width, line_color='color', line_alpha=fill_alpha,
                         hover_line_color='color', hover_line_alpha=1.0,
                         source=source)

            ### generate circle 

            circles = circles.rename(index=str, columns={year_var: "year", value_var: "value_start"})
            circles = ColumnDataSource(circles)

            if dots ==True: 
                r = p.circle(y='value_start',x='year', source =circles, color='color', size=2*line_width)


                p.add_tools(HoverTool(show_arrow=False, line_policy='next', renderers = [r], tooltips=[
                    ('Obs', '@country_name'),
                    ('X', '@year'), 
                    ('Y', '@value_start')
                ]))

            if dots==False: 
                p.add_tools(HoverTool(show_arrow=False, line_policy='next', tooltips=[
                    ('Obs', '@label'),

                ]))     

            #give details
            if print_details==True: 
                print('The dictionary of values')
                print(detail_1)

            ######################
            ### styling options 
            ######################


            # legend 
            p.legend.glyph_width= 60
            p.legend.border_line_color=None

            
            p = USAID_style(p, font=font)

            p.title.text = title_text
            p.legend.background_fill_color = 'white'

            ######### legend location 
            p.legend.orientation = legend_orientation
            if legend_outside==True: 
                p.legend.location = 'center'
                new_legend = p.legend[0]
                p.legend[0].plot = None
                p.add_layout(new_legend, legend_location)
                p.legend.border_line_color=None

            else: 
                p.legend.location = legend_location 


            ######## drop tools if prompted 
            if no_tools==True: 
                p.toolbar.logo = None
                p.toolbar_location = None
                

    
        
        ### if no data
        else: 
            
            # generate plot dimentions with scale 
            plot_dim = (plot_dim[0]*scale, (plot_dim[1])*scale)
            
            # plot empty plot
            p =  empty_plot(plot_dim, title='Something', scale=scale, scale_text=1)
            
            p.title.text_color='white'
            
            
            # print details if asked. 
            if print_details == True: 
                print('The dictionary of values:')
                print(detail_1)

    
    # if the wrong specification -> return this sentence. 
    else:
        print('This function does not support multiple country and indicator selections. Please revisit the obs_sel and focus_sel selections and var_names.')


        
    return p






###############################################
##############################################333
#############  RADAR CHART 
################################################
################################################









def gen_radar(df, obs_var, cat_var, value_var='value_start',  title_text = '', fill_alpha=.2, 
            scale=1, line_alpha=.6, line_width = 5, legend_location='top_right', no_tools=False, print_details=False, axis_marks='default', grid_color ='#8C8985', patch_colors = 'default', 
                font='Gill Sans MT', legend_orientation='vertical', plot_dim=(500, 500), label_font_size=14, num_font_size=10, 
                 custom_tooltip=None):

    ###########################################
    ### data input 
    ###########################################

    
    
    # generate the unique observation variables 
    obs = list(df[obs_var].astype('str').unique())

    # generate new list of texts
    text = list(df[cat_var].astype('str').unique())
     
    # find min and max values
    max_var = df[value_var].max()
    min_var = df[value_var].min()

    if axis_marks == 'default': 
        # generate tick marks if default 
        l = matplotlib.ticker.AutoLocator()
        l.create_dummy_axis()

        # get tick marks based on our min and max values 
        axis_values = l.tick_values(min_var, max_var)
        # scale each value by the second to last value for plotting 
        # this is because the plot is a 1 by 1 plot which we label differently depending on 
        # values. 
        axis_scaled = np.array(axis_values)/axis_values[-2]
        # address if the tick values are too many
        length = len(axis_values) 
        if length>6: 
            ## access every other observatation beginning from the second to last observation moving backwards
            ### add the extra value for consistancy in the labelling from [-1] no matter the length
            axis_values = list(reversed([axis_values[-2+(-2*i)] for i in range(0, int(np.round(len(axis_values)/2)))]))+[1]
            axis_scaled = list(reversed([axis_scaled[-2+(-2*i)] for i in range(0, int(np.round(len(axis_scaled)/2)))]))+[1]
            
            
            
    else: 
        # if axis values are provided 
        axis_values = np.array(axis_marks)
        # scale values for reasons stated above (last value)
        axis_scaled = np.array(axis_values)/axis_values[-1]

    # depending on whether the scale is given or automated, we select the last or second to last 
    # value in the list as the reference point for scaling. here we define this. 
    a = -1
    if axis_marks=='default': 
        # select the second value
        a= -2
    
    # generate dictionary of all 
    reals = {}
    scales = {}
    for i in list(df[obs_var].unique()):
        
        reals[str(i)] = df[df[obs_var]==i][value_var].values
        #scale by the largest value in the axis generated by matplotlib
        scales[str(i)] = df[df[obs_var]==i][value_var].values/axis_values[a]/2
     
    
    # make the 'reals' dictionary the return value if detailed needed. 
    detail_1 = reals
    
    # try to build plot, send empty plot if fail. 
    try: 
        
        flist=[]
        for i in range(0, len(obs)): 
            flist.append(scales[obs[i]])


        ## generate the number of vars to generate the shape. 
        num_vars = len(text)

        ##############################################
        ######## Functions 

        theta = np.linspace(0, 2*np.pi, num_vars, endpoint=False)
        # rotate theta such that the first axis is at the top
        theta += np.pi/2

        def unit_poly_verts(theta, r):
            """Return vertices of polygon for subplot axes.
            This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
            """
            x0, y0, r = [0.5, 0.5, r]
            verts = [(r*np.cos(t) + x0, r*np.sin(t) + y0) for t in theta]
            return verts

        # turn data into circlular options
        def radar_patch(r, theta):
            yt = (r) * np.sin(theta) + 0.5
            xt = (r) * np.cos(theta) + 0.5
            return xt, yt


        #### scale plot 
        plot_dim = (plot_dim[0]*scale, plot_dim[1]*scale)
        line_width = line_width*scale

        ######### Generate plot

        p = figure(title="", plot_width = plot_dim[1], plot_height=plot_dim[0], 
                   x_range=(-.23,1.55), y_range=(-.1,1.2), 
                   tools='save,tap,reset') 

        #################################
        #### Generate labels 
        #################################

        # generate the locations of the labels 
        verts = unit_poly_verts(theta, 0.55)
        x = [v[0] for v in verts] 
        y = np.array([v[1] for v in verts])-.03

        # separate between right and left side vars 

        # if there are more than four cat_var's, then make one more label point to the left
        num_cat = len(text)
        if num_cat >3: 
            a = (int(np.round(len(text)/2)))+1
            left_labels = text[:a]
            right_labels = text[a:]
        else: 
            a = (int(np.round(len(text)/2)))
            left_labels = text[:a]
            right_labels = text[a:]  


        # plot right and left labels (difference -> text align)
        source_left = ColumnDataSource({'x':x[:a],'y':y[:a],'text':left_labels})
        source_right = ColumnDataSource({'x': x[a:]+[0.5],'y':y[a:],'text':right_labels})

        # set font size
        fsize = str(label_font_size*scale)+'pt'
        
        label_left = LabelSet(x="x",y="y",text="text",source=source_left, text_font=font, text_font_size=fsize, 
                         text_color=grid_color, text_align = 'right')
        label_right = LabelSet(x="x",y="y",text="text",source=source_right, text_font=font, text_font_size=fsize, 
                         text_color=grid_color)
        # add to plot
        p.add_layout(label_left)
        p.add_layout(label_right)


        #################################
        # generate background 
        #################################
        # circles

        for i in axis_scaled:
            glyph = Ellipse(x=0.5, y=0.5, width=i, height=i, fill_color=None, line_width=scale, line_color=grid_color, line_alpha=0.5) 
            p.add_glyph(glyph)

        #lines - generate coordinates - lines from center to coordinates 
        verts = unit_poly_verts(theta, 0.50)
        x_lines = [v[0] for v in verts] 
        y_lines = [v[1] for v in verts]

        for i in range(0,len(x_lines)): 
            p.line(x=(0.5, x_lines[i]), y=(0.5, y_lines[i]), line_width=3*scale, line_color=grid_color, line_alpha=0.5)

        #### numbered  
        # access all but the last number in the axis_values list (we don't plot the last one in default)
        nums = axis_values 
        if axis_marks=='default': 
            nums = axis_values[:-1]
        # we only  plot on half the circle (divide the length in half)
        x = np.array(axis_scaled)/2
        x = [.5-i for i in  np.array(axis_scaled)/2]        
        # place the numbers in a horizontal line. 
        y =[0.5, 0.5, 0.5, 0.5, 0.5]

        source = ColumnDataSource({'x':x,'y':y,'text':nums})

        fsize=str(num_font_size*scale)+'pt'
        # place numbers on plot 
        numbers = LabelSet(x="x",y="y",text="text",source=source, text_font=font, text_font_size=fsize, 
                         text_color=grid_color)

        p.add_layout(numbers)


        ##################################
        ####### Plot Patches and circles 
        ###################################

        # this also sets a maximum number of observations at six which is reasonable
        if patch_colors =='default': 
            colors = [palette[i] for i in ['USAID Blue', 'USAID Red', 'Medium Blue', 'Light Blue', 'Dark Red', 'Medium Gray']]
        else: 
            colors = patch_colors 

        sources1 = pd.DataFrame()

        ##### Patches
        for i in range(len(flist)):
            xt, yt = radar_patch(flist[i], theta)

            sources1 = sources1.append(pd.DataFrame({'xt': [xt], 'yt': [yt], 'obs': obs[i], 'colors':colors[i]}))


        details_1 = sources1 
        
        TOOLTIPS = """
            <div> 

                <div>
                    <span style="font-size: 10px; font: 'Open Sans'; color: black;"><b>@obs</b></span>
                </div>
            </div>
        """
        if custom_tooltip!=None: 
            try:
                TOOLTIPS = custom_tooltip[0]
            except: 
                print('Must pass custom tooltip in a list.')


        r = p.patches(xs='xt', ys='yt', fill_alpha=fill_alpha, line_alpha =line_alpha,color='colors', line_width = line_width, legend='obs', 
                  source = ColumnDataSource(sources1), hover_line_color='colors', hover_line_alpha=1, hover_color='colors',
                     hover_fill_alpha=.35)
        hover_p = HoverTool(
                renderers=[r],
                tooltips=TOOLTIPS

        )
        p.add_tools(hover_p)              


        #### CIRCLE Graph (eventually change to be one source file)

        sources = {}
        for i in range(0, len(obs)): 
            xt, yt = radar_patch(flist[i], theta)
            sources[i] = {'Category': text, 'Obs': [obs[i]]*len(text), 'Value': reals[obs[i]], 'yt': yt, 'xt': xt}


        ########## tooltip settings 
        
        TOOLTIPS = """
            <div> 
                <div>
                    <span style="font-size: 15px; font: 'Open Sans'; color: black; "><b>@Obs</b></span>

                </div>
                <div>
                    <span style="font-size: 15px; font: 'Open Sans';color: black;"><b>@Category:</b> @Value{0.0}</span>
                </div>
            </div>
        """
        if custom_tooltip!=None: 
            try:
                TOOLTIPS = custom_tooltip[1]
            except: 
                print('There are two tooltips, to change them both, pass two separate tooltips in a list.')

        for i in range(0, len(obs)): 
            s = p.circle(x='xt', y='yt', color = colors[i], source=sources[i],size = line_width*2, fill_alpha=.6, 
                        hover_line_color='black', hover_color=colors[i])
            hover_circle = HoverTool(
                    renderers=[s],
                    tooltips=TOOLTIPS
            )
            p.add_tools(hover_circle)


        #############################
        #### LEGENDs and STYLE
        ##############################


        p.legend.location = legend_location
        p.legend.orientation = legend_orientation

        p.title.text = title_text

        p = USAID_style(p, font=font)

        # basic formatting of the chart. 
        p.axis.axis_label=None
        p.axis.visible=False
        p.grid.grid_line_color = None
        
        
    
    except ValueError: 

        # generate plot dimentions with scale 
        plot_dim = (plot_dim[0]*scale, (plot_dim[1])*scale)

        # plot empty plot
        p =  empty_plot(plot_dim, title='Something', scale=scale, scale_text=1)

        p.title.text_color='white'


        # print details if asked. 
        if print_details == True: 
            print('The dictionary of values:')
            print(detail_1)       
    
    return p
