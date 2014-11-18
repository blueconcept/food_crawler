class Business():
    '''
    Encapsulates the Business attributes 
    '''
    
    def __init__(self, mongo_doc):
        '''
        INPUT: Dictionary
        DESCRIPTION: Initializes Business and assigns various attributes
        OUTPUT: None
        '''
        self.name = mongo_doc['name']
        self.business_id = mongo_doc['business_id']
        self.categories = mongo_doc['categories']
        self.latitude = mongo_doc['latitude']
        self.longitude = mongo_doc['longitude']
        self.stars = mongo_doc['stars']
        self.review_count = mongo_doc['review_count']
        self.address = mongo_doc['full_address']
        self.city = mongo_doc['city']
        self.yelp = self.yelp_url()

    def yelp_url(self):
        '''
        INPUT: None
        DESCRIPTION: Generates the url for yelp
        OUTPUT: String
        '''
        yelp = "http://www.yelp.com/biz/"
        def add_dashes(string):
            return string.replace("@","at").replace("&", 'and').replace(" ", '-').replace("'",'')
        return yelp + add_dashes(self.name).lower() +'-'+add_dashes(self.city).lower()

    def get_info(self):
        '''
        INPUT: None
        DESCRIPTION: Returns a summary of attributes relevant for printing
        OUTPUT: String, String, String, String
        '''
        return self.stars, self.review_count, self.city, self.name