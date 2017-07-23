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
    if request.args.get('latitude') is not None:
        session["latitude"] = request.args.get('latitude')
    if request.args.get('longitude') is not None:
        session["longitude"]= request.args.get('longitude')
    category = request.args.get('text')
    cuisine = request.args.get('cuisine')
    #print(cuisine)
    #print(longitude)
    #print(latitude)
    #print(query_string)
    output ={"messages": [{ "attachment":{"type":"template", "payload":{"template_type":"generic","elements":[]}}}]}
    testing_output = z.parse("collections","lat="+str(session["latitude"]) + ","+ "lon="+str(session["longitude"]))
    #output of parse is a dict, so quite convinient to find details using inbuit features of python dict
    for i in range(9):
    #len(testing_output["collections"])):
        collection_dict={}
        button=[]
        button_dict={}
        button_dict["type"]="show_block"
        button_dict["block_name"]= "collection" 
        button_dict["set_attributes"] = {"collection_id": testing_output["collections"][i]["collection"]["collection_id"]} 
        button_dict["title"]= "Explore"
        button.append(button_dict)
        collection_dict["title"] = testing_output["collections"][i]["collection"]["title"]
        collection_dict["subtitle"] = testing_output["collections"][i]["collection"]["description"]
        collection_dict["image_url"] = testing_output["collections"][i]["collection"]["image_url"]
        collection_dict["buttons"] = button 
        output["messages"][0]["attachment"]["payload"]["elements"].append(collection_dict)
    print(output)
    return jsonify(output)   	
    #return jsonify({"messages":[{"attachment":{"type":"template","payload":{"template_type":"generic","elements":[{"title":"Classic White T-Shirt","image_url":"http://petersapparel.parseapp.com/img/item100-thumb.png","subtitle":"Soft white cotton t-shirt is back in style","buttons":[{"type":"web_url","url":"https://petersapparel.parseapp.com/view_item?item_id=100","title":"View Item"},{"type":"web_url","url":"https://petersapparel.parseapp.com/buy_item?item_id=100","title":"Buy Item"}]},{"title":"Classic Grey T-Shirt","image_url":"http://petersapparel.parseapp.com/img/item101-thumb.png","subtitle":"Soft gray cotton t-shirt is back in style"}]}}}]})   	
@app.route('/collection', methods=['POST', 'GET'])
def collection():
    z = Zomato("ZOMATO-API-KEY")
    collection_id = request.args.get('collection_id')
    print(request.query_string)
    output ={"messages": [{ "attachment":{"type":"template", "payload":{"template_type":"generic","elements":[]}}}]}
    testing_output = z.parse("search","lat="+str(session["latitude"]) + ","+ "lon="+str(session["longitude"]) + ","+"collection_id="+str(collection_id))
    k = 8
	if testing_output["results_found"]<8:
        k = testing_output["results_found"]
    for i in range(k)):
	#len(testing_output["collections"])):
        restaurant_dict={}
        button=[]
        button_dict={}
        button_dict["type"]="show_block"
        button_dict["block_name"]= "restaurant" 
        button_dict["set_attributes"] = {"res_id": testing_output["restaurants"][i]["restaurant"]["id"]} 
        button_dict["title"]= "Check Reviews"
        button.append(button_dict)
        restaurant_dict["title"] = testing_output["restaurants"][i]["restaurant"]["name"]
        restaurant_dict["subtitle"] = "Average cost for 2: " + str(testing_output["restaurants"][i]["restaurant"]["average_cost_for_two"])
        restaurant_dict["image_url"] = testing_output["restaurants"][i]["restaurant"]["featured_image"]
        restaurant_dict["buttons"] = button 
        output["messages"][0]["attachment"]["payload"]["elements"].append(restaurant_dict)
    print(testing_output)
    return jsonify(output)

@app.route('/restaurant', methods=['POST', 'GET'])
def restaurant():
    z = Zomato("ZOMATO-API-KEY")
    collection_id = request.args.get('res_id')
    print(request.query_string)
    output ={"messages": [{ "attachment":{"type":"template", "payload":{"template_type":"generic","elements":[]}}}]}
    testing_output = z.parse("search","lat="+str(session["latitude"]) + ","+ "lon="+str(session["longitude"]) + ","+"collection_id="+str(collection_id))
    for i in range(len(testing_output["restaurants"])):
	#len(testing_output["collections"])):
        restaurant_dict={}
        button=[]
        button_dict={}
        button_dict["type"]="show_block"
        button_dict["block_name"]= "restaurant" 
        button_dict["set_attributes"] = {"res_id": testing_output["restaurants"][i]["restaurant"]["id"]} 
        button_dict["title"]= "Check Reviews"
        button.append(button_dict)
        restaurant_dict["title"] = testing_output["restaurants"][i]["restaurant"]["name"]
        restaurant_dict["subtitle"] = "Average cost for 2: " + str(testing_output["restaurants"][i]["restaurant"]["average_cost_for_two"])
        restaurant_dict["image_url"] = testing_output["restaurants"][i]["restaurant"]["featured_image"]
        restaurant_dict["buttons"] = button 
        output["messages"][0]["attachment"]["payload"]["elements"].append(restaurant_dict)
    print(testing_output)
    return jsonify(output)
if __name__ == '__main__':
  app.debug = True
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port = port)