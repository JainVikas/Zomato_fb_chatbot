import json,sys
import urllib3
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

class Zomato:
    
    def __init__(self,api_key,response_content_type="application/json",base_url="https://developers.zomato.com/api/v2.1/"):
        if api_key:
            self.api_key = "c86d87b3580dd6a8bcb1eefacdcdea63"
        else:
            print("NO API KEY GIVEN.")
            return
            
        self.response_content_type = response_content_type
        self.base_url = base_url
        self.response_content_type = response_content_type
        self.all_endpoints = ["categories","cities","collections","cuisines","establishments","geocode","location_details","locations","dailymenu","restaurant","reviews","search"]
        self.endpoint_param = {"categories":{},"cities":{"q":{'type':'string'},"lat":{'type':'double'},"lon":{'type':'double'},"city_ids":{'type':'string'},"count":{'type':'integer'}},"collections":{"lat":{'type':'double'},"lon":{'type':'double'},"city_id":{'type':'integer'},"count":{'type':'integer'}},"cuisines":{"lat":{'type':'double'},"lon":{'type':'double'},"city_id":{'type':'integer'}},"establishments":{"lat":{'type':'double'},"lon":{'type':'double'},"city_id":{'type':'integer'}},"geocode":{"required":["lat","lon"],"lat":{'type':'double'},"lon":{'type':'double'}},"location_details":{"required":["entity_id","entity_type"],"entity_id":{'type':'integer'},"entity_type":{'type':'string'}},"locations":{"required":["query"],"query":{'type':'string'},"lat":{'type':'double'},"lon":{'type':'double'},"count":{'type':'integer'}},"dailymenu":{"required":["res_id"],"res_id":{'type':'integer'}},"restaurant":{"required":["res_id"],"res_id":{'type':'integer'}},"reviews":{"required":["res_id"],"res_id":{'type':'integer'},"start":{'type':'integer'},"count":{'type':'integer'}},"search":{"entity_id":{'type':'integer'},"entity_type":{'type':'string'},"start":{'type':'integer'},"count":{'type':'integer'},"lat":{'type':'double'},"lon":{'type':'double'},"q":{'type':'string'},"radius":{'type':'double'},"cuisines":{'type':'string'},"establishment_type":{'type':'string'},"collection_id":{'type':'string'},"category":{'type':'string'},"order":{'type':'string'},"sort":{'type':'string'}}}
    
    def parse(self,endpoint,parameters=None):
        if endpoint not in self.all_endpoints:
            print("Not a valid endpoint.")
            print(self.all_endpoints)
            return
        all_parameters = ""
        parameters = parameters.replace(" ","")
        params = parameters.split(",")
        print(params)
        para_value = []
        for param in params:
            para_value.extend( param.split("="))
        endpoint_dict = self.endpoint_param[endpoint]
        print(para_value)
        if parameters:
            if "required" in endpoint_dict.keys():
                required_param_list = endpoint_dict["required"]
                if not all(required_param in para_value for required_param  in required_param_list):
                    print("Required value missing!!!")
                    return
            i = 0
            length = len(para_value)
            while i < length:
                if para_value[i] in self.endpoint_param[endpoint.lower()].keys():
                    all_parameters = all_parameters + str(para_value[i])+"="+str(para_value[i+1])+"&"
                else:
                    print("Parameter is not valid, use help to find the list of all parameter for a given endpoint.")
                    return
                i = i + 2
        else:
            if "required" in endpoint_dict.keys():
                print("Required value missing!!!!")
                return
                
        if all_parameters:
            all_parameters = all_parameters[:-1]
        return self._execute(endpoint.lower(),all_parameters)
            
    def _execute(self,endpoint,parameter):
        url = self.base_url + endpoint + "?" + parameter
        req = Request(url)
        if self.response_content_type == "application/json": 
            req.add_header('Accept', self.response_content_type)
            req.add_header("user_key", self.api_key) 
            try:
                res = urlopen(req)
                print(res.getcode())
                json_data = json.load(res)
                return json_data
            except HTTPError as e:
                print(str(e.code)+"\t"+e.reason)
                return
        elif self.response_content_type == "application/xml":
            req.add_header('Accept', self.response_content_type)
            req.add_header("user_key", self.api_key) 
            try:
                res = urlopen(req)
                return res.code()
            except HTTPError as e:
                print(str(e.code)+"\t"+e.reason)
                return
        else:
            print("ERROR: Response content type can only be applcation/json or application/xml.")
            return
    
            
