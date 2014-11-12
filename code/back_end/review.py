class Review():
    '''
    Encapsulates the Review attributes 
    '''
    
    def __init__(self, mongo_doc):
        '''
        INPUT: MongoToPython
        DESCRIPTION: Initializes Review and assigns various attributes
        OUTPUT: None
        '''
        self.review_id = mongo_doc['review_id']
        self.user_id = mongo_doc['user_id']
        self.business_id = mongo_doc['business_id']
        self.stars = mongo_doc['stars']