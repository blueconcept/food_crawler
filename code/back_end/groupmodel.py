import graphlab as gl
import sys

class GroupModel():
    '''
    Makes the group recommendations
    '''
    
    def __init__(self, model, users, new_users_list=[]):
        '''
        INPUT: Model, List, List
        DESCRIPTION: Initializes the grouped SFrame 
        OUTPUT: None
        '''

        self.model = model
        recommend_df = model.recommend(users=users, k=sys.maxint)
        self.grouped = recommend_df.groupby('business_id', {'Average':gl.aggregate.AVG('score'), 
            'LeastMisery':gl.aggregate.MIN('score'), 'Bohrs':gl.aggregate.SUM('rank')})
        
    def least_misery(self):
        '''
        INPUT: None
        DESCRIPTION: Gets the minimum score for each resturant given by each individual
        OUTPUT: SFrame
        '''
        return self.grouped.sort(['LeastMisery'], ascending=False)[['business_id', 'LeastMisery']]
    
    def average_score(self):
        '''
        INPUT: None
        DESCRIPTION: Gets the average score for each resturant given by each individual
        OUTPUT: SFrame
        '''
        return self.grouped.sort(['Average'], ascending=False)[['business_id', 'Average']]
    
    def bohrs(self):
        '''
        INPUT: None
        DESCRIPTION: Gets the bohr score for each resturant sum by each individual's bohr score
        OUTPUT: SFrame
        '''
        return self.grouped.sort(['Bohrs'], ascending=True)[['business_id', 'Bohrs', 'score']]
