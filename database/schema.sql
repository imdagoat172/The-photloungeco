-- MySQL Schema for Photo Lounge Co.

CREATE TABLE owner (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    business_name VARCHAR(150) NOT NULL,
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE services (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    duration_hours INT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES owner(id) ON DELETE CASCADE
);

CREATE TABLE inquiries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    event_type VARCHAR(50),
    event_date DATE,
    message TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES owner(id) ON DELETE CASCADE
);

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    service_id INT NOT NULL,
    inquiry_id INT,
    client_name VARCHAR(100) NOT NULL,
    client_email VARCHAR(100) NOT NULL,
    client_phone VARCHAR(20),
    event_date DATE NOT NULL,
    event_location VARCHAR(255),
    total_amount DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'pending',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES owner(id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(id),
    FOREIGN KEY (inquiry_id) REFERENCES inquiries(id) ON DELETE SET NULL
);

CREATE TABLE gallery (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    image_url VARCHAR(255) NOT NULL,
    title VARCHAR(150),
    description TEXT,
    category VARCHAR(50),
    display_order INT,
    is_featured BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES owner(id) ON DELETE CASCADE
);

CREATE TABLE testimonials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    client_name VARCHAR(100) NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    event_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES owner(id) ON DELETE CASCADE
);

CREATE TABLE sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    owner_id INT NOT NULL,
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES owner(id) ON DELETE CASCADE
);

-- Create indexes for better query performance
CREATE INDEX idx_owner_id ON inquiries(owner_id);
CREATE INDEX idx_owner_id_services ON services(owner_id);
CREATE INDEX idx_owner_id_bookings ON bookings(owner_id);
CREATE INDEX idx_owner_id_gallery ON gallery(owner_id);
CREATE INDEX idx_inquiry_status ON inquiries(status);
CREATE INDEX idx_booking_status ON bookings(status);
