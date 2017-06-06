from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os, json, boto3
import pandas as pd

data= pd.DataFrame();
filename="";
app = Flask(__name__)
language = [{'name':'JS'},{'name':'python'}]
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    filepath = req.get("filename")
    if filepath != filename:
      filename= filepath
	 
	 #fileread(filename)
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = pd.read_csv(url, names=names) 
    data = dataset
    l1 = list(data)	
    return jsonify({'list':filename})


@app.route('/predict', method = ['POST'])
def predictVariable():
  req = request.get_json(silent=True, force=True)
  
  return json
 
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port = port)