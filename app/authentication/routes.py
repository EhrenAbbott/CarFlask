from forms import UserLoginForm
from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash

from flask_login import login_user, logout_user, LoginManager, current_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email, password)

            user = User(email, password = password)

            db.session.add(user)
            db.session.commit()



            flash(f'You have made a new account {email}', 'User-created')
            return redirect(url_for('site.home'))
    except:
        raise Exception('Form data is not valid: Please revise')
    return render_template('sign_up.html', form=form)

@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
    
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                flash("Congrats, you're in! Welcome!", "auth-sucess")
                return redirect(url_for('site.profile'))
            else:
                flash('Sorry, you were unable to successfully access this content', 'auth-failed')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Form data is not valid: Please revise')
    return render_template('sign_in.html', form=form)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('site.home'))