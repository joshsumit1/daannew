import stripe
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from flask import send_file


app = Flask(__name__)

# Stripe Configuration
stripe.api_key = 'sk_test_yourSecretKeyHere'  # Replace with your Stripe Secret Key

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ngo_donor.db'  # SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Models
class NGO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    certificate = db.Column(db.String(100), nullable=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('ngo.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('ngo.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship('NGO', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('NGO', foreign_keys=[receiver_id], backref='received_messages')


class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    photo = db.Column(db.String(100), nullable=True)  # Store the photo filename
    donations = db.relationship('Donation', backref='donor', lazy=True)

class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(20), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


# Create tables
with app.app_context():
    db.create_all()

# Helper Functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        amount = request.form.get('amount')
        donor_id = request.form.get('donor_id')

        # Initiate the Stripe payment process
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(float(amount) * 100),  # Amount in cents
                currency='usd',
                metadata={'donor_id': donor_id}
            )
            return render_template('donate.html', client_secret=intent.client_secret, donor_id=donor_id)
        except Exception as e:
            flash(str(e), 'danger')
            return redirect(url_for('donate'))

    return render_template('donate.html')

@app.route('/process_payment', methods=['POST'])
def process_payment():
    try:
        donor_id = request.form.get('donor_id')
        amount = request.form.get('amount')

        # Save the donation in the database
        donation = Donation(amount=float(amount), date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), donor_id=donor_id)
        db.session.add(donation)
        db.session.commit()

        flash("Payment successful!", 'success')
        return redirect(url_for('donor_dashboard', donor_id=donor_id))
    except Exception as e:
        flash(f"Payment failed: {str(e)}", 'danger')
        return redirect(url_for('donate'))


@app.route('/donor_dashboard/<int:donor_id>')
def donor_dashboard(donor_id):
    donor = Donor.query.get_or_404(donor_id)
    donations = Donation.query.filter_by(donor_id=donor.id).all()
    return render_template(
        'donor_dashboard.html',
        donor=donor,
        donations=donations
    )

@app.route('/register/donor', methods=['GET', 'POST'])
def donor_register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        # Add the donor to the database
        donor = Donor(name=name, email=email, phone=phone)
        db.session.add(donor)
        db.session.commit()

        return redirect(url_for('donor_dashboard', donor_id=donor.id))

    return render_template('donor_register.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/ngo_register', methods=['GET', 'POST'])
def ngo_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        certificate = request.files.get('certificate')

        # Save the certificate if it exists and is of allowed type
        if certificate and allowed_file(certificate.filename):
            filename = secure_filename(certificate.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            certificate.save(filepath)
        else:
            filename = None  # No certificate uploaded

        # Save the NGO details to the database
        ngo = NGO(name=name, email=email, password=password, certificate=filename)
        db.session.add(ngo)
        db.session.commit()

        return redirect(url_for('ngo_dashboard'))

    return render_template('ngo_register.html')

@app.route('/ngo_dashboard', methods=['GET', 'POST'])
def ngo_dashboard():
    ngos = NGO.query.all()
    selected_ngo = ngos[0] if ngos else None  # Default to the first NGO for demo

    # Handle search functionality
    search_query = request.args.get('search', '')
    if search_query:
        ngos = NGO.query.filter(NGO.name.like(f"%{search_query}%")).all()

    return render_template(
        'ngo_dashboard.html',
        ngos=ngos,
        selected_ngo=selected_ngo,
        search_query=search_query
    )



@app.route('/update_profile', methods=['POST'])
def update_profile():
    donor_id = request.form.get('donor_id')  # Ensure you're sending the donor's ID in the form
    donor = Donor.query.get(donor_id)  # Fetch the donor from the database

    if donor is None:
        flash('Donor not found.', 'danger')
        return redirect(url_for('donor_dashboard', donor_id=donor_id))  # Redirect back to the donor's dashboard

    # Handling photo upload
    photo = request.files.get('photo')
    phone = request.form.get('phone')

    if photo:
        # Save the uploaded photo to the appropriate folder
        photo_path = f"static/uploads/{secure_filename(photo.filename)}"
        photo.save(photo_path)

        # Update the donor's photo URL in the database
        donor.photo = photo_path

    if phone:
        donor.phone = phone  # Update the phone number if provided

    # Commit the changes to the database
    db.session.commit()

    flash('Profile updated successfully!', 'success')
    return redirect(url_for('donor_dashboard', donor_id=donor.id))

@app.route('/campaigns', methods=['GET', 'POST'])
def manage_campaigns():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        # Save campaign logic here
    campaigns = Campaign.query.all()
    return render_template('campaigns.html', campaigns=campaigns)

@app.route('/donations_report')
def download_report():
    donations = Donation.query.all()
    # Generate CSV or PDF report logic
    return send_file('donations_report.csv', as_attachment=True)

@app.route('/ngo_report/<int:ngo_id>')
def ngo_report(ngo_id):
    ngo = NGO.query.get_or_404(ngo_id)
    return render_template('ngo_report.html', ngo=ngo)

  

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    ngos = NGO.query.all()

    if request.method == 'POST':
        sender_id = request.form['sender_id']
        receiver_id = request.form['receiver_id']
        content = request.form['content']

        new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('messages'))

    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('messages.html', ngos=ngos, messages=messages)


if __name__ == '__main__':
    app.run(debug=True)
