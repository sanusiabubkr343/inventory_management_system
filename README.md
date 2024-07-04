# Simple INVENTORY MANAGEMENT SYSTEM

## Overview
This project is a Django-based inventory management system designed to handle user authentication with role-based access control, inventory management for admins, order tracking, and reporting functionalities. It leverages Django and Django REST Framework, emphasizing best practices for code quality, documentation, and including unit tests and basic error handling mechanisms.

## Getting Started

### Prerequisites
Ensure you have Python installed on your machine. The project requires Python 3.10 or newer.

### Setup

1. **Clone the Repository**
   First, clone the repository to your local machine using Git. Replace `<repository_url>` with the actual URL of your repository.
  run this: git clone <repository_url> cd inventory_management_system

2. **Enviroment variable**
 Create a `.env` file in the root folder by copying the `.env.sample` file. Fill in the required environmental variables in the `.env` file.


3. **Set Up the Virtual Environment**
   Navigate to the project directory and create a virtual environment to isolate the project's dependencies.
   run this : python -m venv venv

Activate the virtual environment:
- On Windows:
cmd .\venv\Scripts\activate
- On macOS/Linux:
bash source venv/bin/activate


4. **Install Dependencies**
   With the virtual environment activated, install the project's dependencies using `pip`.
   run:pip install -r requirements.txt


5. **Run Migrations**
   Apply migrations to set up the database schema.
   run: python manage.py migrate

6. **Run the Development Server**
   Start the development server to interact with the application through a web browser.
   run: python manage.py runserver
   Access the application by navigating to `http://127.0.0.1:8000/api/v1/doc` in your web browser.


  

7. **Running Tests**
   Execute tests using `pytest -vv` to ensure the application behaves as expected.
   run:pytest -vv

Make sure to replace `<repository_url>` with the actual URL of your repository. Also, ensure that the image URLs point to the correct locations in your repository.









