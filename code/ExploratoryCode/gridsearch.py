import graphlab as gl

reviews = gl.load_sframe("../../data/reviews")

secret_key = 'PpF/mJwf8Anr13uBj1yZeB+8ZujswnnpDUlGIjYI'

train_file_path = 's3://stdofcumsum/train_file_path'
test_file_path = 's3://stdofcumsum/test_file_path'
train, test = gl.recommender.util.random_split_by_user(reviews, item_id='business_id', max_num_users=10000, random_seed=42)
train.save(train_file_path)
test.save(test_file_path)

gl.aws.set_credentials('AKIAJ2MQ7EWTNHLPESOA', secret_key)
ec2_env = gl.deploy.environment.EC2('ec2 env', 's3://stdofcumsum/log-dir', 
                                    instance_type="t2.micro", 
                                    region='us-east-1b', 
                                    security_group="launch-wizard-1")

# secret_key_path = ''
# ec2 = gl.deploy.environment.EC2('ec2', aws_access_key='AKIAIOKKJCZF7OVTXONQ',
#                                 aws_secret_key=secret_key_path,
#                                 s3_log_folder_path='s3://bucket/logpath',
#                                 region='us-east-1b',
#                                 instance_type='t1.micro')

constant_params = {'item_id':'business_id', 'target':'stars'}
search_params = {'similarity_type':['jaccard', 'cosine', 'pearson'], 'only_top_k':[50,100,200,500]}

# model.businesses.save('s3://stdofcumsum/businesses_file_path')
save_file_path = 's3://stdofcumsum/save_file_path'
gridjob = gl.toolkits.model_parameter_search(ec2_env, gl.recommender.item_similarity_recommender.create, 
                                             train_file_path, save_file_path, test_set_path=test_file_path, 
                                   standard_model_params=constant_params, hyper_params=search_params, name='ItemtoItemSim2')

search_params = {'num_factors':[60000], 'ranking_regularization':[0, 0.1, 0.5, 1.]}
gridjob = gl.toolkits.model_parameter_search(ec2_env, gl.recommender.ranking_factorization_recommender.create, train_file_path, save_file_path, 
                                   test_set_path=test_file_path, standard_model_params=constant_params, hyper_params=search_params)