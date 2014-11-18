from mongotopandas import MongoToPython
import graphlab as gl
import pandas as pd

'''
The purpose of this code was to explore if the other features would improve the models
This meant going through the data on MongoDB and extracting the features into a clean df.
The data was found to be very sparse and given domain knowledge only a few appeared to be useful.
'''

def remove_dictionaries(all_df):
    '''
    INPUT: DataFrame
    DESCRIPTION: Removes dictionaries 
    OUTPUT: DataFrame
    '''
    unique = []
    for col in all_df.columns:
        try:
            pd.unique(all_df[col])
        except TypeError:
            all_df = all_df.drop(col, axis=1)
    return all_df

def discretize(all_df):
    '''
    INPUT: DataFrame
    DESCRIPTION: changes strings (categories) into integers
    OUTPUT: DataFrame
    '''
    for col in all_df.columns:
        uniques = pd.unique(all_df[col])
        if len(uniques) == 1:
            all_df = all_df.drop(col, axis=1)
        else:
            for i, item in enumerate(pd.unique(all_df[col])):
                all_df = all_df.replace(to_replace=item, value=i)
    return all_df

def cleaned_df(df):
    '''
    INPUT: DataFrame
    DESCRIPTION: Initializes methods, gets all reviews, prints the summary of the individual recommendations.
    OUTPUT: DataFrame
    '''
    all_df = pd.concat([df, pd.DataFrame(df['Ambience'].to_dict()).T,pd.DataFrame(df['Good For'].to_dict()).T])
    all_df = remove_dictionaries(all_df)
    all_df = all_df.fillna(value=0)
    final_df = discretize(all_df)
    final_df = final_df.drop('Accepts Insurance', axis=1)
    final_df = final_df.drop('BYOB', axis=1)
    final_df = final_df.drop('BYOB/Corkage', axis=1)
    return final_df

def get_business_data_cleaned(mongo):
    '''
    INPUT: MongoToPython
    DESCRIPTION: Initializes methods, gets all reviews, prints the summary of the individual recommendations.
    OUTPUT: DataFrame
    '''
    i = 0
    dic_of_dict = {}
    bus_ids = []
    for doc in mongo.query_all('businesses'):
        dic_of_dict[i] = doc['attributes']
        bus_ids.append(doc['business_id'])
        i += 1
    df = pd.DataFrame(dic_of_dict).T
    df['business_id'] = pd.Series(bus_ids)
    return cleaned_df(df)