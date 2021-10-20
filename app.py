from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from base64 import b64encode
from random import randint
import smtplib


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Inavish15@localhost/fynd'
db = SQLAlchemy(app)
otp = randint(000000, 999999)


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    itemname = db.Column(db.String(20), primary_key=False)
    itemprice = db.Column(db.String(20), unique=False, nullable=False)
    itemcolor = db.Column(db.String(20), unique=False, nullable=False)
    photo = db.Column(db.LargeBinary)



# @app.route("/")
# def home():
#     sql = text('select * from items')
#     result = db.engine.execute(sql)
#
#     return render_template("index.html", items=result)
@app.route('/')
def home():
    # sql = text('select * from car')
    # all_data = db.engine.execute(sql)

    all_data = Items.query.all()
    for i in all_data:
        i.photo = b64encode(i.photo).decode("utf-8")
    return render_template("index.html", items=all_data)


@app.route("/insertitem", methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        id = request.form.get('id')
        itemname = request.form.get('itemname')
        itemprice = request.form.get('itemprice')
        itemcolor = request.form.get('itemcolor')
        photo = request.files['photo']
        entry = Items(id=id, itemname=itemname, itemprice=itemprice, itemcolor=itemcolor, photo=photo.read())
        db.session.add(entry)
        db.session.commit()

    return render_template("AdminIndex.html")

# Chat bot code
# Chat bot training data-----------------------------------------------------------------------------------------
#
# #
# with open('file.txt', 'r') as file:
#     conversation = file.read()
#
# bot1 = ChatBot("Fynd ChatBot")
# trainer2 = ListTrainer(bot1)
# trainer2.train(["Hey",
# "Hi there!",
# "Hi",
# "Hi!",
# "How are you doing?",
# "I'm doing great.",
# "That is good to hear",
# "Thank you.",
# "You're welcome.",
# "What is your name?", "My name is Fynd ChatBot",
# "Who created you?", "Shivani",
# "Tell me about yourself",
# "My name is Fynd Chatbot. I am created to help customers for there general queries",
# "Contact",
# "Email : Fynd@gmail.com, Mobile number : +91 1234567890 Location : Mumbai, Maharashtra",
# "Available items","T-shirt, Dress, Jeans, Jeans, saree etc",
#
# "Projects",""])
#
# trainer2.train(conversation)


# Functions for chatbot-----------------------------------------------------------------------------------------


@app.route("/chatbott")
def chatbott():

    return render_template("fyndChatbot.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(bot1.get_response(userText))
# ------------------------------------------------------------


# Booking by users


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    uname = db.Column(db.String(20), primary_key=False)
    uemail = db.Column(db.String(20), unique=False, nullable=False)
    uphone = db.Column(db.String(20), unique=False, nullable=False)
    uaddress = db.Column(db.String(200), unique=False, nullable=False)


def sendotp(uemail):
    messege1 = str(otp)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("shivani151020@gmail.com", "#")
    server.sendmail("shivani151020@gmail.com", uemail, messege1)


@app.route('/validate',methods=['POST'])
def validate():
    if request.method == 'POST':
        id = request.form.get('id')
        uname = request.form.get('uname')
        uemail = request.form.get('uemail')
        uphone = request.form.get('uphone')
        uaddress = request.form.get('uaddress')
        user_otp=request.form['otp']
        if otp==int(user_otp):
            entry = Users(id=id, uname=uname, uemail=uemail, uphone=uphone, uaddress=uaddress)
            db.session.add(entry)
            db.session.commit()
            return "<h3>Receipt has been sent to you on your email</h3>"
        return "<h3>Please Try Again</h3>"


@app.route("/order", methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        id = request.form.get('id')
        uname = request.form.get('uname')
        uemail = request.form.get('uemail')
        uphone = request.form.get('uphone')
        uaddress = request.form.get('uaddress')
        sendotp(uemail)
        # messege = "Your order is successfully recieved!"
        # server = smtplib.SMTP("smtp.gmail.com", 587)
        # server.starttls()
        # server.login("shivani151020@gmail.com", "Shiv@ni#1510")
        # server.sendmail("shivani151020@gmail.com", uemail, messege)

    return render_template("otpVerification.html",id = id, uname=uname, uemail=uemail, uphone=uphone, uaddress=uaddress)

# Admin Section
@app.route("/adminpage")
def adminPage():
    # SQL INNER JOIN
    sql = text('select items.id, items.itemname,items.itemprice,items.itemcolor,items.photo,users.uname,'
               ' users.uemail,users.uphone,users.uaddress from items inner join users on items.id = users.id;')
    result = db.engine.execute(sql)
    # for row in result:
    #     row = dict(row.items)
    #     row.photo = b64encode(row.photo).decode("utf-8")
    # for row in result:
    #     d = dict(row.items())
    #     d['photo'] = b64encode(d['photo']).decode("utf-8")
    return render_template("AdminIndex.html", order=result)


if __name__ == "__main__":
    app.run(debug = True)
