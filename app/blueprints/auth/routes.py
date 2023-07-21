from flask import render_template, flash, redirect, request, url_for
from app.forms import SignUpForm, LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from . import bp as auth




@auth.route('/sign-in', methods=['GET','POST'])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        email = login_form.email.data
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(login_form.password.data):
            login_user(user)
            flash(f'{login_form.email.data} logged in successfully', category='success')
            return redirect(url_for('main.home'))
        else:
            flash('Incorrect login information', category='danger')
            
    return render_template('signin.jinja', title='Fakebook Sign In', form = login_form)

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    sign_up_form = SignUpForm()
    if sign_up_form.validate_on_submit():
        user_dict = {
            'email' : sign_up_form.email.data,
            'username' : sign_up_form.username.data,
            'first_name' : sign_up_form.first_name.data,
            'last_name' : sign_up_form.last_name.data,
        }
        try:
            user = User()
            user.from_dict(user_dict)
            user.hash_password(sign_up_form.password.data)
            user.commit()
            login_user(user)
            flash(f'{user.first_name if user.first_name else user.email} logged in successfully', category='success')
            return redirect(url_for('main.home'))
        except:
            flash(f'Email already taken, please try again', category='warning')
    elif request.method == 'POST':
        flash('Incorrect sign up information', category='danger')
        print(sign_up_form)
    return render_template('signup.jinja', title='Fakebook Sign Up', form = sign_up_form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))