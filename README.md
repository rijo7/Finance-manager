# Finance Manager - Django Web App

**Live Site:** [https://web-production-b68bc.up.railway.app](https://web-production-b68bc.up.railway.app)

---

## 📖 Overview

Finance Manager is a Django web application for tracking income and expenses.  
Users can register, log in, add transactions, view summaries, and export transaction history as a PDF.  

---

## ✨ Features

- User registration and login
- Dashboard with transaction summary
- Income and expense categories with subcategories
- PDF export of transactions
- Secure user authentication
- PostgreSQL database (Supabase)
- Production-ready deployment with Gunicorn and Railway

---

## 🚀 Tech Stack

- **Backend:** Django 5.2
- **Frontend:** Django Templates, HTML, CSS
- **Database:** Supabase (PostgreSQL)
- **Deployment:** Railway
- **PDF Generation:** pdfkit / wkhtmltopdf
- **Static Files:** Whitenoise

---

## ⚙️ Setup & Installation

1. **Clone this repo:**
   ```bash
   git clone https://github.com/rijo7/Finance-manager.git
   ```
2. **Create virtual environment and activate it**

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your `.env` file with:**
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `ALLOWED_HOSTS`
   - `CSRF_TRUSTED_ORIGINS`

5. **Run migrations and create superuser:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Start development server:**
   ```bash
   python manage.py runserver
   ```

---

## ⚡ Deployment

- Railway (uses Gunicorn and a Dockerfile)
- Static files handled by Whitenoise

---

## 🌱 Database Seeding

A one-time `/seed/` view was used to create default categories and subcategories.  
This route should be removed after initial use.

---

## 🪪 License

MIT
