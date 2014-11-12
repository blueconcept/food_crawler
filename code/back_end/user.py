class User():
    '''
    Encapsulates the User 
    '''
    
    def __init__(self, mongo_doc):
        '''
        INPUT: MongoToPython
        DESCRIPTION: Initializes User and assigns user_id and friends
        OUTPUT: None
        '''
        self.name = mongo_doc['name']
        self.user_id = mongo_doc["user_id"]
        self.friends = mongo_doc["friends"]