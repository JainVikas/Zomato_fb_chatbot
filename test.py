from zomato import Zomato
z = Zomato("ZOMATO-API-KEY")
# A call to categories endpoint from zomato API.
z.parse("categories","")
# A call to restaurants endppoint from zomato 
# API with required parameters res_id
z.parse("restaurant","res_id=16774318")
