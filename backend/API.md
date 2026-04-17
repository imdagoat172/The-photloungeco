# API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication

Owner routes require JWT token:
```
Authorization: Bearer <token>
```

---

## Public Routes

### 1. Submit Inquiry
**POST** `/inquiry`

Request:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-1234",
  "event_type": "Wedding",
  "event_date": "2024-06-15",
  "message": "Interested in wedding photography",
  "owner_id": 1
}
```

Response (201):
```json
{
  "message": "Inquiry submitted successfully",
  "inquiry_id": 1
}
```

---

### 2. Get Services
**GET** `/services?owner_id=1`

Response:
```json
[
  {
    "id": 1,
    "name": "Wedding",
    "description": "Full day coverage",
    "price": 795.00,
    "duration_hours": 8,
    "is_active": true
  }
]
```

---

### 3. Get Gallery
**GET** `/gallery?owner_id=1`

Response:
```json
[
  {
    "id": 1,
    "image_url": "https://example.com/image.jpg",
    "title": "Wedding",
    "description": "Beautiful wedding shot",
    "category": "Wedding",
    "is_featured": true
  }
]
```

---

## Owner Routes (Requires Authentication)

### Authentication

#### Register
**POST** `/auth/register`

Request:
```json
{
  "email": "owner@example.com",
  "password": "securepassword123",
  "name": "John Smith",
  "business_name": "Photo Lounge Co.",
  "phone": "555-0000"
}
```

Response (201):
```json
{
  "message": "Registration successful",
  "owner": {
    "id": 1,
    "name": "John Smith",
    "email": "owner@example.com",
    "business_name": "Photo Lounge Co.",
    "phone": "555-0000",
    "created_at": "2024-04-17T10:00:00"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

#### Login
**POST** `/auth/login`

Request:
```json
{
  "email": "owner@example.com",
  "password": "securepassword123"
}
```

Response (200):
```json
{
  "message": "Login successful",
  "owner": {
    "id": 1,
    "name": "John Smith",
    "email": "owner@example.com",
    "business_name": "Photo Lounge Co.",
    "phone": "555-0000",
    "created_at": "2024-04-17T10:00:00"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

---

### Owner Profile

#### Get Profile
**GET** `/owner/profile`

Headers:
```
Authorization: Bearer <token>
```

Response (200):
```json
{
  "id": 1,
  "name": "John Smith",
  "email": "owner@example.com",
  "business_name": "Photo Lounge Co.",
  "phone": "555-0000",
  "created_at": "2024-04-17T10:00:00"
}
```

---

#### Update Profile
**PUT** `/owner/profile`

Request:
```json
{
  "name": "Jane Smith",
  "business_name": "Updated Photo Lounge",
  "phone": "555-1111"
}
```

Response (200):
```json
{
  "message": "Profile updated successfully",
  "owner": { ... }
}
```

---

### Services Management

#### Get Services
**GET** `/owner/services`

Response (200):
```json
[
  {
    "id": 1,
    "name": "Wedding",
    "description": "Full day coverage",
    "price": 795.00,
    "duration_hours": 8,
    "is_active": true
  }
]
```

---

#### Create Service
**POST** `/owner/services`

Request:
```json
{
  "name": "Birthday Party",
  "description": "4-hour party coverage",
  "price": 495.00,
  "duration_hours": 4,
  "is_active": true
}
```

Response (201):
```json
{
  "message": "Service created successfully",
  "service": { ... }
}
```

---

#### Update Service
**PUT** `/owner/services/1`

Request:
```json
{
  "price": 850.00,
  "duration_hours": 10
}
```

Response (200):
```json
{
  "message": "Service updated successfully",
  "service": { ... }
}
```

---

#### Delete Service
**DELETE** `/owner/services/1`

Response (200):
```json
{
  "message": "Service deleted successfully"
}
```

---

### Inquiries Management

#### Get Inquiries
**GET** `/owner/inquiries?status=pending`

Response (200):
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-1234",
    "event_type": "Wedding",
    "event_date": "2024-06-15",
    "message": "Interested in wedding photography",
    "status": "pending",
    "created_at": "2024-04-17T10:00:00"
  }
]
```

---

#### Update Inquiry
**PUT** `/owner/inquiries/1`

Request:
```json
{
  "status": "contacted"
}
```

Response (200):
```json
{
  "message": "Inquiry updated successfully",
  "inquiry": { ... }
}
```

---

### Bookings Management

#### Get Bookings
**GET** `/owner/bookings?status=confirmed`

Response (200):
```json
[
  {
    "id": 1,
    "service_id": 1,
    "inquiry_id": 1,
    "client_name": "John Doe",
    "client_email": "john@example.com",
    "client_phone": "555-1234",
    "event_date": "2024-06-15",
    "event_location": "Grand Hotel",
    "total_amount": 795.00,
    "status": "confirmed",
    "created_at": "2024-04-17T10:00:00"
  }
]
```

---

#### Create Booking
**POST** `/owner/bookings`

Request:
```json
{
  "service_id": 1,
  "inquiry_id": 1,
  "client_name": "John Doe",
  "client_email": "john@example.com",
  "client_phone": "555-1234",
  "event_date": "2024-06-15",
  "event_location": "Grand Hotel",
  "total_amount": 795.00,
  "status": "confirmed",
  "notes": "Client wants 2 photographers"
}
```

Response (201):
```json
{
  "message": "Booking created successfully",
  "booking": { ... }
}
```

---

#### Update Booking
**PUT** `/owner/bookings/1`

Request:
```json
{
  "status": "completed",
  "notes": "Event went well"
}
```

Response (200):
```json
{
  "message": "Booking updated successfully",
  "booking": { ... }
}
```

---

### Gallery Management

#### Get Gallery
**GET** `/owner/gallery`

Response (200):
```json
[
  {
    "id": 1,
    "image_url": "https://example.com/image.jpg",
    "title": "Wedding",
    "description": "Beautiful wedding shot",
    "category": "Wedding",
    "is_featured": true
  }
]
```

---

#### Add Gallery Image
**POST** `/owner/gallery`

Request:
```json
{
  "image_url": "https://example.com/new-image.jpg",
  "title": "Sunset Wedding",
  "description": "Beautiful sunset photography",
  "category": "Wedding",
  "display_order": 1,
  "is_featured": true
}
```

Response (201):
```json
{
  "message": "Image added to gallery",
  "image": { ... }
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "message": "Missing required fields"
}
```

### 401 Unauthorized
```json
{
  "message": "Invalid token"
}
```

### 404 Not Found
```json
{
  "message": "Service not found"
}
```

### 409 Conflict
```json
{
  "message": "Email already registered"
}
```

### 500 Server Error
```json
{
  "message": "Internal server error"
}
```
