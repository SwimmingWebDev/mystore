from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app, photos
from shop.products.models import Item, Category
from pathlib import Path
import secrets

# Add items to shopping cart
# reference
# https://youtu.be/nBAxuxM9tpw?si=jMr1qwNgsC7-9l4Q

def mergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    else:
        False

@app.route("/addcart", methods=['GET', 'POST'])
def addcart():

    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))
  
    product = Item.query.filter_by(id=product_id).first()

    if product_id and quantity and request.method == "POST":
        cartItems = {product_id:{'name': product.name, 'price': product.price, 'quantity':quantity, 'image':product.photo}}
        
        if 'shoppingcart' in session:
            print(session['shoppingcart'])
            
            if product_id in session['shoppingcart']:
                for key, item in session['shoppingcart'].items():
                    if int(key) == int(product_id):
                        session.modified = True
                        item['quantity'] += quantity

            else:
                session['shoppingcart'] = mergeDicts(session['shoppingcart'], cartItems)
                return redirect(request.referrer)
        
        else:
            session['shoppingcart'] = cartItems
            return redirect(request.referrer)
        

    return redirect(request.referrer)


@app.route('/cart')
def getcart():
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    estimated = 0
    for key, product in session['shoppingcart'].items():
        subtotal += float(product['price'] * int(product['quantity']))
        tax = ("%.2f" % (0.06 * float(subtotal)))
        estimated = float("%.2f" % (1.06 * subtotal))

    return render_template('products/carts.html', tax = tax, estimated = estimated)


@app.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        session.modified = True
        for key, item in session['shoppingcart'].items():
            if int(key) == code:
                item['quantity'] = quantity
                flash(" Item is updated ")
                return redirect(url_for('getcart'))
            
@app.route('/clearcart')
def clearcart():
    session.pop('shoppingcart', None)
    return redirect(url_for('home')) 

@app.route('/delete-cart-item/<int:id>')
def deletecartitem(id):
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect(url_for('home'))

    session.modified = True
    for key, item in session['shoppingcart'].items():
        if int(key) == id:
            session['shoppingcart'].pop(key, None)
            flash(" Item is deleted ")
            return redirect(url_for('getcart'))