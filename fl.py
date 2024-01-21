from flask import Flask,render_template,jsonify,request,json,redirect
import mysql.connector
import os
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequestKeyError
from flost import flost
import glob

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="LAF"
)

mycursor = mydb.cursor()
insert_queryLost="insert into LOST(Lostid, DeviceName,MainTag,Date,Location,Photo) values (%s,%s,%s,%s,%s,%s)"
insert_queryFound= "INSERT INTO FOUND (Foundid, Photo, Maintag, Location) VALUES (%s, %s, %s, %s)"
def convertdata(filename):
    with open(filename, 'rb') as file:
        binary_data = file.read()

    # Ensure the length of the binary data is within the allowed limit for the 'BLOB' column
    if len(binary_data) > 65535:  # Adjust this limit based on your actual column size
        raise ValueError("Binary data exceeds maximum allowed length for 'BLOB' column")

    return binary_data


def reverseConvertdata(binary_data,output_filename):
    with open(output_filename, 'wb') as file:
        file.write(binary_data)
        

        
count=0
mycursor.execute('select max(Lostid) from LOST')
for x in mycursor:
    if x[0]!=None:
        count=x[0]+1

count2=0
mycursor.execute('select max(Foundid) from FOUND')
for x in mycursor:
    if x[0]!=None:
        count2=x[0]+1

fl=flost(mycursor)
app=Flask(__name__)
app.config['UPLOAD_FOLDER']="uploads"

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
    img = " "
    
    try:
        photo = request.files['photo']

        if photo.filename != '':
            # return "<h1>No selected file</h1>"

            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

            filename = secure_filename(photo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(filepath)
            print(filepath)
            img=convertdata(filepath)
    except BadRequestKeyError:
        return "<h1>No file part in the request</h1>"

    # img=convertdata(filepath)

    clientIP = request.remote_addr
    print(clientIP)

    data_insert=(count,clientIP,description,date,location,img)
    mycursor.execute(insert_queryLost,data_insert)
    mydb.commit()
    count+=1

    files = glob.glob('renders/*')
    for f in files:
        os.remove(f)

    query=description
    qt="found"
    listing=fl.listing(query,qt)


    data = []
    for x in listing:
        mycursor.execute("SELECT Foundid,Maintag,Photo FROM FOUND WHERE Foundid = %s"%(x))
        for y in mycursor:
            print(y)
            data.append(y[1])
            reverseConvertdata(y[2],'/home/autrio/college-linx/project/Hackiiit/test/renders/%s.jpg'%(x))


    return render_template("listings.html",entries=data)
    

@app.route("/found",methods=['POST'])
def app_found():
    global count2
    date=request.form.get('date')
    location=request.form.get('location')
    description=request.form.get('description')
    try:
        photo = request.files['photo']

        if photo.filename == '':
            return "<h1>No selected file</h1>"

        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        filename = secure_filename(photo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(filepath)
        print(filepath)
    except BadRequestKeyError:
        return "<h1>No file part in the request</h1>"

    img=convertdata(filepath)
    data_insert=(count2,img,description,location)
    mycursor.execute(insert_queryFound,data_insert)
    mydb.commit()
    count2+=1
    return "<h1> Thankyou for your service! </h1>"


if __name__ == "__main__":
    app.run(debug=True)
