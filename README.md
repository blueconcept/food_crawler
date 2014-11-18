FoodCrawler by Thang Tran

Project Summary:

FoodCrawler is a prototype for a Social Platform that uses data science to recommend restaurants to individuals and groups of people and thereby making restaurant selection more of a social activity.

With FoodCrawler, you can create groups, get group recommendations, find and add friends, find and review businesses, and get your own individual recommendations.

Data Explorations:

I used the data from Yelp’s Challenge Dataset.  The dataset has information on the reviews with ratings, data on users, and other files with no relevance to this project.  

I first explored the data through importing json briefly to understand what the data looks like overall.  

Getting the Data and first Exploration

Exploring the data I realized that a majority of the data was from Las Vegas and Phoenix.  I considered the idea of isolating my dataset geographically (ie to one city like Las Vegas) but I decided to try to see if using multiple cities would be viable since doing so would add to the functionality of the app (user might be in another city that he or she usually is not in).  I also left other business types in for the option to expand to other domains to recommend as well (and allow the user to choose what type of business, this would be tested later on as well).   

I decided to use all of the reviews and tossed my json data files into MongoDB.  This done through “json_to_mongo.py” under the “data_prep” folder such that my database has these collections:

-users
-reviews
-businesses

and added later on solely for OLTP operations:

-groups
-group_invitations
-invitations (for friends)

Models and Experimentation for Individual Recommendations:

I used GraphLab to train and build models.  I knew I wanted to use and compare item-based collaborative filtering as well as factorization since those have been optimized by Graphlab.  

The file “eda.py” is the first experiment I used to evaluate my models.  I tested by viewing the accuracy/precision, RMSE, and recommendations from the models.  To me, the actually recommendations was the most important factor in choosing a model because the metrics themselves serve to predict the ratings a user would give rather than a produce recommendations relevant to the user.  Everyone knows that if you went to a 5 star restaurant with the best service and most high quality food you are going to give that restaurant 5 stars hands down but that does not necessarily mean this restaurant is reflective of kind of food you like or what kind of dining experience you prefer to have. 

Looking at the first recommendations I received from a few random users using ranking factorization, I noticed that the recommendations were the same or very similar.  Because of this, I tested the models both with normalizing the ratings by businesses and unnormalized.  I also ran a test comparing the performances of the models when using only restaurant reviews compared to using all reviews and saw no improvements in any metrics.

The code in “eda.py” and “recommendation_test.py” was used to answer these questions:

1. Do different methods give more personalized results? 

Only item similarity content based filtering gave unique recommendations to users.  In most outcomes, the recommendations for the other models had the exact top 10 or a set of the same similar top 10.
  
2. Do different methods score better in terms of RMSE?

Ranking factorization and factorization gave better RMSE, I hypothesized that the higher scoring was only partly due to overfitting rather than actual useful predictions or rather the models served to produce a recommendation list of the top quality restaurants, normalized and unnormalized.  

3. Does normalizing the ratings lead to better personalized results?

They did not.

4. Does normalizing the users lead to better personalized results?

Doing this did not achieve that result.



These results lead me to adopt item similarity as it was the only model that gave personalized results reflective of user’s past reviews.  

I further tested this conclusion by inserting artificial users into the dataset with preferences for a specific type of restaurant and again seeing if the recommendations made sense.  This was done in IPython Notebook but the code can be found at insertartificialusers.py which also served to test MongoInterface class.  The results of that code showed that only item similarity gave relevant recommendations whereas the other models did not carry a signal.

Group Recommendations

For group recommendations, I found from the literature on the subject that simple aggregation of group’s individual recommendation lists would make sufficient recommendations.  I implement 3 methods but kept only one for performance purposes.  I am currently using 
average which was implemented by only summing the scores (without dividing by the number of users).

Model Optimization

I grid searched item similarity in the file “gridsearch.py” which consisted of using GraphLab to find which distance metric to use.  I found that cosine was the best metric to use based on RMSE.

Model Saving and Back-End

I saved my model using “Model.py” to a binary folder using GraphLab.  I had used pickling also to see which took less time and GraphLab’s storage option took a lot less time.  

I created classes for making Recommendations, Groups, Users, Reviews, and so forth.  Important classes to note are MongoToPython, a class for getting data out of mongo which was used during EDA and for my app, MongoInterface a class for specifically getting data from Mongo specific to the application, Model, a class wrapping around my GraphLab models which could also test the models, and GroupModel has the group recommendations. 

Front-End

For front-end, the main file is “app.py” and many HTML files using Boostrap with scripts of JavaScript and CSS styling.  
 
Next Steps and Potential Improvements

The Reviews and making Reviews through finding businesses could be more efficient and take less time.
  
I wished I had time to implement features like a Group and Friend Suggestor based on recommendation list similarity, or a recommendation system for dissimilarity. 

I would also use separate OLTP and OLAP databases in order to improve the Reviews and making Reviews.
