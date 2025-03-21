from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import stripe
import os
from werkzeug.security import generate_password_hash, check_password_hash  # Import hash functions
from wtforms.validators import DataRequired


# Define Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'secret_key_here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'your_secret_key')

# Models
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)  # Renamed to password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ProductAdminView(ModelView):
    column_list = ('name', 'price', 'description')
    form_columns = ('name', 'price', 'description')
    column_searchable_list = ('name',)

    def is_accessible(self):
        # Check for admin role via username
        return current_user.is_authenticated and current_user.username == 'admin'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Admin Setup
admin = Admin(app, name='Admin Dashboard', template_mode='bootstrap3')
admin.add_view(ProductAdminView(Product, db.session))

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Login')

@app.route('/')
def home():
    # Example products. Ideally, you should fetch these from the database
    products = Product.query.all()  # Fetch products from DB
    return render_template('home.html', products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):  # Use hashed password comparison
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', form=form)


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Make sure you set a secret key for session management


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # You can add your login logic here (e.g., check username/password)
        if username == 'admin' and password == 'password':
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))  # Redirect to a dashboard page or any other page
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html', form=form)


@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    cart_items = [Product.query.get(id) for id in cart if Product.query.get(id)]  # Only valid products
    return render_template('cart.html', cart_items=cart_items)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if product:
        cart = session.get('cart', [])
        if product.id not in cart:
            cart.append(product.id)
            session['cart'] = cart
        else:
            flash("This item is already in your cart.", "info")
    else:
        flash("Product not found.", "danger")
    return redirect(url_for('home'))

@app.route('/checkout')
@login_required
def checkout():
    return render_template('checkout.html')

@app.route('/charge', methods=['POST'])
def charge():
    token = request.form['stripeToken']
    cart = session.get('cart', [])
    total_amount = sum([Product.query.get(id).price * 100 for id in cart])  # Total in cents
    
    # Check if cart is empty
    if not cart:
        flash("Your cart is empty. Please add items to your cart.", 'warning')
        return redirect(url_for('home'))

    try:
        charge = stripe.Charge.create(
            amount=total_amount,  # Total amount in cents
            currency="zar",  # Make sure the currency is correctly set
            description="Product purchase",
            source=token,
        )
        session['cart'] = []  # Clear cart after successful purchase
        flash('Payment successful! Thank you for your purchase.', 'success')
        return redirect(url_for('success'))
    except stripe.error.StripeError as e:
        flash(f"Error: {e.user_message}", 'danger')
        return redirect(url_for('checkout'))

@app.route('/success')
def success():
    return render_template('success.html')

# Create app function
def create_app():
    db.create_all()  # Create the database tables
    return app

# Main Entry
if __name__ == "__main__":
    app = create_app()  # Initialize the app here
    app.run(debug=True)
