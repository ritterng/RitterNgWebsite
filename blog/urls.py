from django.urls import path
from . import views
urlpatterns = [
    path('',views.articles_list, name = 'articles_list'),
    path('add/',views.add_article, name="add_article"),
]
