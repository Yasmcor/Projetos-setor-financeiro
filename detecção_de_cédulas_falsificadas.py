# -*- coding: utf-8 -*-
"""Detecção de Cédulas Falsificadas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1w4q_MpI72ecKcyvxsem4kKVYtS9W26Eq

#<font color='white'>FAKE NOTES DETECTION</font>


#<font color='Gray'>DETECÇÃO DE NOTAS FALSIFICADAS</font>

###**CONTEXTO**
#### O recebimento de cédulas falsas é um problema real para as empresas. Todos os anos, o BC retém e tira de circulação centenas de milhares de cédulas falsificadas. Em 2019, foram quase 500 mil notas, que representavam cerca de R$ 32 milhões em “dinheiro” recolhido.

###**Problema de negócio**
####Construir uma maquina preditiva que detecte cédulas falsas.
"""

# Import libraries and packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

"""#**Análise exploratória**"""

#Import data and visualize first rows
data = pd.read_csv('https://raw.githubusercontent.com/amankharwal/Website-data/master/data_banknote_authentication.txt', header=None)
data.columns = ['var', 'skew', 'curt', 'entr', 'auth']
data.head()

#Checking null values
data.isna().sum()

#Dimenction of dataset
data.info()

#Graphical data analysis
chart = sns.pairplot(data, hue='auth')
chart

"""#**Pré Processamento de dados**"""

#Balance data
plt.figure(figsize=(10,8))
plt.title('Distribuition of target', size=18)
sns.countplot(x=data['auth'])
target_count = data.auth.value_counts()
plt.text(x=(-0.04), y=(10+target_count[0]), s=target_count[0], size=12)
plt.text(x=(0.96), y=(10+target_count[1]), s=target_count[1], size=12)
plt.ylim(0,900)
plt.show()

#Subsampling
nb_to_delet = target_count[0] - target_count[1]
data=data[nb_to_delet:]
print(data['auth'].value_counts())

#Separation of variables in train e test
x = data.iloc[:, data.columns != 'auth']
y = data.iloc[:, data.columns == 'auth']
x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.3, random_state=7)

#Standardization of variables
scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(x_train)
x_test = scaler.transform(x_test)

"""#**Construindo máquina preditiva**"""

#Creating predictive machine
clf = LogisticRegression(solver='lbfgs', random_state=42, multi_class='auto')
clf.fit(x_train, y_train.values.ravel())

#Prediction with test data
y_pred = np.array(clf.predict(x_test))

#Evaluating model
conf_mat = pd.DataFrame(confusion_matrix(y_test, y_pred),
                       columns=['Pred.Negative', 'Pred.Positive'],
                       index=['Act.Negative', 'Act.Positive'])
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
accuracy = round((tn+tp)/(tn+fp+fn+tp), 4)
print(conf_mat)
print(f'\n Accuracy = {round(100*accuracy, 2)}%')

#Entering new data for new prediction
new_banknote = np.array([4.5, -8.1, 2.4, 1.4], ndmin=2)
new_banknote = scaler.transform(new_banknote)
print(f'Prediction: Class {clf.predict(new_banknote)[0]}')
print(f'Probability [0/1]: {clf.predict_proba(new_banknote)[0]}')