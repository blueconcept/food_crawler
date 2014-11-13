from groupmodel import GroupModel
import graphlab as gl
import sys

class Recommendation():
    '''
    Encapulates the predictions
    '''
    
    def __init__(self, user_id_list, model):
        '''
        INPUT: List, Model
        DESCRIPTION: Saves the model and builds the group model
        OUTPUT: None
        '''
        self.model = model
        self.user_id_list = user_id_list
        self.groupmodel = self.group_predictions()
        
    def individual_prediction(self):
        '''
        INPUT: List
        DESCRIPTION: Generates a dictionary of dataframes containing 
        the recommendations for each user in the List
        OUTPUT: Dictionary
        '''
        return {user_id:self.model.recommend([user_id], k = sys.maxint) for user_id in self.user_id_list}
    
    def group_predictions(self):
        '''
        INPUT: List
        DESCRIPTION: Creates a groupmodel based on the user_id_list
        OUTPUT: GroupModel
        '''
        return GroupModel(self.model, self.user_id_list)

    def evaluate_rmse(self):
        '''
        INPUT: List
        DESCRIPTION: Evaluates the RMSE between the users and the group Recommendation, expect a list between 2-6
        OUTPUT: float, float
        '''
        user_count = len(self.user_id_list)
        individual_predictions = self.individual_prediction()
        
        leastmisery = 0.0
        average = 0.0
        bohr = 0.0

        lm = self.groupmodel.least_misery().sort('business_id')['LeastMisery']
        lm = lm[0:len(lm)]
        ave = self.groupmodel.average_score().sort('business_id')['Average']
        ave = ave[0:len(ave)]
        
        length = 40000

        for user_id,predictions in individual_predictions.iteritems():
            pred = predictions.sort('business_id')['score']
            leastmisery += gl.evaluation.rmse(lm[0:length], pred[0:length])
            average += gl.evaluation.rmse(ave[0:length], pred[0:length])
        return leastmisery/user_count, average/user_count