# Deployment to a local host

1) Install the required Python packages in requirements.txt
2) Run the following commands inside of 2nd `QRLogin` directory
```python
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
```
3) Follow the prompts to create an admin account. Currently this is the only method for creating an account on the demonstration site, as the actual account creation process would heavily depend on the how the third-party site wants to implement it. 
4) To run the demonstrations site on localhost (127.0.0.1:8000) use
```python
py manage.py runserver
```

