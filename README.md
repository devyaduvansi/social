# My Social Networking App

## Installation

### Prerequisites
- Python 3.11.x
- pip

# Setup Virtual Environment (Optional but recommended)


## 1.- Create a virtual environment
```bash
python -m venv venv
```
## 2.-Activate the virtual environment

### On Windows
```bash
.\venv\Scripts\activate
```
### On Linux/Mac
```bash
source venv/bin/activate
```
## 3.- Install Dependencies
```bash
pip install -r requirements.txt
```
## 4.- Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
## 5.- Create an admin user to access the Django admin panel (optional)
```bash
python manage.py createsuperuser
```
## 6.- Run the Development Server
```bash
python manage.py runserver
```
The development server will be accessible at http://127.0.0.1:8000/.

# Note: Postman Collection is available in the same directory


# API Endpoints


## User Signup:

URL: /api/signup/<br>
Method: POST<br>
Fields: email, password<br>

## User Login:
URL: /api/login/<br>
Method: POST<br>
Fields: email, password<br>

## User Search:
URL: /api/search/<br>
Method: GET<br>
Fields: search_keyword<br>

## Friend Requests:
URL: /api/friend/request/<br>
Method: POST<br>
Fields: to_user_id<br>

## Accept Friend Request:
URL: /api/friend/accept/<br>
Method: POST<br>
Fields: friendship_id<br>

## Reject Friend Request:
URL: /api/friend/reject/<br>
Method: POST<br>
Fields: friendship_id<br>

## List Friends:
URL: /api/friend/list/<br>
Method: GET<br>

## List Pending Friend Requests:
URL: /api/friend/pending_requests/<br>
Method: GET<br>

# Rate Limiting
Users cannot send more than 3 friend requests within a minute.

# Contribution
Feel free to contribute or report issues.

