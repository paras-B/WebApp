from flask import Flask, render_template, url_for, flash
from werkzeug.utils import redirect
import os
import smtplib
from flask_mail import Mail, Message
from shreya_blog.forms import QueryForm
from shreya_blog import app
import smtplib
from email.message import EmailMessage
import json
from threading import Thread


def send_async_email(app, msg):
    with open('/home/paras/Desktop/shreya_bhatia/config.json') as config_file:
        config = json.load(config_file)
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.login('1usernameismine@gmail.com', config.get('USER_PW'))
    with app.app_context():
        mailserver.send_message(msg)
        mailserver.quit()


# Adding mailserver
def mailFunction(body):
    msg = EmailMessage()
    msg['Subject'] = "New Query Recieved"
    msg.set_content(body)
    msg['From'] = '1usernameismine2gmail.com'
    msg['To'] = 'parasbhatia999@gmail.com'
    # mailserver.send_message(msg)
    # mailserver.quit()
    Thread(target=send_async_email, args=(app, msg)).start()


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/great')
def say_hello():
    return render_template("index.html")


@app.route("/home")
def home_page():
    return render_template("home.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact_page():
    form = QueryForm()
    if form.validate_on_submit():
        data = {'firstname': form.firstname.data, 'lastname': form.lastname.data,
                'phone': form.phone.data, 'message': form.message.data}
        flash('Message sent. I will contact you as soon as possible.', 'success')
        """trying flaskmail 
        """
        text = """New query received 
                    Name: {0}, {1}
                    phone: {2} 
                    Email: {3}
                    message: {4} """.format(form.firstname.data, form.lastname.data,
                                            form.phone.data,
                                            form.email.data, form.message.data)
        mailFunction(text)
        return redirect(url_for('query_sent'))
    return render_template("contactform.html", form=form)


@app.route("/sent")
def query_sent():
    return render_template("sentpage.html")


@app.errorhandler(404)
def not_found_error(error):
    return render_template("404.html")


@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html")
