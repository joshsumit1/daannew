# 🤝 Daan Project – Connecting NGOs with Donors & Helpers

**Daan** is a full-stack donation and coordination platform that connects **NGOs**, **donors**, and **helpers**. Built with Flask and Stripe, it allows NGOs to register, launch campaigns, receive donations, and communicate with contributors — all within a secure, point-based system.

> ⚙️ Designed for transparency and ease of donation in social good projects.

---

## 🚀 Features

- 🧾 NGO & Donor registration
- 💳 Stripe-based secure payments
- 📦 Campaign creation & management
- 📤 Certificate uploads (NGO validation)
- 📷 Donor profile updates with photo uploads
- 📨 Messaging system between NGOs
- 🧮 Points-based donation records
- 📈 CSV/PDF donation reports
- 🎯 Simple SQLite3 database
- 📊 Donor dashboard with history


---

## 🧑‍💻 Tech Stack

- **Backend**: Python (Flask)
- **Database**: SQLite3 (via SQLAlchemy)
- **Payments**: Stripe
- **Frontend**: Jinja2 (HTML templating)
- **Storage**: Local for uploads (certificates, photos)

---

## 🛠️ Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/joshsumit1/daan-project.git
cd daan-project
2. Create a Virtual Environment
bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
pip install -r requirements.txt
Make sure your requirements.txt includes:

nginx
Flask
Flask_SQLAlchemy
stripe
Werkzeug
4. Configure Stripe API
Create a .env file or replace directly in app.py:

python
stripe.api_key = 'sk_test_yourSecretKeyHere'
🔒 Replace with your real Stripe secret key.

5. Run the App
bash
python app.py
Visit: http://localhost:5000
