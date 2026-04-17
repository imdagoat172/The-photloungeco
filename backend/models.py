from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Owner(db.Model):
    """Owner/Admin model"""
    __tablename__ = 'owner'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    business_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    services = db.relationship('Service', backref='owner', lazy=True, cascade='all, delete-orphan')
    inquiries = db.relationship('Inquiry', backref='owner', lazy=True, cascade='all, delete-orphan')
    bookings = db.relationship('Booking', backref='owner', lazy=True, cascade='all, delete-orphan')
    gallery = db.relationship('Gallery', backref='owner', lazy=True, cascade='all, delete-orphan')
    testimonials = db.relationship('Testimonial', backref='owner', lazy=True, cascade='all, delete-orphan')
    sessions = db.relationship('Session', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'business_name': self.business_name,
            'phone': self.phone,
            'created_at': self.created_at.isoformat()
        }

class Service(db.Model):
    """Service offered by owner"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    duration_hours = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'duration_hours': self.duration_hours,
            'is_active': self.is_active
        }

class Inquiry(db.Model):
    """Customer inquiry"""
    __tablename__ = 'inquiries'
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    event_type = db.Column(db.String(50))
    event_date = db.Column(db.Date)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, contacted, converted, archived
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'event_type': self.event_type,
            'event_date': self.event_date.isoformat() if self.event_date else None,
            'message': self.message,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class Booking(db.Model):
    """Confirmed booking"""
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    inquiry_id = db.Column(db.Integer, db.ForeignKey('inquiries.id'), nullable=True)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(100), nullable=False)
    client_phone = db.Column(db.String(20))
    event_date = db.Column(db.Date, nullable=False)
    event_location = db.Column(db.String(255))
    total_amount = db.Column(db.Float)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    service = db.relationship('Service', backref='bookings')
    inquiry = db.relationship('Inquiry', backref='bookings')
    
    def to_dict(self):
        return {
            'id': self.id,
            'service_id': self.service_id,
            'inquiry_id': self.inquiry_id,
            'client_name': self.client_name,
            'client_email': self.client_email,
            'client_phone': self.client_phone,
            'event_date': self.event_date.isoformat(),
            'event_location': self.event_location,
            'total_amount': self.total_amount,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

class Gallery(db.Model):
    """Portfolio gallery"""
    __tablename__ = 'gallery'
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(150))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    display_order = db.Column(db.Integer)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'image_url': self.image_url,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'is_featured': self.is_featured
        }

class Testimonial(db.Model):
    """Client testimonial/review"""
    __tablename__ = 'testimonials'
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer)  # 1-5 stars
    review = db.Column(db.Text)
    event_type = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'client_name': self.client_name,
            'rating': self.rating,
            'review': self.review,
            'event_type': self.event_type,
            'created_at': self.created_at.isoformat()
        }

class Session(db.Model):
    """Owner session tokens"""
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
