from flask import Flask, json, request, render_template
from sklearn import linear_model
import sklearn.externals
from sklearn.externals import joblib
import math
from flask_cors import CORS, cross_origin
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

app = Flask('uberestimator')
CORS(app)

clf = joblib.load(dir_path + '/model.pkl') 

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/getPrice', methods = ['POST'])
def getPrice():
    data=json.loads(request.data)
    pickupTime = int(data[1]['timeNo'])
    ppl = int(data[1]['passengerNo'])
    dist = float(data[1]['distanceinmile'])
    temp = float(data[0]['temp'])
    wind = float(data[0]['wind'])
    weather = float(data[0]['weather'])

    return str(calculatePrice(pickupTime, ppl, dist, temp, wind, weather))

def calculatePrice(a_pickupTime, a_ppl, a_dist, a_temp, a_wind, a_weather):
    # test_data = [a_pickupTime,a_ppl,a_dist,a_temp,a_wind,a_weather]
    factor = 1.0
    if (a_weather == 4):
        factor = factor * 1.05
    elif (a_weather == 5):
        factor = factor * 1.1
    print 'weather:', a_weather, 'factor:', factor
    test_data = [a_pickupTime,a_ppl,a_dist]
    estimated_price = math.ceil(math.ceil(clf.predict(test_data)[0]) * factor)
    # print 'estimated total_amount: ', estimated_price
    return estimated_price

if __name__ == '__main__':
    app.run()

# restart apache2 cmd:
# sudo service apache2 restart
# sudo apachectl restart