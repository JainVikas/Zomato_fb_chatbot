from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os, json, boto3
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import numpy as np
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC

app = Flask(__name__)
language = [{'name':'JS'},{'name':'python'}]
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
#read filename/path from Json   
    filepath = req.get("filename")
	#read dependant variable(6/6/17: not used right now)
    dependant = req.get("dependant")
    #read user choice of model
    model = req.get("model")
    #newdata= np.array(req.get("newdata"))
    newdata = np.array([[5.0, 2.0, 4.0, 1.9]])
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = pd.read_csv(filepath, names=names) 
    data = dataset
    L1 = list(data)
    array = data.values
    X = array[:,0:4]
    Y = array[:,4]
    validation_size = 0.20
    seed = 7
# Spliting  data into 80/20 train_test_split
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
# Dictionary to select model based on user input  
    Models = {
      "LR": LogisticRegression(),
      "LDA": LinearDiscriminantAnalysis(),
      "KNN": KNeighborsClassifier(),
      "CART": DecisionTreeClassifier(),
      "NB": GaussianNB(),
      "SVM": SVC(),
      }
    selectedModel = Models[model]	
# Training User selected model	
    selectedModel.fit(X_train, Y_train)
# Prediction based on validation data    
    predictions = selectedModel.predict(X_validation)
# Checking prediction accuracy    
    score = accuracy_score(Y_validation, predictions)
    category = selectedModel.predict(newdata)
    return jsonify({'column': newdata,'category':category})

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port = port)