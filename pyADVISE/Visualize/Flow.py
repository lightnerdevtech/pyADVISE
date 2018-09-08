
# import packages 
import numpy as np
import holoviews as hv
import pandas as pd
from bokeh.io import show, curdoc
from pyADVISE.data_step import merge_country_name, transform_to_codes 
from bokeh.models import HoverTool



# set extension to holoviews to bokeh 
hv.extension('bokeh')





####################################################
####################################################
#########           SANKEY PLOT 
####################################################
####################################################







####################################
#### generate functions 
####################################




def year_range_sum(data, year_range): 

    # select this in the data
    data = data[data['year'].between(year_range[0], year_range[1])]

    # group by pairing and sum. 
    data = data[['country_name_to', 'country_name_from', 'value']].groupby(['country_name_to', 'country_name_from']).sum().reset_index()
    
    # return dataset 
    return data






def gen_nodes(data, to_var='country_name_to', from_var='country_name_from'): 
    '''this function generates the nodes dataset based on to and from variables'''
    
    data = data.sort_values([to_var, from_var])
    
    # generate unique list of 'to' countries receivers, rename for appending
    country_to = data[[to_var]].drop_duplicates().rename(index=str, columns={to_var:'country_name'})

    # add space to country_name from for each name (make from var unique from to countries)
    data[from_var] = [i + ' ' for i in data[from_var]]
    # generate a unique list of all countries from, rename for appending later
    country_from = data[[from_var]].drop_duplicates().rename(index=str, columns={from_var:'country_name'})
    
    # append data to create the nodes dataset 
    nodes = country_to.append(country_from).reset_index(drop=True).dropna()
    
    # return data with unique from countries and the nodes dataset 
    return data, nodes






def add_ids(data, nodes, country_stem='country_name'): 
    
    # generate values for location and replacement
    index = [i for i in range(0, len(nodes))]
    countries = nodes['country_name'].values

    # for each unique observation
    for i in range(0, len(index)): 
        # for both variables to and from
        for f in ['to', 'from']: 
            # where countryname = the country, set the new id variable to the index
            data.loc[data['country_name_'+f]==countries[i], 'id_'+f] = index[i]

    return data



def zip_edges(data, vars_int=['id_from', 'id_to', 'value']): 
    '''this function generates the edges (connectors) for the sanky plot'''
    data = data.dropna()
    
    edges = list(zip(data[vars_int[0]].astype('int'),data[vars_int[1]].astype('int'), data[vars_int[2]].astype('int')))
    
    # return edges
    return edges




def make_sankey_data(data, year_range, number): 
    '''this function generate the data for the slank chart given 
    the year and value thresholds'''
    
    # select year range
    data_y = year_range_sum(data=data, year_range=(1990, 2016))
    
    # select data over a particular value
    data_values = data_y[data_y['value']>number].reset_index(drop=True).dropna()
    
    data_values['value'] = np.round(data_values['value']/1000)
    data_values['value'] = data_values['value'].astype('int')
    
    
    # this function generates the nodes dataset based on to and from variables
    data, nodes = gen_nodes(data=data_values)
    
    data.dropna(inplace=True)
    nodes.dropna(inplace=True)
    
    # add in unique identifiers from 0 to len(nodes)
    data_edges = add_ids(data=data, nodes=nodes)
    
    # define the edges (connection of the data)
    edges = zip_edges(data_edges)
    
    # place nodes in holoviews dataset for plotting 
    nodes_plot = hv.Dataset(enumerate(nodes['country_name']), 'index', 'label')
    
    # return edges and nodes to plot
    return edges, nodes_plot




#####################################
#### generate the plot 
#####################################

def gen_sankey_plot(nodes, edges, title_text='Sankey Chart'): 
    options = hv.Store.options('bokeh')
    options.Sankey = hv.Options('style', node_line_alpha=0, node_nonselection_alpha=0.2, node_size=10, node_line_width=0,
                                 edge_cmap=['#002F6C', '#BA0C2F', '#A7C6ED', '#212721'], cmap=['#002F6C', '#BA0C2F',  '#212721', '#212721'],
                               edge_nonselection_alpha=0.2, edge_line_alpha=0, edge_fill_alpha=0.7,
                                edge_hover_alpha=1, edge_hover_color='#002F6C', 
                               label_text_font_size='8pt')
    
    
    sankey = hv.Sankey((edges, nodes), ['From', 'To']).options(
    label_index='label', label_position='left', width=800, height=800, edge_color_index='To'
    )
    # pass to bokeh for further changes 
    renderer = hv.renderer('bokeh')
    plot = renderer.get_plot(sankey , doc=curdoc()).state
    
    # return plot 
    return plot
