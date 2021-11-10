#IMPORT NECESSARY LIBRARIES
import joblib  #for importing your machine learning model
from flask import Flask, render_template, request, jsonify, make_response
import pandas as pd 
import sklearn

# SQLALCHEMY SETUP
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import psycopg2

import pickle
from pickle import dump as dump, load as load
import numpy as np

#os allows you to call in environment variables
# we will set the remote environment variables in heroku 
# from dotenv import load_dotenv
import os 

# load_dotenv()


#################################################
# Database Setup
#################################################

#make sure you have your own .env on your computer
#comment out when you plan to deploy from heroku

url = os.getenv('URL')


#uncomment line below when you want to deploy to heroku
# url = os.environ.get("URL")


engine = create_engine(f'{url}')


# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
EnvironmentData = Base.classes.envdata

# create instance of Flask app
app = Flask(__name__)


#Line below will load your machine learning model
#load the scaler
loaded_scaler=pickle.load("ml_picklefiles/Xscaler_new.pkl","rb")
#load the model 
model = joblib.load("ml_picklefiles/finalized_model_nov9.sav","rb")



app.route('/', methods = ['GET','POST'])

def result():
    
    column_names=[ 'Size__1-200 employees', 'Size__1000+ employees',
       'Size__10000+ employees', 'Size__200+ employees',
       'Size__500+ employees', 'Type_of_ownership_College / University',
       'Type_of_ownership_Company - Private',
       'Type_of_ownership_Company - Public', 'Type_of_ownership_Contract',
       'Type_of_ownership_Franchise', 'Type_of_ownership_Government',
       'Type_of_ownership_Hospital',
       'Type_of_ownership_Nonprofit Organization',
       'Type_of_ownership_Other Organization',
       'Type_of_ownership_Private Practice / Firm',
       'Type_of_ownership_School / School District',
       'Type_of_ownership_Self-employed',
       'Type_of_ownership_Subsidiary or Business Segment',
       'Type_of_ownership_Unknown', 'Sector__Accounting & Legal',
       'Sector__Aerospace & Defense',
       'Sector__Arts, Entertainment & Recreation',
       'Sector__Biotech & Pharmaceuticals', 'Sector__Business Services',
       'Sector__Construction, Repair & Maintenance',
       'Sector__Consumer Services', 'Sector__Education', 'Sector__Finance',
       'Sector__Government', 'Sector__Health Care',
       'Sector__Information Technology', 'Sector__Insurance',
       'Sector__Manufacturing', 'Sector__Media', 'Sector__Mining & Metals',
       'Sector__Non-Profit', 'Sector__Oil, Gas, Energy & Utilities',
       'Sector__Real Estate', 'Sector__Restaurants, Bars & Food Services',
       'Sector__Retail', 'Sector__Telecommunications',
       'Sector__Transportation & Logistics', 'Revenue__$1+ billion',
       'Revenue__$1+ million', 'Revenue__$100+ million',
       'Revenue__$50 million', 'Revenue__Less than $1 million',
       'Rating_new_1.0', 'Rating_new_2.0', 'Rating_new_2.5', 'Rating_new_3.0',
       'Rating_new_3.5', 'Rating_new_4.0', 'Rating_new_4.5', 'Rating_new_5.0']
    
    mylist=[0]*55
    column_df=pd.DataFrame(columns=column_names)
    column_df.loc[0]=mylist
    
    
    
    
    if request.method == 'POST':
        print(request.form)
        #get the contents of the input field.
        size= request.form.get("dropdown")
        column_df[size]=1
        
        ownership = request.form.get("dropdown2")
        column_df[ownership]=1
        sector= request.form.get("dropdown3")
        column_df[sector]=1
        revenue= request.form.get("dropdown4")
        column_df[revenue]=1
        rating= request.form.get("dropdown5")
        column_df[rating]=1
        
        # Encode user inputs
        scaled_user_input = loaded_scaler.transform([column_df.loc[0]])
        
        
        
        prediction =model.predict(scaled_user_input)   
        
        print(prediction)   
        
        if int(prediction)== 1:
            prediction ='yes,easy to apply'
        else:
            prediction ='not easy,but still can try'           
    return render_template("index.html", prediction = prediction)

#make an endpoint for data you are using in charts. You will use JS to call this data in
#using d3.json("/api/data")
# @app.route("/api/data")
# def data():
    
    
#     # Create our session (link) from Python to the DB
#     session = Session(engine)
    
#     #Query Database. Check SqlAlchemy documentation for how to query
#     EData = session.query(EnvironmentData).all()
#     myData = []

    
#     #here I decided I want a list of dictionaries, where each dictionary represents a row of data
#     #from my sql database. This format makes filter and map functions in js easy. 
#     for x in EData:

#         fullEdata = {}

#         fullEdata = {
#             "Country": x.Country,
#             "HDI":x.HDI,
#             "Footprint_Crop":x.Footprint_Crop,
#             "Footprint_Graze":x.Footprint_Graze,
#             "Footprint_Forest":x.Footprint_Forest,
#             "Footprint_Carbon":x.Footprint_Carbon,
#             "Footprint_Fish":x.Footprint_Fish,
#             "Footprint_Total":x.Footprint_Total,
#             "Land_Urban":x.Land_Urban,
#             "Emission_CO2":x.Emissions_CO2,
#             "BioCap":x.Biocapacity_Total,
#             "BioCap_RD":x.BioCap_RD,
#             "Data_Quality":x.Data_Quality
#         }

#         myData.append(fullEdata)
        
#     session.close()
    
#     #Return the JSON representation of your dictionary
#     return (jsonify(myData))

if __name__ == '__main__':
    app.run(debug=True)
