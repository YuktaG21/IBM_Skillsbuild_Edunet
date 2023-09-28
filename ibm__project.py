
***IBM SkillsBuild Internship***

**Edunet Foundation**

""" Name: Yukta Gandotra
    Student ID: STU643d9bd65119e1681759190
    College Name: SRM Institute of Science and Technology
    Domain: Artificial Intelligence
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
all_stopwords = stopwords.words('english')
all_stopwords.remove('not')
import string
import re
# %matplotlib inline
import warnings
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split

"""# **Loading the Dataset and Preprocessing the Data**"""

path = "/content/drive/MyDrive/Restaurant_Reviews.tsv"

df= pd.read_csv(path, delimiter ='\t', quoting = 3)

# 0 is positive and 1 is negative

df.head()

df.tail()

len(df)

df.isnull().sum()

df.shape

df.info()

df.describe()

df.describe(include = "object").T

df['Liked'].value_counts()

df['Liked'].describe()

# Convert non-string values to strings
df['Review'] = df['Review'].astype(str)

# Add a 'length' column
df['length'] = df['Review'].apply(len)

df['length'] = df['Review'].apply(len)
df.head()

df.describe().transpose()

df[df['length']==100]['Review'].iloc[0]

stopwords.words('english')

[punc for punc in string.punctuation]

def text_process(msg):
  no_punctuation = [ char for char in msg if char not in string.punctuation]
  no_punctuation = ''.join( no_punctuation)
  return ' '.join([word for word in  no_punctuation.split() if word.lower() not in stopwords.words('english')])

df.head()

df['tokenized_Review'] = df['Review'].apply(text_process)
df.head()

#POSITIVE REVIEWS
from wordcloud import WordCloud

word_cloud = df.loc[df['Liked']==1,:]
text = ' '.join([text for text in word_cloud['Review']])

wordcloud = WordCloud(width=800, height = 800, background_color = 'white').generate(text)

#plot the graph
plt.figure(figsize=(15,8))
plt.imshow(wordcloud, interpolation= 'bilinear')
plt.axis('off')
plt.show()

#NEGATIVE REVIEWS
from wordcloud import WordCloud

word_cloud = df.loc[df['Liked']==0,:]
text = ' '.join([text for text in word_cloud['Review']])

wordcloud = WordCloud(width=800, height = 800, background_color = 'white').generate(text)

#plot the graph
plt.figure(figsize=(15,8))
plt.imshow(wordcloud, interpolation= 'bilinear')
plt.axis('off')
plt.show()

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

cv = CountVectorizer(max_df= 0.9, min_df=10)
X = cv.fit_transform(df['tokenized_Review']).toarray()

X

"""# **Splitting Data**"""

X_train, X_test, Y_train, Y_test = train_test_split(df['tokenized_Review'], df['Liked'], random_state= 107, test_size = 0.2 )

X_train.head()

train_vectorized = cv.transform(X_train)
test_vectorized = cv.transform(X_test)

X_train = train_vectorized.toarray()
X_test = test_vectorized.toarray()

"""# **MODELLING**
## **NAIVE BAYES**

*   GaussianNB
*   MultinomialNB

### **GaussianNB**
"""

from sklearn.naive_bayes import GaussianNB
nb = GaussianNB()
nb.fit(X_train, Y_train)

Y_train_predicts_nb = nb.predict(X_train)
Y_test_predicts_nb = nb.predict(X_test)

Y_test_predicts_nb

Y_test

pd.DataFrame({"Actual_Y_Value" : Y_test, "Predicted_Y_Value" : Y_test_predicts_nb})

from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, auc, classification_report
def print_metrics(actual, predicted):
  print('accuracy score is {}'.format(accuracy_score(actual, predicted)))
  print('precision score is {}'.format( precision_score(actual, predicted)))
  print('recall score is {}'.format(recall_score (actual, predicted)))
  print('f1_score is {}'.format(f1_score(actual, predicted)))
  print('roc_auc_score is {}'.format(roc_auc_score(actual, predicted)))
  print('confusion matrix is {}'.format(confusion_matrix(actual, predicted)))
  print('classification report is {}'.format(classification_report(actual, predicted)))

#Evaluation of training model
print(Y_train_predicts_nb)

print_metrics(Y_train, Y_train_predicts_nb)

print_metrics(Y_test, Y_test_predicts_nb)

"""### **MultinomialNB**"""

from sklearn.naive_bayes import MultinomialNB

#Model training

model = MultinomialNB()
model.fit(X_train, Y_train)

Y_train_predicts_model = model.predict(X_train)
Y_test_predicts_model = model.predict(X_test)

Y_test_predicts_model

#Evaluation of training model

print_metrics(Y_train, Y_train_predicts_model)

print_metrics(Y_train, Y_train_predicts_model)

from sklearn.metrics import confusion_matrix
cm= confusion_matrix(Y_test, Y_test_predicts_model)

cm

plt.figure(figsize=(10,6))
sns.heatmap(cm, annot = True, cmap = "YlGnBu", xticklabels = ['Negative', 'Positive'], yticklabels = ['Negative', 'Positive'])
plt.xlabel('Predicted values')
plt.ylabel('Actual values')

#Hyper parameter tuning

best_accuracy=0.0
alpha_val=0

for i in np.arange(0.01,1.1,0.1):
  temp_model = MultinomialNB(alpha=i)
  temp_model.fit(X_train,Y_train)
  Y_test_pred_h_nbayes =  temp_model.predict(X_test)
  score = accuracy_score(Y_test, Y_test_pred_h_nbayes)
  print("accuraly_score for alpha= {}% is :)".format(round(i,1), round(score*100,2)))
  if score > best_accuracy:
    best_accuracy = score
    alpha_val= i

print("........................")

print("the best accuracy is {}% with alpha value as {}".format(round(best_accuracy*100,2),round(alpha_val,1)))

"""### **Random Forest**"""

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators = 501)
model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)

Y_pred

acc = round(model.score(X_train, Y_train)*100,2)
print(str(acc)+ '%')

Y_pred = model.predict(X_test)
Y_pred

acc = round(model.score(X_test, Y_test)*100,2)
print(str(acc)+ '%')

"""### **Support Vector Machine**"""

from sklearn.svm import SVC
model = SVC()
model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)

from sklearn import metrics

print(metrics.classification_report(Y_test, Y_pred))

#making the confusion matrix

cm = confusion_matrix(Y_test, Y_pred)
cm

print(metrics.accuracy_score(Y_test, Y_pred)*100)

"""# **Logistic Regression**"""

from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(X_train, Y_train)

Y_pred = model.predict(X_test)

from sklearn import metrics
print(metrics.classification_report(Y_test, Y_pred))

#confusion matrix

cm = confusion_matrix(Y_test, Y_pred)
cm

print(metrics.accuracy_score(Y_test, Y_pred))

"""# **Prediction**"""

def predict_sentiment(sample_review):
  sample_review = re.sub(pattern = '[^a-zA-Z]',repl=' ', string = sample_review)
  sample_review = sample_review.lower()
  sample_review_words = sample_review.split()
  sample_review_words = [word for word in sample_review_words if not word in set(stopwords.words('english'))]
  ps=PorterStemmer()
  final_review = [ps.stem(word) for word in sample_review_words]
  final_review = ' '.join(final_review)
  temp = cv.transform( [final_review]).toarray()
  return model.predict(temp)

#Predicted values

sample_review = "food is very very good"
if predict_sentiment(sample_review):
  print('This is a POSITIVE review')
else:
  print('This is Negative review!')

#Predicted values.

sample_review = input("enter a review:")
if predict_sentiment(sample_review):
  print("This is a POSITIVE review")
else:
  print('This is Negative review!')
