import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

from config import config
from models import db, Owner, Inquiry, Service, Booking, Gallery, Testimonial

app = Flask(__name__)

# Load configuration
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Initialize extensions
db.init_app(app)
CORS(app)

# ==================== Authentication Routes ====================

def token_required(f):
    """Decorator to verify JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_owner = Owner.query.get(data['owner_id'])
            if not current_owner:
                return jsonify({'message': 'Invalid token'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_owner, *args, **kwargs)
    return decorated

def generate_token(owner_id):
    """Generate JWT token for owner"""
    payload = {
        'owner_id': owner_id,
        'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
    }
    return jwt.encode(payload, app.config['JWT_SECRET_KEY'], algorithm='HS256')

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new owner"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'password', 'name', 'business_name']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    if Owner.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 409
    
    owner = Owner(
        email=data['email'],
        name=data['name'],
        business_name=data['business_name'],
        phone=data.get('phone')
    )
    owner.set_password(data['password'])
    
    db.session.add(owner)
    db.session.commit()
    
    token = generate_token(owner.id)
    return jsonify({
        'message': 'Registration successful',
        'owner': owner.to_dict(),
        'token': token
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Owner login"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'password']):
        return jsonify({'message': 'Missing email or password'}), 400
    
    owner = Owner.query.filter_by(email=data['email']).first()
    if not owner or not owner.check_password(data['password']):
        return jsonify({'message': 'Invalid email or password'}), 401
    
    token = generate_token(owner.id)
    return jsonify({
        'message': 'Login successful',
        'owner': owner.to_dict(),
        'token': token
    }), 200

# ==================== Owner Dashboard Routes ====================

@app.route('/api/owner/profile', methods=['GET'])
@token_required
def get_owner_profile(current_owner):
    """Get owner profile"""
    return jsonify(current_owner.to_dict()), 200

@app.route('/api/owner/profile', methods=['PUT'])
@token_required
def update_owner_profile(current_owner):
    """Update owner profile"""
    data = request.get_json()
    
    if 'name' in data:
        current_owner.name = data['name']
    if 'business_name' in data:
        current_owner.business_name = data['business_name']
    if 'phone' in data:
        current_owner.phone = data['phone']
    
    db.session.commit()
    return jsonify({
        'message': 'Profile updated successfully',
        'owner': current_owner.to_dict()
    }), 200

# ==================== Services Routes ====================

@app.route('/api/services', methods=['GET'])
def get_public_services():
    """Get all public services"""
    owner_id = request.args.get('owner_id', type=int)
    if owner_id:
        services = Service.query.filter_by(owner_id=owner_id, is_active=True).all()
    else:
        services = Service.query.filter_by(is_active=True).all()
    
    return jsonify([s.to_dict() for s in services]), 200

@app.route('/api/owner/services', methods=['GET'])
@token_required
def get_owner_services(current_owner):
    """Get owner's services"""
    services = Service.query.filter_by(owner_id=current_owner.id).all()
    return jsonify([s.to_dict() for s in services]), 200

@app.route('/api/owner/services', methods=['POST'])
@token_required
def create_service(current_owner):
    """Create new service"""
    data = request.get_json()
    
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({'message': 'Missing required fields'}), 400
    
    service = Service(
        owner_id=current_owner.id,
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        duration_hours=data.get('duration_hours'),
        is_active=data.get('is_active', True)
    )
    
    db.session.add(service)
    db.session.commit()
    
    return jsonify({
        'message': 'Service created successfully',
        'service': service.to_dict()
    }), 201

@app.route('/api/owner/services/<int:service_id>', methods=['PUT'])
@token_required
def update_service(current_owner, service_id):
    """Update service"""
    service = Service.query.get(service_id)
    
    if not service or service.owner_id != current_owner.id:
        return jsonify({'message': 'Service not found'}), 404
    
    data = request.get_json()
    if 'name' in data:
        service.name = data['name']
    if 'description' in data:
        service.description = data['description']
    if 'price' in data:
        service.price = data['price']
    if 'duration_hours' in data:
        service.duration_hours = data['duration_hours']
    if 'is_active' in data:
        service.is_active = data['is_active']
    
    db.session.commit()
    return jsonify({
        'message': 'Service updated successfully',
        'service': service.to_dict()
    }), 200

@app.route('/api/owner/services/<int:service_id>', methods=['DELETE'])
@token_required
def delete_service(current_owner, service_id):
    """Delete service"""
    service = Service.query.get(service_id)
    
    if not service or service.owner_id != current_owner.id:
        return jsonify({'message': 'Service not found'}), 404
    
    db.session.delete(service)
    db.session.commit()
    
    return jsonify({'message': 'Service deleted successfully'}), 200

# ==================== Inquiries Routes ====================

@app.route('/api/inquiry', methods=['POST'])
def submit_inquiry():
    """Submit new inquiry (public)"""
    data = request.get_json()
    owner_id = data.get('owner_id', 1)  # Default to first owner for public form
    
    if not all(k in data for k in ['name', 'email']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    inquiry = Inquiry(
        owner_id=owner_id,
        name=data['name'],
        email=data['email'],
        phone=data.get('phone'),
        event_type=data.get('event_type'),
        event_date=data.get('event_date'),
        message=data.get('message'),
        status='pending'
    )
    
    db.session.add(inquiry)
    db.session.commit()
    
    return jsonify({
        'message': 'Inquiry submitted successfully',
        'inquiry_id': inquiry.id
    }), 201

@app.route('/api/owner/inquiries', methods=['GET'])
@token_required
def get_owner_inquiries(current_owner):
    """Get owner's inquiries"""
    status = request.args.get('status')
    query = Inquiry.query.filter_by(owner_id=current_owner.id)
    
    if status:
        query = query.filter_by(status=status)
    
    inquiries = query.order_by(Inquiry.created_at.desc()).all()
    return jsonify([i.to_dict() for i in inquiries]), 200

@app.route('/api/owner/inquiries/<int:inquiry_id>', methods=['PUT'])
@token_required
def update_inquiry(current_owner, inquiry_id):
    """Update inquiry status"""
    inquiry = Inquiry.query.get(inquiry_id)
    
    if not inquiry or inquiry.owner_id != current_owner.id:
        return jsonify({'message': 'Inquiry not found'}), 404
    
    data = request.get_json()
    if 'status' in data:
        inquiry.status = data['status']
    
    db.session.commit()
    return jsonify({
        'message': 'Inquiry updated successfully',
        'inquiry': inquiry.to_dict()
    }), 200

# ==================== Bookings Routes ====================

@app.route('/api/owner/bookings', methods=['GET'])
@token_required
def get_owner_bookings(current_owner):
    """Get owner's bookings"""
    status = request.args.get('status')
    query = Booking.query.filter_by(owner_id=current_owner.id)
    
    if status:
        query = query.filter_by(status=status)
    
    bookings = query.order_by(Booking.event_date).all()
    return jsonify([b.to_dict() for b in bookings]), 200

@app.route('/api/owner/bookings', methods=['POST'])
@token_required
def create_booking(current_owner):
    """Create new booking"""
    data = request.get_json()
    
    if not all(k in data for k in ['client_name', 'client_email', 'event_date']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    booking = Booking(
        owner_id=current_owner.id,
        service_id=data.get('service_id'),
        inquiry_id=data.get('inquiry_id'),
        client_name=data['client_name'],
        client_email=data['client_email'],
        client_phone=data.get('client_phone'),
        event_date=data['event_date'],
        event_location=data.get('event_location'),
        total_amount=data.get('total_amount'),
        status=data.get('status', 'pending'),
        notes=data.get('notes')
    )
    
    db.session.add(booking)
    db.session.commit()
    
    return jsonify({
        'message': 'Booking created successfully',
        'booking': booking.to_dict()
    }), 201

@app.route('/api/owner/bookings/<int:booking_id>', methods=['PUT'])
@token_required
def update_booking(current_owner, booking_id):
    """Update booking"""
    booking = Booking.query.get(booking_id)
    
    if not booking or booking.owner_id != current_owner.id:
        return jsonify({'message': 'Booking not found'}), 404
    
    data = request.get_json()
    if 'status' in data:
        booking.status = data['status']
    if 'event_date' in data:
        booking.event_date = data['event_date']
    if 'total_amount' in data:
        booking.total_amount = data['total_amount']
    if 'notes' in data:
        booking.notes = data['notes']
    
    db.session.commit()
    return jsonify({
        'message': 'Booking updated successfully',
        'booking': booking.to_dict()
    }), 200

# ==================== Gallery Routes ====================

@app.route('/api/gallery', methods=['GET'])
def get_public_gallery():
    """Get public gallery"""
    owner_id = request.args.get('owner_id', type=int)
    if owner_id:
        gallery = Gallery.query.filter_by(owner_id=owner_id).order_by(Gallery.display_order).all()
    else:
        gallery = Gallery.query.order_by(Gallery.display_order).all()
    
    return jsonify([g.to_dict() for g in gallery]), 200

@app.route('/api/owner/gallery', methods=['GET'])
@token_required
def get_owner_gallery(current_owner):
    """Get owner's gallery"""
    gallery = Gallery.query.filter_by(owner_id=current_owner.id).order_by(Gallery.display_order).all()
    return jsonify([g.to_dict() for g in gallery]), 200

@app.route('/api/owner/gallery', methods=['POST'])
@token_required
def add_gallery_image(current_owner):
    """Add image to gallery"""
    data = request.get_json()
    
    if 'image_url' not in data:
        return jsonify({'message': 'Image URL required'}), 400
    
    image = Gallery(
        owner_id=current_owner.id,
        image_url=data['image_url'],
        title=data.get('title'),
        description=data.get('description'),
        category=data.get('category'),
        display_order=data.get('display_order', 0),
        is_featured=data.get('is_featured', False)
    )
    
    db.session.add(image)
    db.session.commit()
    
    return jsonify({
        'message': 'Image added to gallery',
        'image': image.to_dict()
    }), 201

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)