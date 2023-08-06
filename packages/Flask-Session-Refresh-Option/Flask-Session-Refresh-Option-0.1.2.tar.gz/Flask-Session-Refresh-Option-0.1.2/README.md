Flask-Session-Refresh-Option
=============

Flask-Session is an extension for Flask that adds support for Server-side Session to your application. Not refreshing session on each request option allowed

Using should_set_session method on RedisSessionInterface

You can config ap to not refresh session if using SESSION_TYPE=redis
```
app.config["SESSION_REFRESH_EACH_REQUEST"] = False
```

To another configurations see [Docs](https://flask-session.readthedocs.io/en/latest/)

