import os
from celery import Celery

# Указываем Django-сеттинги по умолчанию для Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Загружаем настройки из Django settings, но начинающиеся с "CELERY"
app.config_from_object("django.conf:settings", namespace="CELERY")

# Автоматически находит таски во всех приложениях
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
