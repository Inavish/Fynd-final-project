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
# Admin Section


@app.route("/adminpage")
def adminPage():

    return render_template("AdminIndex.html")


if __name__ == "__main__":
    app.run(debug = True)
