from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap
from datetime import date
import smtplib
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('MY_SECRET_KEY')
Bootstrap(app)


class ContactForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Email")


@app.context_processor
def inject_year():
    return {"year": date.today().year}


@app.route('/', methods=["GET", "POST"])
def home():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():

        email_message = f'Subject: New Message from Jackie\'s Blog\n\n' \
                        f'Name: {contact_form.name.data}\n' \
                        f'Email: {contact_form.email.data}\n' \
                        f'Message: {contact_form.message.data}\n'

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(os.getenv('EMAIL'), os.getenv('EMAIL_PASSWORD'))
            connection.sendmail(from_addr=os.getenv('EMAIL'),
                                to_addrs=os.getenv('MY_EMAIL'),
                                msg=email_message.encode("utf-8")
                                )
        return redirect(url_for("home"))
    return render_template("index.html", form=contact_form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
