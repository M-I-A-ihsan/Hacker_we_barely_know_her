from flask import Flask,render_template,jsonify,request,json,redirect
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="LAF"
)

mycursor = mydb.cursor()
insert_queryLost="insert into LOST(Lostid, DeviceName,MainTag,Date,Location) values (%s,%s,%s,%s,%s)"
insert_queryFound= "INSERT INTO FOUND (Foundid, Photo, Maintag, Location) VALUES (%s, %s, %s, %s)"

count=10
count2=12
app=Flask(__name__)

@app.route("/")
def hello() -> str:
    return render_template("HomePage.html")

@app.route("/FormLost.html",methods=['GET'])
def redirL():
    return render_template("FormLost.html")

@app.route("/FormFound.html",methods=['GET'])
def redirF():
    return render_template("FormFound.html")


@app.route("/lost",methods=['POST'])
def app_lost():
    global count
    date=request.form.get('date')
    location=request.form.get('location')
    description=request.form.get('description')
    photo=request.form.get('photo')
    data_insert=(count,1234,description,date,location)
    mycursor.execute(insert_queryLost,data_insert)
    mydb.commit()
    count+=1
    return "<h1> successful </h1>"
    

@app.route("/found",methods=['POST'])
def app_found():
    global count2
    date=request.form.get('date')
    location=request.form.get('location')
    description=request.form.get('description')
    photo=request.form.get('photo')
    data_insert=(count2,photo,description,location)
    mycursor.execute(insert_queryFound,data_insert)
    mydb.commit()
    count2+=1
    return "<h1> successful </h1>"


if __name__ == "__main__":
    app.run(debug=True)