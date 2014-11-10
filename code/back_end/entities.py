class Entity(object):
    '''
    Encapsulates a general 'business' class
    '''
    def __init__(self, mongo_doc):
        '''
        INPUT: MongoToPython
        DESCRIPTION: Initializes Entity and assigns a name using MongoToPython
        OUTPUT: None
        '''
        self.name = mongo_doc['name']
        
    def __str__(self):
        '''
        INPUT: None
        DESCRIPTION: Prints out name
        OUTPUT: None
        '''
        return self.name

class User(Entity):
    '''
    Encapsulates the User and inherits from Entity
    '''
    
    def __init__(self, mongo_doc):
        '''
        INPUT: MongoToPython
        DESCRIPTION: Initializes User and assigns user_id and friends
        OUTPUT: None
        '''
        Entity.__init__(self, mongo_doc)
        self.user_id = mongo_doc["user_id"]
        self.friends = mongo_doc["friends"]
        
        
class Business(Entity):
    '''
    Encapsulates the Business attributes and inherits from Entity
    '''
    
    def __init__(self, mongo_doc):
        '''
        INPUT: MongoToPython
        DESCRIPTION: Initializes Business and assigns various attributes
        OUTPUT: None
        '''
        Entity.__init__(self, mongo_doc)
        self.business_id = mongo_doc['business_id']
        self.categories = mongo_doc['categories']
        self.latitude = mongo_doc['latitude']
        self.longitude = mongo_doc['longitude']
        self.city = mongo_doc['city']
        self.stars = mongo_doc['stars']
        self.review_count = mongo_doc['review_count']

    def get_info(self):
        '''
        INPUT: None
        DESCRIPTION: Returns a summary of attributes relevant for printing
        OUTPUT: String, String, String, String
        '''
        return self.stars, self.review_count, self.city, self.name

class Group(Entity):
    '''
    Encapsulates the Group attributes and inherits from Entity
    '''
    
    def __init__(self, mongo_doc):
        '''
        INPUT: MongoToPython
        DESCRIPTION: Initializes Group and assigns various attributes
        OUTPUT: None
        '''
        Entity.__init__(self, mongo_doc)
        self.group_id = mongo_doc['group_id']
        self.leader_id = mongo_doc['leader_id']
        self.members = mongo_doc['members']

class Invitation():
    '''
    Encapsulates the Group attributes and inherits from Entity
    '''
    
    def __init__(self, mongo_doc):
        '''
        INPUT: MongoToPython
        DESCRIPTION: Initializes Invitation and assigns various attributes
        OUTPUT: None
        '''
        self.invitation_id = mongo_doc['invitation_id']
        self.inviter_id = mongo_doc['inviter_id']
        self.invited_id = mongo_doc['invited_id']

class Review():
    '''
    Encapsulates the Review attributes and inherits from Entity
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