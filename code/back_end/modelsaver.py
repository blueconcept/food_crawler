import pandas as pd 
import graphlab as gl

def save_cleaned_data():
    '''
    INPUT: None
    DESCRIPTION: 
    OUTPUT: None
    '''
    df = get_business_data_cleaned()
    df['business_id'] = df.index
    mongo = MongoInterface()
    gl.SFrame(mongo.reviews()).save("reviews")
    gl.SFrame(df).save("businesses")
    
    
def making_models(list_methods = ['item_similarity_recommender', 'factorization_recommender', 
                    'ranking_factorization_recommender']):
    '''
    INPUT: None
    DESCRIPTION: 
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
        DESCRIPTION: 
        OUTPUT: None
        '''
    list_methods = ['factorization_recommender', 'factorization_recommender',
                    'ranking_factorization_recommender']
    model = Model(model=gl.load_model('item_similarity_recommender'))
    print model.sample_recommendation(20, 10)
    for model_name in list_methods:
        model.model = gl.load_model(model_name)
        print model.sample_recommendation(20,10)