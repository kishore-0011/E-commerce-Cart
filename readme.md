# ElectroShop - Django E-commerce Shopping Cart

Django-based shopping cart system that allows users to browse products and manage their shopping cart with proper inventory management and business rules.


## Features

- **Product Catalog**: Browse electronics with filtering and search
- **Shopping Cart**: Session-based cart for guests and authenticated users
- **User Authentication**: Register, login, and logout functionality
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS
- **Modern UI**: Clean, professional design with Font Awesome icons
- **Advanced Filtering**: Filter by category, price range, and search
- **Real-time Updates**: AJAX cart operations without page reload

## Tech Stack

- **Backend**: Django 4.2
- **Database**: SQLite 
- **Frontend**: Django Templates + Bootstrap/Tailwind CSS
- **Authentication**: Django's built-in authentication system
- **Session Management**: Django sessions for cart persistence

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kishore-0011/E-commerce-Cart.git
cd EcommerceCart
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install requirements.txt
```

## Database Setup

### Step 1: Create Migrations

```bash
python manage.py makemigrations
```

### Step 2: Apply Migrations

```bash
python manage.py migrate
```

### Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

**Add these credentials**
- Username 
- Email (optional)
- Password (minimum 8 characters)

### Step 6: Load Sample Data

```bash
python manage.py populate_db
```

## Running the Development Server

```bash
python manage.py runserver
```

**Access the application:**
- Main Site: http://127.0.0.1:8000/
- Cart: http://127.0.0.1:8000/cart/
- Admin Panel: http://127.0.0.1:8000/admin/
- Login: http://127.0.0.1:8000/accounts/login/
- Register: http://127.0.0.1:8000/accounts/register/

## Admin Panel Access

1. Navigate to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Manage:
   - Products (add, edit, delete)
   - Categories
   - Users

## User Workflows

### Guest User Flow
1. Browse products without logging in
2. Search and filter products
3. Add items to cart (session-based)
4. Click "Proceed to Checkout" → Redirected to login

### Registered User Flow
1. Register an account
2. Login automatically after registration
3. Browse and add items to cart
4. Proceed to checkout (placeholder)
5. Logout when done

## API Endpoints

### Shop URLs
- `/` - Product listing page
- `/cart/` - Shopping cart
- `/cart/add/<id>/` - Add product to cart (POST)
- `/cart/remove/<id>/` - Remove from cart (POST)
- `/cart/update/<id>/` - Update quantity (POST)
- `/checkout/` - Checkout page (login required)

### Authentication URLs
- `/accounts/register/` - User registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout (POST)