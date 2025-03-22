# Lyric Masti

## Setup Guide

### 1. Clone the Repository
```sh
git clone https://github.com/gitprajapati/lyrics_masti_game_backend.git
```

### 2. Create a `.env` File
Create a `.env` file in the root directory and add the following environment variables:

```
SQLALCHEMY_DATABASE_URI = 'sqlite:///lyricsmasti.sqlite3'
SECRET_KEY = ""
SECURITY_PASSWORD_SALT = ""
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False
SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'
JWT_SECRET_KEY = ""
UPLOAD_FOLDER = 'static/files/'
STATIC_FOLDER = 'static'
SESSION_COOKIE_SECURE = False  
JWT_VERIFY_SUB = False
GEMINI_API_KEY = ''
```

Fill in the required secrets before running the application.

### 3. Create and Activate a Virtual Environment

#### Windows:
```sh
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux:
```sh
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Requirements
```sh
pip install -r requirements.txt
```

### 5. Run the Application
```sh
python main.py
```
### 6. Admin Credentials
```sh
user id: admin@test.com
password: admin
```
Your app should now be running at `http://127.0.0.1:5000/`.

### 6. Deactivating the Virtual Environment
When you're done working on the project, deactivate the virtual environment with:
```sh
deactivate
```

