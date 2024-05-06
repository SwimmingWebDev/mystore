from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt
from .models import User
from flask_login import login_user
# import os

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Pleas login first')
        return redirect(url_for('login'))
    # products = Addproduct.query.all()
    return render_template('admin/index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['email'] = email
            flash(f'Welcome, {email} You are logged in.')
            # login_user(user, remember=remember)
            return redirect(url_for('home') or url_for('admin')) 
   
        else:
            flash(f'Please try again.')
    else:
        return render_template('admin/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       
        email = request.form.get('email')
        name = request.form.get('name')
        profile = request.form.get('photo')

        hash_password = bcrypt.generate_password_hash(request.form.get('password'))
        
        # user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        # if user: # if a user is found, we want to redirect back to signup page so user can try again
        # flash('Email address already exists')
        # return redirect(url_for('login'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        user = User(email=email, name=name, password=hash_password)

        # add the new user to the database
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {name}, Thank you for registering')
        
        return redirect(url_for('home'))
    else: 
        return render_template('admin/register.html')

