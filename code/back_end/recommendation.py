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
        self.groupmodel = self.group_predictions(user_id_list)
        
    def individual_prediction(self, user_id_list):
        '''
        INPUT: List
        DESCRIPTION: Generates a dictionary of dataframes containing 
        the recommendations for each user in the List
        OUTPUT: Dictionary
        '''
        return { user_id:model.recommend(user_id, k=sys.maxint) for user_id in user_id_list}
    
    def group_predictions(self, user_id_list):
        '''
        INPUT: List
        DESCRIPTION: Creates a groupmodel based on the user_id_list
        OUTPUT: GroupModel
        '''
        return GroupModel(self.model, user_id_list)

    def evaluate_rmse(self, user_id_list):
        '''
        INPUT: List
        DESCRIPTION: Evaluates the RMSE between the users and the group Recommendation, expect a list between 2-6
        OUTPUT: None
        '''
        user_count = len(user_id_list)
        individual_predictions = self.individual_prediction(user_id_list)
        group_model = self.group_predictions(user_id_list)
        leastmisery = 0.0
        average = 0.0
        bohr = 0.0

        lm = gl.group_model.least_misery(user_id_list).sort('business_id')['score']
        ave = gl.group_model.average(user_id_list).sort('business_id')['score']
        bo = gl.group_model.average(user_id_list).sort('business_id')['score']

        for user_id,predictions in individual_predictions.iteritems():
            pred = predictions.sort('business_id')['score']
            leastmisery += gl.evaluate.rmse(lm, pred)
            average += gl.evaluate.rmse(ave, pred)
            bohr += gl.evaluate.rmse(bo, pred)

        return (leastmisery/user_count, average/user_count, bohr/user_count)