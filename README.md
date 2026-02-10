Capstone Project Roadmap: ICT Assets Management API
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
