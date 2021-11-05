#IMPORT NECESSARY LIBRARIES
import joblib  #for importing your machine learning model
from flask import Flask, render_template, request, jsonify, make_response
import pandas as pd 



# SQLALCHEMY SETUP
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import psycopg2

#os allows you to call in environment variables
# we will set the remote environment variables in heroku 
from dotenv import load_dotenv
import os 

load_dotenv()


#################################################
# Database Setup
#################################################

#make sure you have your own .env on your computer
#comment out when you plan to deploy from heroku

#url = os.getenv('DATABASE_URL')


#uncomment line below when you want to deploy to heroku
url = os.environ.get("URL")


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
#model = joblib.load("<filepath to saved model>")



# create route that renders index.html template
@app.route("/", methods=["GET","POST"])
def home():
    
    #If you have the user submit a form
    if request.method == 'POST': 
        
        #get the contents of the input field. This is referenced by the name argument
        #in the input html
        input_1 = request.form.get("dropdown")
        input_2 = request.form.get("dropdown2")
        
        #all forms return a string, if you want your input to convert to numeric check
        #that the input is numeric and then convert. Skip if you need string inputs for your model
        if input_1.isnumeric():
            
            #convert to integer
            variable_1 = int(input_1)
            variable_2 = int(input_2)

            #plug your inputs into the model you loaded. In this case my model just
            #adds the variables and multiplies. Your model is your machine learning model.
            outcome = (variable_1+variable_2)*2 #model(input_1,input_2)
        
        #This ensures that if a non numeric input is passed, nothing happens
        else:
            outcome = 'What Will Your Value Be?' 
        
        return render_template("index.html", outcome=outcome)
    
    #if you are not recieving form data from a user, for instance when the pager first loads
    #this is what happens. 
    else:
        outcome = 'What Will Your Value Be?' 
         
        return render_template("index.html", outcome=outcome)


#make an endpoint for data you are using in charts. You will use JS to call this data in
#using d3.json("/api/data")
@app.route("/api/data")
def data():
    
    
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    #Query Database. Check SqlAlchemy documentation for how to query
    EData = session.query(EnvironmentData).all()
    myData = []

    
    #here I decided I want a list of dictionaries, where each dictionary represents a row of data
    #from my sql database. This format makes filter and map functions in js easy. 
    for x in EData:

        fullEdata = {}

        fullEdata = {
            "Country": x.Country,
            "HDI":x.HDI,
            "Footprint_Crop":x.Footprint_Crop,
            "Footprint_Graze":x.Footprint_Graze,
            "Footprint_Forest":x.Footprint_Forest,
            "Footprint_Carbon":x.Footprint_Carbon,
            "Footprint_Fish":x.Footprint_Fish,
            "Footprint_Total":x.Footprint_Total,
            "Land_Urban":x.Land_Urban,
            "Emission_CO2":x.Emissions_CO2,
            "BioCap":x.Biocapacity_Total,
            "BioCap_RD":x.BioCap_RD,
            "Data_Quality":x.Data_Quality
        }

        myData.append(fullEdata)
        
    session.close()
    
    #Return the JSON representation of your dictionary
    return (jsonify(myData))

if __name__ == '__main__':
    app.run(debug=True)
