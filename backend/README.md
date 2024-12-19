# frontend

## Project setup


### Create virtual envioroment

```
python -m venv .venv
```


### Install requirements
```
pip install -r requirements.txt
```

### Config Database
En en archivo ./backend/settings.py modificar las siguientes lineas de codigo para la base de datos a usar,
```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'prueba-tecnica',
        'USER': 'root',
        'PASSWORD': '2269',
    }
}
```
En caso de cambiar la base de datos instalar las dependencias correspondientes para usar la nueva base de datos

##### Configuracion con SQLlite3
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}
```

Ver [Configuration Reference Databases](https://docs.djangoproject.com/en/5.1/ref/settings/#databases). 


### Create migrations
```
python manage.py migrate
```


### Run server
```
python manage.py runserver
```

### Customize configuration
See [Configuration Reference](https://docs.djangoproject.com/en/5.1/).
