from django.contrib import admin
from index.models import Book, Author,  UserInfo
# Register your models here.

admin.site.register([Book, Author, UserInfo])