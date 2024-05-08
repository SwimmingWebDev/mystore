from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from .models import Item, Category
from pathlib import Path
import secrets

@app.route('/')
def home():
    products = Item.query.all()
    categories = Category.query.all()
    return render_template('products/index.html', products = products, categories=categories)


@app.route('/category/<int:id>')
def getcategory(id):
    categories = Category.query.all()
    category_items = Item.query.filter_by(category_id=id)
    return render_template('products/index.html', categories=categories, category_items=category_items)

@app.route('/product/<int:id>')
def itemdetails(id):
    product = Item.query.get_or_404(id)
    categories = Category.query.all()
    return render_template('products/item-details.html', product=product, categories=categories)

@app.route('/additem', methods=['GET', 'POST'])
def additem():
    if 'email' not in session:
        flash(f'Pleas login first')
        return redirect(url_for('login'))
    
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
    if 'email' not in session:
        flash(f'Pleas login first')
        return redirect(url_for('login'))
    
    if request.method=='POST':
        getCategory = request.form.get('category')
        category = Category(name=getCategory)
        db.session.add(category)
        db.session.commit()
        flash(f'The category {getCategory} was added to your database')
        return redirect(url_for('addcategory'))
    
    return render_template('products/additem.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):
    if 'email' not in session:
        flash(f'Pleas login first')
        return redirect(url_for('login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecategory.name = category
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('products/updatecat.html', updatecategory=updatecategory)


@app.route('/updateitem/<int:id>', methods=['GET', 'POST'])
def updateitem(id):
    
    categories = Category.query.all()
    product = Item.query.get_or_404(id)
    
    name = request.form.get('name')
    price = request.form.get('price')
    quantity =request.form.get('quantity')
    description = request.form.get('description')
    category_id = request.form.get('category')
    photo = request.files.get('item-photo')

    if request.method == 'POST':
        product.name = name
        product.price = price
        product.quantity = quantity
        product.description = description
        product.category_id = category_id
        if photo :
            try:
                Path(current_app.root_path, "static", "img", product.photo).unlink()
                product.photo = photos.save(request.files.get('item-photo'), name=secrets.token_hex(10) + ".")
            except:
                product.photo = photos.save(request.files.get('item-photo'), name=secrets.token_hex(10) + ".")

        db.session.commit()

        return redirect(url_for('admin'))
        
    return render_template('products/updateitem.html', categories=categories, product=product)
    

@app.route('/deletecat/<int:id>')
def deletecategory(id):

    category = Category.query.get_or_404(id)

    db.session.delete(category)
    db.session.commit()
    flash(f'The category {category.name} was deleted')
    return redirect(url_for('category'))
    

@app.route('/deleteitem/<int:id>')
def deleteitem(id):

    item = Item.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()
    flash(f'The item {item.name} was deleted')
    return redirect(url_for('admin'))
    


