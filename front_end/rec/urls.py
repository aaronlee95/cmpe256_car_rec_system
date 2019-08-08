from django.urls import path
from . import views

urlpatterns = [
    # path('', views.countries_view, name='countries_view'),
    path('', views.home, name='home'),
    path('recommend', views.recommend, name='recommend')
]