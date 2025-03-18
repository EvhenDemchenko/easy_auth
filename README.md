Let me introduce simple DRF Auth_module witch you can easy set-up and user in your projects.

It includes 
   - registration
   - login
   - logout
   - change email with confirmation email list
   - change password with confirmation email list
   - reset password with email list
   - profile get/patch requests

Do this commands step by step to set-up this module to your project 

   - python3 -m venv .env
   - pip install -r req.txt 

makemigrations and migrate 

fill all fieds with your data
   - SECRET_KEY generate your own key
   - DATABASES connect to your own db
   - AUTH_USER_MODEL modify your own model    
   - REST_FRAMEWORK 
   - JWT_SETTINGS configure your settings 
   - SIMPLE_JWT configure your settings 
   - EMAIL_BACKEND configure smtp
   - EMAIL_HOST configure smtp
   - EMAIL_HOST_USER configure smtp
   - EMAIL_HOST_PASSWORD configure smtp
   - EMAIL_PORT configure smtp
   - EMAIL_USE_TLS configure smtp


will be added soon Celery & Redis 
