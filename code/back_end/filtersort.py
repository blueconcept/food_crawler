from business import Business
from mongointerface import MongoInterface
import graphlab as gl

class BusinessFilter():
    '''
    Stores the recommender_sf to be filtered and changed into objects for the front end
    '''
    
    def __init__(self, business_id_list, mongointerface, categories = ["Restaurants"], cities = ['Las Vegas']):
        '''
        INPUT: List, List, String
        DESCRIPTION: Takes in a list of businesses_id and filters them out given a list of categories and city
        OUTPUT: None
        '''
        self.business_id_list = business_id_list
        self.categories = categories
        self.cities = cities
        self.mongointerface = mongointerface
    
    def get_filtered_list(self, top_n_items=10):
        '''
        INPUT: int 
        DESCRIPTION: Returns the top n elements of the filtered list of Business objects
        OUTPUT: List
        '''
        n = 0
        bus_list = []
        for business_id in self.business_id_list:
            business = self.mongointerface.get_business(business_id)
            if self.check_business(business):
                bus_list.append(business)
            if len(bus_list) == top_n_items:
                break
        return bus_list

    def check_business(self, business):
        '''
        INPUT: Business
        DESCRIPTION: Takes a Business object and returns true if the object has the meet the criteria
        OUTPUT: boolean
        '''
        return set(self.categories).issubset(business.categories) and (business.city in self.cities)