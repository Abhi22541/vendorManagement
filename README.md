# Vendor and Purchase Order API

## Overview

This API provides endpoints for managing vendors and purchase orders. It includes functionality for performance metrics evaluation, purchase order acknowledgment, and CRUD operations for vendors and purchase orders.

## Features

- **Vendor Management**: Create, retrieve, update, and delete vendors.
- **Purchase Order Management**: Create, retrieve, update, delete, and list purchase orders with optional filtering by vendor.
- **Performance Metrics**: Retrieve performance metrics for vendors, including on-time delivery rate, quality rating, average response time, and fulfillment rate.
- **Purchase Order Acknowledgment**: Acknowledge purchase orders to update their acknowledgment status.

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Django 4.0 or higher
- Django REST Framework
- Django REST Framework Simple JWT
- drf-yasg (for Swagger documentation)

### Installation

1. **Clone the Repository**

   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. Create and Activate a Virtual Environment
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install Dependencies
    pip install -r requirements.txt

4. Apply Migrations
    python manage.py migrate

5.python manage.py createsuperuser
    python manage.py createsuperuser

6.python manage.py runserver
    python manage.py runserver

You will need to create a user from the Django admin panel. To access the admin panel, navigate to http://localhost/admin/ and log in with the superuser credentials you just created.

