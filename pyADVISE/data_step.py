import pandas as pd
path='C:/Users/alightner/Documents/Source_Updates/ESDB/Database/'


import country_converter  as coco
cc = coco.CountryConverter()


def transform_to_codes(data, col, new_col_name, name_type='ISO3'): 
    data.replace('Congo, Dem. Rep.', 'DR Congo', inplace=True)
    data[col_name] = cc.convert(names =list(data[col]), to='ISO3', not_found=None)

    return data

def merge_country_name(data, left_on='country_id', right_on='country_id',country_name=['country_name'],  file=path): 

    # read excel file, select vars of interest [[  ]]
    df_countries = pd.read_sas(file+'countries.sas7bdat')
    
    
    
    # decode string vars from sas
    for i in country_name: 
        df_countries[i] = df_countries[i].str.decode('UTF-8') 
    
    
    
    # merge data on column of choice 
    df = pd.merge(data, df_countries[['country_id']+ country_name], left_on=left_on, right_on=right_on, how='left')
    
    # print the names which do not merge 
    print(df[~df[right_on].notnull()][left_on].unique())

    
    return df 



def merge_country_class(data, class_type='World Bank Income'):
    '''Provide data, the variable you would like to merge on, and the type of income 
    category the user would like to examine. Need to expand to other types of income groups.'''
    
    
    # set to shared file location in the future file = 
    file1 = 'C:/Users/alightner/Documents/Source Updates/Gen Data'
    
    
    # bring in relevant data sources
    codes = pd.read_sas(file1 + '/country_classification_values.sas7bdat')
    values = pd.read_sas(file1 + '/classification_values.sas7bdat')
    
    
    # change classification value name in values to UTU-08 
    values['classification_value_name'] = values['classification_value_name'].str.decode('UTF-8')
    
    
    # if class == 'World Bank Income' then just merge these codes 
    if class_type =='World Bank Income': 
        # keep only the WB codes (first 4 observations)
        values = values.iloc[0:4, :]
        # keep only the country code values where classif.. is bewteen 0 and 4. 
        codes = codes[codes['classification_value_id'].between(0,4)]
    
    
    # merge codes to dataset provided. 
    classif = pd.merge(codes, values, on='classification_value_id', how='left')
    # rename class_year to year to limit repetitiveness 
    classif.rename(index=str, columns={"classification_year": "year"}, inplace=True)
    
    # select only the max year
    max_year = max(list(classif['year'].unique()))
    
    # select the most recent year 
    classif = classif[classif['year']==max_year]
    
    # drop year
    classif.drop('year', axis=1, inplace=True)
    
    # merge datasets 
    df = pd.merge(data, classif, on=['country_id'], how='left')
    
    
    
    return df


def merge_series_names(data, include_vars=['series_name'], file='C:/Users/alightner/Documents/Source Updates/029 ILO/'): 

    # read excel file, select vars of interest [[  ]]
    df_series = pd.read_excel(file+'Mappings/mapping series.xlsx')
    
    # merge data series and data provided 
    df = pd.merge(data, df_series[['series_id']+include_vars], on='series_id', how='left')
    
    return df

###########################################################
###########################################################
############   ACCESS FINISHED DATA 
###########################################################
###########################################################

def get_esdb(table_num, path='C:/Users/alightner/Documents/Source_Updates/ESDB/Database/', 
            country_sel=None, year_sel=(1960, 2019), series_sel=None, silence=False,
            return_columns = ['series_id', 'country_name', 'country_id', 'year', 'value_start'], 
            series_df_short = True):
    '''This function will return a final dataset within a source update file. The user
    specifies only the table number (without the _) if the data is in the same folder in 
    typical ASVISE format.'''
    
    
    # define paths to data
    data_path = path+'_'+ table_num+'data.sas7bdat'
    country_path = path+'countries.sas7bdat'
    series_path =  path+'series.sas7bdat'

    
    ###########################
    # read dataset
    ############################
    
    ### read data 
    data = pd.read_sas(data_path) 
    countries = pd.read_sas(country_path)[['country_id', 'country_name']]
    series = pd.read_sas(series_path)
    

    ### python is case sensitive while sas is not, thus we need to make ssure all column names are lowercase 
    datasets = [data, countries, series]
    for df in datasets: 
        df.columns = [i.lower() for i in df.columns]
    
    
    
    # select year observations 
    data = data[(data['year'].between(year_sel[0], year_sel[1]))]
    
    # select series if asked
    if series_sel != None: 
        data = data[(data['series_id'].isin(series_sel))]
    # select countries if prompted
    if country_sel != None: 
        data = data[(data['country_id'].isin(country_sel))]
    
    
    
    
    # change country_id, year, periodicity_id source_id, and start_value to int. 
    for i in ['series_id', 'country_id', 'year', 'periodicity_id', 'source_id']: 
        data[i] = data[i].astype('int')
    
    # set list of variables which need to change from bytes to string
    country_change = ['country_name']
    series_change = ['series_name', 'series_definition']


    # change series vars from bytes to string
    for i in series_change: 
        series[i] = series[i].str.decode('UTF-8')

        
        
    # place definitions of variables in dictionary, then drop multiple observations 
    if series_sel !=None: 
        series = series[series['series_id'].isin(series_sel)]
    
    if series_df_short ==True: 
        series = series[['series_id', 'series_name', 'series_definition']]
    
    series_df = series.drop_duplicates(['series_id', 'series_name', 'series_definition'])
    
    series_df['series_id'] = series_df['series_id'].astype('int')
    
    
    
    
    # change countries from bytes    
    for i in country_change: 
        countries[i] = countries[i].str.decode('UTF-8')


    # change country_id to int 
    countries['country_id'] = countries['country_id'].astype('int')
    
    #################################
    # merge in country and series on respect datasets
    ##################################
    
    if silence==False:
        print('The length of the dataset from '+table_num+ ' is ' +str(len(data)))
        

    data1 = pd.merge(data, countries, on='country_id', how='inner')

    
    data1= data1[return_columns]
    #data2 = pd.merge(data1, series, on='series_id', how='inner')
    #print('After merging series: ' +str(len(data)))
    
    series_df = series_df.reset_index()
        
    return data1, series_df


#####################################################
#####  FIND SOURCE 
######################################################


def find_source(series_sel, path='C:/Users/alightner/Documents/Source_Updates/ESDB/Database/'): 
    
    '''this function takes a list of series ids and returns a dataframe of the source_ids along with 
    their definitions and names'''
    
    # acces series file 
    series_path =  path+'series.sas7bdat'
    series = pd.read_sas(series_path)
    
    # make sure column names are lower case 
    series.columns = [i.lower() for i in series.columns]

    # change from coded to UTf-8
    series_change = ['series_name', 'series_definition']
    # change series vars from bytes to string
    for i in series_change: 
        series[i] = series[i].str.decode('UTF-8')
        
    # change series_id to int 
    series['series_id'] = series['series_id'].astype('int')
    series['source_id'] = series['source_id'].astype('int')
    
    # return series 
    series = series[series['series_id'].isin(series_sel)]
    
    
    
    series = series[['source_id', 'series_id', 'series_name', 'series_definition']]
    
    return series


def get_esdb_by_dict(dictionary, country_list, year_sel=(1990, 2019),  silent=False):
    '''this function takes a dictionary where the keys are the the source_ids and the values 
    are lists of series_ids associated with the source_ids. 
    '''
    # # empty dataframes to be filled 
    data = pd.DataFrame()
    series_info = pd.DataFrame()
    
    # loop through and access 
    for i in dictionary: 
        
        print('Source: '+ str(i))

        # turn i into str, add 0 if len(2) 
        i = str(i)
        length_i = len(i)
        if length_i==1: 
            i = '00'+i
        elif length_i ==2: 
            i = '0'+i
        
        # for each source, get data
        data_temp, series_info_temp = get_esdb(i, series_sel=dictionary[int(i)], 
                                country_sel=country_list, year_sel=(year_sel[0], year_sel[1]))

        # append data to main dataset 
        data = data.append(data_temp)
        series_info = series_info.append(series_info_temp)
    
    return data, series_info
    
    
    
def get_data_from_serieslist(file, country_list, year_sel=(2000, 2017), sheet_name='Data', silence=False): 
    
    '''preps a list of series_ids from an excel and a list of countries of interest to use the get_esdb by dict. '''
    
    # list of series
    series_df = pd.read_excel(file, sheet_name=sheet_name)
    series_list = list(series_df.series_id.dropna().astype('int').unique())
    
    # find source_ids for the source 
    sources = find_source(series_list)
    
    # generate a dictionary of lists of serires_ids by located by source_id keys
    ind_bysource = { i : sources[sources['source_id']==i]['series_id'].tolist() for i in sources['source_id'].unique()}
    
    # get data using this ind_bysource 
    data, series_info = get_esdb_by_dict(dictionary=ind_bysource, country_list=country_list, year_sel=year_sel)
    
    return data, series_info 




def get_ids(data, key_col, value_col): 
    
    '''this function takes a dataset and two columns and returns 
    a dictionary with the key_col as the keys (unique) and their 
    associated unique value_col'''
    
    # unqiue and consise dataset
    data = data[[key_col, value_col]].drop_duplicates()
    
    data = {i[0]: i[1] for i in zip(data[key_col], data[value_col])}
        
    return data



def most_recent_data(data, on=['country_id', 'series_id'], date_var='year', ascending=[True, True, False]):
    
    '''takes a dataset and returns most recent, based on the on selection'''
    
    sort_vars = on+[date_var]
    # sort by country_id, descending series_id
    data = data.sort_values(sort_vars, ascending=ascending)
    

    # drop duplicates based on the 'on' option 
    data = data.drop_duplicates(on)
    
    return data