from datetime import datetime
from sqlalchemy import ForeignKey,DECIMAL
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    user_id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_firstname= db.Column(db.String(100),nullable=False)
    user_lastname= db.Column(db.String(100),nullable=False)
    user_email= db.Column(db.String(100),nullable=False,unique=True)
    user_phone= db.Column(db.String(45),unique=True)
    username = db.Column(db.String(45),nullable=False,unique=True)
    user_gender = db.Column(db.Enum('Male', 'Female', name='gender'), nullable=False)
    user_address= db.Column(db.String(255))
    user_state = db.Column(db.String(100))
    user_bio= db.Column(db.String(255))
    user_password= db.Column(db.String(255),nullable=False)
    user_picture= db.Column(db.String(255))
    user_joindate= db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    user_status= db.Column(db.Enum('Active', 'Inactive', name='status'),default='Active',nullable=False)

    
    

class Categories(db.Model):
    cat_id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    cat_name= db.Column(db.String(45),nullable=False)
    cat_description= db.Column(db.String(255),nullable=False)


class Sellers(db.Model):
    seller_id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    seller_user_id= db.Column(db.Integer,db.ForeignKey('user.user_id', ondelete="CASCADE"),nullable=False)
    seller_category_id= db.Column(db.Integer,db.ForeignKey('categories.cat_id', ondelete="CASCADE"),nullable=False)
    seller_reviews= db.Column(db.String(255))
    seller_joined= db.Column(db.DateTime,default=datetime.utcnow,nullable=False)

    category = db.relationship('Categories',backref='sellers', passive_deletes=True)
    seller_detail = db.relationship('User',backref='sellers', passive_deletes=True)    




class Artworks(db.Model):
    art_id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    art_seller_id= db.Column(db.Integer,db.ForeignKey('sellers.seller_id', ondelete="CASCADE"),nullable=False)
    art_description= db.Column(db.String(255),nullable=False)
    art_category_id= db.Column(db.Integer,db.ForeignKey('categories.cat_id', ondelete="CASCADE"),nullable=False)
    art_price= db.Column(db.DECIMAL(10,2))
    art_posted_at= db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    art_quantity= db.Column(db.Integer,default=1)
    art_image= db.Column(db.String(255),nullable=False)

    category = db.relationship('Categories',backref='artworks', passive_deletes=True)
    seller = db.relationship('Sellers',backref='artworks', passive_deletes=True)


class ArtImages(db.Model):
    __tablename__ = 'art_images'
    img_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    image_url = db.Column(db.String(255), nullable=False) 
    img_art_id = db.Column(db.Integer, db.ForeignKey('artworks.art_id', ondelete="CASCADE"), nullable=False)


class Favorites(db.Model):
    fav_id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    fav_user_id= db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
    fav_artwork_id= db.Column(db.Integer,db.ForeignKey('artworks.art_id'),nullable=False)


class Orders(db.Model):
    order_id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    order_user_id= db.Column(db.Integer,db.ForeignKey('user.user_id', ondelete="CASCADE"),nullable=False)
    order_time= db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    order_status= db.Column(db.Enum('pending', 'completed', 'failed', name='order_status'),default='pending',nullable=False)
    order_total_price= db.Column(db.Float,nullable=False)
    order_reference= db.Column(db.String(255),nullable=False,unique=True)
    order_address= db.Column(db.String(255),nullable=False)

    user = db.relationship('User', backref='orders', passive_deletes=True)



class OrderDetails(db.Model):
    __tablename__ = 'order_details'
    	
    order_details_id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    order_detail_order_id= db.Column(db.Integer,db.ForeignKey('orders.order_id', ondelete="CASCADE"),nullable=False)
    order_art_id= db.Column(db.Integer,db.ForeignKey('artworks.art_id', ondelete="CASCADE"),nullable=False)
    order_art_price= db.Column(db.Float,nullable=False)
    order_quantity= db.Column(db.Integer,nullable=True)

    order = db.relationship('Orders', backref='order_details', passive_deletes=True)
    artwork = db.relationship('Artworks', backref='order_details', passive_deletes=True)
	

class Payment(db.Model):
    __tablename__ = 'payment_details'
    						
    pay_id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    payment_order_id= db.Column(db.Integer,db.ForeignKey('orders.order_id', ondelete="CASCADE"),nullable=False)
    payment_method= db.Column(db.String(45))
    transaction_id= db.Column(db.String(255))
    payment_amount= db.Column(db.Float, nullable=False)
    payment_status= db.Column(db.Enum('pending', 'completed','failed'),default='pending',nullable=False)
    payment_date= db.Column(db.DateTime,default=datetime.utcnow,nullable=False)
    
    orders = db.relationship('Orders', backref='payment_details', passive_deletes=True)	


class Reviews(db.Model):
    
    review_id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    rev_buyer_id= db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
    rev_seller_id= db.Column(db.Integer,db.ForeignKey('sellers.seller_id'),nullable=False)
    review= db.Column(db.String(255))
    review_time= db.Column(db.DateTime,default=datetime.utcnow)	


class Messages(db.Model):
    				
    message_id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    mssg_user_id= db.Column(db.Integer,db.ForeignKey('user.user_id'),nullable=False)
    mssg_seller_id= db.Column(db.Integer,db.ForeignKey('sellers.seller_id'),nullable=False)
    mssg_text= db.Column(db.Text,nullable=False)
    mssg_time_sent= db.Column(db.DateTime,default=datetime.utcnow,nullable=False)	


class Admin(db.Model):
    admin_id= db.Column(db.Integer,primary_key=True,autoincrement=True)
    admin_user= db.Column(db.String(45),nullable=False)
    admin_password= db.Column(db.String(255),nullable=False)	