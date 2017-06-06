from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify
import os, json, boto3
import pandas as pd


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
    data = dataset
    l1 = list(data)
    res = predictVariable(data)
    return jsonify({'coulumn':res })


def predictVariable(data):
  
  return jsonify("10")	
 
if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port = port)