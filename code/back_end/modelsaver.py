from model import Model
from mongointerface import MongoInterface
import pandas as pd 
import graphlab as gl

'''
Functions for save the models, later moved to the backend
'''

fp = '../../data/'

def save_cleaned_data():
    '''
    INPUT: None
    DESCRIPTION: Saves the business data
    OUTPUT: None
    '''
    df = get_business_data_cleaned()
    df['business_id'] = df.index
    mongo = MongoInterface()
    gl.SFrame(mongo.reviews()).save(fp+"reviews")
    gl.SFrame(df).save(fp+"businesses")
    
def making_models(list_methods = ['item_similarity_recommender', 'factorization_recommender', 
                    'ranking_factorization_recommender']):
    '''
    INPUT: None
    DESCRIPTION: Makes and saves the model (deprecated)
    OUTPUT: None
    '''
    model = Model()
    model.save('item_similarity_recommender')
    for method in list_methods:
        model.model = model.build(method)
        model.save(method)
        
def test_models():
    '''
    INPUT: None
    DESCRIPTION: Tests the model
    OUTPUT: None
    '''
    list_methods = ['factorization_recommender', 'factorization_recommender',
                    'ranking_factorization_recommender']
    model = Model(model=gl.load_model(fp+'item_similarity_recommender'))
    print model.sample_recommendation(20, 10)
    for model_name in list_methods:
        model.model = gl.load_model(model_name) 
        print model.sample_recommendation(20,10)