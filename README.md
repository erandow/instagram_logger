# Clone the Project Repository
git clone https://github.com/rezaebrh/instagram_logger/

# Navigate to the Project Directory
cd instagram_logger

# Create a Virtual Environment
python -m venv venv

# Activate the Virtual Environment (Windows)
venv\Scripts\activate

# or (macOS/Linux)
# source venv/bin/activate

# Install Required Packages
pip install -r requirements.txt

# Run Database Migrations
python manage.py migrate

# Create a Superuser
python manage.py createsuperuser

# Run the Django Development Server
python manage.py runserver

# In a New Terminal for Celery (make sure to activate the virtual environment again)
# Activate the Virtual Environment Again (Windows)
venv\Scripts\activate

# or (macOS/Linux)
# source venv/bin/activate

# Run the Celery Worker
celery -A instagram_logger worker --loglevel=info
