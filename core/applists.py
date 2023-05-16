# Application definition

__DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
)

__MY_APPS = (
    'bloodplus_v1',
)

__THIRD_PARTY_APPS = (
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
)

INSTALLED_APPS = __DJANGO_APPS + __MY_APPS + __THIRD_PARTY_APPS
