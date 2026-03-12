from flask import Flask,request,jsonify,render_template
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


# create flask app
application= Flask(__name__)
app=application

## import ridge regression and standard sclaer pickle 
ridge_model=pickle.load(open('D:/Programs/project_deployment/models/ridge.pkl','rb'))
Standard_Scaler=pickle.load(open('D:/Programs/project_deployment/models/scaler.pkl','rb'))



# route for homepage
##  this is our route to load the page for the deployment 

@app.route("/")
def index():
    return render_template('index.html')

## in the get we just retriveing the info anf the post means we want to gather the information from there 


## this will open the home page and by this we get our main prediction page 
@app.route('/predictdata',methods=['GET','POST'])
def predict_datapoint():
     if request.method == "POST":

        # get values from form
        Temperature = float(request.form.get("Temperature"))
        RH = float(request.form.get("RH"))
        Ws = float(request.form.get("Ws"))
        Rain = float(request.form.get("Rain"))
        FFMC = float(request.form.get("FFMC"))
        DMC = float(request.form.get("DMC"))
        ISI = float(request.form.get("ISI"))
        Classes = float(request.form.get("Classes"))
        Region = float(request.form.get("Region"))
        DC = float(request.form.get("DC"))
        
        # convert to array
        data = [[Temperature, RH, Ws, Rain, FFMC, DMC, ISI, Classes, Region,DC]]

        # scale data
        scaled_data = Standard_Scaler.transform(data)

        # prediction
        prediction = ridge_model.predict(scaled_data)

        result = round(prediction[0], 2)

        return render_template("home.html", prediction_text=f"Predicted Fire Weather Index: {result}")
     else:
        return render_template('home.html')
    


# run the server
if __name__ == "__main__":
    app.run(host="0.0.0.0")