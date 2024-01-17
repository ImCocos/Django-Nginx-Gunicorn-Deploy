# Django + gunciron + nginx easy deploy
Tired from copipasting your comfigs over and over?

This is great solution for you!
Have **no dependencies** besides python, pip, venv

# Installing

```bash
git clone https://github.com/ImCocos/Django-Nginx-Gunicorn-Deploy.git
```

Done!

# Deploying

## Config way:

1. ```
    cd Django-Nginx-Gunicorn-Deploy
    cp config.example.ini <site_name>.ini
    ```
2. Fill the config

3. ```
    python deploy.py config.ini
    ```

## Or if don't like writing configs to generate configs

```
cd Django-Nginx-Gunicorn-Deploy
python deploy.py
```
