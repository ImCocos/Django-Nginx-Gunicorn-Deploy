# Django + gunciron + nginx easy deploy
Tired from copipasting your configs over and over?

This is great solution for you!
Have **no dependencies** besides python, pip, venv

# Installing

```bash
git clone https://github.com/ImCocos/Django-Nginx-Gunicorn-Deploy.git
```

# Deploying

1. ```
    cd Django-Nginx-Gunicorn-Deploy
    cp config.example.ini <site_name>.ini
    ```

2. Fill the config.
    > Required fileds are marked with *, other aren't necessary.

3. ```
    python main make <site_name>.ini
    ```

# Dependencies

 - nginx
 - gunicorn(in virtual environment of your project)