# Backend Setup Guide

## Prerequisites
- Python 3.8+
- MySQL Server running
- pip

## Installation

1. **Create MySQL Database**
   ```sql
   CREATE DATABASE photolounge_db;
   ```

2. **Import Schema**
   ```bash
   mysql -u root -p photolounge_db < database/schema.sql
   ```

3. **Install Python Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your MySQL credentials:
   ```
   DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/photolounge_db
   JWT_SECRET_KEY=your-secret-key-change-this
   FLASK_ENV=development
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

## Database Structure

### Tables
- **owner** - Owner/Admin accounts
- **services** - Photography services offered
- **inquiries** - Customer inquiries/leads
- **bookings** - Confirmed bookings
- **gallery** - Portfolio images
- **testimonials** - Client reviews
- **sessions** - Owner login sessions

## Authentication

All owner routes require JWT token in the `Authorization` header:
```
Authorization: Bearer <token>
```

## API Routes Overview

### Public Routes (No Auth Required)
- `POST /api/inquiry` - Submit inquiry
- `GET /api/services` - Get services
- `GET /api/gallery` - Get gallery

### Owner Routes (Auth Required)

#### Authentication
- `POST /api/auth/register` - Register new owner
- `POST /api/auth/login` - Owner login

#### Profile
- `GET /api/owner/profile` - Get profile
- `PUT /api/owner/profile` - Update profile

#### Services
- `GET /api/owner/services` - List services
- `POST /api/owner/services` - Create service
- `PUT /api/owner/services/<id>` - Update service
- `DELETE /api/owner/services/<id>` - Delete service

#### Inquiries
- `GET /api/owner/inquiries` - List inquiries
- `PUT /api/owner/inquiries/<id>` - Update inquiry

#### Bookings
- `GET /api/owner/bookings` - List bookings
- `POST /api/owner/bookings` - Create booking
- `PUT /api/owner/bookings/<id>` - Update booking

#### Gallery
- `GET /api/owner/gallery` - List gallery
- `POST /api/owner/gallery` - Add gallery image
