from flask import Flask, render_template, request, redirect, url_for, flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from collections import defaultdict
from functools import wraps
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from sqlalchemy import func
from flask import render_template
 
from collections import defaultdict
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role=db.Column(db.String(60), nullable=False,default="user")

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category=db.Column(db.String(150),nullable=False)
    subcategory=db.Column(db.String(150),nullable=False)
    subsubcategory=db.Column(db.String(150),nullable=False)
    name=db.Column(db.String(150),nullable=False)
    image=db.Column(db.String,nullable=False)
    Price=db.Column(db.Integer,nullable=False)


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(150),nullable=False)
    email=db.Column(db.String(150),nullable=False)
    rating=db.Column(db.Integer,nullable=False)
    comment=db.Column(db.String(350),nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category=db.Column(db.String(150),nullable=False)
    subcategory=db.Column(db.String(150),nullable=False)
    subsubcategory=db.Column(db.Integer,nullable=False)
    name=db.Column(db.String(350),nullable=False)
    image=db.Column(db.String,nullable=False)
    Price=db.Column(db.Integer,nullable=False)
    cup=db.Column(db.String(150),nullable=False)



class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.Text, nullable=False)  # Store items as JSON
    subtotal = db.Column(db.Float, nullable=False)
    gst = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



products = [
    { "id": 1, "name": "Espresso Beans", "category": "Coffee", "price": 250, "image": "espresso_beans.jpg" },
    { "id": 2, "name": "Cold Brew", "category": "Coffee", "price": 150, "image": "cold_brew.jpg" },
    { "id": 3, "name": "Cappuccino Mix", "category": "Coffee", "price": 200, "image": "cappuccino_mix.jpg" },
    { "id": 4, "name": "Flour", "category": "Essentials", "price": 150, "image": "cinnamon_roll.jpg" },
    { "id": 5, "name": "Coffee Filter", "category": "Essentials", "price": 50, "image": "coffee_filter.jpg" },
    { "id": 6, "name": "Almond Milk", "category": "Milk", "price": 120, "image": "almond_milk.jpg" },
    { "id": 7, "name": "Caramel Latte Mix", "category": "Coffee", "price": 250, "image": "espresso_beans.jpg" },
    { "id": 8, "name": "Wheet", "category": "Essential", "price": 150, "image": "cold_brew.jpg" },
    { "id": 9, "name": "Peach", "category": "Fruits", "price": 200, "image": "cappuccino_mix.jpg" },
    { "id": 10, "name": "Cinnamon Powder", "category": "Essentials", "price": 100, "image": "cinnamon_roll.jpg" },
    { "id": 11, "name": "Sugar", "category": "Essential", "price": 50, "image": "coffee_filter.jpg" },
    { "id": 12, "name": "Oat Milk", "category": "Milk", "price": 120, "image": "almond_milk.jpg" },
    { "id": 13, "name": "Chocolate Syrup", "category": "Syrup", "price": 250, "image": "espresso_beans.jpg" },
    { "id": 14, "name": "Mango", "category": "Fruits", "price": 150, "image": "cold_brew.jpg" },
    { "id": 15, "name": "Strawberry Syrup", "category": "Syrup", "price": 200, "image": "cappuccino_mix.jpg" },
    { "id": 16, "name": "Whole Milk", "category": "Milk", "price": 100, "image": "cinnamon_roll.jpg" },
    { "id": 17, "name": "Apple", "category": "Fruits", "price": 50, "image": "coffee_filter.jpg" },
    { "id": 18, "name": "Soya Milk", "category": "Milk", "price": 120, "image": "almond_milk.jpg" },
]

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    quantity = db.Column(db.Float, default=0)
    price = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize the database and create initial products
 
        
        

# Your existing routes remain the same
@app.route('/available_inventory')
def available_inventory():
    inventory_items = InventoryItem.query.all()
    inventory_dict = {item.name: item.quantity for item in inventory_items}
    categories = sorted(set(p['category'] for p in products))
    return render_template('available_inventory.html',
                         products=products,
                         categories=categories,
                         inventory=inventory_dict)

@app.route('/inventory')
def inventory():
    inventory_items = InventoryItem.query.all()
    return render_template('inventory.html', inventory=inventory_items)

@app.route('/add_to_inventory', methods=['POST'])
def add_to_inventory():
    product_id = int(request.form.get('product_id'))
    quantity = float(request.form.get('quantity'))
    
    if quantity <= 0:
        flash('Please enter a valid quantity', 'error')
        return redirect(url_for('available_inventory'))
    
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('available_inventory'))
    
    inventory_item = InventoryItem.query.filter_by(name=product['name']).first()
    
    if inventory_item:
        inventory_item.quantity += quantity
        inventory_item.last_updated = datetime.utcnow()
    else:
        inventory_item = InventoryItem(
            name=product['name'],
            category=product['category'],
            quantity=quantity,
            price=product['price']
        )
        db.session.add(inventory_item)
    
    db.session.commit()
    flash(f'Added {quantity}kg of {product["name"]} to inventory', 'success')
    return redirect(url_for('available_inventory'))

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    item = InventoryItem.query.get(product_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f'{item.name} deleted successfully.', 'success')
    else:
        flash('Product not found.', 'error')
    return redirect(url_for('inventory'))



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# # Create the database and tables
with app.app_context():
    db.create_all()

    #  # Check if database is empty
    # if not InventoryItem.query.first():
    #         # Add initial products with 0 quantity
    #     for product in products:
    #         item = InventoryItem(
    #             name=product['name'],
    #             category=product['category'],
    #             quantity=0,
    #             price=product['price']
    #             )
    #         db.session.add(item)
    #         db.session.commit()
     
            


def admin_required(func):
    @wraps(func)
    def wrapper_func(*args,**kwargs):
        if current_user.role!="admin":
            flash ("You are not permitted to access this page","danger")
            return redirect(url_for('admin'))
        return func(*args,**kwargs)
    return wrapper_func
@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/menu",methods=["GET","POST"])
# def menu():
#     items=Menu.query.all()
#     return render_template("menu.html",items=items)

 

@app.route('/menu',methods=["GET","POST"])
def menu():
    # Query all menu items from database
    menu_items = db.session.query(Menu).all()
    
    # Create nested dictionary to organize menu items
    organized_menu = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    # Organize items by category > subcategory > subsubcategory
    for item in menu_items:
        organized_menu[item.category][item.subcategory][item.subsubcategory].append({
            'id': item.id,
            'name': item.name,
            'image': item.image
        })
   

    
    return render_template('menu1.html', menu_data=organized_menu)

@app.route
def order_selection():
    return render_template("Order_selection.html")

@app.route('/order_now')
def order_now():
    return render_template("order_now.html")

@app.route('/cart')
def cart():
    return render_template("cart.html")

@app.route("/feedback",methods=["GET","POST"])
def feedback():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        rating = request.form.get("rating")
        comment = request.form.get("comment")
        new_comment=Feedback(username=username,email=email,rating=rating,comment=comment)
        db.session.add(new_comment)
        db.session.commit()
        flash("Feedback Submitted Successfully","success")
        return redirect(url_for('order_now'))

    return render_template("feedback.html")

@app.route("/order_selection/<int:id>",methods=["GET","POST"])
def order(id):
    item = Menu.query.get_or_404(id)
    return render_template("Order_selection.html",item=item)
    

@app.route("/learn_more")
def learn():
    return render_template("learn.html")


@app.route("/bestsellers")
def bestsellers():
    return render_template("bestsellers.html")
@app.route("/chocolates")
def chocolates():
    return render_template("chocolates.html")
@app.route("/food")
def food():
    return render_template("food.html")
@app.route("/drinks")
def drinks():
    return render_template("drinks.html")

@app.route("/cookies")
def cookies():
    return render_template("cookies.html")
@app.route("/desserts")
def desserts():
    return render_template("desserts.html")

 
@app.route("/reviews")
@login_required
@admin_required
def reviews():
    feedbacks=Feedback.query.all()
    return render_template("reviews.html",reviews=feedbacks)



@app.route("/dashboard")
@login_required
@admin_required
def dashboard():
    return render_template("dashboard.html")



 
        
 


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        # Get cart data from form submission
        cart_data = request.form.get('cart_data', '[]')
        subtotal = request.form.get('subtotal', '0.00')
        gst = request.form.get('gst', '0.00')
        total = request.form.get('total', '0.00')
        
        # Parse the cart data to extract just the names
        try:
            cart_items = json.loads(cart_data)
            item_names = [item['name'] for item in cart_items]
            items_string = ', '.join(item_names)
        except:
            items_string = "Your order"
        
        # Store in session for later use
        session['order_items'] = items_string
        session['subtotal'] = subtotal
        session['gst'] = gst
        session['total'] = total
        
    else:  # GET request
        # Check if we have data in session
        if 'order_items' not in session:
            # Redirect to cart if no data
            return redirect(url_for('cart'))
        
        items_string = session.get('order_items', "Your order")
        subtotal = session.get('subtotal', '0.00')
        gst = session.get('gst', '0.00')
        total = session.get('total', '0.00')

        new_order = Order(
        items=items_string, 
        subtotal=subtotal, 
        gst=gst, 
        total=total
        )
        db.session.add(new_order)
        db.session.commit()
    
    # Render template with just the item names
    return render_template('payment.html', 
                           order_items=items_string,
                           subtotal=subtotal,
                           gst=gst,
                           total=total)




@app.route("/payment_successfull")
def payment_successfull():
    return render_template("paymentsuccessfull.html")

# @app.route('/')
# def home():
#     if current_user.is_authenticated:
#         return f"Welcome {current_user.full_name}! <a href='/logout'>Logout</a>"
#     return redirect(url_for('signup'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Check if email or username already exists
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('signup'))
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('signup'))
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create new user
        new_user = User(email=email, full_name=full_name, username=username, password=hashed_password,role="user")
        db.session.add(new_user)
        db.session.commit()
        
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth.html', form_type='signup')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash('Login successful!', 'success')
            return redirect(url_for('admin'))
        else:
            flash('Login unsuccessful. Please check your username and password', 'danger')
    
    return render_template('auth.html', form_type='login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

 
@app.route("/admin")
@login_required
def admin():
    return render_template("admin.html")

@app.route("/contact_us")
@login_required
def contact_us():
    return render_template("contact.html")

@app.route("/about_us")
@login_required
def about_us():
    return render_template("about.html")

@app.route("/order_history")
@login_required
@admin_required
def order_history():
    return render_template("order_history.html")

@app.route("/sales")
@login_required
@admin_required
def sales():
    return render_template("sales.html")


@app.route("/revenue")
@login_required
@admin_required
def revenue():
    return render_template("revenue.html")


@app.route('/edit_item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = Menu.query.get_or_404(item_id)
    
    if request.method == 'POST':
        # Update item details
        item.subcategory = request.form.get('subcategory')
        item.subsubcategory = request.form.get('subsubcategory')
        item.name = request.form.get('name')
        item.Price = request.form.get('price')
         
        
        db.session.add(item)
        db.session.commit()
        flash('Menu item updated successfully', 'success')
        return redirect(url_for('menu'))
    
    return render_template('edit_menu.html', item=item)

@app.route('/delete_item/<int:item_id>', methods=['GET','POST'])
def delete_item(item_id):
    item = Menu.query.get_or_404(item_id)
    
    
    
    # Delete from database
    db.session.delete(item)
    db.session.commit()
    
    flash('Menu item deleted successfully', 'success')
    return redirect(url_for('menu'))
 

@app.route("/termsandconditions")
def termsandconditions():
    return render_template("termsandconditions.html")

@app.route("/add_item",methods=["GET","POST"])
def add_item():
    if request.method=="POST":
        category=request.form.get("item_category")
        item_name=request.form.get("item_name")
        subcategory=request.form.get("subcategory")
        subsubcategory=request.form.get("subsubcategory")
        price=request.form.get("price")
        # image_file = request.files['image']
        # if image_file and image_file.filename != '':
        #     filename = secure_filename(image_file.filename)
        #     image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #     image_file.save(image_path)  # Save image to folder
        #     db_image_path = f"uploads/{filename}"  # Relative path for DB
        # else:
        #     db_image_path = None  # No image provided

    

        new_item=Menu(category=category,subcategory=subcategory,subsubcategory=subsubcategory,name=item_name,image="../static/images/a.jpg",Price=price)
        db.session.add(new_item)
        db.session.commit()
        flash("Item Added in the menu","success")
        return redirect(url_for('menu'))



    return render_template("add_item.html")

@app.route("/new_cart",methods=["GET","POST"])
def new_cart():
    if request.method=="POST":
        item_name = request.form.get('item_name')
        item_price = float(request.form.get('item_price'))
        item_image = request.form.get('item_image')
        
        item_category=request.form.get('item_category')
        item_subcategory=request.form.get('item_subcategory')
        item_subsubcategory=request.form.get('item_subsubcategory')
        cup=request.form.get('item_size')

        print("Item Name:", item_name)
        print("Item Price:", item_price)
        print("Item Image:", item_image)
        print("Item Category:", item_category)
        print("Item Subcategory:", item_subcategory)
        print("Item Subsubcategory:", item_subsubcategory)
        print("Cup Size:", cup)
        new_item=Cart(name=item_name,category=item_category,subcategory=item_subcategory,subsubcategory=item_subsubcategory,Price=item_price,image=item_image,cup=cup)
        db.session.add(new_item)
        db.session.commit()
    cart_items=Cart.query.all()
    total_price = db.session.query(func.sum(Cart.Price)).scalar()
    item_names = [item.name for item in Cart.query.all()]
    subtotal=total_price
    gst=total_price/10
    total=subtotal+gst
    order_items = ", ".join(item_names) 
    total_entries = Cart.query.count()
    
    return render_template("new_cart.html",cart_items=cart_items,total_price=total_price,total_entries=total_entries,order_items=order_items,subtotal=subtotal,gst=gst,total=total)
@app.route("/new_payement",methods=["POST","GET"])
def new_payment():
    if request.method=="POST":
        order_items=request.form.get("order_items")
        subtotal=request.form.get("subtotal")
        gst=request.form.get("gst")
        total=request.form.get("total")

    return render_template("new_payment.html",order_items=order_items,subtotal=subtotal,gst=gst,total=total)

if __name__ == '__main__':
    app.run(debug=True)
