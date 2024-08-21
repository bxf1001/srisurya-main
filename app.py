from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_login import current_user
from datetime import datetime

app = Flask(__name__)
app.secret_key = '07e0d903dac5f687ce8e6c9679dd6b56'  # Add this line near the app initialization
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
db = SQLAlchemy(app)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
class Message(db.Model):
    __tablename__ = 'messages' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/supplies')
def supplies():
    return render_template('supplies.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']
        
        new_message = Message(name=name, email=email, subject=subject, message=message)
        db.session.add(new_message)
        db.session.commit()
        
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')



@app.route('/admin')
def admin():
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    messages = Message.query.order_by(Message.date_sent.desc()).all()
    return render_template('admin.html', messages=messages)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
def create_admin_user():
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', password=generate_password_hash('1234'))
        db.session.add(admin)
        db.session.commit()

with app.app_context():
    db.create_all()
    create_admin_user()
if __name__ == '__main__':
    app.run(debug=True)
    

