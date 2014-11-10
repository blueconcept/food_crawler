import graphlab as gl

class FilterSort():
    '''
    Stores the recommender_sf to be filtered and changed into objects for the front end
    '''
    
    def __init__(self, recommender_sf):
        '''
        INPUT: SFrame
        DESCRIPTION: 
        OUTPUT: None
        '''
        self.recommender_sf = recommender_sf
        self.booleans = {}
    
    def get_filtered_list(self, top_n_items=10):
        '''
        INPUT: None
        DESCRIPTION: 
        OUTPUT: None
        '''
        pass