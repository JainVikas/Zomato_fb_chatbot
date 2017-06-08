from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, redirect, url_for
import os, json, boto3
from botocore.client import Config
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
#rendering page
from werkzeug.utils import secure_filename
############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
app = Flask(__name__)
@app.route('/account/')
def account():
    return render_template('account.html')
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
    #newdata = json.loads(req.get("newdata"))	
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = pd.read_csv(filepath, names=names) 
    data = dataset
    L1 = list(data)
    array = data.values
#dividing X and y, considering Class is the last column
    X = array[:,0:-1]
    Y = array[:,-1]
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
    return jsonify({'score':score})
#AWS s3 bucket for file uploads to be read later by webhook


@app.route("/upload",methods = ['POST','GET'])
def upload(): 
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
			s3 = boto3.resource('s3', aws_access_key_id= 'AKIAIBKBOVF6DTJ3LPQQ', aws_secret_access_key='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',config=Config(signature_version='s3v4'))
            s3.Bucket('python-app-bucket-upload').upload_file(file,filename)
            return 'successful upload'
    return jsonify({'score':'correct'})
      
    
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port = port)