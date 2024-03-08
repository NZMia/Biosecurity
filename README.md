# New Zealand Animal Pest Biosecurity Guide

Welcome to the New Zealand Animal Pest Biosecurity Guide web application! This Flask Python application provides a comprehensive guide to animal pests in New Zealand, focusing on biosecurity measures. The application features a secure login system and role-based dashboards for Pest Controllers, Staff, and Administrators.

## Introduction

The New Zealand Animal Pest Biosecurity Guide web application is designed to provide users with valuable information about animal pests in New Zealand. The application includes a secure login system and role-based dashboards for Pest Controllers, Staff, and Administrators.

## Features

- Secure user authentication and registration.
- Role-based access control for Pest Controllers, Staff, and Administrators.
   - Pest Controller Role:
      - Can view and update personal information.
      - Can view the list of pests.

   - Staff Role:
      - Can view and update personal information.
      - Can view Pest Controller's information.
      - Can view the list of pests.
      - May have additional privileges based on specific requirements.

   - Administrator Role:
      - Can view and update personal information.
      - Can view and update Pest Controller's information.
      - Can view the list of pests.
      - Has full access to system administration and configuration.
      - Highest level of access and control.

- Attractive home page reflecting the New Zealand animal pest theme.
- User management for Pest Controllers, Staff, and Administrators.
- Comprehensive animal pest guide with detailed information and images.
- Responsive design for optimal viewing on various devices.
  

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Python (version 3.10)
- Flask
- MySQL
- Bootstrap 5 (included in the project)

### Installation

1. Clone the repository:

   ```bash
   git clone git@github.com:your-username/Biosecurity.git
   ```
2. Navigate to the project directory:
   ```
   cd Biosecurity
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Set up the database using the provided env.example as example.
6. Run the application:
   ```
   flask run
   ```
   The application should now be running locally.

## Usage

1. Open your web browser and go to [http://localhost:5000](http://localhost:5000).
2. Explore the home page, and use the login or registration links to get started.

## File Structure

The project file structure is organized as follows:

```
Biosecurity/
│
├── webApp/
│   ├── config /
│   │   ├── __init__.py
│   │   ├── app_config.py
│   │   └── data_config.py
│   ├── static/
│   │   ├── uploads /
│   │   │   └── ....
│   │   ├── bg.png
│   │   └── styles.css
│   └── templates/
│   │   ├── components /
│   │   │   └── ....
│   │   ├── layouts /
│   │   │   └── ....
│   │   ├── dashboard /
│   │   │   └── ....
│   │   ├── pest /
│   └── │   └── ....
│   │   ├── __init__.py
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── reset__password.html
│   │   ├── register.html
│   └── __init__.py
│   └── auth.py
│   └── dashboard.py
│   └── gereral_view.py
│   └── models.py
│   └── data_operations.py
├── .env.example
├── .gitignore
├── README.md
└── app.py
├── biosecurity.local.sql
├── biosecurity.pythonanywhere.sql
├── wsgi.py
├── .vscode
├── requirements.txt
├── wsgi.py
```

