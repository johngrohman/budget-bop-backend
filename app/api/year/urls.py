from django.urls import path
from .api import router as year_router

urlpatterns = [
    path('', year_router, name='Year'),
]