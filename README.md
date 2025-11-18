 # Hangman Game Backend (Django + OpenAI GenAI)
 This repository contains the backend service for a GenAI powered Hangman game built using Django and Django REST Framework. This application integrates OpenAI models using prompt engineering techniques.

 ## 🚀 Getting Started

 ### 1. Clone the Repository

 ### 2. Set up the virtual environment
python -m venv .venv

.\.venv\Scripts\activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Database Setup
python manage.py makemigrations

python manage.py migrate

Create a superuser to access the Django Admin

python manage.py createsuperuser

### 5. Run the server
Start the development server

python manage.py runserver

The API will be accessible at http://127.0.0.1:8000/

