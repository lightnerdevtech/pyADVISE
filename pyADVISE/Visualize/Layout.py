


# import themes from within the directory
from pyADVISE.Visualize.Themes.USAID_themes import USAID_style





def create_Div(div, text_type ='text'): 
    from bokeh.models import Div
    
    # options for text: title, subtitle, text 
    if text_type == 'text': 
        a  = '<p>\n' + div + '\n</p>\n'
        
    if text_type == 'title': 
        a = '<h1>\n' + div + '\n</h1>\n'
    if text_type == 'subtitle': 
        a = '<h3>\n' + div + '\n</h3>\n' 
    
    doc = Div(text='<style>\nh1 { font-family: "Gill Sans", "Gill Sans MT", Calibri, sans-serif; font-size: 24px; font-style: normal; font-variant: normal; font-weight: 500; line-height: 26.4px; }\n h3 { font-family: "Gill Sans", "Gill Sans MT", Calibri, sans-serif; font-size: 14px; font-style: normal; font-variant: normal; font-weight: 500; line-height: 15.4px; }\n p {\n    font: Gill Sans", "Gill Sans MT", Calibri, sans-serif;\n    text-align: justify;\n    text-justify: inter-word;\n    max-width: 500;\n}\n\n\n\n</style>\n\n'+ a, width=800)
    
    
    return doc