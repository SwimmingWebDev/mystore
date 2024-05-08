from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt
from .models import User
from shop.products.models import Item, Category

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Pleas login first')
        return redirect(url_for('login'))
    else:
        products = Item.query.all()
        return render_template('admin/index.html', products = products)
    
@app.route('/category')
def category():
    if 'email' not in session:
        flash(f'Pleas login first')
        return redirect(url_for('login'))
    else:
        categories = Category.query.all()
        return render_template('admin/category.html', categories = categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['email'] = email
            flash(f'Welcome, {email} You are logged in.')
            # login_user(user, remember=remember)
            # return redirect(url_for('home') or url_for('admin')) 
            return redirect(url_for('admin'))
        else:
            flash(f'Please try again.')
            return render_template('admin/login.html')
    else:
        return render_template('admin/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       
        email = request.form.get('email')
        name = request.form.get('name')
        profile = request.form.get('photo')

        hash_password = bcrypt.generate_password_hash(request.form.get('password'))
        
        user = User(email=email, name=name, password=hash_password)

        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {name}, Thank you for registering')
        
        return redirect(url_for('login'))
    else: 
        return render_template('admin/register.html')

