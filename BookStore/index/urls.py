from django.urls import path
from index import views

urlpatterns = [
    path('search_title_form/', views.search_title_form),
    path('search_title/', views.search_title),
    path('all_book/', views.book_table),
    path('add_book/', views.add_book),
    path('book_not_list/', views.book_not_list)
]

