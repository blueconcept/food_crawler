from mongotopandas import MongoToPython
from entities import User
from entities import Business
from entities import Group
from entities import Invitation
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
    
#
# Get a Single Object from Mongo
#

    def get_user(self, user_id):
        '''
        INPUT: String
        DESCRIPTION: Initializes and returns a User object with the user_id from MongoDB
        OUTPUT: User
        '''
        return User(self.mongo.get_one(self.users_collection, "user_id", user_id ))
    
    def get_business(self, business_id):
        '''
        INPUT: String
        DESCRIPTION: Initializes and returns a Business object with the user_id, business_id from MongoDB
        OUTPUT: Business
        '''
        return Business(self.mongo.get_one(self.businesses_collection, "business_id", business_id))

    def get_group(self, group_id):
        '''
        INPUT: String
        DESCRIPTION: Initializes and returns a Group object with the group_id from MongoDB
        OUTPUT: Group
        '''
        return Group(self.mongo.get_one(self.groups_collection, "group_id", group_id))

    def get_invitation(self, invitation_id):
        '''
        INPUT: String
        DESCRIPTION: Initializes and returns a Invitation object with the invitation_id
        OUTPUT: Group
        '''
        return Invitation(self.mongo.get_one(self.invitations_collection, "invitation_id", invitation_id))

#
# Get all of a user's objects from Mongo
#

    ### May want to check if count is 0 then return None ###
    def get_all_friends(self, user_id):
        '''
        INPUT: String
        DESCRIPTION: Gets all of the user's friends
        OUTPUT: List
        '''
        return [self.get_user(friend_id) for friend_id in self.mongo.get_one(self.users_collection, {'user_id':user_id})['friends']]

    def get_all_reviews(self, user_id):
        '''
        INPUT: String
        DESCRIPTION: Gets all of the users reviews
        OUTPUT: List
        '''
        return [Reviews(doc) for doc in self.mongo.query_all(self.reviews_collection, dict_requirements = {"user_id":user_id})]

    def get_all_lead_groups(self, user_id):
        '''
        INPUT: String
        DESCRIPTION: Gets all of the users group that she/he is leader of 
        OUTPUT: List
        '''
        return [Group(doc) for doc in self.mongo.query_all(self.groups_collection, dict_requirements = {"leaders_id":user_id})]

    def get_all_member_groups(self, user_id):
        '''
        INPUT: String
        DESCRIPTION: Gets all of the user's group that she/he is a member of
        OUTPUT: List
        '''
        return [Group(doc) for doc in self.mongo.query_all(self.groups_collection) if user_id in doc['friends']]

    def get_all_out_invitations(self, user_id):
        '''
        INPUT: String
        DESCRIPTION: Gets all of the user's outgoing invitations
        OUTPUT: List
        '''
        return [Invitation(doc) for doc in self.mongo.query_all(self.invitations_collection) if user_id in doc['inviter_id']]

    def get_all_in_invitations(self, user_id):
        '''
        INPUT: String
        DESCRIPTION: Gets all of the user's incoming invitations
        OUTPUT: List
        '''
        return [Invitation(doc) for doc in self.mongo.query_all(self.invitations_collection) if user_id in doc['invited_id']]

#
# Inserts into MongoDB
#

    def create_user(self, name, unique_id=None):
        '''
        INPUT: String, String
        DESCRIPTION: Inserts a user into the MongoDB
        OUTPUT: Group
        '''
        if unique_id == None:
            unique_id = self.get_next_id(self.users_collection)
        
        self.mongo.insert(self.users_collection, {'user_id':unique_id, 'name':name, 'friends':[]})

    def create_review(self, user_id, business_id, stars):
        '''
        INPUT: String, String, int
        DESCRIPTION: Inserts a review into the MongoDB
        OUTPUT: None
        '''
        self.mongo.insert(self.reviews_collection , {'user_id':user_id, 'business_id': business_id, 'stars': stars})

    def create_group(self, leader_user_id, name, members_id = {}):
        '''
        INPUT: String, Dictionary
        DESCRIPTION: Inserts a group into a the MongoDB
        OUTPUT: None
        '''
        self.mongo.insert(self.groups_collection, {'leaders_id': leader_user_id, 'members_id':members})

    def create_invitation(inviter_id, invited_id):
        '''
        INPUT: String, String
        DESCRIPTION: Inserts an invitation into the MongoDB 
        OUTPUT: None
        '''
        invitation_count = inviter_id+inviter_id+self.get_next_id(self.invitations_collection)
        self.mongo.insert(self.invitations_collection, {'invitation_id':invitation_count, 'inviter_id':inviter_id, 'inviter_id':invited_id, 'status':'pending'})

#
# Updates for MongoDB
#

    def add_friend_group(self, group_id, friend_id):
        '''
        INPUT: String, String
        DESCRIPTION: Adds friend into existing group for MongoDB
        OUTPUT: None
        '''
        groups_dict = self.mongo.get_one(self.groups_collection)
        groups_dict['members'].append(friend_id)
        self.mongo.replace(self.groups_collection, {'members': groups_dict['members']}, 'group_id', group_id)

    def add_friend(self, user_id, friend_id):
        '''
        INPUT: user_id, friend_id
        DESCRIPTION: Adds a friend to user's friends' list
        OUTPUT: None
        '''
        user = self.mongo.get_one({'user_id':user_id})
        user['friends'].append(friend_id)
        self.mongo.replace(self.users, {'friends':user['friends']}, 'user_id', user_id )

    def change_invitation_status(invitation_id, status = 'Accept'):
        '''
        INPUT: String, String
        DESCRIPTION: Changes the status of a invitation
        OUTPUT: None
        '''
        self.mongo.replace(invitations_collection, {'status':status}, 'invitation_id', invitation_id)

#
# Other functions
#
    def login(user_id):
        '''
        INPUT: String, String
        DESCRIPTION: Changes the status of a invitation
        OUTPUT: None
        '''
        if mongo.get_one(self.users_collection, 'user_id', user_id) == None:
            return False
        return True

    def get_next_id(collection_name):
        '''
        INPUT: String
        DESCRIPTION: Fetch the next id for a collection that uses a simple count id
        OUTPUT: String
        '''
        return str(self.mongo.mongo[collection_name].count() + 1)

    def reviews(self, dict_requirements=None):
        '''
        INPUT: Dictionary
        DESCRIPTION: Initializes and returns a dataframe of the reviews
        OUTPUT: None
        '''
        return self.mongo.mongo_to_df(self.reviews_collection, ['user_id', 'business_id', 'stars'], dict_requirements=dict_requirements)

    def save_reviews(self, file_name = 'reviews', dict_requirements=None):
        '''
        INPUT: String
        DESCRIPTION: Takes all of Mongo's Reviews and saves them as a binary file for later use
        OUTPUT: None
        '''
        path = '../../data/'
        gl.SFrame(self.reviews(dict_requirements = dict_requirements)).save(path + file_name)

    def save_business(self, file_name):
        '''
        INPUT: String
        DESCRIPTION: Takes all of Mongo's Businesses and saves them as a binary file for later use
        OUTPUT: None
        '''
        path = '../../data/'
        gl.SFrame(cleaned(self.mongo)).save(path + file_name)