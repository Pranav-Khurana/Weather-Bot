#IMPORTING THE REQUIRED LIBRARIES
from __future__ import print_function
from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import os
from flask import Flask
from flask import request
from flask import make_response

#FLAST APP MUST START IN GLOBAL LAYOUT
app = Flask(__name__)


#STARTING WEBHOOK
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    api = req.get("queryResult").get("action")
    if api == "weather":
        print ("CALL TO WEATHER API")
        res = weather(req)
    elif api == "bus":
        print ("CALL TO BUS API")
        res = bus(req)
    else:
        print("INVALID OR UNREGISTERED ACTION, PLEASE CHECK THE ACTION IN DIALOGFLOW")
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def weather(req):
    print ("STARTED PROCESSING: WORKING GOOD")
    baseurl = "https://api.openweathermap.org/data/2.5/weather?"
    result = req.get("queryResult")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        print ("ERROR IN CITY, VERIFY IT TO BE 'geo-city'")
        return None
    print("REQUEST IS FOR " + str(city) + " CITY")
    yql_url = baseurl + urlencode({'q': city}) + "&APPID=f5936c77dc85dc090132f79160f4008e&units=metric"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    #for some the line above gives an error and hence decoding to utf-8 might help
    #data = json.loads(result.decode('utf-8'))
    print("QUERY PROCESSED : RECEIVED DATA FROM WEATHER API")
    tp = data.get('main').get('temp')
    msg = data['weather'][0]['description']
    speech = "There is " + str(msg) + " today  and the temperature is "+str(tp)+" degree celcius in " + str(city)
    print("WORK COMPLETE")
    ans={ "fulfillmentText": speech, "source": "Weather" }
    return ans


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')


