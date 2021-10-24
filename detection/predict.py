from random import randrange
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
tp = open("saved_tree_backup","rb")
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


#Take accuracy with entire data as test set
prediction = test_samples(tree,data)
score = test_score(data, prediction)
print('Scores: %s' % score)