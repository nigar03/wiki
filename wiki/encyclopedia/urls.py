
from django.urls import path
from .views import entry_view,index_view,search_view,create_page_view,edit_page_view,random_page_view
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('', index_view, name='index'),
    path('search/', search_view, name='search'),
    path('wiki/<str:title>/', entry_view, name='entry_view'),
    path('create/', create_page_view, name='create_page'),
    path('wiki/<str:title>/edit/', edit_page_view, name='edit_page'),
    path('random/', random_page_view, name='random_page'),
]


