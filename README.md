project: ALX Capstone Project 
API: ICT Assets Management API


# ICT Assets Management API

Deployed Django REST API to manage ICT Assets

## Features
- CRUD operations for inventory items and users
- View current inventory levels
- Interactive API documentation via Swagger

## Deployed API
[https://lincolnmk.pythonanywhere.com](https://lincolnmk.pythonanywhere.com)
Swagger docs: [https://lincolnmk.pythonanywhere.com/swagger/](https://lincolnmk.pythonanywhere.com/swagger/)

## Technologies
- Django 6
- Django REST Framework
- SQLite (PythonAnywhere Free Plan)

1. The Project Idea

The ICT Assets Management API aims to manage ICT equipment from acquisition (through donors or buyers) to allocation and tracking. Its goal is to ensure transparency in how assets are received, distributed, and monitored within the organization to support informed decision-making. The system will provide visibility into equipment that has not yet been distributed, as well as items that have already been allocated. Allocations will also serve as an analytical tool, offering an overview of equipment distribution to highlight areas that may have been left out. This ensures that when new equipment arrives, those underserved areas can be prioritized. Furthermore, when auditors conduct follow-ups, the API will enable the generation of detailed reports showing each piece of equipment and its organizational location, allowing them to verify its existence and usage on the ground.

2. The Main Features of the ICT Assets Management 

CRUD Operations 
Manage inventory items, users, donors/buyers, and locations.
Asset Inventory Tracking 
View current equipment inventory.
Track allocation history (who received what, when, and where).
Donor/Buyer Management 
Record who donated or purchased equipment.
Link donors/buyers to specific inventory items.
Audit & Compliance 
Timestamps and user tracking for all changes.
Historical logs of updates using Django-simple-history.

3. Frameworks to Be Used 

Framework: Django REST Framework (DRF).
Database Interaction: Django ORM.
Deployment Option: PythonAnywhere (MySQL/SQLite).

4. To Deploy  
    ✔ Install requirements.txt
    ✔ Configure Database in settings.py
    ✔ Migrate database
    ✔ Collect static files
    ✔ Configure webserver
    ✔ Enable firewall

Endpoints: 
base_url: https://lincolnmk.pythonanywhere.com/api/
Documentation: https://lincolnmk.pythonanywhere.com/redoc/
Documentation2: https://lincolnmk.pythonanywhere.com/swagger/


Authentication:
1. Login
        POST: api/auth/login/

        sample payload 

        {
                "username":"myusername",
                "Password":"mypassword"
        }

2. Logout:
        POST: api/auth/logout/ 
3. Token Refresh
        POST: api/auth/token/refresh/ 
       
Usermanagement: 
1. list users 
        GET: api/users/
2. create users
        POST: api/users/
    payload sample: 
                {
                    "username": "string",
                    "email": "user@example.com",
                    "first_name": "string",
                    "last_name": "string",
                    "role": 1,
                    "password": "string",
                    "is_active": true
                }
3. Location Management
4. Assets management
5. Donor Buyer Management
6. Allocation Management
7. reports