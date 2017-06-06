from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os, json, boto3
import pandas as pd

data= pd.DataFrame()

app = Flask(__name__)
language = [{'name':'JS'},{'name':'python'}]
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    filepath = req.get("filename")
    dependant = reg.get("dependant")
    model = req.get("model")
    names = ['sepal-length', 'sepal-width', 'petal-length', 'petal-width', 'class']
    dataset = pd.read_csv(filepath, names=names) 
    z= data.combine(dataset)
    array = data.values
    X = array[:,0:]
    Y = array[:,-1]
    validation_size = 0.20
    seed = 7
    X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size, random_state=seed)
    
    return jsonify({'coulumn': list(z) })

 
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port = port)