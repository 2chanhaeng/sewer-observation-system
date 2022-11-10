from django.urls import path
from . import views

urlpatterns = [
    path("<str:gubn>/", views.rainfall_sewage_view),
]
