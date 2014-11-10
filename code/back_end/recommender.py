import graphlab as gl

class Recommender():
    '''
    Produces recommendations using a model
    '''
    
    def __init__(self, filePath='../../data/ranking_factorization_recommender'):
        '''
        INPUT: String
        DESCRIPTION: Loads and saves the model given a filepath
        OUTPUT: None
        '''
        self.model = gl.load_model(filePath)
    
    def make_prediction(self, user_list):
        '''
        INPUT: List
        DESCRIPTION: Initializes a Recommendation given the user_list
        OUTPUT: Recommendation
        '''
        return Recommendation(user_list, self.model)