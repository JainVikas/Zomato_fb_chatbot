from flask import Flask, flash, redirect, render_template, request, session, abort, jsonify, redirect, url_for, make_response
import pandas as pd
import os, json
from pandas.tools.plotting import scatter_matrix
import numpy as np
from zomato import Zomato
import urllib.parse as urlparse
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
    query_string = request.query_string
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    category = request.args.get('text')
    print(longitude)
    print(latitude)
    print(query_string)
    param = "lat="+str(latitude) + ","+ "lon="+str(longitude) + "," + "category=" +str(category)
    testing_output = z.parse("search",param)
    #output of parse is a dict, so quite convinient to find details using inbuit features of python dict
    
    #return jsonify({"messages": [{"text": "How can I help you?"}, {"text": "your api key is"+testing_output["restaurants"][0]["restaurant"]["apikey"]}]})   	
    return jsonify({"messages":[{"attachment":{"type":"template","payload":{"template_type":"generic","elements":[{"title":"Classic White T-Shirt","image_url":"http://petersapparel.parseapp.com/img/item100-thumb.png","subtitle":"Soft white cotton t-shirt is back in style","buttons":[{"type":"web_url","url":"https://petersapparel.parseapp.com/view_item?item_id=100","title":"View Item"},{"type":"web_url","url":"https://petersapparel.parseapp.com/buy_item?item_id=100","title":"Buy Item"}]},{"title":"Classic Grey T-Shirt","image_url":"http://petersapparel.parseapp.com/img/item101-thumb.png","subtitle":"Soft gray cotton t-shirt is back in style","buttons":[{"type":"web_url","url":"https://petersapparel.parseapp.com/view_item?item_id=101","title":"View Item"},{"type":"web_url","url":"https://petersapparel.parseapp.com/buy_item?item_id=101","title":"Buy Item"}]}]}}}]})   	
if __name__ == '__main__':
  app.debug = True
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port = port)