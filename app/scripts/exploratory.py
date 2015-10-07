from __future__ import division
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
from sklearn.ensemble import RandomForestRegressor
import matplotlib

df = pd.read_csv(open('data/echo_music_merge.csv'), header=0)

df['Valence'] = df['Valence']/df['Valence'].max()
df['Arousal'] = df['Arousal']/df['Arousal'].max()


def train_test(num, fraction = 0.4):
    superset = xrange(num)
    test = random.sample(superset,int(fraction*num))
    train = list(set(superset) - set(test))
    return train, test

from sklearn import datasets, linear_model
from sklearn import cross_validation
import random

regrA = linear_model.LinearRegression()
regrV = linear_model.LinearRegression()
train, test = train_test(df.shape[0], 0.3)

V_train = df['Valence'][train]
V_test = df['Valence'][test]
A_train = df['Arousal'][train]
A_test = df['Arousal'][test]
E_train = df['energy'][train]
E_test = df['energy'][test]
features = df[['energy', 'tempo', 'acousticness' , 'danceability', 'loudness', 'valence']]
features = df[['tempo', 'loudness']]
features_train = features.take(train)
features_test = features.take(test)
#Happiness
regrV.fit(features_train, V_train)
print('Coefficients: \n', regrV.coef_)
print("Residual sum of squares of train: %.2f"
      % np.mean((regrV.predict(features_train) - V_train) ** 2))
# The mean square error
print("Residual sum of squares of test: %.2f"
      % np.mean((regrV.predict(features_test) - V_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regrV.score(features_test, V_test))

#Excitement
regrA = linear_model.LinearRegression()
regrA.fit(features_train, A_train)
print('Coefficients: \n', regrA.coef_)
print("Residual sum of squares of train: %.2f"
      % np.mean((regrA.predict(features_train) - A_train) ** 2))
# The mean square error
print("Residual sum of squares of test: %.2f"
      % np.mean((regrA.predict(features_test) - A_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regrA.score(features_test, A_test))
predicted_lsr = regrA.predict(features_test)

estimator = RandomForestRegressor(n_estimators=100)
estimator.fit(features_train, A_train)
predicted_rf = estimator.predict(features_test)

# energy
regrE = linear_model.LinearRegression()
regrE.fit(features_train, E_train)
print('Coefficients: \n', regrE.coef_)
print("Residual sum of squares of train: %.2f"
      % np.mean((regrE.predict(features_train) - E_train) ** 2))
# The mean square error
print("Residual sum of squares of test: %.2f"
      % np.mean((regrE.predict(features_test) - E_test) ** 2))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % regrE.score(features_test, E_test))
predicted_lsr = regrE.predict(features_test)

estimator = RandomForestRegressor(n_estimators=100)
estimator.fit(features_train, E_train)
predicted_e_rf = estimator.predict(features_test)

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 13}
matplotlib.rc('font', **font)
plt.figure()
#plt.subplot(1, 2, 1)
plt.scatter(predicted_e_rf, E_test, c = 'r', label='Random Forest')
plt.scatter(predicted_lsr, E_test, c = 'b', label='Linear Regression')
plt.xlabel('Predicted Energy')
plt.ylabel('EchoNest Energy')
plt.legend()

feature_importance = estimator.feature_importances_
# make importances relative to max importance
feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0]) + .5
plt.subplot(1, 2, 2)
plt.barh(pos, feature_importance[sorted_idx], color='gray', align='center')
plt.yticks(pos, features.columns[sorted_idx])
plt.xlabel('Relative Importance')
plt.title('Variable Importance')
plt.show()


def get_target_label(v):
  if v <= 0.33:
    return 0
  elif v > 0.33 and v <= 0.55:
    return 1  
  elif v > 0.55 and v<= 0.75:
    return 2
  else:
    return 3

target_names = ['dull', 'sober', 'Fun', 'Exciting']
target_label = np.array([get_target_label(x) for x in A_test])
predicted_label_lsr = np.array([get_target_label(x) for x in predicted_lsr])
predicted_label_rf = np.array([get_target_label(x) for x in predicted_rf])

from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(cm, target_names, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

cm = confusion_matrix(target_label, predicted_label_rf)
np.set_printoptions(precision=2)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
plt.figure()
plot_confusion_matrix(cm_normalized, target_names, title='Normalized confusion matrix')


font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}
matplotlib.rc('font', **font)
plt.figure()
plt.subplot(1, 2, 1)
plt.scatter(predicted_rf, A_test, c = 'darkgray', label='Random Forrest')
plt.xlabel('Predicted Excitement')
plt.ylabel('MusicOvery Excitement')
plt.legend()

feature_importance = estimator.feature_importances_
# make importances relative to max importance
feature_importance = 100.0 * (feature_importance / feature_importance.max())
sorted_idx = np.argsort(feature_importance)
pos = np.arange(sorted_idx.shape[0][:9]) + .5
plt.subplot(1, 2, 2)
plt.barh(pos, feature_importance[sorted_idx], color='gray', align='center')
plt.yticks(pos, features.columns[sorted_idx])
plt.xlabel('Relative Importance')
plt.title('Variable Importance')
plt.show()
# Support vector regression for Excitement
from sklearn.svm import SVR
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_lin = SVR(kernel='linear', C=1e3)
svr_poly = SVR(kernel='poly', C=1e3, degree=2)
y_rbf = svr_rbf.fit(features_train, A_train).predict(features_test)
y_lin = svr_lin.fit(features_train, A_train).predict(features_test)
y_poly = svr_poly.fit(features_train, A_train).predict(features_test)
plt.scatter(y_rbf, A_test, c='g', label='RBF model')
plt.scatter(y_lin, A_test, c='r', label='Linear model')
plt.scatter(y_poly, A_test, c='b', label='Polynomial model')
##########Classification############

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
from sklearn.decomposition import PCA
from sklearn.lda import LDA
from sklearn import svm
import random
from sklearn import ensemble

def train_test(num, fraction = 0.4):
    superset = xrange(num)
    test = random.sample(superset,int(fraction*num))
    train = list(set(superset) - set(test))
    return train, test


df = pd.read_csv(open('data/echo_music_merge.csv'), header=0)
df['Valence'] = df['Valence']/100000
df['Arousal'] = df['Arousal']/100000
df.sort(columns=['Valence'],inplace=True)

train, test = train_test(df.shape[0], 0.3)

features = df[['energy', 'tempo', 'acousticness' , 'danceability', 'loudness', 'valence']]
features_train = features.take(train)
features_test = features.take(test)

y = df['Valence'].copy()
y[ y<=4.5 ] = 0
y[ y> 4.5 ] = 1
V_train = y[train]
V_test = y[test]

params = {'n_estimators': 500, 'max_depth': 4, 'min_samples_split': 1,
          'learning_rate': 0.01, 'loss': 'ls'}

clf = ensemble.GradientBoostingRegressor(**params)

clf.fit(features_train, V_train)          

'''pca = PCA(n_components=2)
X_r = pca.fit(features).transform(features)
print('explained variance ratio (first two components): %s'
      % str(pca.explained_variance_ratio_))'''

'''y[ y<=3.3 ] = 0
y[ (y> 3.3) & (y<=6.6)] = 1
y[y>6.6] = 2

lda = LDA(n_components=2)
X_r2 = lda.fit(features, y).transform(features)

target_names = ['sad', 'medium', 'happy']

plt.figure()
for c, i, target_name in zip("rgb", [0, 1, 2], target_names):
    plt.scatter(X_r[(y == i).values, 0], X_r[(y == i).values, 1], c=c, label=target_name)

plt.legend()
plt.title('PCA of dataset')

plt.figure()
for c, i, target_name in zip("rgb", [0, 1, 2], target_names):
    plt.scatter(X_r2[(y == i).values, 0], X_r2[(y == i).values, 1], c=c, label=target_name)

plt.figure()
plt.plot(X_r2[(y == i).values, 0], X_r2[(y == i).values, 1], c=c, label=target_name)

qda = QDA()
y_pred = qda.fit(features, y).predict(features)

plt.legend()
plt.title('LDA of dataset')
plt.show()'''


#### using chord progressions#####
import pandas as pd
import random, re
from __future__ import division
import numpy as np

root_key = ['Ca','Db','Da','Eb','Ea','Fa','Gb','Ga','Ab','Aa','Bb','Ba']
major_keys = [x+'j' for x in root_key]
minor_keys = [x+'m' for x in root_key]

total_keys = major_keys
total_keys.extend(minor_keys)
feature_space = {}
index = 0
for ikey in total_keys:
  for jkey in total_keys:
      feature_space[ikey + ':' + jkey] = index
      index+= 1

def train_test(num, fraction = 0.4):
    superset = xrange(num)
    test = random.sample(superset,int(fraction*num))
    train = list(set(superset) - set(test))
    return train, test


def get_target_label(v):
  if v <= 0.5:
    return 1
  #elif v> 2.5 and v <= 5.5:
  #  return 1  
  else:
    return 2  

df = pd.read_csv(open('data/echo_music_merge_chords.csv'), header=0)
df['Valence'] = df['Valence']/100000
df['Arousal'] = df['Arousal']/100000

df['Valence'] = df['Valence']/df['Valence'].max()
train, test = train_test(df.shape[0], 0.3)
df_train = df.take(train)
df_test = df.take(test)

X_train_features = []
target_train = []

for index, row in df_train.iterrows():
  valence = row['Valence']
  cp = row['Chord_progression']
  target_train.append(get_target_label(valence))
  x = [0]*len(feature_space)
  cps = re.compile('\|').split(cp)
  for i in range(len(cps)-1):
    if cps[i] == 'X':
      continue
    if cps[i+1] == 'X':
      continue  
    x[feature_space[cps[i] + ':' + cps[i+1]]] += 1
  if len(cps) > 1:  
    x = [y/(len(cps)-1) for y in x]
  x.extend([row['valence'], row['energy'], row['danceability'],row['tempo']])
  X_train_features.append(x)  

X_train = np.array(X_train_features)
target_train = np.array(target_train)

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train, target_train)

X_test_features = []
target_test = []

for index, row in df_test.iterrows():
  valence = row['Valence']
  cp = row['Chord_progression']
  target_test.append(get_target_label(valence))
  x = [0]*len(feature_space)
  cps = re.compile('\|').split(cp)
  for i in range(len(cps)-1):
    if cps[i] == 'X':
      continue
    if cps[i+1] == 'X':
      continue  
    x[feature_space[cps[i] + ':' + cps[i+1]]] += 1
  if len(cps) > 1:  
    x = [y/(len(cps)-1) for y in x]
  x.extend([row['valence'], row['energy'], row['danceability'],row['tempo']])
  X_test_features.append(x)  

X_test = np.array(X_test_features)
target_test = np.array(target_test)

predicted = clf.predict(X_test)


### Classification of Arousal#####
import pandas as pd
import random, re
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

def train_test(num, fraction = 0.4):
    superset = xrange(num)
    test = random.sample(superset,int(fraction*num))
    train = list(set(superset) - set(test))
    return train, test


def get_target_label(v):
  if v <= 0.33:
    return 0
  elif v > 0.33 and v <= 0.55:
    return 1  
  elif v > 0.55 and v<= 0.75:
    return 2
  else:
    return 3  

df = pd.read_csv(open('data/echo_music_merge_chords.csv'), header=0)
df['Valence'] = df['Valence']/df['Valence'].max()
df['Arousal'] = df['Arousal']/df['Arousal'].max()

train, test = train_test(df.shape[0], 0.3)
df_train = df.take(train)
df_test = df.take(test)
target_train = []

for index, row in df_train.iterrows():
  arousal = row['Arousal']
  target_train.append(get_target_label(arousal))

target_train = np.array(target_train)
features_train = df_train[['energy', 'tempo', 'acousticness' , 'danceability', 'loudness', 'valence']]
target_test = []
for index, row in df_test.iterrows():
  arousal = row['Arousal']
  target_test.append(get_target_label(arousal))

target_test = np.array(target_test)
features_test = df_test[['energy', 'tempo', 'acousticness' , 'danceability', 'loudness', 'valence']]

from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, class_weight='auto')
clf.fit(features_train, target_train)
predicted = clf.predict(features_test)
from sklearn.metrics import classification_report
target_names = ['0', '1', '2', '3']
print classification_report(target_test, predicted, target_names=target_names)
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(cm, target_names, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

cm = confusion_matrix(target_test, predicted)
np.set_printoptions(precision=2)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
plt.figure()
plot_confusion_matrix(cm_normalized, target_names, title='Normalized confusion matrix')


#### Classification using only EchoNest summary features!
import pandas as pd
import random, re
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def train_test(num, fraction = 0.4):
    superset = xrange(num)
    test = random.sample(superset,int(fraction*num))
    train = list(set(superset) - set(test))
    return train, test


def get_target_label(v):
    if v <=0.48:
        return 0
    #elif v > 0.33 and v <= 0.66:
    #    return 1
    else:
        return 1 

df = pd.read_csv(open('data/echo_music_merge_chords.csv'), header=0)
df['Valence'] = df['Valence']/df['Valence'].max()
df['Arousal'] = df['Arousal']/df['Arousal'].max()

train, test = train_test(df.shape[0], 0.3)
df_train = df.take(train)
df_test = df.take(test)
target_train = []

for index, row in df_train.iterrows():
  arousal = row['Valence']
  target_train.append(get_target_label(arousal))

target_train = np.array(target_train)
features_train = df_train[['energy', 'tempo', 'acousticness' , 'danceability', 'loudness', 'valence']]
target_test = []
for index, row in df_test.iterrows():
  arousal = row['Valence']
  target_test.append(get_target_label(arousal))

target_test = np.array(target_test)
features_test = df_test[['energy', 'tempo', 'acousticness' , 'danceability', 'loudness', 'valence']]

from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100, class_weight='auto')
clf.fit(features_train, target_train)
predicted = clf.predict(features_test)
from sklearn.metrics import classification_report
target_names = ['sad', 'happy']
print classification_report(target_test, predicted, target_names=target_names)

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}
matplotlib.rc('font', **font)

from sklearn.metrics import roc_curve, auc
fpr, tpr, thresholds = roc_curve(predicted, target_test, pos_label=1)
roc_auc = auc(fpr, tpr)
plt.figure()
plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")
plt.show()


from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(cm, target_names, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

cm = confusion_matrix(target_test, predicted)
np.set_printoptions(precision=2)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
plt.figure()
plot_confusion_matrix(cm_normalized, target_names, title='Normalized confusion matrix')


########### using only chords!!
from __future__ import division
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib
from sklearn.decomposition import PCA
import random, re
from sklearn.ensemble import RandomForestClassifier


df = pd.read_csv(open('data/echo_music_merge_chords.csv'), header=0)

df['Valence'] = df['Valence']/df['Valence'].max()
def train_test(num, fraction = 0.4):
    superset = xrange(num)
    test = random.sample(superset,int(fraction*num))
    train = list(set(superset) - set(test))
    return train, test

def get_target_label(v):
    if v <=0.48:
        return 0
    #elif v > 0.25 and v <= 0.48:
    #    return 1
    else:
        return 1   

root_key = ['Ca','Db','Da','Eb','Ea','Fa','Gb','Ga','Ab','Aa','Bb','Ba']
major_keys = [x+'j' for x in root_key]
minor_keys = [x+'m' for x in root_key]

total_keys = major_keys
total_keys.extend(minor_keys)
feature_space = {}
index = 0
for ikey in total_keys:
  for jkey in total_keys:
      feature_space[ikey + ':' + jkey] = index
      index+= 1


train, test = train_test(df.shape[0], 0.3)
df_train = df.take(train)
df_test = df.take(test)

X_train_features = []
target_train = []
for index, row in df_train.iterrows():
  valence = row['Valence']
  cp = row['Chord_progression']
  target_train.append(get_target_label(valence))
  x = [0]*len(feature_space)
  cps = re.compile('\|').split(cp)
  for i in range(len(cps)-1):
    if cps[i] == 'X':
      continue
    if cps[i+1] == 'X':
      continue  
    x[feature_space[cps[i] + ':' + cps[i+1]]] += 1
  if len(cps) > 1:
    x = [y/(sum(x)+0.01) for y in x]
  #x.extend([row['valence'], row['energy'], row['danceability'],row['tempo']])
  X_train_features.append(x)  

X_train = np.array(X_train_features)
target_train = np.array(target_train)
X_test_features = []
target_test = []

for index, row in df_test.iterrows():
  valence = row['Valence']
  cp = row['Chord_progression']
  target_test.append(get_target_label(valence))
  x = [0]*len(feature_space)
  cps = re.compile('\|').split(cp)
  for i in range(len(cps)-1):
    if cps[i] == 'X':
      continue
    if cps[i+1] == 'X':
      continue  
    x[feature_space[cps[i] + ':' + cps[i+1]]] += 1
  if len(cps) > 1:
    x = [y/(sum(x)+0.01) for y in x]
  #x.extend([row['valence'], row['energy'], row['danceability'],row['tempo']])
  X_test_features.append(x)  

X_test = np.array(X_test_features)
target_test = np.array(target_test)

clf = RandomForestClassifier(n_estimators = 100, class_weight='auto')
clf.fit(X_train, target_train)

predicted = clf.predict(X_test)
from sklearn.metrics import classification_report
target_names = ['Sad', 'Happy']
print classification_report(target_test, predicted, target_names=target_names)
from sklearn.metrics import confusion_matrix

def plot_confusion_matrix(cm, target_names, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(target_names))
    plt.xticks(tick_marks, target_names, rotation=45)
    plt.yticks(tick_marks, target_names)
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

cm = confusion_matrix(target_test, predicted)
np.set_printoptions(precision=2)
cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
plt.figure()
plot_confusion_matrix(cm_normalized, target_names, title='Normalized confusion matrix')


features = []
for ikey in total_keys:
    for jkey in total_keys:
        features.append(ikey + ':' + jkey)

features.extend(['valence','energy','danceability', 'tempo'])
for x in clf.feature_importances_.argsort()[-10:][::-1]:
    print features[x] + '    '  + str(clf.feature_importances_[x])











