import re
from urllib.parse import quote, quote_plus
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date

from world_data import countries, REGIONS
from bd_data import destinations

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'tripnest_secret_key_2026'
db = SQLAlchemy(app)

# ---- CHANGE THIS to your own phone number. Whoever signs up with it becomes admin. ----
ADMIN_PHONE = '01700000000'

GUIDE_FEE = 1500  # per day

# ---------------- hotel packages ----------------
# 'base' = estimated price (BDT) per room per night. Real price = base x place factor.
PACKAGES = [
    {'id': 'eco', 'tier': 'Budget', 'name': 'Economy Room', 'icon': '🛏️', 'base': 1200,
     'stay': True, 'ac': False, 'room': 'Normal', 'meal': 'No meals', 'pool': False, 'wifi': False,
     'desc': 'Fan, attached bath. Simple and cheap.'},
    {'id': 'budget_ac', 'tier': 'Budget', 'name': 'Budget AC Room', 'icon': '❄️', 'base': 2200,
     'stay': True, 'ac': True, 'room': 'Normal', 'meal': 'Complimentary breakfast', 'pool': False, 'wifi': True,
     'desc': 'AC room with free breakfast.'},
    {'id': 'business', 'tier': 'Standard', 'name': 'Business Room', 'icon': '💼', 'base': 3800,
     'stay': True, 'ac': True, 'room': 'Business', 'meal': 'Complimentary breakfast', 'pool': False, 'wifi': True,
     'desc': 'Work desk, fast Wi-Fi, quiet floor.'},
    {'id': 'resort', 'tier': 'Premium', 'name': 'Resort Room (Pool)', 'icon': '🏖️', 'base': 6000,
     'stay': True, 'ac': True, 'room': 'Normal', 'meal': 'Breakfast buffet', 'pool': True, 'wifi': True,
     'desc': 'Resort stay with swimming pool.'},
    {'id': 'premium', 'tier': 'Premium', 'name': 'Premium Buffet Package', 'icon': '🍽️', 'base': 9500,
     'stay': True, 'ac': True, 'room': 'Business', 'meal': 'A to Z buffet (3 meals)', 'pool': True, 'wifi': True,
     'desc': 'Business room, pool and full buffet all day.'},
    {'id': 'luxury', 'tier': 'Luxury', 'name': 'Luxury Suite', 'icon': '👑', 'base': 15000,
     'stay': True, 'ac': True, 'room': 'Suite', 'meal': 'Full buffet (3 meals)', 'pool': True, 'wifi': True,
     'desc': 'Suite with spa access and airport/station pickup.'},
    {'id': 'daytrip', 'tier': 'Day trip', 'name': 'Day trip (no hotel)', 'icon': '🎒', 'base': 0,
     'stay': False, 'ac': False, 'room': '-', 'meal': '-', 'pool': False, 'wifi': False,
     'desc': 'Just visit and return. No hotel needed.'},
]

# Price multiplier by division, and special cases for some places.
DIVISION_FACTOR = {
    'Dhaka': 1.3, 'Chattogram': 1.1, 'Sylhet': 1.1, 'Khulna': 1.0,
    'Rajshahi': 0.9, 'Barishal': 0.9, 'Rangpur': 0.85, 'Mymensingh': 0.9,
}
PLACE_FACTOR = {
    "Cox's Bazar": 1.35, "Cox's Bazar Marine Drive": 1.35,
    "Saint Martin's Island": 1.3, 'Sajek Valley': 1.25, 'Kuakata': 1.0,
}

# Add REAL hotels here when you have them (fixed price, id must be 20 characters or less).
# SPECIAL_PACKAGES = {
#     "Cox's Bazar": [
#         {'id': 'cox_hotel1', 'tier': 'Premium', 'name': 'Your Hotel Name', 'icon': '🏨', 'price': 7000,
#          'stay': True, 'ac': True, 'room': 'Normal', 'meal': 'Breakfast buffet', 'pool': True, 'wifi': True,
#          'desc': 'Sea view, 5 minutes from beach.'},
#     ],
# }
SPECIAL_PACKAGES = {}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100))
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    place = db.Column(db.String(200), nullable=False)
    kind = db.Column(db.String(10), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100))
    departure_city = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    adults = db.Column(db.Integer, nullable=False)
    children = db.Column(db.Integer, default=0)
    rooms = db.Column(db.Integer, default=1)
    hotel_type = db.Column(db.String(20), nullable=False)   # stores the package id
    transport = db.Column(db.String(20), nullable=False)    # kept for old data, always 'None' now
    guide = db.Column(db.Boolean, default=False)
    note = db.Column(db.String(300))
    total_price = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def ref(self):
        return 'TN-' + str(self.id).zfill(6)

    @property
    def nights(self):
        return (self.end_date - self.start_date).days


with app.app_context():
    db.create_all()


# ---------------- helpers ----------------
def clean_phone(raw):
    p = re.sub(r'[\s\-()]', '', raw or '')
    if p.startswith('+880'):
        p = '0' + p[4:]
    elif p.startswith('880') and len(p) == 13:
        p = '0' + p[3:]
    if re.fullmatch(r'01[3-9]\d{8}', p):
        return p
    if re.fullmatch(r'\+\d{8,15}', p):
        return p
    return None


def is_admin():
    return session.get('user_phone') == ADMIN_PHONE


def place_factor(place, kind):
    if kind != 'bd':
        return 1.0
    if place in PLACE_FACTOR:
        return PLACE_FACTOR[place]
    division = next((d['division'] for d in destinations if d['name'] == place), None)
    return DIVISION_FACTOR.get(division, 1.0)


def packages_for(place, kind):
    factor = place_factor(place, kind)
    result = []
    for p in PACKAGES:
        item = dict(p)
        item['price'] = int(round(p['base'] * factor / 50.0)) * 50
        result.append(item)
    result.extend(dict(s) for s in SPECIAL_PACKAGES.get(place, []))
    return result


def get_package(pid, place, kind):
    return next((p for p in packages_for(place, kind) if p['id'] == pid), None)


@app.context_processor
def inject_helpers():
    def pkg_name(pid):
        for p in PACKAGES:
            if p['id'] == pid:
                return p['name']
        for lst in SPECIAL_PACKAGES.values():
            for p in lst:
                if p['id'] == pid:
                    return p['name']
        return pid
    return {'is_admin': is_admin(), 'pkg_name': pkg_name}


def admin_required():
    if 'user_id' not in session:
        flash('Please login.')
        return redirect(url_for('login'))
    if not is_admin():
        abort(403)
    return None


def build_links(origin, place):
    d = quote_plus(place)
    route = 'https://www.google.com/maps/dir/?api=1&destination=' + d
    if origin:
        route += '&origin=' + quote_plus(origin)
    flight_q = 'Flights ' + ('from ' + origin + ' ' if origin else '') + 'to ' + place
    return {
        'drive': route + '&travelmode=driving',
        'transit': route + '&travelmode=transit',
        'flights': 'https://www.google.com/travel/flights?q=' + quote(flight_q),
        'hotels_map': 'https://www.google.com/maps/search/?api=1&query=' + quote_plus('hotels in ' + place),
        'booking': 'https://www.booking.com/searchresults.html?ss=' + d,
        'train': 'https://eticket.railway.gov.bd',
        'bus': 'https://www.shohoz.com/bus-tickets',
        'biman': 'https://www.biman-airlines.com',
    }


# ---------------- public pages ----------------
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/destinations')
def destinations_page():
    session['section'] = 'bd'
    query = request.args.get('search', '').strip()
    if query:
        q = query.lower()
        filtered = [
            d for d in destinations
            if q in d['name'].lower() or q in d['division'].lower()
        ]
    else:
        filtered = destinations
    return render_template('destinations.html', destinations=filtered, search_query=query)


@app.route('/world')
def world():
    session['section'] = 'world'
    search_query = request.args.get('search', '').strip()
    region = request.args.get('region', 'All')
    result = countries

    if region != 'All':
        result = [c for c in result if c['region'] == region]

    if search_query:
        q = search_query.lower()
        result = [
            c for c in result
            if q in c['name'].lower() or any(q in s.lower() for s in c['spots'])
        ]

    return render_template(
        'world.html',
        countries=result,
        search_query=search_query,
        region=region,
        regions=REGIONS,
        total=len(countries),
    )


@app.route('/world/<code>')
def country_page(code):
    session['section'] = 'world'
    country = next((c for c in countries if c['code'] == code.lower()), None)
    if country is None:
        abort(404)
    return render_template('country.html', country=country)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        text = request.form['message'].strip()

        if not name or not email or not text:
            flash('Please fill in all fields.')
            return redirect(url_for('contact'))

        db.session.add(Message(name=name, email=email, text=text))
        db.session.commit()
        flash('Thank you! Your message has been sent.')
        return redirect(url_for('contact'))

    return render_template('contact.html')


# ---------------- logged-in pages ----------------
@app.route('/book', methods=['GET', 'POST'])
def book():
    if 'user_id' not in session:
        flash('Please login to book a trip.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        f = request.form
        place = f.get('place', '').strip()
        kind = f.get('kind', 'bd')
        if kind not in ('bd', 'world'):
            kind = 'bd'

        if not place:
            flash('Please choose a destination first.')
            return redirect(url_for('destinations_page'))

        def back():
            return redirect(url_for('book', place=place, kind=kind))

        full_name = f.get('full_name', '').strip()
        phone = clean_phone(f.get('phone', ''))
        email = f.get('email', '').strip()
        departure_city = f.get('departure_city', '').strip()
        hotel_type = f.get('hotel_type', '')
        guide = f.get('guide') == 'yes'
        note = f.get('note', '').strip()[:300]

        if not (full_name and departure_city):
            flash('Please fill in all required fields.')
            return back()

        if phone is None:
            flash('Please enter a valid phone number (e.g. 01XXXXXXXXX).')
            return back()

        pkg = get_package(hotel_type, place, kind)
        if pkg is None:
            flash('Please choose a hotel package.')
            return back()

        try:
            start_date = datetime.strptime(f.get('start_date', ''), '%Y-%m-%d').date()
            end_date = datetime.strptime(f.get('end_date', ''), '%Y-%m-%d').date()
            adults = int(f.get('adults', '0'))
            children = int(f.get('children', '0'))
            rooms = int(f.get('rooms', '0'))
        except ValueError:
            flash('Please enter valid dates and numbers.')
            return back()

        if start_date < date.today():
            flash('Start date cannot be in the past.')
            return back()
        if end_date <= start_date:
            flash('Return date must be after the start date.')
            return back()

        nights = (end_date - start_date).days
        if nights > 30:
            flash('A single booking can be at most 30 nights.')
            return back()
        if adults < 1 or adults > 20 or children < 0 or children > 20:
            flash('Please check the number of adults and children.')
            return back()
        if rooms < 1 or rooms > 10:
            flash('Rooms must be between 1 and 10.')
            return back()

        total = pkg['price'] * rooms * nights + (GUIDE_FEE * nights if guide else 0)

        booking = Booking(
            user_id=session['user_id'],
            place=place, kind=kind,
            full_name=full_name, phone=phone, email=email,
            departure_city=departure_city,
            start_date=start_date, end_date=end_date,
            adults=adults, children=children, rooms=rooms,
            hotel_type=hotel_type, transport='None', guide=guide,
            note=note, total_price=total,
        )
        db.session.add(booking)
        db.session.commit()
        flash('Booking request received!')
        return redirect(url_for('booking_done', booking_id=booking.id))

    place = request.args.get('place', '').strip()
    kind = request.args.get('kind', 'bd')
    if kind not in ('bd', 'world'):
        kind = 'bd'
    if not place:
        return redirect(url_for('destinations_page'))
    session['section'] = kind

    user = db.session.get(User, session['user_id'])
    return render_template(
        'book.html',
        place=place, kind=kind,
        today=date.today().isoformat(),
        user=user,
        packages=packages_for(place, kind),
        guide_fee=GUIDE_FEE,
    )


@app.route('/booking/<int:booking_id>')
def booking_done(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    booking = db.session.get(Booking, booking_id)
    if booking is None or (booking.user_id != session['user_id'] and not is_admin()):
        abort(404)
    pkg = get_package(booking.hotel_type, booking.place, booking.kind)
    links = build_links(booking.departure_city, booking.place)
    return render_template('booking_done.html', b=booking, pkg=pkg, links=links)


@app.route('/my-bookings')
def my_bookings():
    if 'user_id' not in session:
        flash('Please login to see your bookings.')
        return redirect(url_for('login'))
    items = (Booking.query
             .filter_by(user_id=session['user_id'])
             .order_by(Booking.created_at.desc())
             .all())
    return render_template('my_bookings.html', bookings=items)


@app.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    booking = db.session.get(Booking, booking_id)
    if booking is None or booking.user_id != session['user_id']:
        abort(404)
    booking.status = 'Cancelled'
    db.session.commit()
    flash('Booking cancelled.')
    return redirect(url_for('my_bookings'))


# ---------------- admin only ----------------
@app.route('/admin')
def admin():
    denied = admin_required()
    if denied:
        return denied
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    users = User.query.order_by(User.created_at.desc()).all()
    pending = sum(1 for b in bookings if b.status == 'Pending')
    return render_template('admin.html', bookings=bookings, users=users, pending=pending)


@app.route('/admin/booking/<int:booking_id>/status', methods=['POST'])
def admin_set_status(booking_id):
    denied = admin_required()
    if denied:
        return denied
    status = request.form.get('status', '')
    if status not in ('Pending', 'Confirmed', 'Cancelled'):
        abort(400)
    booking = db.session.get(Booking, booking_id)
    if booking is None:
        abort(404)
    booking.status = status
    db.session.commit()
    flash('Booking ' + booking.ref + ' marked as ' + status + '.')
    return redirect(url_for('admin'))


@app.route('/messages')
def messages():
    denied = admin_required()
    if denied:
        return denied
    all_messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('messages.html', messages=all_messages)


# ---------------- accounts (login + signup share one page) ----------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = clean_phone(request.form.get('phone', ''))
        email = request.form.get('email', '').strip() or None
        password = request.form.get('password', '')

        if not name:
            flash('Please enter your name.')
            return redirect(url_for('signup'))
        if phone is None:
            flash('Please enter a valid phone number (e.g. 01XXXXXXXXX).')
            return redirect(url_for('signup'))
        if len(password) < 6:
            flash('Password must be at least 6 characters.')
            return redirect(url_for('signup'))

        if User.query.filter_by(phone=phone).first():
            flash('This phone number is already registered. Please login.')
            return redirect(url_for('login'))

        new_user = User(name=name, phone=phone, email=email,
                        password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully! Please login.')
        return redirect(url_for('login'))

    return render_template('login.html', tab='signup')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = clean_phone(request.form.get('phone', ''))
        password = request.form.get('password', '')

        user = User.query.filter_by(phone=phone).first() if phone else None
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_phone'] = user.phone
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid phone number or password.')
            return redirect(url_for('login'))

    return render_template('login.html', tab='login')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_phone', None)
    flash('Logged out successfully.')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)