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
Copy
Edit
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
Make sure your requirements.txt includes:

nginx
Copy
Edit
Flask
Flask_SQLAlchemy
stripe
Werkzeug
4. Configure Stripe API
Create a .env file or replace directly in app.py:

python
Copy
Edit
stripe.api_key = 'sk_test_yourSecretKeyHere'
🔒 Replace with your real Stripe secret key.

5. Run the App
bash
Copy
Edit
python app.py
Visit: http://localhost:5000

🧾 Available Routes
Route	Description
/	Home page
/about	About page
/donate	Donation form
/process_payment	Handle Stripe payment + DB entry
/register/donor	Donor registration
/donor_dashboard/<id>	Donor dashboard with donation history
/ngo_register	NGO registration with certificate
/ngo_dashboard	NGO management interface
/campaigns	Create/view campaigns
/messages	NGO-to-NGO messaging system
/uploads/<filename>	Serve uploaded certificates/photos
/update_profile	Update donor profile (photo, phone)
/donations_report	Download all donations (CSV/PDF)
/ngo_report/<id>	NGO profile report

🎯 Points System (Concept)
Each donor’s contribution is stored and could be mapped to a points system for future:

1 USD = 1 point (or configurable)

Used to reward top contributors

Visible in dashboards or rankings (future scope)

📌 Future Improvements
 Admin dashboard

 Real-time notifications

 Donor leaderboards

 Email alerts on donation/message

 Volunteer system integration

 Convert to PostgreSQL (for production)
