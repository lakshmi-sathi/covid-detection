import random #import randrange
import pickle

data = []
fp = open('corona_data_processed.csv')
feats = fp.readline()
i = 0
for line in fp:
    line = line[:-1]
    #print(line.split(","))
    try:
        data.append([int(l) for l in line.split(",")])
    except:
        print (line.split(","),line,i)
    i = i +1

# Calculate accuracy percentage
def accuracy_metric(actual, predicted):
	correct = 0
	for i in range(len(actual)):
		if actual[i] == predicted[i]:
			correct += 1
	return correct / float(len(actual)) * 100.0
 
# Split a dataset based on an attribute and an attribute value
def trial_split(index, value, dataset):
	left, right = list(), list()
	for row in dataset:
		if row[index] < value:
			left.append(row)
		else:
			right.append(row)
	return left, right
 
#Calculate gini score
def gini_index(groups, classes):
	# count all samples at split point
	n_instances = float(sum([len(group) for group in groups]))
	# sum weighted Gini index for each group
	gini = 0.0
	for group in groups:
		size = float(len(group))
		# avoid divide by zero
		if size == 0:
			continue
		score = 0.0
		# score the group based on the score for each class
		for class_val in classes:
			p = [row[-1] for row in group].count(class_val) / size
			score += p * p
		# weight the group score by its relative size
		gini += (1.0 - score) * (size / n_instances)
	return gini
 
# Select the best split point for a dataset
def get_split(dataset):
	class_values = list(set(row[-1] for row in dataset))
	b_index, b_value, b_score, b_groups = 999, 999, 999, None
	for index in range(len(dataset[0])-1):
		for row in dataset:
			groups = trial_split(index, row[index], dataset)
			gini = gini_index(groups, class_values)
			if gini < b_score:
				b_index, b_value, b_score, b_groups = index, row[index], gini, groups
	return {'index':b_index, 'value':b_value, 'groups':b_groups}

# Create a terminal node value
def termcheck(data):
	outputs = [sample[-1] for sample in data]
	return max(set(outputs), key=outputs.count)
 
# Create child splits for a node or make terminal
def grow_rec(node, max_depth, min_size, depth):
	left, right = node['groups']
	del(node['groups'])
	# check for a no split
	if not left or not right:
		node['left'] = node['right'] = termcheck(left + right)
		return
	# check for max depth
	if depth >= max_depth:
		node['left'], node['right'] = termcheck(left), termcheck(right)
		return
	# process left child
	if len(left) <= min_size:
		node['left'] = termcheck(left)
	else:
		node['left'] = get_split(left)
		grow_rec(node['left'], max_depth, min_size, depth+1)
	# process right child
	if len(right) <= min_size:
		node['right'] = termcheck(right)
	else:
		node['right'] = get_split(right)
		grow_rec(node['right'], max_depth, min_size, depth+1)
 
# Build a decision tree
def make_tree(train, max_depth, min_size):
	root = get_split(train)
	grow_rec(root, max_depth, min_size, 1)
	return root
  
# Make a prediction with a decision tree
def predict(node, sample):
	if sample[node['index']] < node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'], sample)
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], sample)
		else:
			return node['right']
 
# Classification and Regression Tree Algorithm
def decision_tree(train, test, max_depth, min_size):
    tree = make_tree(train, max_depth, min_size)
    tf = open("saved_tree", "wb")
    pickle.dump(tree, tf)
    predictions = list()
    for row in test:
    	prediction = predict(tree, row)
    	predictions.append(prediction)
    return(predictions)


count = 0
samples = []
#Selecting subset of data for balancing the classes and shuffling
for i in data:
	if count < 2000:
		if i[-1] == 0:
			samples.append(i)
			count = count + 1
	else:
		break
count = 0
for i in data:
	if count < 2000:
		if i[-1] == 1:
			samples.append(i)
			count = count + 1
	else:
		break
random.shuffle(samples)

max_depth = 16
min_size = 10
#Run the decision tree and take accuracy
def train_dt(samples, algo, max_depth, min_size):
	train_set = samples[:int(4*len(samples)/5)]
	test_set = samples[int(4*len(samples)/5):]
	predicted = algo(train_set, test_set, max_depth, min_size)
	actual = [sample[-1] for sample in test_set]
	accuracy = accuracy_metric(actual, predicted)
	return accuracy
	
score = train_dt(samples, decision_tree, max_depth, min_size)
#scores = evaluate_algorithm(samples, decision_tree, n_folds, max_depth, min_size)
print("---Training Complete---")
print('Accuracy: %s' % score)

