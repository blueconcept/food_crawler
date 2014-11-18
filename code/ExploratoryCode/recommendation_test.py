import graphlab as gl
import random
import pandas as pd

'''
Gets a summary of individual recommendations for a model
'''

def get_user_rec(m, user_list, mongo):
    '''
    INPUT: Model, List, MongoToPython 
    DESCRIPTION: Gets the name of each business given an id
    OUTPUT: Dictionary
    '''
    return {user:[ mongo.get_one('businesses', 'business_id', bus_id)['name'] for bus_id in m.recommend(users=[user], k=10)['business_id'] ] for user in user_list}
    
def run_model(sf, method_name, user_list, mongo, target='stars'):
    '''
    INPUT: SFrame, String, List, MongoToPython
    DESCRIPTION: Splits the data into train and test sets, trains the model then tests the model
    OUTPUT: DataFrame
    '''
    (train_set, test_set) = sf.random_split(0.8)
    m = gl.recommender.create(train_set, user_id='user_id', item_id='business_id', target=target, method=method_name)
    m.evaluate(test_set, verbose=True)
    
    return pd.DataFrame(get_user_rec( m, user_list, mongo))

def normalize(value, average):
    '''
    INPUT: int, float
    DESCRIPTION: Scales the value to an 
    OUTPUT: float
    '''
    return ((value-average)+0.0)/average

def normalize_ratings(sf, grouping_column, target='stars'):
    '''
    INPUT: SFrame, String
    DESCRIPTION: Normalizes the SFrame's according to the grouping_column parameter
    OUTPUT: SFrame
    '''
    group_averages = sf.groupby(grouping_column, {'average':gl.aggregate.MEAN(target)})
    average_dict = group_averages.to_dataframe().set_index(grouping_column).to_dict()
    i = 0
    lst = []
    for row in sf:
        lst.append(normalize(row[target], average_dict['average'][row[grouping_column]]))
        
    sf[target] = gl.SArray(lst)
    return sf

def summary_recommend(all_reviews, methods, mongo, target='stars'):
    '''
    INPUT: DataFrame, List, MongoToPython
    DESCRIPTION: prints the summary of the individual recommendations.
    OUTPUT: None
    '''
    norm = gl.SFrame(all_reviews)
    #norm = normalize_ratings(norm, 'user_id')
    norm = normalize_ratings(norm, 'business_id')
    user_ids = random.sample(norm['user_id'], 10)
    for method in methods:
        print 'Method: ',method
        print run_model(norm, method, user_ids, mongo, target='stars')
        
def main():
    '''
    INPUT: None
    DESCRIPTION: Initializes methods, gets all reviews, prints the summary of the individual recommendations.
    OUTPUT: None
    '''
    methods = ['item_means', 'item_similarity', 'factorization_model', 'linear_model', 'matrix_factorization', 'popularity']
    all_reviews = mongo.mongo_to_df('reviews', ['business_id', 'user_id', 'stars'], dict_requirements={})
    summary_recommend(all_reviews, methods, mongo)
    
if __name__ == '__main__':
    main()