from flask import Flask, request, render_template,url_for
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("car_price_prediction.pkl","rb"))



@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")




@app.route("/predict", methods = ["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Year
        year = int(request.form["Year"])
        no_of_years = 2021 - year

        # KM Driven
        km_driven = int(request.form["Kms_Driven"])

        # Fuel
        fuel=request.form['Fuel_Type']
        if(fuel=='Diesel'):
            Diesel = 1
            Electric = 0
            LPG = 0
            Petrol = 0

        elif(fuel=='Electric'):
            Diesel = 0
            Electric = 1
            LPG = 0
            Petrol = 0

        elif(fuel=='LPG'):
            Diesel = 0
            Electric = 0
            LPG = 1
            Petrol = 0

        elif(fuel=='Petrol'):
            Diesel = 0
            Electric = 0
            LPG = 0
            Petrol = 1

        else:
            Diesel = 0
            Electric = 0
            LPG = 0
            Petrol = 0

        #Seller type
        seller_type=request.form['Seller_Type']
        if(seller_type =='Individual'):
            Individual = 1
            Trustmark_Dealer = 0

        elif(seller_type =='Trustmark_Dealer'):
            Individual = 0
            Trustmark_Dealer = 1

        else:
            Individual = 0
            Trustmark_Dealer = 0

        #Transmission
        transmission=request.form['Transmission']
        if(transmission=='manual'):
            Manual = 1

        else:
            Manual = 0

        #Owner
        owner=request.form['Owner']
        if(owner=='Fourth_and_Above_Owner'):
            Fourth_and_Above_Owner = 1
            Second_Owner = 0
            Test_Drive_Car = 0
            Third_Owner = 0

        elif(owner=='Second_Owner'):
            Fourth_and_Above_Owner = 0
            Second_Owner = 1
            Test_Drive_Car = 0
            Third_Owner = 0

        elif(owner=='Test_Drive_Car'):
            Fourth_and_Above_Owner = 0
            Second_Owner = 0
            Test_Drive_Car = 1
            Third_Owner = 0

        elif(owner=='Third_Owner'):
            Fourth_and_Above_Owner = 0
            Second_Owner = 0
            Test_Drive_Car = 0
            Third_Owner = 1

        else:
            Fourth_and_Above_Owner = 0
            Second_Owner = 0
            Test_Drive_Car = 0
            Third_Owner = 0

#Name of the columns
#[km_driven', 'no_of_years', 'fuel_Diesel',
#       'fuel_Electric', 'fuel_LPG', 'fuel_Petrol', 'seller_type_Individual',
#       'seller_type_Trustmark Dealer', 'transmission_Manual',
#       'owner_Fourth & Above Owner', 'owner_Second Owner',
#       'owner_Test Drive Car', 'owner_Third Owner']

        prediction=model.predict([[
                km_driven,
                no_of_years,
                Diesel,
                Electric,
                LPG,
                Petrol,
                Individual,
                Trustmark_Dealer,
                Manual,
                Fourth_and_Above_Owner,
                Second_Owner,
                Test_Drive_Car,
                Third_Owner,
            ]])

        output=round(prediction[0],2)

        return render_template('index.html',prediction_text="Your Car Selling price is Rs. {}".format(output))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
