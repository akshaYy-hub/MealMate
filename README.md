# 🍽️ MealMate – Online Food Ordering System

MealMate is a Django-based web application that allows users to browse restaurants, view menus, add items to cart, and place food orders with online payment integration.

---

## 🚀 Features

- User Authentication (Sign Up / Sign In)
- Browse Restaurants
- View Restaurant Menus
- Add Items to Cart
- Increase / Decrease Item Quantity
- View Cart Summary
- Checkout and Place Orders
- Razorpay Payment Integration (Test Mode)
- Order Success Page
- Admin can manage restaurants and menu items

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **Payment Gateway:** Razorpay
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

MealMate/
│
├── delivery/ # Main app (views, models, urls)
├── mealmate/ # Project configuration
├── templates/ # HTML templates
├── static/ # CSS files
├── manage.py
├── db.sqlite3


---

## ⚙️ How to Run the Project Locally

1. Clone the repository
```bash
git clone https://github.com/akshaY-hub/MealMate.git


Navigate into the project directory

cd MealMate


Install required dependencies

pip install django razorpay


Apply database migrations

python manage.py migrate


Start the development server

python manage.py runserver


Open the application in your browser

http://127.0.0.1:8000/

💳 Payment Information

Razorpay is integrated in test mode

Use Razorpay test card details for payments

No real money is charged

📌 Future Enhancements

Order history page

Email notifications

Cloud deployment

Improved UI/UX

Role-based access (Admin / User)

👨‍💻 Author

Akshay

⭐ Support

If you like this project, please give it a ⭐ on GitHub.
