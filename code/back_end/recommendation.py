class Recommendation():
    '''
    Encapulates the predictions
    '''
    
    def __init__(self, user_list, model):
        '''
        INPUT: None
        DESCRIPTION: 
        OUTPUT: None
        '''
        self.methods = ['average', 'least misery', 'bohr']
        self.individuals = self.individual_predictions(model)
        self.groups = self.group_predictions(model)
        
    def individual_predictions(self):
        '''
        INPUT: None
        DESCRIPTION: 
        OUTPUT: None
        '''
        pass
    
    def group_predictions(self):
        '''
        INPUT: None
        DESCRIPTION: 
        OUTPUT: None
        '''
        pass