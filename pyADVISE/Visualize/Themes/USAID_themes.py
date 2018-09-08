
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def USAID_fonts(font_file='C:/Users/alightner/Documents/fonts/'): 
    
    '''this function loads USAID fonts '''
    # path to folder with fonts
    font_file = font_file
    
    
    #############################
    #### Open Sans 
    #############################
    
    # generate font
    files = ['OpenSans-Bold.ttf', 'OpenSans-BoldItalic.ttf', 'OpenSans-ExtraBoldItalic.ttf', 
             'OpenSans-ExtraBold.ttf', 'OpenSans-Italic.ttf', 'OpenSans-Light.ttf', 
             'OpenSans-Light.ttf', 'OpenSans-LightItalic.ttf', 'OpenSans-Regular.ttf',
              'OpenSans-SemiBold.ttf', 'OpenSans-SemiBoldItalic.ttf']

    # generate names by take off the .ttf
    names = [i[:-4] for i in files]


    for i in range(0, len(files)): 
        pdfmetrics.registerFont(TTFont(names[i], font_file+files[i]))
    
    
    ###############################
    #####   Gill Sans MT
    ###############################
    
    
    ### Bring in the needed font
    pdfmetrics.registerFont(TTFont('Gill Sans MT', 'gil_____.ttf'))
    pdfmetrics.registerFont(TTFont('Gill Sans MT Bold', 'gilb____.ttf'))
    pdfmetrics.registerFont(TTFont('Gill Sans MT It', 'gili____.ttf'))
    
    
    #############################
    #### others 
    #############################
    
    return 



def USAID_style(p, font='Gill Sans MT'): 

    
    #######################
    ###  title 
    #######################
    p.title.text_color = '#383951'
    p.title.text_font = font
    p.title.text_font_style = "bold"    
    p.title.text_font_size= '15pt' 
    
    #######################
    ### Grid options 
    #######################
    
    # grid lines 
    p.grid.grid_line_color='white'
    p.grid.grid_line_width=.8
    p.grid.grid_line_alpha=0.7
    
    
    
    #######################
    #### Axis styles 
    #######################
    
    ### labels
    p.xaxis.axis_label = ''
    p.yaxis.axis_label = ''

    
    p.axis.axis_label_text_color = '#999999'
    p.axis.axis_label_text_font_style = 'normal'
    p.axis.axis_label_text_font = font
    p.axis.major_label_text_font_size = '14pt'
    p.axis.major_label_text_font = font
    p.axis.axis_label_text_font_size ='14pt'    
    
    ## axis colors 
    #p.axis.line_color = ''
    #p.yaxis.axis_label = ''
    
    # axis  line options 
    p.axis.axis_line_color = '#999999'
    p.axis.axis_line_alpha = .8
    p.axis.axis_line_width = 1

    
    
    ### axis visable
    #p.yaxis.visible = False  
    #p.xaxis.visible = False
    #p.axis.axis_line_color=None
    
    
    ### major ticks
    p.axis.major_label_text_color='#999999'
    p.axis.major_tick_line_color='#999999'
    
    ### minor ticks 
    p.xaxis.minor_tick_line_color = None # turn off x-axis minor ticks
    p.yaxis.minor_tick_line_color = None
    
    
    ######################
    #### Legend styles
    ######################
    
    p.legend.label_text_font =  font
    p.legend.label_text_font_size = '14pt'
    p.legend.background_fill_alpha = 1
    p.legend.background_fill_color = 'white'
    p.legend.border_line_color=None
    

    ####################
    # plot outline
    ####################
    
    p.outline_line_color = None
    p.legend.border_line_alpha=0
    p.yaxis.major_label_standoff=10
    p.xaxis.major_label_standoff=0
    p.axis.major_tick_in=0
    p.axis.major_tick_out=6
    
    ######### borders 
    p.min_border_right = 20
    p.min_border_bottom = 20
    
    
    # logos 
    p.toolbar.logo = None
    
    return p




def USAID_interactive(p, font='Gill Sans MT'): 

    
    #######################
    ###  title 
    #######################
    p.title.text_color = '#383951'
    p.title.text_font = font
    p.title.text_font_style = "bold"    
    p.title.text_font_size= '15pt' 
    
    #######################
    ### Grid options 
    #######################
    
    # grid lines 
    p.grid.grid_line_color='#999999'
    p.grid.grid_line_width=.7
    p.grid.grid_line_alpha=0.5
    
    
    
    #######################
    #### Axis styles 
    #######################
    
    ### labels
    p.xaxis.axis_label = ''
    p.yaxis.axis_label = ''

    
    p.axis.axis_label_text_color = '#999999'
    p.axis.axis_label_text_font_style = 'normal'
    p.axis.axis_label_text_font = font
    p.axis.major_label_text_font_size = '11pt'
    p.axis.major_label_text_font = font
    p.axis.axis_label_text_font_size ='11pt'    
    
    ## axis colors 
    #p.axis.line_color = ''
    #p.yaxis.axis_label = ''
    
    # axis  line options 
    p.axis.axis_line_color = '#999999'
    p.axis.axis_line_alpha = .5
    p.axis.axis_line_width = .7

    
    
    ### axis visable
    #p.yaxis.visible = False  
    #p.xaxis.visible = False
    #p.axis.axis_line_color=None
    
    
    ### major ticks
    p.axis.major_label_text_color='#999999'
    p.axis.major_tick_line_color='#999999'
    
    ### minor ticks 
    p.xaxis.minor_tick_line_color = None # turn off x-axis minor ticks
    p.yaxis.minor_tick_line_color = None
    
    
    ######################
    #### Legend styles
    ######################
    
    p.legend.label_text_font =  font
    p.legend.label_text_font_size = '12pt'
    p.legend.background_fill_alpha = 0
    p.legend.background_fill_color = 'white'
    p.legend.border_line_color=None
    

    ####################
    # plot outline
    ####################
    
    p.outline_line_color = None
    p.legend.border_line_alpha=0
    p.yaxis.major_label_standoff=10
    p.xaxis.major_label_standoff=0
    p.axis.major_tick_in=0
    p.axis.major_tick_out=6
    
    ######### borders 
    p.min_border_right = 20
    p.min_border_bottom = 20
    
    
    # logos 
    p.toolbar.logo = None
    
    return p




