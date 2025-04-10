from flask import Flask,render_template,redirect,request,session,url_for,flash
from werkzeug.security import check_password_hash
from package import app
from package.forms import AdminLoginForm
from package.models import User,Sellers,db,Categories,Artworks,Admin,Orders,OrderDetails,Payment


@app.route('/see-art/admin/login/',methods=['GET','POST'])
def admin_login():
    adminform = AdminLoginForm()
    adminid = session.get('adminloggedin')
    if adminid:
        adminavailable = Admin.query.get(adminid)
    else:
        adminavailable = None
    if adminavailable:
        return redirect(url_for('admin_dashboard'))
    
    if adminform.validate_on_submit():
        details = db.session.query(Admin).filter(Admin.admin_user==adminform.username.data).first()
        if details:
            saved_password = details.admin_password
            check = check_password_hash(saved_password,adminform.password.data)
            if check:
                session['adminloggedin'] = details.admin_id
                flash('Login successful',category='success')
                return redirect('/see-art/admin/')
            else:
                flash('Invalid password',category='failed')
                return redirect(url_for('admin_login'))
        else:
            flash('This is not an admin username',category='failed')
            return redirect(url_for('admin_login'))
        
    return render_template('admin/admin_login.html', adminform=adminform)

@app.route('/see-art/admin/logout/')
def admin_logout():
    session.pop('adminloggedin', None)
    return redirect(url_for('admin_login'))


@app.route('/see-art/admin/')
def admin_dashboard():
    adminid = session.get('adminloggedin')
    if adminid:
        adminavailable = Admin.query.get(adminid)
    else:
        adminavailable = None
    
    if adminavailable == None:
        flash('You are not logged in',category='failed')
        return redirect(url_for('admin_login'))
    
    users = User.query.all()
    sellers = Sellers.query.all()
    categories = Categories.query.all()
    artworks = Artworks.query.all()
    orders = Orders.query.all()
    orderdetails = OrderDetails.query.all()
    payments = Payment.query.all()
    return render_template('admin/index.html', users=users, sellers=sellers, categories=categories, artworks=artworks,adminavailable=adminavailable,orders=orders,orderdetails=orderdetails,payments=payments)

@app.route('/see-art/admin/users/')
def admin_users():
    adminid = session.get('adminloggedin')
    if adminid:
        adminavailable = Admin.query.get(adminid)
    else:
        adminavailable = None
    
    if adminavailable == None:
        flash('You are not logged in',category='failed')
        return redirect(url_for('admin_login'))
    users = User.query.all()
    return render_template('admin/users.html', users=users,adminavailable=adminavailable)

@app.route('/see-art/admin/sellers/')
def admin_sellers():
    adminid = session.get('adminloggedin')
    if adminid:
        adminavailable = Admin.query.get(adminid)
    else:
        adminavailable = None
    
    if adminavailable == None:
        flash('You are not logged in',category='failed')
        return redirect(url_for('admin_login'))
    
    sellers = Sellers.query.all()
    return render_template('admin/sellers.html', sellers=sellers,adminavailable=adminavailable)

@app.route('/see-art/admin/products/')
def admin_products():
    adminid = session.get('adminloggedin')
    if adminid:
        adminavailable = Admin.query.get(adminid)
    else:
        adminavailable = None
    
    if adminavailable == None:
        flash('You are not logged in',category='failed')
        return redirect(url_for('admin_login'))
    
    artworks = Artworks.query.all()
    return render_template('admin/products.html',artworks=artworks,adminavailable=adminavailable)

@app.route('/see-art/admin/categories/')
def admin_categories():
    adminid = session.get('adminloggedin')
    if adminid:
        adminavailable = Admin.query.get(adminid)
    else:
        adminavailable = None
    
    if adminavailable == None:
        flash('You are not logged in',category='failed')
        return redirect(url_for('admin_login'))
    
    categories = Categories.query.all()
    return render_template('admin/categories.html', categories=categories,adminavailable=adminavailable)

@app.route('/see-art/admin/orders/')
def admin_orders():
    adminid = session.get('adminloggedin')
    if adminid:
        adminavailable = Admin.query.get(adminid)
    else:
        adminavailable = None
    
    if adminavailable == None:
        flash('You are not logged in',category='failed')
        return redirect(url_for('admin_login'))
    
    orders = Orders.query.all()
    orderdetails = OrderDetails.query.all()
    payments = Payment.query.all()
    
    return render_template('admin/orders.html',adminavailable=adminavailable,orders=orders,orderdetails=orderdetails,payments=payments)

@app.route('/ban/<int:user_id>/')
def ban_user(user_id):
    adminid = session.get('adminloggedin')
    if adminid:
        adminavailable = Admin.query.get(adminid)
    else:
        adminavailable = None
    
    if adminavailable == None:
        flash('You are not logged in',category='failed')
        return redirect(url_for('admin_login'))
    
    user = User.query.get(user_id)
    if user:
        user.user_status = 'Inactive'
        db.session.add(user)
        db.session.commit()
        flash('User banned successfully',category='success')
    else:
        flash('User banned or incorrect user id',category='failed')
    
    return redirect(url_for('admin_users'))

@app.route('/unban/<int:user_id>/')
def unban_user(user_id):
    adminid = session.get('adminloggedin')
    if adminid:
        adminavailable = Admin.query.get(adminid)
    else:
        adminavailable = None
    
    if adminavailable == None:
        flash('You are not logged in',category='failed')
        return redirect(url_for('admin_login'))
    
    user = User.query.get(user_id)
    if user:
        user.user_status = 'Active'
        db.session.add(user)
        db.session.commit()
        flash('User unbanned successfully',category='success')
    else:
        flash('User not banned or incorrect user id',category='failed')
    
    return redirect(url_for('admin_users'))

@app.route('/delete/<int:user_id>/')
def delete_user(user_id):
    adminid = session.get('adminloggedin')
    if adminid:
        adminavailable = Admin.query.get(adminid)
    else:
        adminavailable = None
    
    if adminavailable == None:
        flash('You are not logged in',category='failed')
        return redirect(url_for('admin_login'))
    
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully',category='success')
    else:
        flash('User not found',category='failed')
    
    return redirect(url_for('admin_users'))
