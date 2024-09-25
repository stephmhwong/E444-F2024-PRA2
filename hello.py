from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap

from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email

app = Flask(__name__)

bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['SECRET_KEY'] = 'hard to guess string'

def contains_utoronto(string):
    def _contains_utoronto(form, field):
        if string not in field.data:
            raise ValidationError(f"The email must be a '{string}' email.")
    return _contains_utoronto

class FullForm(FlaskForm):
    name = StringField('What is your name?', validators = [DataRequired()])
    email = StringField('What is your UofT Email address?', validators = [
                                                                DataRequired(),
                                                                Email(granular_message = True),
                                                                contains_utoronto('utoronto')])
    submit = SubmitField('Submit')

@app.route('/', methods = ['GET', 'POST'])
def index():
    name = None
    form = FullForm()

    if form.validate_on_submit():

        # name form content
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data

        # email form content
        old_email = session.get('email')
        if old_email is not None and old_email != form.email.data:
            flash('Looks like you have changed your email!')
        session['email'] = form.email.data

        return redirect(url_for('index'))

    return render_template('index.html', form = form, name = session.get('name'), email = session.get('email'), current_time = datetime.utcnow())

# @app.route('/user/<name>')
# def user(name):
#     return render_template('user.html', name=name)