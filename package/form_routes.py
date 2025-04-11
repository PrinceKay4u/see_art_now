import secrets
from flask import Flask,render_template,redirect,request,session,flash,url_for,make_response
from werkzeug.security import generate_password_hash,check_password_hash
from package import app,mail
from package.forms import RegisterForm,LoginForm,ContactForm,PublicDetailForm,PrivateDetailForm,PasswordChange,SellersForm,CreatePost,EditPost
from package.models import db,User,Sellers,Categories,Artworks
from flask_mail import Message

@app.route('/see-art/login/',methods=['POST','GET'])
def login():
    loginform = LoginForm()
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None
    if loggedin:
        return redirect(url_for('index'))   
    
    if loginform.validate_on_submit():
        details = db.session.query(User).filter(User.user_email==loginform.email.data).first()
        if details:
            saved_password = details.user_password
            check = check_password_hash(saved_password,loginform.password.data)
            if check:
                session['isloggedin'] = details.user_id
                return redirect('/see-art/profile/')
            else:
                flash('Your password is incorrect',category='failed')
                return redirect(url_for('login'))
        else:
            flash('This email is not registered yet',category='failed')
            return redirect(url_for('login'))
    return render_template('login.html',loginform=loginform,loggedin=loggedin)


@app.route('/checkusername/',methods=['POST'])
def check_username():
    username = request.form.get('username')
    check_user = User.query.filter(User.username==username).first()
    if username == '':
        return f'<span class="text-danger fw-bold">Username cannot be empty</span>'
    if check_user:
        return f'<span class="text-danger fw-bold">Username is taken</span>'
    else:
        return '<span class="text-success fw-bold">Username is available</span>'

@app.route('/see-art/register/',methods=['POST','GET'])
def register():
    registerform = RegisterForm()
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None
    if loggedin:
        return redirect(url_for('index'))
    
    if registerform.validate_on_submit():
        firstname = registerform.firstname.data
        lastname = registerform.lastname.data
        email = registerform.email.data
        gender = registerform.gender.data
        phone = registerform.phone.data
        username = registerform.username.data
        password = registerform.password.data

       
        check_user = User.query.filter(User.username==username).first()
        if check_user:
            save = make_response(redirect(url_for('register')))
            save.set_cookie('firstname',firstname,max_age=120)
            save.set_cookie('lastname',lastname,max_age=120)
            save.set_cookie('email',email,max_age=120)
            save.set_cookie('phone',phone,max_age=120)
            flash('Username taken already, please select another one',category='failed')
            return save

       
        check_user = User.query.filter(User.user_email==email).first()
        if check_user:
            flash('Email already registered, Use Login',category='failed')
            return redirect(url_for('register'))
        
       
        check_phone = User.query.filter(User.user_phone==phone).first()
        if check_phone:
            flash('Phone already registered, if you have an account please use login instead',category='failed')
            return redirect(url_for('register'))


        secure = generate_password_hash(password)
        user = User(user_firstname=firstname,user_lastname=lastname,user_email=email,user_gender=gender,user_phone=phone,username=username,user_password=secure)
        db.session.add(user)
        db.session.commit()
        id = user.user_id
        
        if id:
            msg = Message(subject='Welcome to See Art - Let Your Creativity Shine!',sender=('See Art Now',email),recipients=[email])
            # msg.body = contactform.message.data+f'\n My email is {email}'
            msg.html = f'<html lang="en"> <head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>See Art Now</title> <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.5/dist/css/bootstrap.min.css" type="text/css"> </head> <body> <nav class="navbar navbar-expand-lg bg-body-tertiary"> <div class="container-fluid"> <a href="https://postimg.cc/jwkCvGRP"><img src="https://i.postimg.cc/jwkCvGRP/Screenshot-11-4-2025-95536-127-0-0-1.jpg"/></a> </div> </nav> <div class="container"> <div class="row"> <div class="col-10 offset-1"> <h2 class="text-center">Welcome to See Art Now</h2> <p class="mb-1">Hi {username},</p> <p class="mb-1"> Welcome to See Art - we are so excited to have you on board!</p> <p class="mb-1">Whether you are here to discover unique creations or share your artistic talent with the world, you are in the right place. See Art connects buyers with amazing artists, including painters, potters, embroiderers, interior designers, and more.</p> <p>✨ Here is what you can do:</p> <ul> <li>Explore and purchase one-of-a-kind artworks</li> <li>Hire talented artists for custom pieces</li> <li>Build your own artist profile and showcase your work (if you are an artist!)</li> </ul> <p class="mb-1"> We are here to help you on your creative journey. If you have any questions or need assistance, just hit reply — we would love to hear from you.</p> <p class="mb-1">Happy exploring,</p> <p class="mb-1">The See Art Team</p> <p>[seeartnow.com.ng]</p> </div> </div> </div> </body> </html>'
            mail.send(msg)
            flash('Account registered successfully, please login to continue. Check your email for a message from us, You can check the spam folder if not found',category='success')
            return redirect(url_for('login'))
        else:
            flash('an error occured, please try again',category='failed')
            return redirect(url_for('register'))
    return render_template('register.html',registerform=registerform)

@app.route('/see-art/contact-us/',methods=['GET','POST'])
def contact():
    contactform = ContactForm()
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None

    if contactform.validate_on_submit():
        email = 'amonymous@domain.com'
        if contactform.email.data:
            email = contactform.email.data
        msg = Message(subject='Feedback From See Art',sender=('See Art Now',email),recipients=['seeartnow.com.ng@gmail.com'])
        msg.body = contactform.message.data+f'\n My email is {email}'
        mail.send(msg)
        flash('Feedback Recieved successfully, Thank You For Reaching out to Us',category='success')
        return redirect('/see-art/contact-us/')
    return render_template('contact.html',contactform=contactform,loggedin=loggedin)

@app.route('/see-art/edit/<int:id>/public/',methods=['GET','POST'])
def public_details(id):
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
    
    if pd.validate_on_submit():
        update = User.query.get(id)
        username = pd.username.data
        bio = pd.bio.data
        picture = pd.upload.data
        if picture:
            filename = picture.filename
            split = filename.split('.')
            ext = split[-1]
            generated = secrets.token_hex(20)+'.'+ext
       
        db.session.commit()
        
        check_update = db.session.query(User).filter(User.username == username,User.user_id != id).first()
        if not update:
            flash('Username not found',category='success')
            return redirect('login')
        
        if check_update:
            flash('Username already in use', category='failed')
            return redirect(url_for('settings'))
        
        if username == update.username and bio != update.user_bio or picture != update.user_picture:            
            update.username = username
            update.user_bio = bio
            if picture:
                if generated.endswith('.jpg') or generated.endswith('.png') or generated.endswith('.jpeg'):
                    picture.save('package/static/uploads/'+generated)
                update.user_picture = generated
            db.session.commit()
            flash('Profile Updated successfully',category='success')
            return redirect(url_for('settings'))
        else:
            flash('No changes were made',category='success')
            return redirect(url_for('settings'))
    else:
        flash('Username must be up to 4 Characters, Please Try again',category='failed')
        return redirect(url_for('settings'))

@app.route('/see-art/edit/<int:id>/private/',methods=['GET','POST']) 
def private_details(id):
    prd = PrivateDetailForm()
    pd = PublicDetailForm()
    pc = PasswordChange()
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None

    if loggedin == None:
        return redirect(url_for('login'))

    if prd.validate_on_submit():
        firstname = prd.firstname.data
        lastname = prd.firstname.data
        email = prd.firstname.data
        update = db.session.query(User).get(id)
        update.user_firstname = firstname
        update.user_lastname = lastname
        update.user_email = email
        db.session.commit()
        flash('Details updated successfully',category='success')
        return redirect(url_for('settings'))
    flash('Failed, make sure no field is empty',category='failed')
    return redirect(url_for('settings'))

@app.route('/see-art/edit/<int:id>/password/',methods=['GET','POST'])
def password_change(id):
    prd = PrivateDetailForm()
    pd = PublicDetailForm()
    pc = PasswordChange()
    userid = session.get('isloggedin')
    if userid:
        loggedin = User.query.get(userid)
    else:
        loggedin = None

    if loggedin == None:
        return redirect(url_for('login'))

    if pc.validate_on_submit():
        password1 = pc.password.data
        password2 = pc.confirm_password.data
        update = db.session.query(User).filter(User.user_id==id).first()
        if update:
            password = update.user_password
            check = check_password_hash(password,password1)
            if check:
                safe = generate_password_hash(password2)
                update.user_password = safe
                db.session.commit()
                flash('Password updated successfully',category='success')
                return redirect(url_for('settings'))
            else:
                flash('Old password incorrect, please try again',category='failed')
                return redirect(url_for('settings'))
    flash('Password update failed, Please Try again',category='failed')
    return redirect(url_for('settings'))

@app.route('/logout/')
def logout():
    if session.get('isloggedin') != None:
        session.pop('isloggedin',None)
    return redirect(url_for('login'))



@app.route('/register/seller/<int:id>/',methods=['POST'])
def register_seller(id):
    rs = SellersForm()
    if rs.validate_on_submit():
        category = rs.category.data
        state = rs.state.data

        seller = Sellers(seller_user_id = id,seller_category_id=category)
        user = User.query.get(id)  

        if user:
            user.user_state = state
        else:
            flash('Please register an account to become a seller',category='failed')
            return redirect('register')
        

        db.session.add_all([seller,user])
        db.session.commit()
        flash('Registered as seller successfuly',category='success')
        return redirect(url_for('profile'))
    # return 'failed'
    flash('something happened, please try again',category='failed')
    return redirect(url_for('profile'))


@app.route('/see-art/upload/post/<int:id>/', methods=['POST'])
def upload_post(id):
    cp = CreatePost()
    userid = session.get('isloggedin')
    loggedin = User.query.get(userid) if userid else None
    

    if not loggedin:
        return redirect(url_for('login'))

    seller = Sellers.query.filter_by(seller_id=id).first()
    if not seller:
        flash('Seller not found', category='failed')
        return redirect(url_for('profile'))
    
    if cp.validate_on_submit():
        description = cp.description.data
        price = cp.price.data
        try:
            price = int(cp.price.data) 
        except ValueError:
            flash("Price must be a valid number.", category='failed')
            return redirect(url_for('create_post', id=seller.seller_id))

        image = cp.image.data  
        cat_id = seller.seller_category_id
        seller_id = seller.seller_id

        if not image:
            flash('invalid image',category='failed')
            return redirect(url_for('create_post', id=seller_id))
        if description == '':
            flash('Please fill all fields',category='failed')
            return redirect(url_for('create_post', id=seller_id))

        filename = image.filename
        
        extention = filename.split('.')
        ext = extention[-1]
        generated = secrets.token_hex(20)+'.'+ext
        image.save('package/static/uploads/'+generated)
        artwork = Artworks(art_image=generated,art_description=description,art_price=price,art_category_id=cat_id,art_seller_id=seller_id)
        db.session.add(artwork)
        db.session.commit()

        flash("Post created successfully!", category='success')
        return redirect(url_for('profile')) 
    else:
        flash('An error occurred. Please try again.', category='failed')
        return redirect(url_for('create_post', id=seller_id))

@app.route('/edit/post/<int:id>/', methods=['POST','GET'])
def edit_post(id):
    ep = EditPost()
    userid = session.get('isloggedin')
    loggedin = User.query.get(userid) if userid else None
    seller = Sellers.query.filter_by(seller_user_id=userid).first()
    seller_cat = db.session.query(Sellers).get(seller.seller_id) if seller else None

    
    artwork = Artworks.query.filter_by(art_id=id).first()
    if not loggedin:
        return redirect(url_for('login'))
    
    if not seller:
        flash('Seller not found', category='failed')
        return redirect(url_for('profile'))
    
    if request.method == 'GET':
       
        ep.description.data = artwork.art_description
        ep.price.data = int(artwork.art_price)
    
    if ep.validate_on_submit():
        description = ep.description.data
        price = ep.price.data
        try:
            price = int(price) 
        except ValueError:
            flash("Price must be a valid number.", category='failed')
            return redirect(url_for('edit_post', id=artwork.art_id))

        cat_id = seller.seller_category_id
        seller_id = seller.seller_id
        
        if description == '':
            flash('Please fill all fields',category='failed')
            return redirect(url_for('edit_post', id=artwork.art_id))

        
        artwork.art_description = description
        artwork.art_price = price
        db.session.add(artwork)
        db.session.commit()

        flash("Post updated successfully!", category='success')
        return redirect(url_for('profile')) 
    
    return render_template(
    'edit_post.html',
    loggedin=loggedin,
    ep=ep,
    seller=seller,
    seller_cat=seller_cat,
)

@app.route('/delete/post/<int:id>/', methods=['POST','GET'])
def delete_post(id):
    userid = session.get('isloggedin')
    loggedin = User.query.get(userid) if userid else None
    seller = Sellers.query.filter_by(seller_user_id=userid).first()

    artwork = Artworks.query.filter_by(art_id=id).first()
    
    if not loggedin:
        return redirect(url_for('login'))
    
    if not seller:
        flash('You are not a seller', category='failed')
        return redirect(url_for('profile'))
    
    db.session.delete(artwork)
    db.session.commit()
    return redirect(url_for('profile'))

   
    
    