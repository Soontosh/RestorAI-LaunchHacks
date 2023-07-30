from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os
import random
import string
from cv2 import resize, imdecode, IMREAD_COLOR, imwrite, imread
from numpy import uint8, frombuffer
import model
import sepiaIndividual

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/sapat/Downloads/LaunchHacksWebsite/database.db'
app.config['SECRET_KEY'] = 'SECRET123' #can replace with os.urandom lator
app.config['UPLOAD_FOLDER'] = 'static/files'

app.config["RECAPTCHA_PUBLIC_KEY"] = "" #Remove when uploading to github
app.config["RECAPTCHA_PRIVATE_KEY"] = "" #Remove when uploading to github

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
#db.init_app(app)

recreate = False

loginManager = LoginManager()
loginManager.init_app(app)
loginManager.login_view = "login"


@loginManager.user_loader
def loadUser(userID):
    return User.query.get(int(userID))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    credits = db.Column(db.Integer, nullable = False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"Placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"Placeholder": "Password"})

    recaptcha = RecaptchaField()
    submit = SubmitField("Register")

    def validateUsername(self, username):
        usernameExists = User.query.filter_by(username=username.data).first()

        if usernameExists:
            raise ValidationError("The username provided already exists")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"Placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"Placeholder": "Password"})

    recaptcha = RecaptchaField()
    submit = SubmitField("Login")

class ChangeUserForm(FlaskForm):
    newUsername = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"Placeholder": "New Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"Placeholder": "Password"})

    recaptcha = RecaptchaField()
    submit = SubmitField("Rename")    

class UploadImageForm(FlaskForm):
        file = FileField("File")
        submit = SubmitField("Upload File")

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('home'))
            else:
                raise ValidationError("Password is Incorrect")
        else:
            raise ValidationError("User does not exist")

    return render_template('login.html', form=form)

@app.route('/rename', methods=["GET", "POST"])
@login_required
def rename():
    form = ChangeUserForm()

    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            newUsername = form.newUsername.data
            current_user.username = newUsername
            db.session.commit()
            return redirect(url_for('login'))
        else:
            raise ValidationError("Something Went Wrong!")
    
    return render_template("rename.html", form=form)


@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('index.html', username = current_user.username, creditsLeft = current_user.credits)

@app.route('/uploadImg', methods=['GET', 'POST'])
@login_required
def uploadImg():
    if request.method == 'POST':
        imgFile = request.files.get('file')
        print(imgFile)
        print(imgFile.filename)

        imageString = ''.join(random.choices(string.digits, k=24))
        imageString2 = ''.join(random.choices(string.digits, k=24))
        
        imgArray = frombuffer(imgFile.read(), uint8)
        img = imdecode(imgArray, IMREAD_COLOR)
        img = resize(img, (256, 256))
        
        imwrite(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], str(imageString + ".jpg")), img)
        print(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], str(imageString + ".jpg")))
        session['uploadedFile'] = os.path.join(app.config['UPLOAD_FOLDER'], str(imageString + ".jpg"))

        img = model.predict(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], str(imageString + ".jpg")), os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], str(imageString2 + ".jpg")))
        session['uploadedFileResult'] = os.path.join(app.config['UPLOAD_FOLDER'], str(imageString2 + ".jpg"))


        redirectUrl = url_for('chooseType') # resize image to 256 by 256 btw
        return jsonify({"redirect": redirectUrl})

@app.route('/chooseType')
@login_required
def chooseType():
    #change the image if it is converter using the session
    return render_template("choose.html")

@app.route('/convert')
@login_required
def convert():
    imgFile = session['uploadedFile']

    imageString = ''.join(random.choices(string.digits, k=24))
    imageString2 = ''.join(random.choices(string.digits, k=24))
    
    img = imread(imgFile)
    img = resize(img, (256, 256))
    
    imwrite(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], str(imageString + ".jpg")), img)
    print(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], str(imageString + ".jpg")))
    session['uploadedFile'] = os.path.join(app.config['UPLOAD_FOLDER'], str(imageString + ".jpg"))

    sepiaIndividual.convertImg(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], str(imageString + ".jpg")), os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], str(imageString2 + ".jpg")))
    session['uploadedFileResult'] = os.path.join(app.config['UPLOAD_FOLDER'], str(imageString2 + ".jpg"))


    redirectUrl = url_for('chooseType') # resize image to 256 by 256 btw
    return redirect(url_for("displayImg"))


@app.route('/displayimg')
@login_required
def displayImg():
    currentCredits = current_user.credits - 1
    currentCredits -= 1
    current_user.credits = currentCredits
    db.session.commit()

    imgPath = session['uploadedFile']
    imgPathProcess = session['uploadedFileResult']
    print("imgPathProcess: " + imgPathProcess)
    print("peak")
    return render_template('uploaded.html', imgPath=imgPath, resultPath = imgPathProcess)

@app.route('/purchase', methods=["GET", "POST"])
@login_required
def purchase():
    if request.method == 'POST':
        print('purchase recieved')
        jsonData = request.json
        print(jsonData)

        user = User.query.filter_by(username=jsonData['username']).first()
        currentCredits = user.credits
        currentCredits += jsonData['amount']

        user.credits = currentCredits
        db.session.commit()

        redirectUrl = url_for('logout')
        return jsonify({"redirect": redirectUrl})

    return

@app.route('/delete', methods=["GET", "POST"])
@login_required
def deleteUser():
    if request.method == 'POST':
        print("deletion received")

        jsonData = request.json
        print(jsonData)
        print("Username: " + jsonData['username'])

        User.query.filter_by(username=jsonData['username']).delete()
        db.session.commit()

        redirectUrl = url_for('logout')
        return jsonify({"redirect": redirectUrl})

@app.route('/logout', methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data)
        newUser = User(username=form.username.data, password=hashedPassword, credits=5)

        db.session.add(newUser)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

if __name__ == "__main__":
    if recreate:
        with app.app_context():
                db.create_all()

    app.run(debug=True)