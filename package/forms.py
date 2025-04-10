from flask_wtf import FlaskForm
from wtforms import StringField,EmailField,TextAreaField,PasswordField,SubmitField,RadioField,BooleanField,SelectField
from wtforms.validators import Email,EqualTo,Length,DataRequired
from flask_wtf.file import FileField,FileAllowed,FileRequired


class AdminLoginForm(FlaskForm):
    username = StringField('Enter Your Username',validators=[DataRequired(message='Enter a valid username')])
    password = PasswordField('Enter Your Password',validators=[DataRequired(message='Password cannot be empty')])
    send = SubmitField('Login')


class RegisterForm(FlaskForm):
    firstname = StringField('Enter Your FirstName',validators=[DataRequired(message='Please enter Firstname')])
    lastname = StringField('Enter Your LastName',validators=[DataRequired(message='Please enter Lastname')])
    username = StringField('Pick a Username',validators=[DataRequired(message='Minimum of 4 characters required'),Length(min=4,max=10)])
    phone = StringField('Phone Number',validators=[DataRequired(message='Please enter your phone number'),Length(min=9)])
    email = EmailField('Enter Your Email',validators=[DataRequired(message='Email cannot be empty'),Email(message='Email invalid')])
    gender = RadioField('Gender',choices=[('Male', 'Male'), ('Female', 'Female')],validators=[DataRequired(message='Select a gender')])
    password = PasswordField('Enter Your Password',validators=[DataRequired(message='Enter password'),Length(min=8)])
    confirm_password = PasswordField('Confirm Your Password',validators=[DataRequired(message='Cannot be empty'),EqualTo('password',message='Passwords must match')])
    agree = BooleanField('I hereby agree that all information provided above is correct',validators=[DataRequired(message='Cannot be empty')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = StringField('Enter Your Email',validators=[DataRequired(message='Enter a valid email')])
    password = PasswordField('Enter Your Password',validators=[DataRequired(message='Password cannot be empty')])
    send = SubmitField('Login')

class ContactForm(FlaskForm):
    message = TextAreaField('Enter Message Here',validators=[DataRequired('Field cannot be empty'),Length(min=10)])
    email = EmailField('Email')
    submit = SubmitField('Submit')


class PublicDetailForm(FlaskForm):
    username = StringField('Update Username',validators=[DataRequired('Enter Username')])
    bio = TextAreaField('Update Bio')
    upload =  FileField(validators=[FileAllowed(['jpg','png','jpeg'],'Only Images are allowed')])
    save = SubmitField('Save Changes')


class PrivateDetailForm(FlaskForm):
    firstname = StringField('Update FirstName',validators=[DataRequired(message='Please enter Firstname')])
    lastname = StringField('Update LastName',validators=[DataRequired(message='Please enter Lastname')])
    email = EmailField('Email',validators=[DataRequired(message='Email cannot be empty'),Email(message='Email invalid')])
    save = SubmitField('Save Changes')


class PasswordChange(FlaskForm):
    password = PasswordField('Current password',validators=[DataRequired(message='Enter current password')])
    newpassword = PasswordField('New password',validators=[DataRequired(message='Enter new password')])
    confirm_password = PasswordField('Verify password',validators=[DataRequired(message='Verify password'),EqualTo('newpassword',message='Passwords must match')])
    save = SubmitField('Save Changes')


class SellersForm(FlaskForm):
    category = RadioField('Choose a category',choices=[('1', 'Sketch'), ('2', 'Embroideries'), ('3', 'Paint arts'), ('4', 'Sculptures'), ('5', 'Interior designs')],validators=[DataRequired(message='Select a category')])

    # List of Nigerian States
    states = [
        ('abia', 'Abia'), ('adamawa', 'Adamawa'), ('akwa_ibom', 'Akwa Ibom'), ('anambra', 'Anambra'),
        ('bauchi', 'Bauchi'), ('bayelsa', 'Bayelsa'), ('benue', 'Benue'), ('borno', 'Borno'),
        ('cross_river', 'Cross River'), ('delta', 'Delta'), ('ebonyi', 'Ebonyi'), ('edo', 'Edo'),
        ('ekiti', 'Ekiti'), ('enugu', 'Enugu'), ('gombe', 'Gombe'), ('imo', 'Imo'),
        ('jigawa', 'Jigawa'), ('kaduna', 'Kaduna'), ('kano', 'Kano'), ('katsina', 'Katsina'),
        ('kebbi', 'Kebbi'), ('kogi', 'Kogi'), ('kwara', 'Kwara'), ('lagos', 'Lagos'),
        ('nasarawa', 'Nasarawa'), ('niger', 'Niger'), ('ogun', 'Ogun'), ('ondo', 'Ondo'),
        ('osun', 'Osun'), ('oyo', 'Oyo'), ('plateau', 'Plateau'), ('rivers', 'Rivers'),
        ('sokoto', 'Sokoto'), ('taraba', 'Taraba'), ('yobe', 'Yobe'), ('zamfara', 'Zamfara')
    ]

    state = SelectField('Select Your State', choices=states, validators=[DataRequired(message='You must select a state')])

    submit = SubmitField('Submit')


class CreatePost(FlaskForm):
    description = TextAreaField('Description',validators=[DataRequired(message='Description cannot be empty')])
    price = StringField('Price')
    image =  FileField('Upload Image',validators=[FileAllowed(['jpg','png','jpeg'],'Only Images are allowed')])
    post = SubmitField('Upload') 


class EditPost(FlaskForm):
    description = TextAreaField('Description',validators=[DataRequired(message='Description cannot be empty')])
    price = StringField('Price')
    post = SubmitField('Upload') 
