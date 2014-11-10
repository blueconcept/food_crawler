import graphlab as gl
import random
import pandas as pd
import pickle
import cPickle as cp

class Model():
    
    def __init__(self, method='ranking_factorization_recommender', item_normal=True, model=None):
        '''
        INPUT: String, boolean, boolean
        DESCRIPTION: Gets the business data and review data into SFrames and saves them
        OUTPUT: None
        '''
        self.method = method
        self.mongo_interface = MongoInterface()
        self.businesses = gl.load_sframe("businesses")
        self.reviews = gl.load_sframe("reviews")
        
        if model == None:
            self.model = self.build(method, item_normal)
        else:
            self.model = model
        
    def get_businesses(self, bus_file="businesses.pickle"):
        '''
        INPUT: String
        DESCRIPTION: Loads and gets the business data
        OUTPUT: SFrame
        '''
        businesses = gl.load_sframe("businesses")
        return businesses
    
    def get_reviews(self, rev_file="reviews.pickle"):
        '''
        INPUT: String
        DESCRIPTION: Loads and gets the review data
        OUTPUT: SFrame
        '''
        reviews = gl.load_sframe("reviews")
        return reviews
    
    def build(self, method, item_normal=False):
        '''
        INPUT: String, boolean
        DESCRIPTION: Returns the model chosen by the String of method
        OUTPUT: Model
        '''
        if item_normal:
            self.reviews = normalize_ratings(self.reviews, 'business_id')
        #Could use a dictionary but might be buggier
        if method == "item_similarity_recommender":
            return gl.recommender.item_similarity_recommender.create(self.reviews, item_id="business_id", target="stars", item_data=self.businesses)
        if method == "factorization_recommender":
            return gl.recommender.factorization_recommender.create(self.reviews, item_id="business_id", target="stars", item_data=self.businesses)
        if method == "ranking_factorization_recommender":
            return gl.recommender.ranking_factorization_recommender.create(self.reviews, item_id="business_id", target="stars", item_data=self.businesses)
        if method == "popularity_recommender":
            return gl.recommender.popularity_recommender.create(self.reviews, item_id="business_id", target="stars", item_data=self.businesses)
        raise LookupError("Build Error: not one of the models for recommenders")
    
    def normalize(self, value, average):
        '''
        INPUT: int, float
        DESCRIPTION: Scales the value to an 
        OUTPUT: float
        '''
        return (value-average)/average

    def normalize_ratings(self, sf, grouping_column, target='stars'):
        '''
        INPUT: SFrame, String
        DESCRIPTION: Normalizes the SFrame's according to the grouping_column parameter
        OUTPUT: SFrame
        '''
        group_averages = sf.groupby(grouping_column, {'average':gl.aggregate.MEAN(target)})
        average_dict = group_averages.to_dataframe().set_index(grouping_column).to_dict()
        i = 0
        lst = []
        for row in sf:
            lst.append(self.normalize(row[target], average_dict['average'][row[grouping_column]]))
            
        sf[target] = gl.SArray(lst)
        return sf
        
    def sample_recommendation(self, number_of_users, rec_list_size):
        '''
        INPUT: int, int
        DESCRIPTION: Tests the recommendation of the models
        OUTPUT: DataFrame
        '''
        #get list of user_id samples
        percent_sample = (number_of_users+0.0)/self.reviews.shape[0]
        print percent_sample
        sample_users = self.reviews.sample(percent_sample, seed=5)
        print sample_users.shape
        dict_of_dict = {}
        #for each user id make get rec list and concat
        for user_row in sample_users:
            rec = self.model.recommend([user_row['user_id']], k=rec_list_size)
            user_dict = {}
            i=0
            for business_id in rec:
                business = self.mongo_interface.get_business(business_id['business_id'])
                user_dict[i] = list(business.get_info())
                i += 1
            dict_of_dict[user_row['user_id']] = user_dict
        return pd.DataFrame(dict_of_dict)

    def save(self, file_name='model'):
        '''
        INPUT: int, int
        DESCRIPTION: Saves the model into a model filepath
        OUTPUT: None
        '''
        filepath = '../../data/'
        return self.model.save(filepath+file_name)