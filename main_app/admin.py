from django.contrib import admin
from .models import Spider, Feeding, Decoration, Photo

# Register your models here.
admin.site.register(Spider)
admin.site.register(Feeding)
admin.site.register(Decoration)
admin.site.register(Photo)