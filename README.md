# Flask-Auth

Dependencies:
```
Flask-Sqlalchemy
Flask-Login
```

A simple flask authentication blueprint to be used in your flask app.
Creates login ('auth.login') and logout ('auth.logout') views to be used inside your templates/views.

A basic User class is also provided containing werkzeug password hashing.


## Initialization

Inside your app initialize Flask-Auth as follows:

```
from yourapplication import auth

auth.init_app(app)
```

Flask-Auth assumes the following directory structure:

```
/yourapplication
    runserver.py
    /yourapplication
        __init__.py
        models.py <--must contain a `db = SQLAlchemy` statement
        app.py
        ...
        /Flask-Auth
```

## Protecting your views
Use the @login_required decorator provided by Flask-Login to restrict your views to logged in users:
```
from flask.ext.login import login_required

@login_required
@app.route()
def index():
    return render_template('index.html')
```
