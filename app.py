from datetime import datetime, timedelta
from authlib.integrations.flask_client import OAuth
from flask import Flask, render_template, url_for, session, redirect, request
from flask_sqlalchemy import SQLAlchemy
from auth_decorator import login_required

app = Flask(__name__)
#CORS(app)

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

num = 17

@app.route("/")
@app.route("/home")
def home():
    session['checkin'] = 'false'
    return render_template('home.html')

@app.route("/Feedbackform")
def feedback():
    return render_template('Feedbackform.html')

@app.route("/register")
def register():
    return render_template('Registrationform.html')


@app.route("/restaurant")
def restaurant():
    res_list = Restaurant.query.all()
    items = []
    for item in res_list:
        items.append({'id': item.id, 'name': item.name, 'description': item.bio, 'rating': item.rating, 'people': item.no_of_customers, 'img_src': item.image_file, 'city': item.city})
    
    return render_template('restaurant.html', res_list = items)

@app.route('/res_form/<idx>', methods=['POST'])
def res_form(idx):
    data = request.get_json()
    print(data)
    session['idx']= data['res_id']
    return 'Done'

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


@app.route("/checkout" , methods=['GET','POST'])
@login_required
def checkout():
    idx = session.get('idx', None)
    if idx:
        if request.method=='POST':
            session['checkin']='true'
            result = request.get_json()
            session['customers'] = result['new_customers']
            print(result['new_customers'])
            res_info = Restaurant.query.filter_by(id=idx).first() 
            res_info.no_of_customers = res_info.no_of_customers + int(result['new_customers']) #add new customers to database
            current_customers = res_info.no_of_customers + int(result['new_customers'])
            reviews = res_info.reviews #get all reviews posted by people
            db.session.commit()


            list_of_reviews = []
            for review in reviews:
                list_of_reviews.append({'date_posted': review.date_posted, 'content': review.content})

            item = {'id': res_info.id, 'name': res_info.name, 'description': res_info.bio, 'rating': res_info.rating, 'people': current_customers, 'img_src': res_info.image_file, 'city': res_info.city, 'reviews': list_of_reviews}
            return render_template('checkout.html', res = item)

        else:
            if session['checkin'] == 'true':
                res_info = Restaurant.query.filter_by(id=idx).first()
                reviews = res_info.reviews
                list_of_reviews = []
                for review in reviews:
                    list_of_reviews.append({'date_posted': review.date_posted, 'content': review.content})

                item = {'id': res_info.id, 'name': res_info.name, 'description': res_info.bio, 'rating': res_info.rating, 'people': res_info.no_of_customers, 'img_src': res_info.image_file, 'city': res_info.city, 'reviews': list_of_reviews}
                return render_template('checkout.html', res=item)
            else:
                return redirect('/home')
    
    else:
        return redirect('/home')


@app.route("/feedbackform", methods=['POST'])
def feedbackform():
    result = request.form
    #print(result['review'])
    #print(result['stars'])
    #print(result['restaurantId'])
    last_item = Reviews.query.all()
    if len(result['review'])!=0:
        new_review = Reviews(
            id = last_item[-1].id+1,
            content = result['review'],
            res_id = result['restaurantId']
        )
        db.session.add(new_review)
        db.session.commit()
        res_info = Restaurant.query.filter_by(id=(result['restaurantId'])).first() 
        res_info.no_of_customers = res_info.no_of_customers - int(session['customers'])
        db.session.commit()
    else:
        print('data empty')
    
    return redirect('/home')

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    session['profile'] = user_info
    session['email'] = user_info['email']
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/form')



if __name__ == '__main__':
    app.run(debug=True)