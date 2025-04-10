import secrets,requests,json
from flask import Flask,render_template,redirect,request,session,url_for,flash,jsonify
from package import app
from package.forms import PublicDetailForm,PrivateDetailForm,PasswordChange
from package.models import User,Sellers,db,Categories,Artworks,Orders,Payment,OrderDetails


def get_order_amt(id):
    query = Artworks.query.get(id)
    if query:
        return query.art_price
    else:
        return 0



@app.route('/see-art/collections/')
def collections():
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None
    artworks = Artworks.query.all()
    sellers = Sellers.query.all()
    categories = Categories.query.all()
    return render_template('collections/collections.html',loggedin=loggedin,artworks=artworks,sellers=sellers,categories=categories)

@app.route('/see-art/embroideries/')
def embroideries():
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None
    artworks = Artworks.query.all()
    sellers = Sellers.query.all()
    categories = Categories.query.all()
    return render_template('collections/embroid.html',loggedin=loggedin,artworks=artworks,sellers=sellers,categories=categories)

@app.route('/see-art/interiors/')
def interiors():
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None
    artworks = Artworks.query.all()
    sellers = Sellers.query.all()
    categories = Categories.query.all()
    return render_template('collections/interior.html',loggedin=loggedin,artworks=artworks,sellers=sellers,categories=categories)

@app.route('/see-art/paintings/')
def paintings():
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None
    artworks = Artworks.query.all()
    sellers = Sellers.query.all()
    categories = Categories.query.all()
    return render_template('collections/painting.html',loggedin=loggedin,artworks=artworks,sellers=sellers,categories=categories)

@app.route('/see-art/sculptures/')
def sculptures():
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None
    artworks = Artworks.query.all()
    sellers = Sellers.query.all()
    categories = Categories.query.all()
    return render_template('collections/sculpt.html',loggedin=loggedin,artworks=artworks,sellers=sellers,categories=categories)

@app.route('/see-art/sketches/')
def sketches():
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None
    artworks = Artworks.query.all()
    sellers = Sellers.query.all()
    categories = Categories.query.all()
    return render_template('collections/sketch.html',loggedin=loggedin,artworks=artworks,sellers=sellers,categories=categories)

@app.route('/product/details/<int:id>/')
def item_details(id):
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None
    artworks = Artworks.query.filter_by(art_id=id).first()
    sellers = Sellers.query.filter_by(seller_id=artworks.art_seller_id).first()
    categories = Categories.query.filter_by(cat_id=artworks.art_category_id).first()
    user = User.query.filter_by(user_id=sellers.seller_user_id).first()
    if not artworks:
        return redirect(url_for('collections'))
    return render_template('collections/item_details.html',loggedin=loggedin,artworks=artworks,sellers=sellers,categories=categories,user=user)


@app.route('/add-to-cart/<int:art_id>',methods=['POST'])
def add_to_cart(art_id):
    cart = session.get('cart', [])

    if art_id not in cart:
        cart.append(art_id)
        session['cart'] = cart
        return f"Added to cart! items in cart: {len(cart)}"
    else:
        return "Item already in cart!"


# @app.route('/add-to-carts/', methods=['POST'])
# def add_to_carts():
#     data = request.get_json()  
#     art_id = data.get('art_id') 

#     if not art_id:
#         return jsonify({'message': 'No artwork ID received'}), 400

#     cart = session.get('cart', [])
    
#     # Avoid duplicates (optional)
#     if art_id not in cart:
#         cart.append(art_id)
#         session['cart'] = cart

#     return jsonify({
#         'message': 'Artwork added to cart!',
#         'Items in cart': len(cart)
#     })

    
@app.route('/remove-from-cart/<int:art_id>',methods=['POST'])
def remove_from_cart(art_id):
    cart = session.get('cart', [])
    if art_id in cart:
        cart.remove(art_id)
        session['cart'] = cart
        return 'Item removed'
    else:
        return 'Item not in cart'

@app.route('/clear-cart/',methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    return 'Cart cleared!'


@app.route('/cart/',methods=['GET','POST'])
def view_cart():
    cart = session.get('cart', [])
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None
    
    if not cart:
        flash("Your cart is empty!",category='failed')
        return redirect(url_for('collections'))
    cart_items = Artworks.query.filter(Artworks.art_id.in_(cart)).all()
    total = sum(item.art_price for item in cart_items)
    categories = Categories.query.all()
    if request.method == 'GET':
        if session.get('refno') != None:
            session.pop('refno',None)
        if session.get('orderid') != None:
            session.pop('orderid',None)
        if session.get('price') != None:
            session.pop('price',None)
        if session.get('address') != None:
            session.pop('address',None)
        return render_template("collections/cart_items.html", cart_items=cart_items,loggedin=loggedin,total=total,categories=categories)
    else:
        address = request.form.get('address')
        if address != '':
            orders = []
            price = []
            for item in cart_items:
                orders.append(item.art_id)
                price.append(get_order_amt(item.art_id))
                
            session['orderid'] = [order for order in orders]
            session['price'] = [float(p) for p in price]
            session['address'] = address
            ref = secrets.token_hex(10)
            session['refno'] = ref

            orders = Orders(order_user_id=userid,order_total_price=total, order_status='pending',order_reference=session['refno'],order_address=address)
            db.session.add(orders)
            db.session.commit()
            return redirect(url_for('checkout'))
        else:
            flash("Please enter your address!",category='failed')
            return redirect(url_for('view_cart'))


@app.route('/checkout/',methods=['GET','POST'])
def checkout():
    userid = session.get('isloggedin',[])
    orderid = session.get('orderid',[])
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None
    if not orderid:
        flash("No orders found!",category='failed')
        return redirect(url_for('collections'))
    if session.get('refno') == None:
        flash("No reference number found! Select items to checkout",category='failed')
        return redirect(url_for('collections'))
    
    artwork_orders = Artworks.query.filter(Artworks.art_id.in_(orderid)).all() if orderid else []
    orders = Orders.query.filter_by(order_reference=session.get('refno')).first()
    price =[int(price) for price in session.get('price')]
    total = sum(price)
    categories = Categories.query.all()
    address = session.get('address',[])
    
    if request.method == 'POST' and address != None:
        for order in artwork_orders:
            orderdetails = OrderDetails(order_art_id=order.art_id, order_art_price=order.art_price, order_detail_order_id=orders.order_id, order_quantity=1)
            db.session.add(orderdetails)
            db.session.commit()
        return redirect(url_for('initialize_payment'))
    
    return render_template('collections/checkout.html',loggedin=loggedin,artwork_orders=artwork_orders,total=total,categories=categories)


@app.route('/initialize-payment/',methods=['GET','POST'])
def initialize_payment():
    if session.get('refno') != None:
        ref = session.get('refno')
        pay_details = Orders.query.filter_by(order_reference=ref).first()
        amount = pay_details.order_total_price*100
        email = pay_details.user.user_email
        headers = {"Authorization":"Bearer sk_test_3662d517297546bf734773f5e9a9d7028ef63c1a","Content-Type":"application/json"}
        data = {"amount":amount,"email":email,"callback_url":"http://127.0.0.1:5500/paycomplete/","reference":ref}
        response = requests.post("https://api.paystack.co/transaction/initialize",headers=headers,data=json.dumps(data))
        rsp = response.json()
        if rsp['status'] == True:
            payment_url = rsp['data']['authorization_url']
            payment_details = Payment(payment_order_id=pay_details.order_id,payment_method='Paystack',payment_amount=amount)
            db.session.add(payment_details)
            db.session.commit()
            session.pop('cart',None)
            return redirect(payment_url)
        else:
            flash("Payment initialization failed!",category='failed')
            return redirect(url_for('view_cart'))


@app.route('/paycomplete/')
def paysment_verify():
    if session.get('refno') != None:
        ref = session.get('refno')
        headers = {"Authorization":"Bearer sk_test_3662d517297546bf734773f5e9a9d7028ef63c1a","Content-Type":"application/json"}
        response = requests.get(f"https://api.paystack.co/transaction/verify/{ref}",headers=headers)
        rsp = response.json()
        payment_status = 'failed'
        category = 'failed'
        if rsp and rsp.get('status')== True:
            status = rsp['data']['status']
            if status == 'success':
                payment_status = 'completed'
                category = 'success'
        update = db.session.query(Payment).filter(Payment.payment_order_id==Orders.order_id,Orders.order_reference==ref).first()
        update.payment_status = payment_status
        update.transaction_id = ref
        db.session.commit()
        # popping the saved session data incase the user comes back to the page after payment
        if session.get('refno') != None:
            session.pop('refno',None)
        if session.get('orderid') != None:
            session.pop('orderid',None)
        if session.get('price') != None:
            session.pop('price',None)
        if session.get('address') != None:
            session.pop('address',None)


        if payment_status == 'completed':
            flash(f"Payment {payment_status}!",category=category)
        if payment_status == 'failed':
            order = db.session.query(Orders).filter(Orders.order_reference==ref).first()
            order.order_status = 'failed'
            db.session.commit()
            flash("Payment failed! Please try again.",category='failed')
        return redirect(url_for('profile'))
    else:
        return redirect('/confirm/order/') 

@app.route('/test/',methods=['POST'])
def test():
    return 'test id complete'





