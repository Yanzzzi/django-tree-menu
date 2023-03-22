from django.urls import path
from .views import *

urlpatterns = [
    path('', MenuView.as_view(), name='home'),
]