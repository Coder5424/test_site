from django.contrib import admin
from .models import Modalities, Studies

admin.site.register([Modalities, Studies])
