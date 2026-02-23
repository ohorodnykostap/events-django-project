from .base import *



SECRET_KEY = "django-insecure-ba6^rc5oyttq+3rzs!d_877524uh18xm-ix!wmvr2_o6!7m78h"

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
