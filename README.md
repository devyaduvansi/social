# My Social Networking App

## Installation

### Prerequisites
- Python 3.x
- pip

### Setup Virtual Environment (Optional but recommended)
```bash

### Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
.\venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate

### Install Dependencies

pip install -r requirements.txt

### Run database migrations
python manage.py makemigrations
python manage.py migrate

### Create an admin user to access the Django admin panel (optional)
python manage.py createsuperuser

### Run the Development Server

python manage.py runserver

The development server will be accessible at http://127.0.0.1:8000/.

### Postman Collection is available in the same directory


### API Endpoints


User Signup:

URL: /api/signup/
Method: POST
Fields: email, password
User Login:

URL: /api/login/
Method: POST
Fields: email, password
User Search:

URL: /api/search/
Method: GET
Fields: search_keyword

Friend Requests:
URL: /api/friend/request/
Method: POST
Fields: to_user_id

Accept Friend Request:
URL: /api/friend/accept/
Method: POST
Fields: friendship_id

Reject Friend Request:
URL: /api/friend/reject/
Method: POST
Fields: friendship_id

List Friends:
URL: /api/friend/list/
Method: GET

List Pending Friend Requests:
URL: /api/friend/pending_requests/
Method: GET

Rate Limiting
Users cannot send more than 3 friend requests within a minute.

Contribution
Feel free to contribute or report issues.

