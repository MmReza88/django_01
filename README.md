### To run the server with all functionalities do
python manage.py collectstatic
daphne -b 0.0.0.0 -p 8000 config.asgi:application

### To run the server without the ws do
python .\manage.py runserver 0.0.0.0:8000

### Dependancies
pip install daphne
pip install channels
pip install django-cors-headers
pip install djangorestframework
