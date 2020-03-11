import math
import os
import requests
from flask_sqlalchemy import SQLAlchemy 
from flask import Flask, render_template, request, jsonify, session, redirect, flash, url_for
from flask_session import Session
from sqlalchemy import table, column, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
#postgres://username:password@host:5432/db
engine = create_engine("postgres://postgres:10102000@localhost:5432/postgres")
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def index():
    return render_template ('index.html')

@app.route('/about')
def about():
    return render_template ('about.html')

@app.route('/blog')
def blog():
    return render_template ('blog.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        if not request.form.get("name"):
            return render_template("calculator.html", message="Must Provide Your Name")

        if not request.form.get("email"):
            return render_template("calculator.html", message="Must Provide Your Email")

        if not request.form.get("message"):
            return render_template("calculator.html", message="Must Provide Your Message")

        if db.execute("INSERT INTO contact (name, email, message) VALUES (:name, :email, :message)",
                            {"name":request.form.get("name"),
                            "email":request.form.get("email"),
                            "message":request.form.get("message")}):
            # Commit changes to database
            db.commit()
            message2="We will contact you as soon as possible."
        return render_template ('contact.html', message2=message2)
    else:
        return render_template ('contact.html')
    


@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == "POST":
        data = db.execute("SELECT * FROM data").fetchone()
        gender = db.execute("SELECT gender FROM data").fetchone()
        
        numberCheck = db.execute("SELECT * FROM data WHERE mobile_number = :mobile_number",
                          {"mobile_number":request.form.get("mobile_number")}).fetchone()

        # Check if email already exist
        if numberCheck:
            return render_template("calculator.html", message="Mobile Number already exist")
        
        if not request.form.get("area"):
            return render_template("calculator.html", message="Must Provide Your Area")

        if not request.form.get("gender"):
            return render_template("calculator.html", message="Must Provide Your Gender")
        
        if not request.form.get("exercise"):
            return render_template("calculator.html", message="Must Provide Your Excercise Rate")


        # Insert register into DB
        db.execute("INSERT INTO data (name, mobile_number, weight, height, age, exercise, gender, area) VALUES (:name, :mobile_number, :weight, :height, :age, :exercise, :gender, :area)",
                            {"name":request.form.get("name"),
                            "mobile_number":request.form.get("mobile_number"),
                            "weight":request.form.get("weight"),
                            "height":request.form.get("height"),
                            "age":request.form.get("age"),
                            "exercise":request.form.get("exercise"),
                            "gender":request.form.get("gender"),
                            "area":request.form.get("area")})

        # Commit changes to database
        db.commit()
        
        rows = db.execute("SELECT * FROM data ORDER BY id DESC LIMIT 1;")
        result = rows.fetchone()

        session["id"] = result[0]
        session["name"] = result[1]
        session["mobile_number"] = result[2]
        session["weight"] = result[3]
        session["height"] = result[4]
        session["age"] = result[5]
        session["exercise"] = result[6]
        session["gender"] = result[7]
        print(result)
        
        # Basal metabolic rate and Ideal body weight equations
        if session["gender"] == "male":
            # Basal metabolic rate equation for Men
            bmr =  math.trunc((10 * session["weight"]) + (6.25 * session["height"]) - (5 * session["age"]) + 5)
            # Ideal Body Weight Equation For Men
            idealweight = math.trunc(50 + ( 0.91 * ( session["height"] - 152.4 ) ))
            # Total Body Weight
            tbw = math.trunc(2.447 - 0.09156 * session["age"] + 0.1074 * session["height"] + 0.3362 * session["weight"])
        elif session["gender"] == "female":
            # Basal metabolic rate equation for Women
            bmr = math.trunc((10 * session["weight"]) + (6.25 * session["height"]) - (5 * session["age"]) - 161)
            # Ideal Body Weight Equation For Women
            idealweight = math.trunc(45.5 + ( 0.91 * ( session["height"] - 152.4 ) ))
            # Total Body Weight
            tbw = math.trunc(-2.097 + 0.1069 * session["height"] + 0.2466 * session["weight"])

        # % of Ideal Body Weight equation
        percentIdealWeight = math.trunc( session["weight"] * 100 / idealweight )
        # % of Ideal Body Water equation
        tbwp = math.trunc(tbw / session["weight"] * 100)

        if percentIdealWeight > 100:
            underIdealWeight = False
            overIdealWeight = percentIdealWeight - 100
            percentIdealWeight = False
        elif percentIdealWeight < 100:
            overIdealWeight = False
            underIdealWeight = percentIdealWeight - 100
        print(percentIdealWeight)

        # Calculate bmr 
        if session["exercise"] == 0:
            need = math.trunc(bmr * 1.2)
        elif session["exercise"] == 1:
            need =  math.trunc(bmr * 1.375)
        elif session["exercise"] == 2:
            need =  math.trunc(bmr * 1.55)
        elif session["exercise"] == 3:
            need =  math.trunc(bmr * 1.725)
        
        # Convert Height cm to m
        heightMeter = session["height"] / 100.0

        # Calculate the ratio of weight
        idealrange = math.trunc(session["weight"] / heightMeter ** 2)

        # Select the level of weight
        if idealrange in range (0 ,18):
            weightlevel = "Below Normal"
        elif idealrange in range (18 ,25) :
            weightlevel = "Normal"
        elif idealrange > 25 :
            weightlevel = "Overweight"

        # Define values 
        targetCalorie = False
        meal= False
        workout = False
        normalWeight = False
        
        if weightlevel == "Below Normal":
            targetCalorie = False
            meal = True
            meal = need + 500
        elif weightlevel == "Normal":
            meal = False
            normalWeight = True
        elif weightlevel == "Overweight":
            targetCalorie = True
            targetCalorie = need - 500
            workout = True

        # Redirect user to login page
        return render_template("calculator.html", bmr=bmr, need=need, idealrange=idealrange, weightlevel=weightlevel, targetCalorie=targetCalorie, workout=workout, meal=meal, idealweight=idealweight, percentIdealWeight=percentIdealWeight, overIdealWeight=overIdealWeight, underIdealWeight=underIdealWeight, normalWeight=normalWeight, tbw=tbw, tbwp=tbwp)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("calculator.html")


if __name__ == '__main__':
    app.run(debug=True)     