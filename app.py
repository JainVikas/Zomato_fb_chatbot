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
    cuisine = request.args.get('cuisine')
    print(cuisine)
    print(longitude)
    print(latitude)
    print(query_string)
    output ={"messages": [{ "attachment":{"type":"template", "payload":{"template_type":"generic","elements":[]}}}]}
    testing_output = z.parse("collections","lat="+str(latitude) + ","+ "lon="+str(longitude))
    #output of parse is a dict, so quite convinient to find details using inbuit features of python dict
    for i in range(len(testing_output["collections"])):
        collection_dict={}
        collection_dict["title"] = testing_output["collections"][i]["collection"]["description"]
        collection_dict["image_url"] = testing_output["collections"][i]["collection"]["image_url"]
        output["messages"][0]["attachment"]["payload"]["elements"].append(collection_dict)
    print(output)
    return jsonify({'messages': [{'attachment': {'type': 'template', 'payload': {'template_type': 'generic', 'elements': [{'title': 'The most popular restaurants in town this week', 'image_url': 'https://b.zmtcdn.com/data/collections/e140962ec7eecbb851155fe0bb0cd28c_1463395649.jpg'}, {'title': 'The best new places in town', 'image_url': 'https://b.zmtcdn.com/data/collections/b8499c7a6b74ddf01497ac8afc86d2e2_1476701306.jpg'}, {'title': 'Hyderabadi, Kolkata, Lucknawi...the choice is yours', 'image_url': 'https://b.zmtcdn.com/data/collections/81dc179878a8d9e8b2ab03e4eaeab0df_1459434256.jpg'}, {'title': 'After cloud, sun shines!', 'image_url': 'https://b.zmtcdn.com/data/collections/7145c0e24b2d4c24fb83a64ce29c8287_1499239643.jpg'}, {'title': 'The best bars to relax and enjoy a cold one.', 'image_url': 'https://b.zmtcdn.com/data/collections/7d37c606ce097f1179ccfddc301e5bf2_1497266210.jpg'}, {'title': "Eat to your heart's content", 'image_url': 'https://b.zmtcdn.com/data/collections/5df054585bcc09b8ea426a7c6963f874_1463723941.jpg'}, {'title': 'The perfect spots for a romantic meal', 'image_url': 'https://b.zmtcdn.com/data/collections/8c2611e9f177b47ba905367af063b6f7_1463726322.jpg'}, {'title': 'Great deals on booze. Happy hours indeed', 'image_url': 'https://b.zmtcdn.com/data/collections/8c42959a434bd9cabf283ac56872c996_1463635734.jpg'}, {'title': 'Restaurants serving the best vegetarian fare', 'image_url': 'https://b.zmtcdn.com/data/collections/7dcd65d161813057e74cfaf2903c28fe_1444656532_l.jpg'}, {'title': 'The top places to enjoy a drink', 'image_url': 'https://b.zmtcdn.com/data/collections/f9d822284b336c1eb8c3af8c42216389_1460023238.jpg'}, {'title': 'Just about the perfect way to end the week', 'image_url': 'https://b.zmtcdn.com/data/collections/213094197d171cb9ca214724fcb63abe_1455262413.jpg'}, {'title': "Dine like you're on top of the world", 'image_url': 'https://b.zmtcdn.com/data/collections/54fdeccf0c51141023dd0d58356aec2a_1467631167.jpg'}, {'title': 'Sweet or savoury, pancakes or eggs benny, treat yourself to the perfect pre-midday meal at these breakfast & brunch places near you', 'image_url': 'https://b.zmtcdn.com/data/collections/a7ddff4ee0a77e2b32823c2ce5551579_1460030505.jpg'}, {'title': 'Your top options when dining on a budget', 'image_url': 'https://b.zmtcdn.com/data/collections/3ad9a189e2aa8e44650ba9dd6af82307_1423748769_l.jpg'}, {'title': 'For the times when bottled brews just do not cut it', 'image_url': 'https://b.zmtcdn.com/data/collections/ac0c18ac3c3956269e6a38c7081f9ef1_1470476332.jpg'}, {'title': 'Grab a bite to eat, a cup of coffee, and catch up with friends or family', 'image_url': 'https://b.zmtcdn.com/data/collections/4c1548d8437a2365886a7fcb0f8b5522_1469107319.jpg'}, {'title': 'Banish those midnight cravings with our handy list of late night & 24-hour restaurants serving all your favourite comfort foods', 'image_url': 'https://b.zmtcdn.com/data/collections/1fa3acc57ad83023e1f50170b1b7fc08_1431429354_l.jpg'}, {'title': 'The best and most affordable booze your city has to offer ', 'image_url': 'https://b.zmtcdn.com/data/collections/5ae77acfc2f3d7a9c7cc2dbf4ba6aecd_1421659018_l.jpg'}, {'title': 'Hamburgers, grilled burgers, veggie burgers or just a classic cheeseburger, these burger places near you are acing the B-game ', 'image_url': 'https://b.zmtcdn.com/data/collections/440ace025553890a68cc64a422b462b3_1492063134.jpg'}, {'title': 'The best restaurants in town for a complete fine-dining experience.', 'image_url': 'https://b.zmtcdn.com/data/collections/3eeb8a5d63844348a56f85c8db028418_1443673408_l.jpg'}, {'title': "They say old is gold and here's the proof", 'image_url': 'https://b.zmtcdn.com/data/collections/0a765bdc61f3054f4e97f406e561b63f_1418391127_l.jpg'}, {'title': 'Knock yourself out with these classic & creativel desserts from cakes & cookies to doughnuts & ice creams ', 'image_url': 'https://b.zmtcdn.com/data/collections/2351d53897466eeb5faed7026c0a2796_1430224886_l.jpg'}, {'title': 'Butter chicken, naan and lassi. And so much more', 'image_url': 'https://b.zmtcdn.com/data/collections/a54eb9a04d0075407f3172f4712c9c03_1421668945_l.jpg'}, {'title': 'The best places for Asian fare', 'image_url': 'https://b.zmtcdn.com/data/collections/8293079b406af27a094dd4cdc41a2fb7_1418390791_l.jpg'}, {'title': 'Refreshingly delicious frozen desserts', 'image_url': 'https://b.zmtcdn.com/data/collections/4592b5c066772cbceaae5478999743b1_1436775109_l.jpg'}, {'title': 'The best seafood places in town', 'image_url': 'https://b.zmtcdn.com/data/collections/3348431bcaa616e6cd3ccadc95ceca63_1427263670_l.jpg'}, {'title': 'The best flavors from continental Europe.', 'image_url': 'https://b.zmtcdn.com/data/collections/2ae26e2aa5320e28d8cb0dd80de1a026_1469274200.jpg'}, {'title': 'Now find your favorite restaurants with offers on ICICI Bank cards', 'image_url': 'https://b.zmtcdn.com/data/collections/3de606c4e8cfd8e275936c50ae1ba7f3_1480314164.jpg'}, {'title': 'Get your grub right at your doorstep', 'image_url': 'https://b.zmtcdn.com/data/collections/273612e3880fa4790562ee39cf48be8b_1445579359_l.jpg'}]}}}]})   	
    #return jsonify(output)   	
    #return jsonify({"messages":[{"attachment":{"type":"template","payload":{"template_type":"generic","elements":[{"title":"Classic White T-Shirt","image_url":"http://petersapparel.parseapp.com/img/item100-thumb.png","subtitle":"Soft white cotton t-shirt is back in style","buttons":[{"type":"web_url","url":"https://petersapparel.parseapp.com/view_item?item_id=100","title":"View Item"},{"type":"web_url","url":"https://petersapparel.parseapp.com/buy_item?item_id=100","title":"Buy Item"}]},{"title":"Classic Grey T-Shirt","image_url":"http://petersapparel.parseapp.com/img/item101-thumb.png","subtitle":"Soft gray cotton t-shirt is back in style"}]}}}]})   	
if __name__ == '__main__':
  app.debug = True
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port = port)