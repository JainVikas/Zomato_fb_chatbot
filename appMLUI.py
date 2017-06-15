from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, redirect, url_for, make_response
import os, json, boto3
from boto3.s3.transfer import S3Transfer
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
from sklearn.externals import joblib
from sklearn.naive_bayes import GaussianNB

from sklearn.svm import SVC
#rendering page
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT' #

	
@app.route('/')
def index():
     return render_template('index.html')

	
#AWS s3 bucket for file uploads to be read later by webhook

@app.route("/upload",methods = ['POST','GET'])
def upload(): 
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(filename)
        s3 = boto3.resource('s3', aws_access_key_id= os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),config=Config(signature_version='s3v4'))
        s3.Bucket(os.environ.get('S3_BUCKET')).upload_file(filename,filename)
        awsFilepath= "https://s3.us-east-2.amazonaws.com/"+os.environ.get('S3_BUCKET')+"/" +filename
        data= pd.read_csv(awsFilepath)
        session['data']= awsFilepath
        session['columnNames']=list(data)  
        return jsonify( {'predictors':session['columnNames']})
    return render_template('index.html')

@app.route('/readModels', methods=[ 'GET'])
def readModels():
    filename = os.path.join(app.static_folder, 'model.json')
    with open(filename) as model_file:
        data = json.load(model_file)
    return data
#webhook to extract dependant Variable from user entry
@app.route('/view', methods=['POST', 'GET'])
def view():
    predictor = request.form['predictor']
    target = request.form['target']
    session['predictor']= predictor
    session['target']=target
    data = pd.read_csv(session['data']) 
    predictorValues = data.values[:,list(data).index(predictor)]
    targetValues = data.values[:,list(data).index(target)]
    
    return jsonify({'predict':predictorValues.tolist(),'target':targetValues.tolist()})

#webhook to apply selected model and provide score as session
@app.route('/selectModel', methods =['POST','GET'])
def selectModel():
#extract the user entered model from request.form
    model = request.form['model']
    filepath = session['data']
    data = pd.read_csv(filepath) 
    L1 = list(data)
    targetIndex= L1.index(session['target'])
    array = data.values
#dividing X and y, considering Class is the last column
    X = array[:,0:-1]
    Y = array[:,targetIndex]
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
# following commancd to save the model for later use
    modelfilename = "finalizedModel.sav"
#1. save the model using joblib.dump (#selectedModel is the trained model)
    joblib.dump(selectedModel, modelfilename)
	#saving the filename in session variable
    session['model']=modelfilename
    return jsonify({'score':score, 'model':session['model']})
      
@app.route('/enterValues', methods =['POST','GET'])
def enterValues():
    return render_template('EnterValues.html')

@app.route('/predict', methods =['POST','GET'])
def predict():
    if request.method == 'POST':
        newdata= [] 
        for i in request.form:
            newdata.append(float(request.form[i]))
#Old hard coded way
#        newdata.append(float(request.form['sepal-length']))
#        newdata.append(float(request.form['sepal-width']))
#        newdata.append(float(request.form['petal-length']))
#        newdata.append(float(request.form['petal-width']))
        selectedModel = joblib.load(session['model'])
        predictions = selectedModel.predict(newdata)
        return jsonify({'newdata':newdata, 'prediction':predictions.tolist(), 'requests':request.form})
	#redirect user to webpage to select values for new test data.
    return render_template('EnterValues.html')
	
if __name__ == '__main__':
  app.debug = True
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port = port)