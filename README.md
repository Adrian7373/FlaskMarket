# **Flask Market – A Simple Marketplace Web Application**

Flask Market is a beginner-friendly web application built with **Flask**, **Flask-SQLAlchemy**, **Flask-Login**, and **Bootstrap 4**.
It simulates a small marketplace where users can **register, log in, purchase items, sell items, and list new items**.

The project demonstrates:

* User authentication
* CRUD operations
* Form handling with WTForms
* Database operations with SQLAlchemy
* Template inheritance and modularized HTML using Jinja2

---

## 🚀 **Features**

### 🔐 Authentication

* Register and log in using secure hashed passwords
* Prevents duplicate users
* Flash messages for feedback
* Login required to access the marketplace

### 🛒 Marketplace Features

* View all items in the market
* Buy items (with balance validation)
* Cannot buy own item
* Budgets update after purchases and sales

### 💼 Inventory Features

* View your owned items
* Sell items with a new asking price
* List brand-new items (name, price, description)

### 🎨 User Interface

* Responsive Bootstrap UI
* Reusable modal templates
* Global navigation via `base.html` layout

---

## 🗂️ **Project Structure**

```
FlaskMarket/
│
├── instance/
│   └── market.db                 # Auto-created SQLite database
│
├── market/
│   ├── __init__.py               # App factory & config
│   ├── routes.py                 # All application routes
│   ├── models.py                 # SQLAlchemy models
│   ├── forms.py                  # WTForms forms
│   │
│   ├── images/
│   │   └── main_logo.png         # Logo used in UI
│   │
│   └── templates/
│       ├── base.html             # Main layout
│       ├── home.html             # Home page
│       ├── login.html            # Login form
│       ├── register.html         # Registration form
│       ├── market.html           # Marketplace page
│       │
│       └── includes/             # Reusable modals
│           ├── items_modals.html
│           ├── list_items_modals.html
│           └── owned_items_modals.html
│
└── run.py                        # Entry point to run the app
```

---

## 🛠️ **Technologies Used**

| Technology           | Purpose                |
| -------------------- | ---------------------- |
| **Flask**            | Application framework  |
| **Flask-SQLAlchemy** | ORM for database       |
| **SQLite**           | Local database         |
| **Flask-Login**      | Authentication/session |
| **Flask-Bcrypt**     | Password hashing       |
| **Bootstrap 4**      | Frontend UI            |
| **WTForms**          | Form validation        |
| **Jinja2**           | Templating             |

---

## ⚙️ **Installation & Setup**

### **1. Clone the Project**

```bash
git clone https://github.com/Adrian7373/FlaskMarket.git
cd FlaskMarket
```

### **2. Create & Activate a Virtual Environment**

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

### **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **4. Initialize the Database**

Run Python:

```python
from market import db
db.create_all()
```

This creates `instance/market.db`.

### **5. Run the Application**

```bash
python run.py
```

Visit:
👉 **[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 🧠 **How the Marketplace Works**

### Buying an Item

* User clicks **Purchase**
* System checks:

  * Sufficient budget
  * Item not owned by user
* Database updates:

  * Buyer’s budget decreases
  * Seller’s budget increases
  * Item owner changes

### Selling an Item

* User enters a selling price
* Item becomes available in the marketplace

### Listing a New Item

* User fills out the “List Item” modal
* Item is automatically added to market with user as owner

---

## 📌 **Future Improvements**

* Add product images for each item
* Search bar and category filters
* Admin panel for item/user management
* Paginated items list

---

## 📄 **License**

Free to use for learning or for building on top of it.
