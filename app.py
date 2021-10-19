from flask import Flask, render_template, request, redirect, url_for
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from base64 import b64encode


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Inavish15@localhost/fynd'
db = SQLAlchemy(app)


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
#
# with open('file.txt', 'r') as file:
#     conversation = file.read()
#
# bott = ChatBot("Fynd ChatBot")
# trainer2 = ListTrainer(bott)
# trainer2.train(conversation)


# Functions for chatbot-----------------------------------------------------------------------------------------


@app.route("/chatbott")
def chatbott():

    return render_template("fyndChatbot.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    return str(bott.get_response(userText))
# ------------------------------------------------------------
# Admin Section


@app.route("/adminpage")
def adminPage():

    return render_template("AdminIndex.html")


if __name__ == "__main__":
    app.run(debug = True)