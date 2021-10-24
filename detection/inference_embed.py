#Code to embed into the mobile application
import pickle 

"""
#What is your age?
#1 if age above 60, 0 otherwise
age_above_60 = 

#What is your gender?
#1 if male 0 otherwise
gender = 

#Do you exprience head aches?
#1 if head aches are experienced, 0 otherwise
head_ache = 

#Do you have cough?
#1 if there is cough, 0 otherwise
cough = 

#Do you have fever?
#1 if there is fever, 0 otherwise
fever = 

#Do you have a sore throat?
#1 if there is sore throat, 0 otherwise
sore_throat = 

#Do you face shorness of breath?
#1 if there is shortness of breath, 0 otherwise
shortness_of_breath = 

#Have you recently been in contact with an infected individual?
#1 if there was contact, 0 otherwise
contact =

#Form it into a sample
data_sample = [cough, fever, sore_throat, shortness_of_breath, head_ache, age_above_60, gender, contact]
"""
data_sample = [1,0,0,0,0,0,0,0]

#Load saved model
tp = open("saved_tree","rb")
tree = pickle.load(tp)

#Take prediction 
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

#The output prediction
prediction = predict(tree, data_sample)
print(prediction)