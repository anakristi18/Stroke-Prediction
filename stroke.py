# -*- coding: utf-8 -*-
"""Stroke Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VJFxV-ygKaWGZInVbX5DUWZ2g5SE8oQG
"""

#import pandas and numpy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats.mstats import winsorize
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import svm

from google.colab import files
upload = files.upload()

#import dataset
stroke= pd.read_csv("healthcare-dataset-stroke-data.csv", delimiter=",")
stroke.head()

stroke= stroke.drop(stroke[stroke.gender == "Other"].index)
stroke.head()

stroke['stroke'].value_counts()

stroke.drop('id', axis = 1, inplace = True)
stroke

#stades
stroke.describe()

#missing value
np.sum(stroke.isnull())

#mengisi missing value dengan mean secara langsung
stroke['bmi']=stroke['bmi'].fillna((stroke['bmi'].mean()))

np.sum(stroke.isnull())

"""#DATA EXPLORATION"""

#cek oulier dengan boxplot
sns.boxplot(stroke=stroke)

sns.boxplot(stroke['avg_glucose_level'])
plt.title('Boxplot of Average Glucosa Level')
plt.show()

plt.figure(figsize=(15,5))

boxprops = dict(linestyle='--', linewidth=3, color='#1A759F')
flierprops = dict(marker='o', markerfacecolor='#f9c6c9', markersize=8, linestyle='none')
plt.subplot(1,2,1)
ori = stroke['avg_glucose_level']
plt.boxplot(ori, flierprops=flierprops)
plt.xticks([1], ['Rata-Rata Level Glukosa'])
plt.title('Average Glucose Level')

plt.subplot(1,2,2)
wins_avg_glucose_level = winsorize(stroke['avg_glucose_level'],(0.0,0.125))
plt.boxplot(wins_avg_glucose_level, boxprops=boxprops)
plt.xticks([1], ['Rata-Rata Level Glukosa Setelah Diatasi Outlier'])
plt.title('Winsorized Avg_glucose_level')

plt.show()

sns.boxplot(stroke['bmi'])
plt.title('Boxplot of Body Mass Index')
plt.show()

plt.figure(figsize=(15,5))

boxprops = dict(linestyle='--', linewidth=3, color='#64b6ac')
flierprops = dict(marker='o', markerfacecolor='#1A759F', markersize=8, linestyle='none')
plt.subplot(1,2,1)
ori = stroke['bmi']
plt.boxplot(ori, flierprops=flierprops)
plt.xticks([1], ['Indeks Massa Tubuh (BMI)'])
plt.title('Body Mass Index')

plt.subplot(1,2,2)
wins = winsorize(stroke['bmi'],(0.01,0.05))
plt.boxplot(wins, boxprops=boxprops)
plt.xticks([1], ['Indeks Massa Tubuh (BMI) Setelah Diatasi Outlier'])
plt.title('Winsorized Body Mass Index')

plt.show()

stroke.info()

stroke1 = []
stroke2 = []
for i in range(0,stroke.shape[1]):
    if stroke.iloc[:,i].dtype == float:
        stroke1.append(stroke.iloc[:,i].name)
    else:
        stroke2.append(stroke.iloc[:,i].name)

stroke1

stroke2

_,ax = plt.subplots(2,2,figsize=(20,8),facecolor='white')
sns.countplot(stroke.gender,hue =  stroke.stroke,palette='YlGn',ax =ax[0][0])
sns.countplot(stroke.smoking_status,hue = stroke.stroke,ax=ax[0][1],palette='magma')
sns.countplot(stroke.Residence_type,hue =  stroke.stroke,palette='magma',ax =ax[1][0])
sns.countplot(stroke.work_type,hue = stroke.stroke,ax=ax[1][1],palette='YlGn')
plt.show()

stroke3 = stroke[stroke.stroke == 0].gender.value_counts()
stroke4 = stroke[stroke.stroke == 1].gender.value_counts()
stroke5 = stroke[stroke.stroke == 0].smoking_status.value_counts()
stroke6 = stroke[stroke.stroke == 1].smoking_status.value_counts()

_,ax= plt.subplots(2,2,figsize=(20,12),facecolor='white')
ax[0][0].pie(stroke3,labels=['Female','Male'],shadow =True,autopct = '%1.1f%%',explode = [0.03,0.03],colors =['#f9c6c9','#c6def1'])
ax[0][1].pie(stroke4,labels=['Female','Male'],shadow =True,autopct = '%1.1f%%',explode = [0.03,0.03],colors =['#c9e4de','#d2d2cf'])
ax[1][0].pie(stroke5,labels=['Never Smoked','Formerly Smoked','Unknown','Smokes'],shadow =True,autopct = '%1.1f%%',explode = [0.04,0.04,0.04,0.04],colors =['#f9c6c9','#c6def1','#c9e4de','#d2d2cf'])
ax[1][1].pie(stroke6,labels=['Never Smoked','Formerly Smoked','Unknown','Smokes'],shadow =True,autopct = '%1.1f%%',explode = [0.04,0.04,0.04,0.04],colors =['#c9e4de','#d2d2cf','#f9c6c9','#c6def1'])
ax[0][0].set_title('Stroke = 0',fontsize= 30)
ax[0][1].set_title('Stroke = 1',fontsize= 30)
plt.show()

stroke['smoking_status'].value_counts()

x = ['never smoked', 'formerly smoked', 'unknown', 'smokes']
y = [1269, 720, 608, 558]

plt.barh(x, y, color = ['#c9e4de','#d2d2cf','#f9c6c9','#c6def1']) 
for index, value in enumerate(y):
    plt.text(value, index,
             str(value), color = '#166088', fontweight = 'bold')
plt.xlim(0, 1500)
plt.title("Bar Chart Penyakit Stroke Berdasarkan Status Merokok")
plt.show()

fig=plt.figure(figsize=(20,10),facecolor='white')
columns = 3
rows = 2
a=np.random.rand(2,3)
for i in range(1,len(stroke1)):
    fig.add_subplot(rows, columns, i)
    sns.kdeplot(stroke[stroke1[i-1]],hue = stroke.stroke, palette='magma', shade=True) 
plt.show()

sns.scatterplot(data=stroke, x="avg_glucose_level", y="bmi", hue="stroke", style="stroke",palette='YlGn')
plt.title('Scatterplot Rata-rata Level Gula terhadap Indeks Massa Tubuh')

sns.lineplot(data = stroke, x = 'age', y = 'avg_glucose_level',hue = 'stroke', size='gender',palette='rainbow')

stroke7=stroke.drop(['gender','hypertension','heart_disease','ever_married','work_type','Residence_type','smoking_status','stroke'],axis=1)
stroke7.head()

plt.figure(figsize = (8,6))  
sns.heatmap(stroke7.corr(),annot = True,cmap="Purples")
plt.show()

"""# FEATURE SELECTION"""

stroke

from sklearn.feature_selection import SelectKBest, f_classif

#membuat kode pada variabel kategorik
stroke['gender']=stroke['gender'].map({'Male':0, 'Female':1})
stroke['ever_married']=stroke['ever_married'].map({'No':0, 'Yes':1})
stroke['work_type']=stroke['work_type'].map({'Private':0, 'Self-employed':1, 'children':2, 'Govt_job':3, 'Never_worked':4})
stroke['Residence_type']=stroke['Residence_type'].map({'Urban':0, 'Rural':1})
stroke['smoking_status']=stroke['smoking_status'].map({'never smoked':0, 'Unknown':1, 'formerly smoked':2, 'smokes':3})

#variabel Independen
X_stroke=stroke.iloc[:,0:10]
X_stroke.head()

#variabel Dependen
Y_stroke=stroke.iloc[:,10]
Y_stroke.head()

#F-Test
sel_f = SelectKBest(f_classif, k=8) 
X_train_f = sel_f.fit_transform(X_stroke,Y_stroke)
print(X_train_f.shape)
print(sel_f.get_support())

"""# K-FOLD CV"""

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

LE=LabelEncoder()
stroke.stroke=LE.fit_transform(stroke.stroke)
stroke.head()

#set 70% training and 30% testing
xtrain,xtest,ytrain,ytest=train_test_split(X_train_f,Y_stroke,test_size=0.30, random_state=123)

"""DECISION TREE"""

from sklearn.metrics import make_scorer,recall_score,accuracy_score,precision_score,f1_score
from sklearn.model_selection import cross_val_score
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import confusion_matrix
from numpy import mean

model=tree.DecisionTreeClassifier(random_state=123,criterion='entropy')
model.fit(xtrain,ytrain)

specificity = make_scorer(recall_score, pos_label=0)
results_speci = cross_val_score(model,xtrain,ytrain,cv=5,scoring=specificity)
print(results_speci)

print(results_speci.mean())

sensitivity = make_scorer(recall_score, pos_label=1)
results_sensi = cross_val_score(model,xtrain,ytrain,cv=5,scoring=sensitivity)
print(results_sensi)

print(results_sensi.mean())

results_acu = cross_val_score(model,xtrain,ytrain,cv=5)
print(results_acu)

print(results_acu.mean())

y_pred_tree = model.predict(xtest)

from sklearn.metrics import confusion_matrix

print(confusion_matrix(ytest,y_pred_tree))

false_positive_rate, true_positive_rate, thresholds= roc_curve(ytest, y_pred_tree)
roc_auc = auc(false_positive_rate, true_positive_rate)
roc_auc

import matplotlib.pyplot as plt
plt.figure(figsize=(5,5))
plt.title('ROC Decision Tree Cross Validation')
plt.plot(false_positive_rate,true_positive_rate,color='black',label='AUC= %0.4f' %roc_auc)
plt.legend(loc= 'lower right')
plt.plot([0,1],[0,1],linestyle='--')
plt.axis('tight')
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')

"""NAIVE BAYES"""

from sklearn.naive_bayes import GaussianNB

gnb = GaussianNB()
gnbtrain = gnb.fit(xtrain,ytrain)

y_pred_naive = gnbtrain.predict(xtest)

print(confusion_matrix(ytest,y_pred_naive))

results_acu_naive = cross_val_score(gnb,xtrain,ytrain,cv=5)
print(results_acu_naive)

print(results_acu_naive.mean())

sensitivity = make_scorer(recall_score, pos_label=1)
gnb = GaussianNB()
results_sensi_naive = cross_val_score(gnb,xtrain,ytrain,cv=5,scoring=sensitivity)
print(results_sensi_naive)

print(results_sensi_naive.mean())

specificity = make_scorer(recall_score, pos_label=0)
gnb = GaussianNB()
results_spesi_naive = cross_val_score(gnb,xtrain,ytrain,cv=5,scoring=specificity)
print(results_spesi_naive)

print(results_spesi_naive.mean())

false_positive_rate_naive, true_positive_rate_naive, thresholds_naive= roc_curve(ytest, y_pred_naive)
roc_auc_naive = auc(false_positive_rate_naive, true_positive_rate_naive)
roc_auc_naive

import matplotlib.pyplot as plt
plt.figure(figsize=(5,5))
plt.title('ROC Naive Bayes Cross Validation')
plt.plot(false_positive_rate_naive,true_positive_rate_naive,color='black',label='AUC= %0.4f' %roc_auc_naive)
plt.legend(loc= 'lower right')
plt.plot([0,1],[0,1],linestyle='--')
plt.axis('tight')
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')

"""#REPEATED HOLDOUT"""

ranhold = 5
for i in range(ranhold):
    xtr,xts,ytr,yts = train_test_split(X_stroke,Y_stroke,test_size=0.3,random_state=123)

"""DECISION TREE"""

dt = tree.DecisionTreeClassifier(random_state=123,criterion='entropy')
dt.fit(xtr,ytr)
y_pred_tree_rh = dt.predict(xts)

from sklearn.metrics import confusion_matrix

print(confusion_matrix(yts, y_pred_tree_rh))

akurasi_tree_rh = accuracy_score(yts, y_pred_tree_rh)
print(akurasi_tree_rh)

specificity_tree_rh = precision_score(yts, y_pred_tree_rh)
print(specificity_tree_rh.mean())

sensitivity_tree_rh = recall_score(yts, y_pred_tree_rh)
print(sensitivity_tree_rh.mean())

false_positive_rate_tree_rh, true_positive_rate_tree_rh, thresholds_tree_rh= roc_curve(yts, y_pred_tree_rh)
roc_auc_tree_rh = auc(false_positive_rate_tree_rh, true_positive_rate_tree_rh)
roc_auc_tree_rh

import matplotlib.pyplot as plt
plt.figure(figsize=(5,5))
plt.title('ROC Decision Tree Repeated Holdout')
plt.plot(false_positive_rate_tree_rh,true_positive_rate_tree_rh,color='black',label='AUC= %0.4f' %roc_auc_tree_rh)
plt.legend(loc= 'lower right')
plt.plot([0,1],[0,1],linestyle='--')
plt.axis('tight')
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')

"""NAIVE BAYES"""

gnb_rh = GaussianNB()
gnb_rh.fit(xtr,ytr)
y_pred_naive_rh = gnb_rh.predict(xts)

print(confusion_matrix(yts, y_pred_naive_rh))

akurasi_naive_rh = accuracy_score(yts, y_pred_naive_rh)
print(akurasi_naive_rh)

specificity_naive_rh = precision_score(yts, y_pred_naive_rh)
print(specificity_naive_rh.mean())

sensitivity_naive_rh = recall_score(yts, y_pred_naive_rh)
print(sensitivity_naive_rh.mean())

false_positive_rate_naive_rh, true_positive_rate_naive_rh, thresholds_naive_rh= roc_curve(yts, y_pred_naive_rh)
roc_auc_naive_rh = auc(false_positive_rate_naive_rh, true_positive_rate_naive_rh)
roc_auc_naive_rh

import matplotlib.pyplot as plt
plt.figure(figsize=(5,5))
plt.title('ROC Naive Bayes Repeated Holdout')
plt.plot(false_positive_rate_naive_rh,true_positive_rate_naive_rh,color='black',label='AUC= %0.4f' %roc_auc_naive_rh)
plt.legend(loc= 'lower right')
plt.plot([0,1],[0,1],linestyle='--')
plt.axis('tight')
plt.ylabel('True Positive Rate')
plt.xlabel('False Positive Rate')