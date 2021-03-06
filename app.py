from flask import Flask, render_template, request, redirect, url_for, session
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from base64 import b64encode
from random import randint
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import date


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:inavish15@localhost/fynd'
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

ROWS_PER_PAGE = 6


@app.route('/')
def home():
    # sql = text('select * from car')
    # all_data = db.engine.execute(sql)

    page = request.args.get('page', 1, type=int)
    all_data = Items.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    for i in all_data.items:
        i.photo = b64encode(i.photo).decode("utf-8")
    return render_template("index.html", all_data=all_data)


# Chat bot code
# Chat bot training data-----------------------------------------------------------------------------------------
#
#
with open('file.txt', 'r') as file:
    conversation = file.read()

bot1 = ChatBot('mysqlbot', storage_adapter="chatterbot.storage.SQLStorageAdapter",
               database_uri="mysql+pymysql://root:inavish15@localhost/fynd", )
# bot1 = ChatBot("Fynd ChatBot")
trainer2 = ListTrainer(bot1)
trainer2.train(["Hey",
                "Hi there!",
                "Hi",
                "Hi!",
                "How are you doing?",
                "I'm doing great.",
                "That is good to hear",
                "Thank you.",
                "You're welcome.",
                "What is your name?", "My name is Fynd ChatBot",
                "Who created you?", "Shivani",
                "Tell me about yourself",
                "My name is Fynd Chatbot. I am created to help customers for there general queries",
                "Contact",
                "Email : Fynd@gmail.com, Mobile number : +91 1234567890 Location : Mumbai, Maharashtra",
                "Available items", "T-shirt, Dress, Jeans, Jeans, saree etc",
                "Delivery", "Delivery of product will be done in 3-2 days",
                "Current Offers", "Diwali sale, 50% discount on fist order",
                "Projects", ""])

trainer2.train(conversation)


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
    uid = db.Column(db.Integer, primary_key=True, unique=True, auto_increment=True)
    id = db.Column(db.Integer, unique=False)
    uname = db.Column(db.String(20), primary_key=False)
    uemail = db.Column(db.String(20), unique=False, nullable=False)
    uphone = db.Column(db.String(20), unique=False, nullable=False)
    uaddress = db.Column(db.String(200), unique=False, nullable=False)
    fromdate = db.Column(db.String(200), nullable=False)
    todate = db.Column(db.String(200), nullable=False)
    totalcost = db.Column(db.Integer,nullable=False)
    totaldays = db.Column(db.Integer,nullable=False)


def sendotp(uemail):
    messege1 = str(otp)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("shivani151020@gmail.com", "#")
    server.sendmail("shivani151020@gmail.com", uemail, messege1)


def sendpdf(id, uname, uemail, uphone, uaddress,fromdate, todate,product_details, totaldays, totalcost):
    # html = render_template("receipt_pdf.html", id = id, uname=uname, uemail=uemail, uphone=uphone, uaddress=uaddress)
    # pdf = pdfkit.from_string(html, False)
    # sudo apt-get install wkhtmltopdf
    fromaddr = "shivani151020@gmail.com"
    toaddr = uemail

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Fynd order reciept"
    body = f"Name: {uname}\nEmail: {uemail}\nPhone No.: {uphone}\nAddress: {uaddress}\nProduct Name: {product_details.itemname}\nPrice: {product_details.itemprice} Rs\day\nColour: {product_details.itemcolor}\nFrom Date: {fromdate}\nTo date: {todate}\nNumber of total days for which the product is rented: {totaldays}\nTotal cost for {totaldays} days: {totalcost} Rs "
    msg.attach(MIMEText(body, 'plain'))
    # filename = "Fynd_Order_receipt"
    # attachment = open("shivani.pdf", "rb")
    # part = MIMEBase('application', 'octet-stream')
    # part.set_payload(attachment.read())
    # encoders.encode_base64(part)
    # part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    # msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "#")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()


def days_calc(fromdate, todate):
    year = int(fromdate[:4])
    m = int(fromdate[5:7])
    d = int(fromdate[8:11])
    d0 = date(year, m, d)
    year = int(todate[:4])
    m = int(todate[5:7])
    d = int(todate[8:11])
    d1 = date(year, m, d)
    delta = d1 - d0
    return delta.days


@app.route('/validate', methods=['POST'])
def validate():
    if request.method == 'POST':
        id = request.form.get('id')
        uname = request.form.get('uname')
        uemail = request.form.get('uemail')
        uphone = request.form.get('uphone')
        uaddress = request.form.get('uaddress')
        fromdate = request.form.get('fromdate')
        todate = request.form.get('todate')
        user_otp = request.form['otp']
        q = int(id)
        product_details = Items.query.get(q)
        totaldays = days_calc(fromdate, todate)
        totalcost = totaldays * int(product_details.itemprice)
        if otp == int(user_otp):
            entry = Users(id=id, uname=uname, uemail=uemail, uphone=uphone, uaddress=uaddress, fromdate=fromdate, todate=todate, totaldays=totaldays,totalcost=totalcost)
            db.session.add(entry)
            db.session.commit()
            sendpdf(id, uname, uemail, uphone, uaddress,fromdate, todate,product_details, totaldays, totalcost)
            return redirect(url_for('home'))
        return "<h3>Please Try Again</h3>"


@app.route("/order", methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        id = request.form.get('id')
        uname = request.form.get('uname')
        uemail = request.form.get('uemail')
        uphone = request.form.get('uphone')
        uaddress = request.form.get('uaddress')
        fromdate = request.form.get('fromdate')
        todate = request.form.get('todate')
        q = int(id)
        product_details = Items.query.get(q)
        product_details.photo = b64encode(product_details.photo).decode("utf-8")
        totaldays = days_calc(fromdate, todate)
        totalcost = totaldays * int(product_details.itemprice)
        sendotp(uemail)

    return render_template("otpVerification.html", id=id, uname=uname, uemail=uemail, uphone=uphone, uaddress=uaddress, fromdate=fromdate, todate=todate,product_details=product_details, totaldays=totaldays, totalcost=totalcost )


# Admin Section
@app.route("/adminpage")
def adminPage():
    # SQL INNER JOIN
    sql = text('select items.id, items.itemname,items.itemprice,items.itemcolor,users.uname,users.uid,'
               'users.uemail,users.uphone,users.uaddress,users.fromdate, users.todate,users.totaldays, '
               'users.totalcost from items inner join users on items.id = users.id order by users.uid;')
    result = db.engine.execute(sql)
    page = request.args.get('page', 1, type=int)
    all_data = Items.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    for i in all_data.items:
        i.photo = b64encode(i.photo).decode("utf-8")
    # for row in result:
    #     row = dict(row.items)
    #     row.photo = b64encode(row.photo).decode("utf-8")
    # for row in result:
    #     d = dict(row.items())
    #     d['photo'] = b64encode(d['photo']).decode("utf-8")
    return render_template("AdminIndex.html", order=result, all_data=all_data)


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

    return redirect(url_for('adminPage'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Items.query.get(request.form.get('id'))
        my_data.itemname = request.form['itemname']
        my_data.itemprice = request.form['itemprice']
        my_data.itemcolor = request.form['itemcolor']
        db.session.commit()
        return redirect(url_for('adminPage'))


@app.route('/delete', methods = ['GET', 'POST'])
def delete():
    if request.method == 'POST':
        id = request.form.get('id')
        my_data = Items.query.get(id)
        db.session.delete(my_data)
        db.session.commit()

    return redirect(url_for('adminPage'))


@app.route('/deleteuser', methods = ['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        uid = request.form.get('uid')
        my_data = Users.query.get(uid)
        db.session.delete(my_data)
        db.session.commit()

    return redirect(url_for('adminPage'))


if __name__ == "__main__":
    app.run(debug=True)
