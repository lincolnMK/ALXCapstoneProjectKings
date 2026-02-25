# ICT Assets Management API (ALX Capstone)

# Deployed API
[https://lincolnmk.pythonanywhere.com](https://lincolnmk.pythonanywhere.com)
Swagger docs: [https://lincolnmk.pythonanywhere.com/api/swagger/](https://lincolnmk.pythonanywhere.com/api/swagger/)

# Technologies used
- Django 
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


**Project**: ICT Assets Management — a Django REST API to manage acquisition, inventory, allocation, and reporting for ICT assets.

**Overview**
- **Purpose:** Track assets from donors or buyers through allocation and reporting to improve transparency and auditing.
- **Key domains:** Assets, Locations, Users, Donors/Buyers, Allocations, Reports.

**Features**
- **CRUD:** Create, read, update, delete for assets, users, locations, donors/buyers.
- **Allocation tracking:** Record who received which asset, when, and where.
- **Audit history:** Change tracking with timestamps and historical logs.
- **API docs:** Auto-generated Swagger / ReDoc documentation.

**Tech Stack**
- **Framework:** Django, Django REST Framework
- **DB:** SQLite (default) — easy local setup; production can use PostgreSQL/MySQL
- **Extras:** django-simple-history for auditing

**Prerequisites**
- Python 3.10+ installed
- Git (optional)
- System packages for building Python wheels (on Debian/Ubuntu: `build-essential`, `libpq-dev` for Postgres)

**Quick Setup (local)**
1. Clone the repo (if not already):

```bash
git clone https://github.com/lincolnMK/ALXCapstoneProjectKings.git
cd ALXCapstoneProjectKings
```

2. Create and activate a virtual environment:

```bash
python3 -m venv myenv
source myenv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment:
- Copy `.env.example` to `.env` and set `SECRET_KEY`, `DEBUG`, and database settings if present.

5. Apply database migrations:

```bash
python manage.py migrate
```

6. (Optional) Create a superuser:

```bash
python manage.py createsuperuser
```

7. Run the development server:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/` by default.

**Running Tests**

```bash
python manage.py test
```

**API Documentation**
- Swagger: `/api/swagger/` 


**Common Endpoints (examples)**
- Authentication: `POST /api/auth/login/`, `POST /api/auth/logout/`, `POST /api/auth/token/refresh/`
- Users: `GET /api/users/`, `POST /api/users/`
- Assets, Locations, Donor/Buyer, Allocation endpoints follow the pattern `/api/<resource>/`

**Deployment Notes**
- For production, set `DEBUG=False`, provide a secure `SECRET_KEY`, and use PostgreSQL or MySQL.
- Run `python manage.py collectstatic` and configure your webserver (Gunicorn + Nginx recommended).
