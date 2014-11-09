def func(users, products, k_rank, step_size):
	'''
	INPUT: numpy.array, numpy.array, int, int
	DESCRIPTION: 
	OUTPUT: numpy.array, numpy.array
	'''
	obs = reviews()
	alpha = random.choice(users)
	beta = random.choice(products)
	new_alpha = alpha
	beta = beta
	for observation in obs:
		rhat = compute_rhat(alpha, beta, k_rank)
		for l in xrange(0, k_rank):
			new_alpha[i] = alpha[i] + 2*step_size*beta[i]
			new_beta[i] = beta[i] + 2*step_size*alpha[i]
	return new_alpha, new_beta

def computer_rhat(alpha, beta, k):
	for l in xrange(0, k_rank):
		r += alpha[l]*beta[l]
	return r