# Bytes-and-Brews
Overview

The Bytes and Brews (Café Management System) is a web-based application designed to streamline café operations, providing a seamless experience for both customers and administrators. Built using Python Flask for the backend and HTML, CSS, and JavaScript for the frontend, this system enables customers to browse and order items while allowing admins to manage inventory and track orders efficiently.

Features

Customer Interface:

Order Now Page: Customers can explore various food categories, including:

Bestsellers

Cookies

Drinks

Desserts

chocolates



Cart Management: Users can select items and add them to their cart for checkout,and they can also drop their feedback about the cafe also.



Admin Interface:

Dashboard: Overview of café operations, including orders, revenue, and stock management.

Order Management: Admins can view order history.

Inventory Control: Manage menu items - including updating,deleting and adding menu items, updating  prices, and monitor stock levels.

User Management: View and manage registered customers.

Customer feedback and reviews section

Technologies Used

Backend: Python Flask

Frontend: HTML, CSS, JavaScript

Database: SQLite 

Authentication: Flask-Login / Flask-Security 

Deployment: Can be hosted on platforms like Heroku, AWS, or any Flask-supported environment

Installation & Setup

Prerequisites:

Python 3.x

Flask framework

Database setup (SQLite/MySQL)

Virtual environment (recommended for package management)

Steps to Install:

Clone the Repository

git clone https://github.com/Niyamat0104/Bytes-and-Brews.git
cd cafe-management-system

Create a Virtual Environment (Optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

Install Dependencies

pip install -r requirements.txt

Setup the Database

flask db init
flask db migrate -m "Initial migration."
flask db upgrade

Run the Application

flask run

Access the System

Open your browser and go to http://127.0.0.1:5000/

Future Enhancements

Integration of online payment gateways

 

Advanced analytics dashboard for sales insights

Mobile responsiveness improvements

Contributing

Feel free to fork the repository and submit pull requests. Contributions to improve features or fix bugs are welcome!

 

Contact

For queries or contributions, reach out via email at niyamatkajal0104@gmail.com  or visit GitHub.
