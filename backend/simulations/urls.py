from django.urls import path
from . import views

urlpatterns = [
    path('diffusion/numerical/', views.numerical_diffusion_view, name='numerical_diffusion'),
]
