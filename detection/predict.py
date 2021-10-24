from random import randrange
import random
import pickle 
#Code is used to take predictions on saved model


#load data
data = []
fp = open('corona_data_processed.csv')
feats = fp.readline()
i = 0
for line in fp:
    line = line[:-1]
    try:
        data.append([int(l) for l in line.split(",")])
    except:
        print (line.split(","),line,i)
    i = i + 1
 

#Take prediction
def predict(node, row):
	if row[node['index']] < node['value']:
		if isinstance(node['left'], dict):
			return predict(node['left'], row)
		else:
			return node['left']
	else:
		if isinstance(node['right'], dict):
			return predict(node['right'], row)
		else:
			return node['right']


#Try taking prediction on a single sample 
def try_sample(sample):
	print(sample[:-1],"=>",sample[-1])
	print(predict(tree,sample))


#Load saved model
tp = open("saved_tree","rb")
tree = pickle.load(tp)


#Predict on a test set using the model
def test_samples(tree,test):
	predictions = []
	for row in test:
		prediction = predict(tree, row)
		predictions.append(prediction)
	return predictions


#Take the accuracy
def test_score(test, predictions):
	correct = 0
	for i in range(len(test)):
		if test[i][-1] == predictions[i]:
			correct += 1
	accuracy = correct / float(len(test)) * 100.0
	return accuracy

count = 0
samples = []
#Selecting subset of data for balancing the classes and shuffling
for i in data[80000:]:
	if count < 10000:
		if i[-1] == 0:
			samples.append(i)
			count = count + 1
	else:
		break
count = 0
for i in data[80000:]:
	if count < 10000:
		if i[-1] == 1:
			samples.append(i)
			count = count + 1
	else:
		break
random.shuffle(samples)

#Take accuracy with entire data as test set
prediction = test_samples(tree,samples)
score = test_score(samples, prediction)
print('Scores: %s' % score)