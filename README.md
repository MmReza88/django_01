### To run the server with all functionalities do
```
python manage.py collectstatic
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```


### To run the server without the ws do
```
python .\manage.py runserver 0.0.0.0:8000
```


### Dependancies
```
pip install daphne
pip install channels
pip install django-cors-headers
pip install djangorestframework
```
### aws :
```

mail : mr.sarrami.88@gmail.com  
pass : Mr88098845a
public dns : 13.61.0.132:8000
```

### reclone the repository on aws :
```
rm -rf django_01 && git clone https://github.com/MmReza88/django_01.git
```

### run and stop the server steps :
```
1.source venv/bin/activate
2.cd django_01

--run a new server
3.tmux new -s django_server (if there isn't any running tmux session) 
4.python manage.py runserver 0.0.0.0:8000
5.Ctrl + B, then D (detaches without stopping the server).

--stop server
3.tmux attach -t django_server (attach to the running tmux ession)
4.Ctrl + C (stop running tmux session)
5.exit
```
