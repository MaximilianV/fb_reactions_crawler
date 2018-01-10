import json
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
import pandas as pd
from scipy import stats
import seaborn as sns

def get_main_reaction(reactions):
	temp = dict(reactions)
	temp.pop('like', None)
	return max(temp.items(), key=lambda x:x[1])

def get_percent_reaction(reactions, reaction):
	total = reactions['love'] + reactions['haha'] + reactions['wow'] + reactions['sad'] + reactions['angry'] + reactions['like']
	return (reactions[reaction]*100)/total

	
fname = "data/CNN.json"

data = json.load(open(fname))

labels = ['love','haha','wow','sad','angry']

plt.figure(1)
plt.title('Test Data')
m = 0
for i in range(0,len(labels)):

	for j in range(0,len(labels)):
	
		
		# Initialisations
		X = []
		Y = []
		 
		for id, post in data.items():
			X.append(post['reactions'][labels[i]])
			Y.append(post['reactions'][labels[j]])
			
		# Subplot
		m += 1		
		plt.subplot(5,5,m)
		
		# Plot legend axis
		if j == 0:
			plt.ylabel(labels[i], rotation=45)
		
		if i == 4:
			plt.xlabel(labels[j], rotation=45)
		
		# Diagonal
		if j == i:	
			X_temp = []
			for id, post in data.items():
				X_temp.append(get_percent_reaction(post['reactions'],labels[i]))
			sns.distplot(X_temp);
			#plt.plot(X_temp,'-')
			continue
			
		# Upper side
		if j > i:	
			plt.plot([1,0], [1,0], color="white")
			plt.xticks([])
			plt.yticks([])
			if j > i:
				plt.text(0, 0, "r="+str( round(stats.pearsonr(X,Y)[0],3) ))
			continue
			
		# Down side
		X = np.array(X)
		Y = np.array(Y)
		X=X.reshape(len(X),1)
		Y=Y.reshape(len(Y),1)
		 
		# Split the data into training/testing sets
		X_train = X[:-250]
		X_test = X[-250:]

		# Split the targets into training/testing sets
		Y_train = Y[:-250]
		Y_test = Y[-250:]
		
		# Not enough data until now [to remove]
		X_train = X
		X_test = X
		Y_train = Y
		Y_test = Y
		
		# Plot outputs
		plt.scatter(X_test, Y_test,  color='black')
		plt.xticks(())
		plt.yticks(())		 

		# Create linear regression object
		regr = linear_model.LinearRegression()
		 
		# Train the model using the training sets
		regr.fit(X_train, Y_train)
		 
		# Plot outputs
		plt.plot(X_test, regr.predict(X_test), color='red',linewidth=3)

		# Prediction 
		# print( str(round(regr.predict(5000))) )


plt.show()