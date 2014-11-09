from mongotopandas import MongoToPython
from entities import User
from entities import Business
from mongo_to_binary import get_business_data_cleaned as cleaned
import graphlab as gl
import mongo_to_binary as mtb

class MongoInterface():
    '''
    To go from MongoToPython to Front End
    '''

    def __init__(self):
        '''
        INPUT: None
        DESCRIPTION: Initializes MongoInterface assigns a MongoToPython
        OUTPUT: None
        '''
        self.mongo = MongoToPython('foodcrawler')
        self.reviews_collection = 'reviews'
        self.businesses_collection = 'businesses'
        self.users_collection = 'users'
        self.groups_collection = 'groups'
        self.invitations_collection = 'invitations'
        
    def get_user(self, user_id):
        '''
        INPUT: String
        DESCRIPTION: Initializes and returns a User object with the user_id
        OUTPUT: User
        '''
        return User(self.mongo.get_one(self.users_collection, "user_id", user_id ))
    
    def get_business(self, business_id):
        '''
        INPUT: String
        DESCRIPTION: Returns a 
        OUTPUT: Business
        '''
        return Business(self.mongo.get_one("businesses", "business_id", business_id))

    def get_group(self, group_id):
        '''
        INPUT: String
        DESCRIPTION: Initializes and returns a Group object with the group_id
        OUTPUT: Group
        '''
        pass
    
    def reviews(self, dict_requirements=None):
        '''
        INPUT: Dictionary
        DESCRIPTION: Initializes and returns a dataframe of the 
        OUTPUT: None
        '''
        return self.mongo.mongo_to_df(self.reviews_collection, ['user_id', 'business_id', 'stars'], dict_requirements=dict_requirements)

    def create_review(self, user_id, business_id, stars):
        '''
        INPUT: 
        DESCRIPTION: 
        OUTPUT: None
        '''
        self.mongo.insert(self.reviews_collection , {'user_id':user_id, 'business_id': business_id, 'stars': stars})

    def create_group(self, leader_user_id, members_id={}):
        '''
        INPUT: 
        DESCRIPTION: 
        OUTPUT: None
        '''
        self.mongo.insert(self.groups_collection, {'leaders_id': leader_user_id, 'members_id':members})

    def add_friend_group(self):
        '''
        INPUT: 
        DESCRIPTION: 
        OUTPUT: None
        '''
        self.mongo.replace

    def add_friend(self):
        '''
        INPUT: 
        DESCRIPTION: 
        OUTPUT: None
        '''
        pass

    def add_invitation(inviter_id, invited_id):
        '''
        INPUT: 
        DESCRIPTION: 
        OUTPUT: None
        '''
        pass

    def save_reviews(self, file_name='reviews', dict_requirements=None):
        '''
        INPUT: String
        DESCRIPTION: Takes all of Mongo's Reviews and saves them as a binary file for later use
        OUTPUT: None
        '''
        path = '../../data/'
        gl.SFrame(self.reviews(dict_requirements=dict_requirements)).save(path+file_name)

    def save_business(self, file_name):
        '''
        INPUT: String
        DESCRIPTION: Takes all of Mongo's Businesses and saves them as a binary file for later use
        OUTPUT: None
        '''
        path = '../../data/'
        gl.SFrame(cleaned(self.mongo)).save(path+file_name)