from flask import Flask,render_template,request,url_for,redirect
import json
from gevent import pywsgi
import get_data
app = Flask(__name__)

@app.route('/',methods=['GET'])
# @app.route('/lockPage') 
def lockPage(): 
    return render_template('lockpage.html')
    
@app.route('/homePage',methods=['GET'])
def homePage():
    return render_template('homepage.html')
  
@app.route('/sleepTime',methods=['GET'])
def sleepTime():
    return render_template('sleeptime.html')

@app.route('/sleepCycle',methods=['GET'])
def sleepCycle():
    return render_template('sleepcycle.html')

@app.route('/sleepQuality',methods=['GET'])
def sleepQuality():
    return render_template('sleepquality.html')

@app.route('/heartRate',methods=['GET'])
def heartRate():
    return render_template('heartrate.html')

@app.route('/data',methods=['GET','POST'])
def dataSender():
    # with open("data/data.json", 'r') as f:
    #     data = json.load(f)
    return get_data.get_hr_spo2()

if __name__=="__main__":
   # app.run(debug=True)
    server = pywsgi.WSGIServer(('0.0.0.0',5000),app)
    server.serve_forever()

