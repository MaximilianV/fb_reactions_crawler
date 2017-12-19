import json
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import random
import numpy as np

def get_main_reaction(reactions):
	temp = dict(reactions)
	temp.pop('like', None)
	return max(temp.iteritems(), key=lambda x:x[1])

def get_percent_reaction(reactions, reaction):
	total = reactions['love'] + reactions['haha'] + reactions['wow'] + reactions['sad'] + reactions['angry'] + reactions['like']
	return (reactions[reaction]*100)/total


fname = "data/CNN.json"

data = json.load(open(fname))

# Initialisations
x = []
y = []
labels = ['love','haha','wow','sad','angry']

counter = Counter()

for id, post in data.iteritems():
	key, value = get_main_reaction(post['reactions'])
	x.append(get_percent_reaction(post['reactions'],key))
	#y.append(labels.index(key)+random.uniform(-0.2, 0.2))
	y.append(labels.index(key))
	counter.update([key])

wordcloud = WordCloud()
total_tweets = sum(counter.itervalues())
dict_counter = dict(counter)
for lab, val in dict_counter.iteritems():
	if lab in labels:
		temp_lab = lab
		lab = lab + "("+ str(val*100/total_tweets) + "%)"
		dict_counter[lab] = val
		dict_counter.pop(temp_lab, None)
	
wordcloud.generate_from_frequencies(frequencies=Counter(dict_counter))

plt.figure(1)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Most popular reaction")

plt.figure(2)
for key in labels:
	x_temp = []
	y_temp = []
	for i in range(0,len(x)):
		if y[i] == labels.index(key):
			x_temp.append(x[i])
			y_temp.append(y[i]+random.uniform(-0.3, 0.3))
	# Colored plot
	plt.plot(x_temp,y_temp,'x')
	plt.plot(np.mean(x_temp),labels.index(key),'o')
	
# Full plot
#plt.plot(x,y,'x')

plt.yticks(range(5), labels, rotation=45)
plt.title("Percentage of main reaction for each post")
plt.xlabel('Percentage')
plt.ylabel('Label')
plt.legend()

plt.show()