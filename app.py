from datetime import datetime, timedelta
from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, url_for, session, redirect, request
from flask_sqlalchemy import SQLAlchemy

# decorator for routes that should be accessible only by logged in users
from auth_decorator import login_required

app = Flask(__name__)

app.secret_key = 'random secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://woofuwum:2Kil4h5J98jt9wkRAvr2R6S5zk9qbXC7@hansken.db.elephantsql.com:5432/woofuwum'
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

db = SQLAlchemy(app)
oauth = OAuth(app)

google = oauth.register(
    name = 'google',
    client_id = '583685516615-uc5d7l2664pqins2okedglroeqt4p3o9.apps.googleusercontent.com',
    client_secret = 'yxef4mcr_qQQ7m24BqfnnpIn',
    access_token = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid profile email'}
)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    city = db.Column(db.String(20), nullable=False)
    lattitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_file = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer)
    bio = db.Column(db.String(20), nullable=False)
    no_of_customers = db.Column(db.Integer, nullable=False)
    reviews = db.relationship('Reviews', backref='author', lazy=True)

    def __repr__(self):
        return f"Restaurant('{self.id}', '{self.name}','{self.city}','{self.lattitude}', '{self.longitude}', '{self.image_file}','{self.rating}','{self.no_of_customers}')"


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    res_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'), nullable=False)

    def __repr__(self):
        return f"Reviews('{self.id}', '{self.date_posted}','{self.content}')"

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/restaurant")
def restaurant():
    res_list = Restaurant.query.all()
    items = []
    for item in res_list:
        items.append({'id': item.id, 'name': item.name, 'description': item.bio, 'rating': item.rating, 'people': item.no_of_customers, 'img_src': item.image_file, 'city': item.city})
    
    return render_template('restaurant.html', res_list = items)

@app.route("/res_form/<idx>", methods=['POST'])
def res_form(idx):
    data = request.get_json()
    print(data)
    session['idx']= data['res_id']
    return redirect('/form')

@app.route("/form")
@login_required
def form():
    idx = session.get('idx', None)
    if idx:
        res_info = Restaurant.query.filter_by(id=idx).first()
        reviews = res_info.reviews
        list_of_reviews = []
        for review in reviews:
            list_of_reviews.append({'date_posted': review.date_posted, 'content': review.content})

        item = {'id': res_info.id, 'name': res_info.name, 'description': res_info.bio, 'rating': res_info.rating, 'people': res_info.no_of_customers, 'img_src': res_info.image_file, 'city': res_info.city, 'reviews': list_of_reviews}
        return render_template('form.html', res = item)
    
    else:
        return redirect('/home')


@app.route("/checkout", methods=['GET','POST'])
@login_required
def checkout():
    idx = session.get('idx', None)
    if idx:
        if request.method=='POST':
            result = request.form
            #print(result['customers'])
            res_info = Restaurant.query.filter_by(id=idx).first() 
            res_info.no_of_customers = res_info.no_of_customers + int(result['customers']) #add new customers to database
            current_customers = res_info.no_of_customers + int(result['customers'])
            reviews = res_info.reviews #get all reviews posted by people
            db.session.commit()


            list_of_reviews = []
            for review in reviews:
                list_of_reviews.append({'date_posted': review.date_posted, 'content': review.content})

            item = {'id': res_info.id, 'name': res_info.name, 'description': res_info.bio, 'rating': res_info.rating, 'people': current_customers, 'img_src': res_info.image_file, 'city': res_info.city, 'reviews': list_of_reviews}
            return render_template('checkout.html', res = item)

        else:
            res_info = Restaurant.query.filter_by(id=idx).first()
            reviews = res_info.reviews
            list_of_reviews = []
            for review in reviews:
                list_of_reviews.append({'date_posted': review.date_posted, 'content': review.content})

            item = {'id': res_info.id, 'name': res_info.name, 'description': res_info.bio, 'rating': res_info.rating, 'people': res_info.no_of_customers, 'img_src': res_info.image_file, 'city': res_info.city, 'reviews': list_of_reviews}
            return render_template('checkout.html', res=item)
    
    else:
        return redirect('/home')
