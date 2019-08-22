from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name = 'index'),
    path('home',views.home, name = 'home'),
    path('delete/<list_id>', views.delete, name='delete'),
    path('cross-off/<list_id>', views.cross_off, name='cross-off'),
    path('uncross/<list_id>', views.uncross, name='uncross'),
    path('edit/<list_id>', views.edit, name='edit'),
    path('wish/',views.wish_list_home,name='wish'),
]
