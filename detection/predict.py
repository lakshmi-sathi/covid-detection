from random import randrange
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

 
# Make a prediction with a decision tree
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
 
tp = open("saved_tree","rb")
tree = pickle.load(tp)
test =  data[20000:20100]

def test_samples(tree,test):
	predictions = []
	for row in test:
		prediction = predict(tree, row)
		predictions.append(prediction)
	return predictions

def test_score(test, predictions):
	correct = 0
	for i in range(len(test)):
		if test[i][-1] == predictions[i]:
			correct += 1
	scores = correct / float(len(test)) * 100.0
	return scores

prediction = test_samples(tree,test)
print(prediction)
score = test_score(test, prediction)


print('Scores: %s' % score)

samples = []
for i in data[30000:30100]:
	if i[-1] == 1:
		samples.append(i)

prediction = test_samples(tree,samples)
print(prediction)
score = test_score(samples, prediction)

def try_sample(sample):
	print(sample[:-1],"=>",sample[-1])
	print(predict(tree,sample))

#try_sample(data[2151876])