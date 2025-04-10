from flask import Flask,render_template,redirect,request,session,url_for,flash
from package import app
from package.forms import PublicDetailForm,PrivateDetailForm,PasswordChange,SellersForm,CreatePost
from package.models import User,Sellers,db,Categories,Artworks,Orders,OrderDetails,Payment

@app.before_request
def ensure_sessions_exists():
    if 'cart' not in session:
        session['cart'] = []
    if 'isloggedin' not in session:
        session['isloggedin'] = None

@app.after_request
def after_request(response):
    response.headers['Cache-Control']='no-cache,no-store,must-revalidate'
    return response

@app.errorhandler(404)
def error_404(error):
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None

    return render_template('404.html',error=error,loggedin=loggedin)


@app.errorhandler(500)
def error_500(error):
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None

    return render_template('500.html',error=error,loggedin=loggedin)


@app.errorhandler(503)
def error_503(error):
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None

    return render_template('503.html',error=error,loggedin=loggedin)


@app.route('/see-art/')
def index():
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None
    # artworks = Artworks.query.all()
    sellers = Sellers.query.all()
    categories = Categories.query.all()

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 4, type=int)
    pagination = db.paginate(db.select(Artworks).order_by(Artworks.art_posted_at), page=page, per_page=per_page, error_out=False)
    artworks = pagination.items if pagination.items else []
    total_pages = pagination.pages if pagination.pages else 0

    return render_template('index.html',loggedin=loggedin,artworks=artworks,sellers=sellers,categories=categories,total_pages=total_pages,page=page)


@app.route('/see-art/about/')
def about():
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None


    return render_template('about.html',loggedin=loggedin)

   

@app.route('/see-art/upload/product/<int:id>/', methods=['GET', 'POST'])
def create_post(id):
    cp = CreatePost()
    userid = session.get('isloggedin')
    loggedin = User.query.get(userid) if userid else None

    if not loggedin:
        return redirect(url_for('login'))

    seller = Sellers.query.filter_by(seller_id=id).first()
    seller_cat = db.session.query(Sellers).get(seller.seller_id) if seller else None

    cat_sellers = Categories.query.filter_by(cat_id=seller.seller_category_id).first()
    seller_deets = User.query.all()

    return render_template('create_post.html',loggedin=loggedin,cp=cp,seller=seller,seller_cat=seller_cat,cat_sellers=cat_sellers,seller_deets=seller_deets)
   


    

@app.route('/see-art/profile/')
def profile():
    rs = SellersForm()
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
        
    else:
        loggedin = None
    if loggedin == None:
        return redirect(url_for('login'))
    
    if loggedin:
        seller = Sellers.query.filter_by(seller_user_id=loggedin.user_id).first()
        seller_cat = None
    
    artworks = None
    seller_cat = None
    cat_sellers = None
    pending_deliveries = []
    placed_orders = []

    if seller:
        seller_cat = db.session.query(Sellers).get(seller.seller_id)
        cat_sellers = db.session.query(Categories).filter_by(cat_id=seller_cat.category.cat_id).first()
        artworks = db.session.query(Artworks).filter_by(art_seller_id=seller.seller_id).first()
        pending_deliveries = db.session.query(Orders).filter(Orders.order_user_id!=loggedin.user_id,Orders.order_id==Payment.payment_order_id,Orders.order_status=='pending',OrderDetails.order_art_id==Artworks.art_id,Artworks.art_seller_id==seller.seller_id,Payment.payment_status=='completed').all()
    # artworks = db.session.query(Artworks).filter_by(art_seller_id=seller.seller_id).all()
    placed_orders = db.session.query(Orders).filter(Orders.order_user_id==loggedin.user_id,Orders.order_id==Payment.payment_order_id,Payment.payment_status=='completed').all()

    return render_template('profile.html',loggedin=loggedin,rs=rs,seller=seller,seller_cat=seller_cat,artworks=artworks,cat_sellers=cat_sellers,pending_deliveries=pending_deliveries,placed_orders=placed_orders)

@app.route('/see-art/edit/',methods=['POST','GET'])
def settings():
    pd = PublicDetailForm()
    prd = PrivateDetailForm()
    pc = PasswordChange()
    userid = session.get('isloggedin')

    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None
    if loggedin == None:
        return redirect(url_for('login'))
    
    
    return render_template('settings.html',pd=pd,prd=prd,pc=pc,loggedin=loggedin)


@app.route('/pending/deliveries/')
def pending_deliveries():
    userid = session.get('isloggedin')

    if userid:
        loggedin = User.query.get(userid)
        seller = Sellers.query.filter_by(seller_user_id=loggedin.user_id).first()
    else:
        loggedin = None
    if loggedin == None:
        return redirect(url_for('login'))
    if not seller:
        return redirect(url_for('profile'))
    
    pending_deliveries = db.session.query(Orders).filter(Orders.order_user_id!=loggedin.user_id,Orders.order_id==Payment.payment_order_id,Orders.order_status=='pending',OrderDetails.order_art_id==Artworks.art_id,Artworks.art_seller_id==seller.seller_id,Payment.payment_status=='completed').all()

    if not pending_deliveries:
        flash('No pending deliveries',category='failed')
        return redirect(url_for('profile'))
    
    return render_template('orders/pending_deliveries.html',loggedin=loggedin,pending_deliveries=pending_deliveries,seller=seller)


@app.route('/my/orders/')
def personal_orders():
    userid = session.get('isloggedin')

    if userid:
        loggedin = User.query.get(userid)
        seller = Sellers.query.filter_by(seller_user_id=loggedin.user_id).first()
    else:
        loggedin = None
    if loggedin == None:
        return redirect(url_for('login'))
    
    order_details_list =[]
    sellers_list =[]
    art_cat = []
    orderdetails = db.session.query(OrderDetails).all()
    for order in orderdetails:
        order_details_list.append(order.order_art_id)
    sellers = db.session.query(Artworks).filter(Artworks.art_id.in_(order_details_list)).all()
    for sell in sellers:
        sellers_list.append(sell.art_seller_id)
    categories = db.session.query(Categories).all()
    for cat in categories:
        art_cat.append(cat.cat_id)
    artseller = db.session.query(Sellers).filter(Sellers.seller_id.in_(sellers_list),Sellers.seller_category_id.in_(art_cat)).all()
    placed_orders = db.session.query(Orders).filter(Orders.order_user_id==loggedin.user_id,Orders.order_id==Payment.payment_order_id,Payment.payment_status=='completed').all()
    
    return render_template('orders/my_orders.html',loggedin=loggedin,placed_orders=placed_orders,seller=seller,artseller=artseller)



@app.route('/test/other/sellers/')
def test_template():
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
        seller = Sellers.query.filter_by(seller_user_id=loggedin.user_id).first()
    else:
        loggedin = None
    seller_deets = db.session.query(User).all()
    artworks = db.session.query(Artworks).all()
    # items = db.paginate(db.select(Artworks).order_by(Artworks.art_posted_at),page=1,per_page=5)
    # items = db.paginate(db.select(Artworks).order_by(Artworks.art_posted_at),page=1,per_page=5)
    # items = db.session.query(Artworks).all()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 4, type=int)
    pagination = db.paginate(db.select(Artworks).order_by(Artworks.art_posted_at), page=page, per_page=per_page, error_out=False)
    items = pagination.items if pagination.items else []
    total_pages = pagination.pages if pagination.pages else 0
    

    return render_template('test_template.html',seller_deets=seller_deets,artworks=artworks,loggedin=loggedin,seller=seller,items=items,total_pages=total_pages,page=page)


