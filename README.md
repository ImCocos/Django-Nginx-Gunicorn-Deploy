# gunciron + nginx easy deploy
Tired from copipasting your configs over and over?

This is great solution for you!

# Installing

```bash
git clone https://github.com/ImCocos/Django-Nginx-Gunicorn-Deploy.git
```

# Deploying

1. ```
    cd Django-Nginx-Gunicorn-Deploy
    sudo python3.11 make.py
    cp config.example.ini sites/<site_name>.ini
    ```
2. Reload shell

3. Fill the config.(store it in Django-Nginx-Gunicorn-Deploy/sites)
    > Required fileds are marked with [*], other aren't necessary.

4. ```
    sitemanager help
    ```

# Dependencies

 - nginx
