class Group():
    '''
    Encapsulates the Group attributes and inherits from Entity
    '''
        
    def __init__(self, mongo_doc):
        '''
        INPUT: Dictionary
        DESCRIPTION: Initializes Group and assigns various attributes
        OUTPUT: None
        '''
        self.name = mongo_doc['name']
        self.group_id = mongo_doc['group_id']
        self.leaders_id = mongo_doc['leaders_id']
        self.members = mongo_doc['members_id']