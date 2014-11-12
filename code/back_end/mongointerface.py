from mongotopandas import MongoToPython
from user import User
from business import Business
from group import Group
from invitation import Invitation
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

    def get_all_users(self):
        '''
        INPUT: None
        DESCRIPTION: Gets all of the users
        OUTPUT: List
        '''
        return [user['user_id'] for user in self.mongo.query_all(self.users_collection)]

    def get_all_businesses(self):
        '''
        INPUT: None
        DESCRIPTION: Gets all of the users
        OUTPUT: List
        '''
        return [[business['business_id'], business['name'], business['city'], ' '.join(business['categories'])] for business in self.mongo.query_all(self.businesses_collection)]

    ### May want to check if count is 0 then return None ###
    def get_all_friends(self, user_id):
        '''
        INPUT: String
        DESCRIPTION: Gets all of the user's friends
        OUTPUT: List
        '''
        return self.get_user(user_id).friends

    def get_all_reviews(self, user_id):
        '''
        INPUT: String
        DESCRIPTION: Gets all of the users reviews
        OUTPUT: List
        '''
        return [reviews for reviews in self.mongo.query_all(self.reviews_collection, dict_requirements = {"user_id":user_id})]

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
        field = 'user_id'
        self.duplicate_check(self.users_collection, field, unique_id )
        self.mongo.insert(self.users_collection, {field:unique_id, 'name':name, 'friends':[]})

    def create_review(self, user_id, business_id, stars):
        '''
        INPUT: String, String, int
        DESCRIPTION: Inserts a review into the MongoDB
        OUTPUT: None
        '''
        self.mongo.insert(self.reviews_collection , {'user_id':user_id, 'business_id': business_id, 'stars': stars})

    def create_group(self, leader_user_id, name, members_id = []):
        '''
        INPUT: String, Dictionary
        DESCRIPTION: Inserts a group into a the MongoDB
        OUTPUT: None
        '''
        group_id = name+leader_user_id
        field = 'group_id'
        self.duplicate_check(self.groups_collection, field, group_id)
        self.mongo.insert(self.groups_collection, {field: group_id,'leaders_id': leader_user_id, 'members_id':members_id, 'name':name})

    def create_invitation(self, inviter_id, invited_id):
        '''
        INPUT: String, String
        DESCRIPTION: Inserts an invitation into the MongoDB 
        OUTPUT: None
        '''
        invitation_count = inviter_id+inviter_id+self.get_next_id(self.invitations_collection)
        self.duplicate_check(self.invitations_collection, 'invitation_id',invitation_count)
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
        field = 'members_id'
        groups_dict = self.mongo.get_one(self.groups_collection, 'group_id', group_id)
        self.mongo.replace(self.groups_collection, self.duplicate_check_list(groups_dict, field, friend_id), 'group_id', group_id)

    def add_friend(self, user_id, friend_id):
        '''
        INPUT: user_id, friend_id
        DESCRIPTION: Adds a friend to user's friends' list
        OUTPUT: None
        '''
        user = self.mongo.get_one(self.users_collection, 'user_id', user_id)
        self.mongo.replace(self.users_collection, self.duplicate_check_list(user, 'friends' , friend_id), 'user_id', user_id)

    def change_invitation_status(self, invitation_id, status = 'Accept'):
        '''
        INPUT: String, String
        DESCRIPTION: Changes the status of a invitation
        OUTPUT: None
        '''
        invitation = self.mongo.get_one(self.invitations_collection, 'invitation_id', invitation_id)
        invitation['status'] = status
        self.mongo.replace(invitations_collection, invitation, 'invitation_id', invitation_id)

    def duplicate_check_list(self, dictionary, field, object_id):
        '''
        INPUT: Dictionary, String, String
        DESCRIPTION: Checks for duplicates in the list and returns a dictionary with updated field and throws error otherwise
        OUTPUT: Dictionary
        '''
        if object_id in dictionary[field]:
            raise TypeError("Duplicate Found")
        else:
            dictionary[field].append(object_id)
            return dictionary

    def duplicate_check(self, collection, key_id, value_id):
        '''
        INPUT: String, String, String
        DESCRIPTION: Checks for duplicates and returns true for no duplicates and false for yes duplicates
        OUTPUT: Dictionary
        '''
        if self.mongo.get_one(collection, key_id, value_id) == None:
            return True
        raise TypeError('Duplicate Found')
#
# Other functions
#
    def remove(self, collection, key_id, value_id):
        '''
        INPUT: String, String, String
        DESCRIPTION: Removes an object from a collection given a key and value pair
        OUTPUT: None
        '''
        self.mongo.db[collection].remove(spec_or_id={key_id:value_id})

    def login(self,user_id):
        '''
        INPUT: String, String
        DESCRIPTION: Changes the status of a invitation
        OUTPUT: None
        '''
        user = self.mongo.get_one(self.users_collection, 'user_id', user_id)
        if user == None:
            return False
        else:
            return True

    def get_next_id(self, collection_name):
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
        gl.SFrame(self.reviews(dict_requirements = dict_requirements).replace(to_replace='5', value=5)).save(path + file_name)

    def save_business(self, file_name = 'businesses'):
        '''
        INPUT: String
        DESCRIPTION: Takes all of Mongo's Businesses and saves them as a binary file for later use
        OUTPUT: None
        '''
        path = '../../data/'
        gl.SFrame(cleaned(self.mongo)).save(path + file_name)