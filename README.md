# EdTech Platform

A comprehensive EdTech platform built using Django that enables users to register, view courses, receive notifications, and manage profiles. This project includes an admin-managed notification system, user authentication, course registration, payment integration, and more.

---

## Features

- **Course Listings**: Users can view and register for available courses.
- **Notifications**: Display course-related notifications categorized by date.
- **User Profiles**: Manage personal information and track course progress.
- **Payment Integration**: Register for courses with UPI payment options.
- **Authentication**: Secure login and signup, including OTP-based authentication.
- **Admin Dashboard**: Admin can create, edit, and delete courses and send notifications to users.

---

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **Database**: PostgreSQL
- **Additional Tools**: Git, Docker (optional for containerization), Visual Studio Code

---

## Project Structure

```plaintext
edtech_platform/
├── course/                 # Main Django app for courses and notifications
│   ├── templates/          # HTML templates for different pages
│   ├── static/             # Static assets like CSS and JS files
│   ├── views.py            # Views to handle request-response cycles
│   ├── models.py           # Database models for courses, notifications, etc.
│   ├── urls.py             # URL configurations for app routing
│   └── admin.py            # Customizations for Django admin interface
├── media/                  # Directory for user-uploaded files (e.g., profile pictures)
├── manage.py               # Django management script
├── requirements.txt        # Dependencies
└── README.md               # Project documentation
