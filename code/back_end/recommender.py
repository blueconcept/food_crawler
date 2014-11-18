import graphlab as gl
from recommendation import Recommendation

class Recommender():
    '''
    Produces recommendations using a model
    '''
    
    def __init__(self, filePath='../../data/ranking_factorization_recommender', model=None):
        '''
        INPUT: String
        DESCRIPTION: Loads and saves the model given a filepath
        OUTPUT: None
        '''
        if model == None:
            self.model = gl.load_model(filePath)
        else:
            self.model = model
    
    def make_prediction(self, user_list):
        '''
        INPUT: List
        DESCRIPTION: Initializes a Recommendation given the user_list
        OUTPUT: Recommendation
        '''
        if user_list is None:
            raise TypeError('make_prediction')
        return Recommendation(user_list, self.model)