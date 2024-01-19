# KLM Klimanjaro Core App

Welcome to the KLM Klimanjaro Core App, a Django boilerplate with essential features to kickstart your project.

## Getting Started

### 1. Set Up Virtual Environment

```bash
# Clone the repo
git clone https://github.com/lukuku-dev/django-rest-boilerplate.git
# Change directory
cd django-rest-boilerplate

# Check available Python versions
pyenv install --list
# Install the desired Python version
pyenv install 3.11

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### 2. Install Requirements
- Choose the appropriate requirements file based on your environment:

- For production:
```bash
pip install -r requirements/production.txt
```
- For local development:

```bash
pip install -r requirements/local.txt
```

### Migrate Database
```bash
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

### 5. Run the Server
```bash
python manage.py runserver
```