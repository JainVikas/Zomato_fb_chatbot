from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, redirect, url_for, make_response
import os, json, boto3
from boto3.s3.transfer import S3Transfer
from botocore.client import Config
import pandas as pd
from pandas.tools.plotting import scatter_matrix
import numpy as np
from zomato import Zomato
#rendering page
from werkzeug.utils import secure_filename
############################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################################
app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
def sumSessionCounter():
    try:
        session['counter'] += 1
    except KeyError:
        session['counter'] = 1

@app.route('/')
def index():
    # Initialise the counter, or increment it
    sumSessionCounter()
    return jsonify({"messages": [{"text": "Welcome to our store!"}, {"text": "How can I help you?"}]})

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    z = Zomato("ZOMATO-API-KEY")
	# A call to categories endpoint from zomato API.
    z.parse("categories","")
    # A call to restaurants endppoint from zomato 
    # API with required parameters res_id
    testing_output = z.parse("restaurant","res_id=16774318")
    #response = testing_output.get_json(silent=True, force=True)
    res = json.dumps(testing_output, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    z= r.get_json(silent=True, force=True)
    return jsonify({"messages": [{"text": r.get("apikey") },{"text": z.get("apikey")},{"text": "How can I help you?"}]})    
	
if __name__ == '__main__':
  app.debug = True
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port = port)