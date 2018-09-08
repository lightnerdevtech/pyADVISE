from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Text
from pyADVISE.Visualize.Themes.USAID_themes import USAID_style

 

def empty_plot(plot_dim, title, scale, scale_text=1):
    
    p = figure(plot_height=plot_dim[0], plot_width=plot_dim[1], x_range=(1,10), 
              y_range=(1,10), title=title)
    
    p = USAID_style(p)
    
    font_size = str(20*scale*scale_text)+'pt'
    source = ColumnDataSource({'x': [4], 'y': [5], 'text': ['No Data']})
    glyph = Text(x="x", y="y", text="text", text_color='#999999', text_font='Gill Sans MT', 
                text_font_size=font_size)
    
    p.add_glyph(source, glyph)
    
    p.axis.major_label_text_color = 'white'
    p.toolbar.logo = None
    p.toolbar_location = None
    
    return p




def scale_plot(p, value, glyph_height=20, glyph_width=20, label_font_size=14, legend_font_size = 14, title_font_size=16):
    
    # title 
    p.title.text_font_size  = str(title_font_size*value)+'pt'
    

    # legend sizing
    p.legend.label_text_font_size = str(legend_font_size*value)+'pt'
    p.legend.glyph_height = glyph_height*value
    p.legend.glyph_width= glyph_width*value
    
    # grid and axis options 
    p.grid.grid_line_width=1.5*value
    p.axis.major_label_text_font_size =str(label_font_size*value)+ 'pt'
    p.axis.axis_label_text_font_size = str(label_font_size*value)+'pt'
    p.axis.axis_line_width = 2*value
    p.axis.major_tick_line_width=value*2
    
    
    p.legend.border_line_alpha=0
    p.yaxis.major_label_standoff=10*value
    p.axis.major_tick_in=0
    p.axis.major_tick_out=6*value
    p.min_border_right = 20*value
    p.min_border_bottom = 40*value

    return p 

