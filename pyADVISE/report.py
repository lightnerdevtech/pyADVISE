###########################################
###########################################
####     Function to generate reports in Reportlab
###########################################
###########################################

# libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

## report lab
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# text options 
from textwrap import wrap

# import palettes 
from pyADVISE import palettes


### Bring in the needed font
pdfmetrics.registerFont(TTFont('Gill Sans MT', 'gil_____.ttf'))
pdfmetrics.registerFont(TTFont('Gill Sans MT Bold', 'gilb____.ttf'))
pdfmetrics.registerFont(TTFont('Gill Sans MT It', 'gili____.ttf'))


palette= palettes.USAID_general()



def inch(a): 
    a = a*72
    return a 

# split the notes at the bottom
def split(obs, n): 
    obs = "\n".join(wrap(obs, n)).split('\n')
    return obs

def apply_scripting(textobject, text, rise, font='Gill Sans MT'):
    textobject.setFont(font, 6)
    textobject.setRise(rise)
    textobject.textOut(text)
    textobject.setFont(font, 12)
    textobject.setRise(0)


########################################
###### simple table 
#######################################





def table(c, df, column_w, split_list, height, margin, width, gap, text_font='something', table_ystart=9.19, enter=.24, vert_lines = [3, 3.6, 4.1], font_color = ['Rich Black', 'Rich Black','Rich Black', 'Medium Gray', 'Medium Gray'], font_type = ['', '', '', 'It', 'It'], top_label=False, column_citation = ['footnote_1', None, None, None, None], pic_size=(.25,.25),
              second_line=False, table_title='Table', font='Gill Sans MT', line_width=.5, image_folder='C:/Users/alightner/Documents/Shared/pyADVISE/images/', 
              picture=False, picture_name='Picture', column_labels =['country', 'SSA', 'Year']): 
    
    '''This function generates a table in the style of 
    the country reports. '''
    
    palette= palettes.USAID_general()
    
    ###################################
    ### mapping options
    ####################################
    
    # we only want to plot the non-footnote columns, generate a different dataset, drop witin main 
    footnotes_df = df[[c for c in df.columns if c.lower()[:-2] == 'footnotes']]
    df = df[[c for c in df.columns if c.lower()[:-2] != 'footnotes']]

    #### determine the number of enters needed per column 
    enters_by_row = pd.DataFrame()
    
    for col in range(0, len(list(df.columns))):
        
        # access the values of the column 
        values = df.iloc[:,col].values
        
        # split the values on the associated split_num 
        values_split = [split(values[i], split_list[col]) for i in range(0, len(values))]
        
        # generate the lenght (number of enters for each row in each column)
        length_of_values = [len(values_split[i]) for i in range(0, len(values_split))]
        
        # add lengths to dataframe 
        enters_by_row[col] = length_of_values
    
        
        
    # generate the max of each row, place into an array 
    table_gap = enters_by_row.max(axis=1).to_frame().reset_index()[0].values
    # for some unknown reason, this only works after changing to a list 
    table_gap = list(table_gap)
    # this var is called table gap in th rest of the code 

    # adjust for the difference between gaps for line space and between lines of text. 
    for i in range(0, len(table_gap)): 
        # because there is a header, I subtract one from the count
        a = table_gap[i]-1
        #make all gaps betweeen text only 50 percent of enter value
        if a>0: 
            gap = 1+(a*.45)
            table_gap[i] = gap


    # starting point to be iterated on 
    y = table_ystart

    
    ########################################################
    # generate horizontal lines for table 
    #######################################################
    
    c.setLineWidth(line_width)
    c.setFillColor(palette['Rich Black']) 
    c.setStrokeColor(palette['Rich Black'])    
    
    
    for i in range(0, len(table_gap)):
        c.line(inch(margin), inch(y), inch(margin+column_w), inch(y))
        #print(table_gap[i])
        y= y-(enter*table_gap[i])

    # final line outside of the loop
    c.line(inch(margin), inch(y), inch(margin+column_w), inch(y))

    
    # mark the end of the table => return w
    end_of_table = inch(y)

    
    
    ##############################################
    # generate values for the tables 
    ##############################################
    
    
    #################### formatting choices 
    
    # set font 
    c.setFont(font, size=10, leading = None)
    # set indent for 
    indent_value=0.09   
    
    # choose levels of *** the order matters, the order refers to where each line of text will begin relative to the margin. 
    
    indent = [indent_value]+ [vert_lines[i]+indent_value for i in range(0,len(vert_lines))]
    
    # generate column_footnotes list for plotting
    footnotes_dict = {str(i): footnotes_df['footnotes_'+str(i)].values for i in range(0, len(footnotes_df.columns))}
    
    keys = list(footnotes_dict.keys())
    
    
    # iterate over each colomn 
    for col in range(0, len(list(df))): 
        
        # select the values in the column of interest 
        values = df.iloc[:,col].values
        # generate a list of the given text which consists of strings the size of the split_list[s]  - will not cut words apart. 
        values = [split(values[i], split_list[col]) for i in range(0, len(values))]
        
        
        #################################
        ####    Font Settings 
        #################################
        
        
        ### Select the font type 
        if font_type[col]=='It':
            c.setFont(font+' It', size=10, leading = None)
        elif font_type[col]=='Bold': 
            c.setFont(font+' Bold', size=10, leading = None)
        else: 
            c.setFont(font, size=10, leading = None)
            
        # Select color of the text 
        c.setFillColor(palette[font_color[col]]) 
        c.setStrokeColor(palette[font_color[col]]) 
        
        
        ############################
        ######  place text 
        ############################
        
        
        # choose where the text starts relative to the first line in the table
        y_s = table_ystart-0.16
        
        # loop over each row in a particular column (for longer rows values)
        for i in range(0, len(values)):

            # number of rows
            lines = len(values)
            
            # place text in the respective row (think about generalizing this in the future -- now it just works)
            if lines==1: 
                n = 0 
                # for the one value we have. 
                for g in values[i]:
                    
                    # generate text with superscripting
                    textobject = c.beginText()
                    textobject.setTextOrigin(inch(margin+indent[col]),inch(y_s-(n*0.65*enter)))
                    textobject.textOut(g[0])
                    try:
                        apply_scripting(textobject, footnotes_dict[keys[col]][i], 4)
                        print(keys[col])
                    except: 
                        a = 0
                    c.drawText(textobject)
                    
                    n +=1
                y_s = y_s-(enter*table_gap[i])

            if lines>1:
                n = 0 
                for f in range(0, len(values[i])):
                    # generate text with superscripting
                    textobject = c.beginText()
                    textobject.setTextOrigin(inch(margin+indent[col]),inch(y_s-(n*0.53*enter)))
                    textobject.textOut(values[i][f])
                    try:
                        if f == len(values[i])-1: 
                            apply_scripting(textobject, footnotes_dict[keys[col]][i], 4)
                    except: 
                        a = 0
                    c.drawText(textobject)
                    

                    n +=1
                    
                    
                y_s = y_s-(enter*table_gap[i])

    
    
    
    ########### draw column lines 
    column1 = vert_lines
    c.setFillColor(palette['Rich Black']) 
    c.setStrokeColor(palette['Rich Black'])     
    for i in range(0, len(column1)): 
        c.line(inch(margin+column1[i]), inch(table_ystart),inch(margin+column1[i]), end_of_table)
    if second_line ==True: 
        c.line(inch(margin+column1+1.35), inch(table_ystart),inch(margin+column1+1.35), inch(table_ystart-(enter*4)))


    ########### draw title 
    c.setFont(font+' Bold', size=12, leading = None)
    c.setFillColor(palette['Rich Black']) 
    c.setStrokeColor(palette['Rich Black']) 
    c.drawString(inch(margin+pic_size[1]+0.08+0.2), inch(table_ystart+.075), table_title)
    
    
    ########### draw table labels
    c.setFont(font+' Bold', size=8.5, leading = None)
    
    if top_label ==True: 
        for i in range(0, len(column_labels)): 
            c.drawString(inch(margin+vert_lines[i]+0.05), inch(table_ystart+.075), column_labels[i])
    
    
    ############ place the visuals  
    ############ default is the image folder in pyADVISE
    if picture ==True: 
        image = image_folder+picture_name
        c.drawImage(image, inch(margin+.08), inch(table_ystart+.03), width=np.round(inch(pic_size[1])), height=np.round(inch(pic_size[0])))
    
    
    # return end of the table for reference for next table or plot
    return c, end_of_table 



#####################################
######   USAID Header 
#####################################

def USAID_header(c, height, margin, column_w, gap, width, country='Malawi', date='July 2018',): 
    
    palette= palettes.USAID_general()


    # set current color, every fill color will be this color after this point until changed
    c.setFillColor(palette['Medium Blue']) 
    c.setStrokeColor(palette['Medium Blue'])
    
    # set the top of the box circle 
    top_box = height-0.7
    
    # blue top
    c.rect(0, inch(top_box), inch(9), inch(top_box), fill=1)
    
    #blue line
    c.setLineWidth(2)
    c.line(0, inch(top_box-.55), inch(9), inch(top_box-.55))
    c.setLineWidth(1)
    
    
    # grey box 
    c.setFillColor(palette['Light Gray']) 
    c.setStrokeColor(palette['Light Gray'])    
    c.rect(inch(margin), inch(9.7), inch(margin+column_w-0.5), inch(.6), fill=1)
    
    # title and country
    c.setFont('OpenSans-Light', size=30, leading = None)
    c.setFillColor(palette['White']) 
    c.setStrokeColor(palette['White']) 
    c.drawString(inch(margin+0.12), inch(top_box+.15), 'COUNTRY PROFILE')
    
    c.setFillColor(palette['White']) 
    c.setStrokeColor(palette['White']) 
    c.setFont('OpenSans-Light', size=12, leading = None)
    #c.drawString(inch(margin+0.12), inch(top_box+.15), 'COUNTRY PROFILE')
    c.drawRightString(inch(width-margin), inch(top_box+.15), 'USAID Data Services (EADS)')
    
    
    c.setFillColor(palette['Medium Blue']) 
    c.setStrokeColor(palette['Medium Blue'])
    c.setFont('OpenSans-Bold', size=24, leading = None)
    c.drawString(inch(margin+0.12), inch(top_box-.4), country.upper())
    
    
    c.setFillColor(palette['Medium Blue']) 
    c.setStrokeColor(palette['Medium Blue'])
    c.setFont('OpenSans-Bold', size=15, leading = None)
    c.drawRightString(inch(width-margin), inch(top_box-.4), date.upper())   

    return c



def USAID_footer_text_page1(c, location=(150, 60), font='OpenSans-Light', size=8):
    

    # begin the text object 
    textobject = c.beginText()
    # place the text object
    textobject.setTextOrigin(location[0], location[1])
    # set font for the text options 
    textobject.setFont(font, size=size, leading = None)
    
    
    textobject.textLines('''
    Prepared by USAID Data Services with data from the International Data and Economic Analysis 
    website (https://idea.usaid.gov/). DISCLAIMER: The views expressed in this publication do not necessarily reflect 
    the views of the United States Agency for International Development (USAID) or the United States Government.
    ''')
    c.drawText(textobject)
    
    return c




def SDG_footer_text_page2(c, location=(150, 60), font='OpenSans-Light', size=8):
    

    # set palette
    c.setFillColor(palette['Rich Black']) 
    c.setStrokeColor(palette['Rich Black']) 

    # begin the text object 
    textobject = c.beginText()
    # place the text object
    textobject.setTextOrigin(location[0], location[1])
    # set font for the text options 
    textobject.setFont(font, size=size, leading = None)

    textobject.textLines('''
    Sources: 1. Regions based on USAID classifications.; 2. World Bank, World Development Indicators (WDI); 3. Calculated by Data Services, based on World Bank, World Development Indicators; 4. International 
    Monetary Fund (IMF), World Economic Outlook Database (WEO); 5. World Economic Forum (WEF), Enabling Trade Index; 6. U.S. International Trade Commission (USITC), Trade DataWeb; 7. Food and Agri-
    cultural Organization (FAO), FAOSTAT Land and Fertilizer Data; 8. World Economic Forum (WEF), Global Competitiveness Index; 9. Notre Dame Climate Adaptation Initiative (ND-GAIN) Country Index; 10. UN 
    Office for Disaster Risk Reduction (UNISDR), Global Assessment Report on Disaster Risk Reduction; 11. CIESIN and Yale, Environmental Performance Index (EPI); 12. Demographic and Health Surveys (DHS), 
    STATcompiler; 13. Food and Agricultural Organization (FAO), AQUASTAT; 14. WHO/UNICEF, Joint Monitoring Programme (JMP) for Water Supply, Sanitation, and Hygiene; 15. World Economic Forum (WEF), 
    Networked Readiness Index; 16. World Bank, Millennium Development Goals; 17. World Bank, Enterprise Surveys; 18. World Bank, Enabling the Business of Agriculture; 19. International Telecommun-
    ication Union (ITU), World Telecommunication/ICT Indicators Database'''
    )
    c.drawText(textobject)
    
    return c





#####################################
######   SDG Header 
#####################################

def SDG_header(c, gray_list, height, margin, column_w, gap, width, country='Malawi', date='July 2018',
              title_text='SUSTAINABLE DEVELOPMENT PROFILE', subtitle_text='PREPARED BY USAID DATA SERVICES'): 
    

    # set current color, every fill color will be this color after this point until changed
    c.setFillColor(palette['Medium Blue']) 
    c.setStrokeColor(palette['Medium Blue'])
    
    # set the top of the box circle 
    top_box = height-1
    
    # blue top
    c.rect(0, inch(top_box), inch(9), inch(top_box), fill=1)
    
    #blue line
    c.setLineWidth(1)
    c.line(0, inch(top_box-.4), inch(9), inch(top_box-.4))
    c.setLineWidth(1)
    
    #####################
    # grey box 
    #####################
    
    gray_start = top_box-1.1
    gray_height =  top_box -gray_start- 0.45
    
    c.setFillColor(palette['Light Gray']) 
    c.setStrokeColor(palette['Light Gray'])   
    
    c.rect(inch(margin), inch(gray_start), inch(margin+column_w-0.25), inch(gray_height), fill=1)
    
    # gray texts = Region, Subregion, Income group 
    
    c.setFont('Gill Sans MT Bold', size=10, leading = None)
    
    text_start = (gray_start + gray_height) 
    c.setFillColor(palette['Rich Black']) 
    c.setStrokeColor(palette['Rich Black']) 
    
    labels = ['blank(index at 0)', 'Region¹', 'Subregion', 'Income Group']
    
    for i in [1,2,3]: 
        c.setFont('Gill Sans MT Bold', size=10, leading = None)
        c.drawString(inch(margin+.14),inch(text_start+.09-(0.22*i)), labels[i])
        c.setFont('Gill Sans MT', size=10, leading = None)
        c.drawString(inch(margin+1.8),inch(text_start+.09-(0.22*i)), gray_list[i-1])
        
    ##############################
    # title and country
    ################################
    c.setFont('Gill Sans MT', size=33.5, leading = None)
    c.setFillColor(palette['White']) 
    c.setStrokeColor(palette['White']) 
    c.drawString(inch(margin+0.02), inch(top_box+.48), title_text)
    
    c.setFillColor(palette['White']) 
    c.setStrokeColor(palette['White']) 
    c.setFont('OpenSans-Light', size=12, leading = None)
    c.drawString(inch(margin+0.02), inch(top_box+.17), subtitle_text)
    
    
    c.setFillColor(palette['Medium Blue']) 
    c.setStrokeColor(palette['Medium Blue'])
    c.setFont('Gill Sans MT Bold', size=24, leading = None)
    c.drawString(inch(margin+0.02), inch(top_box-.33), country.upper())
    
    
    c.setFont('Gill Sans MT Bold', size=15, leading = None)
    c.drawRightString(inch(width-margin), inch(top_box-.26), date.upper())   

    return c

def SDG_header_page2(c, country, date, height, margin, width): 
    
    # usaid palette
    palette= palettes.USAID_general()

    
    # set start_point for the text 
    start = height-.3
    
    # write country
    c.setFillColor(palette['Medium Blue']) 
    c.setStrokeColor(palette['Medium Blue'])
    c.setFont('Gill Sans MT Bold', size=14, leading = None)
    c.drawString(inch(margin+0.02), inch(start), country.upper())
    
    # write date 
    c.setFont('Gill Sans MT Bold', size=15, leading = None)
    c.drawRightString(inch(width-margin), inch(start), date.upper())
    
    
    return c 
    
    

    
    
