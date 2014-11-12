class Invitation():
    '''
    Encapsulates the Group attributes
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