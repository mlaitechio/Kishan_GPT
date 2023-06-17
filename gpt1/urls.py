from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("chat/" , views.new_chat, name="new_chat"),
    # path('token_limit_exceeded/', views.token_limit_exceeded_view, name='token_limit_exceeded'),
]