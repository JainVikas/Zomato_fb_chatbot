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

@app.route('/webhook_manually', methods=['POST', 'GET'])
def webhook_manually():
    z = Zomato("ZOMATO-API-KEY")
    testing_output = z.parse("restaurant","res_id=16774318")
    #output of parse is a dict, so quite convinient to find details using inbuit features of python dict
    
    return jsonify({"messages": [{"text": "How can I help you?"}, {"text": "your api key is"+testing_output["apikey"]}]})    
@app.route('/webhook_viaFB', methods=['POST', 'GET'])
def webhook_viaFB():
    z = Zomato("ZOMATO-API-KEY")
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    testing_output = z.parse("q","lat="+str(req.get("latitude")),"lon="+str(req.get("longitude")))
    #output of parse is a dict, so quite convinient to find details using inbuit features of python dict
    
    return jsonify({"messages": [{"text": "How can I help you?"}, {"text": "your locality key is"+str(testing_output["location"]["locality"])}]})   	
if __name__ == '__main__':
  app.debug = True
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port = port)