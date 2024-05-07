from flask import redirect, render_template, url_for, flash, request
from shop import db, app, photos
from .models import Item, Category
import secrets

@app.route('/additem', methods=['GET', 'POST'])
def additem():
    if request.method=='POST':

        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        description = request.form['description']
        category_id = request.form['category']
        photo = photos.save(request.files['item-photo'], name=secrets.token_hex(10) + ".")

        item = Item(name=name, price=price, quantity=quantity, description=description, category_id=category_id, photo=photo)     

        db.session.add(item)
        db.session.commit()
        flash(f'The item {name} was added to your database')
        return redirect(url_for('additem'))
    
    categories = Category.query.all()
    return render_template('products/additem.html', items='items', categories=categories)

@app.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if request.method=='POST':
        getCategory = request.form.get('category')
        category = Category(name=getCategory)
        db.session.add(category)
        db.session.commit()
        flash(f'The category {getCategory} was added to your database')
        return redirect(url_for('addcategory'))
    
    return render_template('products/additem.html')
                                         